import socket
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname('localhost')
message_count = 0


def currenttime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def handshake():
    print('\nWaiting to receive message from Client:')
    hs_data, hs_address = sock.recvfrom(10000)
    hs_data = hs_data.decode()
    print('C: ' + hs_data)

    x = hs_data.split(' ', 1)
    if hs_data.startswith('com-0') and socket.inet_aton(x[1]):
        reply = 'com-0 accept ' + IPAddr
        sock.sendto(reply.encode(), hs_address)
        print('S: ' + reply)
        check_counter = 1

    print('\nWaiting to receive message from Client:')
    hs_data, hs_address = sock.recvfrom(10000)
    hs_data = hs_data.decode()
    print('C: ' + hs_data)

    log = open('Log.txt', 'a')
    log.write("Handshake successful : " + str(check_counter) + "\n")
    log.close()

    if check_counter == 1 and hs_data == 'com-0 accept':
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

while isHandshaken:
    sock.settimeout(4)
    print('\nWaiting to receive message from Client:')
    data, address = sock.recvfrom(10000)
    data = data.decode()

    if data == 'con-h 0x00':
        print('Heartbeat')
    else:
        print('C : ' + data)
        message_communication()
    # If no messages received before 4 seconds disconnect client
except socket.timeout:

    inactive_msg = 'con-res 0xFE'
    inactive_resp = sock.sendto(inactive_msg.encode(), address)

    messages_inactive, address = sock.recvfrom(4096)
    inactive_resp_client = messages_inactive.decode()
    if inactive_resp_client == 'con-res 0xFF':
        print("Client disconnected for inactivity " + inactive_resp_client)
        sock.close()
        exit()
