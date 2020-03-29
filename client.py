import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname("")
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is: " + IPAddr + '\n')
server_address = ('localhost', 10000)
counter = 0
sock.sendto('com-0 '.encode() + IPAddr.encode(), server_address)
# Receive Connection
data, server = sock.recvfrom(4096)
sock.sendto('com-0 accept'.encode(), server_address)

print('Start Chat')

while True:
    # Sending Message to Server
    message = input("\nEnter message: ")
    clientmsg = 'msg-'
    # Send data
    sock.sendto(clientmsg.encode() + str(counter).encode() + b'= ' + message.encode(), server_address)
    counter += 1
    # Receive response
    data, server = sock.recvfrom(4096)
    data = data.split(b'=', 1)
    print('{}'.format(data[1].decode()))
    counter += 1
