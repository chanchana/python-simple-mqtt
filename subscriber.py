import sys
import socket

# default parameter for broker host and port
BUFFER_SIZE = 1024
host = 'localhost'
port = 80

# check valid argument
if len(sys.argv) < 3:
    print('Invalid argument count!')
    print('Usage: subscribe.py [broker_ip_address] [topic_name]')
    exit()

# if there is a specific host and port in argument
ip = sys.argv[1]
splitted = ip.split(':')
host = splitted[0]
if len(splitted) > 1: # have specified port
    port = int(splitted[1])

# get topic from argument
subscribe_topic = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make socket instance, AF_INET = address family ipv4. SOCK_STREAM = connection oriented TCP protocol.
try: # try to connect to the ip
    s.connect((host, port)) # connect
except: # cannot connect
    print('Cannot connect to broker at ' + ip)
    exit()

print('Connected to broker at ' + ip)
message = 'subscribe ' + subscribe_topic # set up the message
data = message.encode('utf-8') # encode to bytes
s.send(data) # send data to breaker

print('Start recieving subscribed data')
while True: # keep recieving data
    data = s.recv(BUFFER_SIZE) # recieve data
    if not data:
        break
    message = data.decode('utf-8') # decode
    print(message) # print message to console

s.close() # close the socket
