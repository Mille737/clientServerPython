import socket
import threading
import time

# Create a UDP socket
from configparser import ConfigParser

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
parser = ConfigParser()
parser.read('configuration.ini')
max_packages = parser.getboolean('MaximumPackages', 'Start')
spam_count = 0
no_spam_detected = True


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
        t2 = threading.Thread(target=check_for_spam)
        t2.start()
        reset_spam()
        return True
    else:
        log = open('Log.txt', 'a')
        log.write("Handshake unsuccessful : " + str(currenttime()) + "\n")
        log.close()
        sock.sendto("Handshake unsuccessful".encode(), hs_address)
        print("Handshake unsuccessful")
        return False


def message_communication():
    global spam_count
    print(spam_count)
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


def check_for_spam():
    while True:
        global spam_count
        if spam_count > int(max_packages):
            global no_spam_detected
            no_spam_detected = False


def reset_spam():
    threading.Timer(1.0, reset_spam).start()
    global spam_count
    spam_count = 0
    global no_spam_detected
    no_spam_detected = True


isHandshaken = handshake()

while isHandshaken:
    try:
        while no_spam_detected:
            print('\nWaiting to receive message from Client:')
            data, address = sock.recvfrom(10000)

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
