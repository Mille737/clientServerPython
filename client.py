import multiprocessing
import socket
import threading
from configparser import ConfigParser

# Create a UDP socket
from multiprocessing.spawn import freeze_support

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname('localhost')
# print("Your Computer Name is:" + hostname)
# print("Your Computer IP Address is: " + IPAddr + '\n')
server_address = ('localhost', 10000)
counter = 0

# read configuration file
parser = ConfigParser()
parser.read('configuration.ini')
max_packages = parser.getboolean('MaximumPackages', 'Start')

sock.sendto('com-0 '.encode() + IPAddr.encode(), server_address)
# Receive Connection
data, server = sock.recvfrom(4096)
data = data.decode()
x = data.split(' ', 2)
if data.startswith('com-0 accept') and socket.inet_aton(x[2]):
    sock.sendto('com-0 accept'.encode(), server_address)


def heartbeat():

    if parser.getboolean('Heartbeat', 'keepalive'):
        threading.Timer(parser.getint('Heartbeat', 'HeartbeatTimer'), heartbeat).start()
        heartbeat_msg = 'con-h 0x00'
        sock.sendto(heartbeat_msg.encode(), server_address)
    else:
        print("Heartbeat not activated")
        sock.close()
        exit()


def maxpackages():

    while max_packages:

        print("maxpackages")
        # Loop to send amount from config file of msg to server
        for x in range(parser.getint('MaximumPackages', 'MaximumPackages')):
            if __name__ == '__main__':
                freeze_support()

                msg = 'maxpackages'
                mp = multiprocessing.Process(target=sock.sendto, args=(msg.encode(), server_address))
                mp.start()
        resp, server = sock.recvfrom(4096)
        print('closing because of message overload')
        print(resp.decode())
        sock.close()
        exit()
        # break


maxpackages()

heartbeat()
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
    if str(data) == 'con-res 0xFE':
        disconnectionmsg = 'con-res 0xFF'
        sock.sendto(disconnectionmsg.encode(), server_address)
        sock.close()
        exit()
    else:
        data = data.split(b'=', 1)
        print('{}'.format(data[1].decode()))
        counter += 1
