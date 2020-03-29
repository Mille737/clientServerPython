import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname("")
i = 0
checkcounter = 0

while True:
    print('\nWaiting to receive message from Client:')
    data, address = sock.recvfrom(10000)
    # print('received {} bytes from {}'.format(len(data), address))
    data = data.decode()
    print('C: ' + data)
    if data.startswith('com-0'):
        x = data.split(' ', 1)
        y = (x[1].split('.', 3))
        if checkcounter == 1 and data == 'com-0 accept':
            checkcounter += 1
        elif (0 <= int(y[0]) <= 255) and (0 <= int(y[1]) <= 255) and (0 <= int(y[2]) <= 255) and (0 <= int(y[3]) <= 255):
            reply = 'com-0 accept ' + IPAddr
            sock.sendto(reply.encode(), address)
            print('S: ' + reply)
            checkcounter += 1
        else:
            print('IP error.')
    elif data.startswith('msg-'):
        if checkcounter < 2:
            print('Unapproved message: connection disabled.')
            break
        if data[4] == str(i):
            i += 1
            reply = 'res-' + str(i) + '= ' + 'I am server'
            print('S: ' + reply)
            i += 1
            sent = sock.sendto(reply.encode(), address)
        # print('sent {} bytes back to {}'.format(sent, address))
    else:
        print('Error in data.')


