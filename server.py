import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
message_count = 0


def handshake():
    print('\nWaiting to receive message from Client:')
    data, address = sock.recvfrom(10000)
    data = data.decode()
    print('C: ' + data)

    x = data.split(' ', 1)
    if data.startswith('com-0') and socket.inet_aton(x[1]):
        reply = 'com-0 accept ' + IPAddr
        sock.sendto(reply.encode(), address)
        print('S: ' + reply)
        check_counter = 1

    print('\nWaiting to receive message from Client:')
    data, address = sock.recvfrom(10000)
    data = data.decode()
    print('C: ' + data)

    if check_counter == 1 and data == 'com-0 accept':
        return True
    else:
        return False


def message_communication():
    if data.startswith('msg-'):
        x = data.split('-')
        y = x[1].split('=')
        global message_count
        if int(y[0]) == message_count:
            message_count += 1
            reply = 'res-' + str(message_count) + '= ' + 'I am server'
            print('S: ' + reply)
            message_count += 1
            sock.sendto(reply.encode(), address)
        else:
            print('Error')
    else:
        print('Error in data.')


isHandshaken = handshake()


while True:
    print('\nWaiting to receive message from Client:')
    data, address = sock.recvfrom(10000)
    data = data.decode()
    print('C : ' + data)
    if isHandshaken:
        message_communication()

