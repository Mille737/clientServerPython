import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is: " + IPAddr)
server_address = ('localhost', 10000)
counter = 0
sent = sock.sendto('Connection Request'.encode(), server_address)
# Receive Connection
data, server = sock.recvfrom(4096)
print('Client Sends: Connection Request')
print('Server Responds: {}'.format(data.decode()))
sent = sock.sendto('Client Accepts'.encode(), server_address)
print('Start Chat')

while True:
    # Sending Message to Server
    message = input("\nEnter message: ")
    clientmsg = 'msg-'
    # Send data
    print(' {}'.format(message), 'To Server', counter)
    sent = sock.sendto(clientmsg.encode() + str(counter).encode() + b'=' + message.encode(), server_address)
    counter += 1
    # Receive response
    data, server = sock.recvfrom(4096)
    print('Server Responds: {}'.format(data.decode()), counter)
    counter += 1
