import sys
import socket

# default parameter for broker host and port
host = 'localhost'
port = 80

# check valid argument
if len(sys.argv) < 4:
    print('Invalid argument count!')
    print('Usage: publish [broker_ip_address] [topic_name] [data to publish]')
    exit()


# if there is a specific host and port in argument
ip = sys.argv[1]
splitted = ip.split(':')
host = splitted[0]
if len(splitted) > 1: # have specified port
    port = int(splitted[1])

# get topic and data from argument
publish_topic = sys.argv[2]
publish_data = sys.argv[3]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make socket instance, AF_INET = address family ipv4. SOCK_STREAM = connection oriented TCP protocol.
try: # try to connect to the ip
    s.connect((host, port)) # connect
except: # cannot connect
    print('Cannot connect to broker at ' + ip)
    exit()

print('Connected to broker at ' + ip)
message = 'publish ' + publish_topic + ' ' + publish_data # message to be sent
data = message.encode('utf-8') # encode the message
s.send(data) # send to broker

print('Sent message to broker : ' + message)
s.close() # close the socket
