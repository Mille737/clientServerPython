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
sock.settimeout(4)
package_counter = 0


def currenttime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def handshake():
    print('\nWaiting to receive message from Client:')
    hs_data, hs_address = sock.recvfrom(10000)
    hs_data = hs_data.decode()
    print('C: ' + hs_data)

    x = hs_data.split(' ', 1)
    check_counter = -1
    if hs_data.startswith('com-0') and socket.inet_aton(x[1]):
        reply = 'com-0 accept ' + IPAddr
        sock.sendto(reply.encode(), hs_address)
        print('S: ' + reply)
        check_counter = 1

    print('\nWaiting to receive message from Client:')
    hs_data, hs_address = sock.recvfrom(10000)
    hs_data = hs_data.decode()
    print('C: ' + hs_data)

    if check_counter == 1 and hs_data == 'com-0 accept':
        log = open('Log.txt', 'a')
        log.write("Handshake successful : " + str(currenttime()) + "\n")
        log.close()
        return True
    else:
        log = open('Log.txt', 'a')
        log.write("Handshake unsuccessful : " + str(currenttime()) + "\n")
        log.close()
        sock.sendto("Handshake unsuccessful".encode(), hs_address)
        print("Handshake unsuccessful")
        return False


def message_communication():
    if data.decode().startswith('msg-'):
        x = data.decode().split('-')
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


def package_count():
    global package_counter
    package_counter += 1
    print(package_counter)
    if package_counter >= 25:
        max_pac = 'Maximum 25 packages allowed'
        time.sleep(5)
        sock.sendto(max_pac.encode(), address)
        print(max_pac)
        sock.close()
        exit()


isHandshaken = handshake()

while isHandshaken:
    try:
        print('\nWaiting to receive message from Client:')
        data, address = sock.recvfrom(10000)

       #  if data.decode() == 'maxpackages' or 'com-0 127.0.0.1':
           # package_count()
        if data.decode() == 'con-h 0x00':
            print('Heartbeat')
        else:
            message_communication()
            print('C : ' + data.decode())

    except socket.timeout:
        inactive_msg = 'con-res 0xFE'
        sock.sendto(inactive_msg.encode(), address)

        messages_inactive, address = sock.recvfrom(4096)
        inactive_resp_client = messages_inactive.decode()
        print("Client disconnected for inactivity " + inactive_resp_client)
        sock.close()
        exit()
