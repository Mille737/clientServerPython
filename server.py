import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
i = 0

while True:
    print('\nWaiting to receive message from Client:')
    data, address = sock.recvfrom(10000)
    # print('received {} bytes from {}'.format(len(data), address))
    data = data.decode()
    if data.startswith('com-0'):
        if 1<2:
            reply = 'com-0 accept' + IPAddr
            print(reply)
            sent = sock.sendto(reply.encode(), address)
        elif accept:
            print(data.decode)
    elif data.startswith('msg-'):

        if data[4] == str(i):
            print(data)
            i += 1
            reply = 'res-' + str(i) + '=' + 'I am server'
            print(reply)
            i += 1
            sent = sock.sendto(reply.encode(), address)
        # print('sent {} bytes back to {}'.format(sent, address))
    else:
        print('Error in data.')
