import socket
import threading
import sys


# --- Global Vars ------------------------------------------------------------------------

# default parameter for broker host and port
BUFFER_SIZE = 1024 # default buffer
host = 'localhost' # default host
port = 80 # default port

# list of subscriber, element = (connection, address, topic)
subscribers = []

# dictionary of topics, key: topic, value: [list of subscribers]
topics = {}


# --- Misc ------------------------------------------------------------------------

# address to string
def address_str(address):
    return str(address[0]) + ':' + str(address[1])

# check if it is the same topic
def same_topic(publisher_topic, subscriber_topic):
    splitted_publisher_topic = publisher_topic.split('/') # split be '/'
    splitted_subscriber_topic = subscriber_topic.split('/') # split be '/'
    # if publisher longer than subscriber => not match
    if len(splitted_publisher_topic) > len(splitted_subscriber_topic):
        return False
    # loop for each splitted
    for index, value in enumerate(splitted_publisher_topic):
        if value == '#': # accept all => matched
            break
        if value == '+': # ignore this one string and continue
            continue
        if value == splitted_subscriber_topic[index]: # same string and continue
            continue
        else: # not same string => not matched
            return False
    # if not return any false => matched
    return True

# get all subscribers that subscribe the topic
def subscirbers_of_topic(topic):
    target_subscribers = [] # return values
    # loop through all subscribers
    for subscriber in subscribers:
        subscriber_topic = subscriber[2] # get subscriber's topic
        if same_topic(topic, subscriber_topic): # if the topic is matched
            target_subscribers.append(subscriber) # add to subscriber list
    return target_subscribers


# --- Data Repository ------------------------------------------------------------------------

# add topic to dictionary
def add_topic(topic):
    print('Add topic: ' + topic)
    topics[topic] = subscirbers_of_topic(topic)

# update topic dictionary by looping all subscriber
def update_topic():
    print('Update topic list')
    # loop by all keys in the dictionary
    for key in topics:
        # update subscriber list for each key
        topics[key] = subscirbers_of_topic(key)

# check if the topic existed
def has_topic(topic):
    return topic in topics

# get subscribers that subscribe the topic
def get_subscribers_of_topic(topic):
    return topics[topic]

# add new subscriber to list
def add_subscriber(connection, address, topic):
    subscribers.append((connection, address, topic))

# remove the subscribers that closed the connection
def update_subscriber():
    targets = [] # target to remove
    # loop through all subscribers
    for subscriber in subscribers:
        connection = subscriber[0] # subscriber connection
        if connection._closed: # the connection is closed
            targets.append(subscriber) # add to remove list
    # remove all subscribers that are in the target list
    for target in targets:
        subscribers.remove(target)


# --- Service Handler ------------------------------------------------------------------------

# handle subscribing job
def subscribe(connection, address, topic):
    print(address_str(address) + ' Subscribed: ' + topic)
    add_subscriber(connection, address, topic) # add new subscriber
    update_topic()

# handle publishing job
def publish(address, topic, data):
    print(address_str(address) + ' Published: ' + topic + ' ' + data)
    if not has_topic(topic): # if the topic is not existed => add the topic
        add_topic(topic)

    # get the subscribers that need to send data
    for subscriber in get_subscribers_of_topic(topic):
        subscriber_connection = subscriber[0]
        subscriber_address = subscriber[1]
        subscriber_connection.send(data.encode('utf-8')) # send to that connection
        print('Send data to ' + address_str(subscriber_address))


# --- Message Handler ------------------------------------------------------------------------

# handle incomming message from any source
def handle_message(connection, address):
    # recieve data forever
    while True:
        data = connection.recv(BUFFER_SIZE) # recieve data from connection
        # if no data = close connection
        if not data:
            break
        # decode the message
        message = data.decode('utf-8') # decode data from bytes to string
        splitted = message.split(' ') # split the command
        # check the command
        if splitted[0] == 'subscribe':
            subscribe(connection, address, splitted[1])
        elif splitted[0] == 'publish':
            publish(address, splitted[1], splitted[2])

    connection.close() # close the connection  
    update_subscriber() # remove colsed subscriber connection 
    update_topic() # update topic dictionary if some subscribers are closed
    print('Closed connection from ' + str(address[0]) + ':' + str(address[1]))


# --- Socket Handler ------------------------------------------------------------------------

# if there is a specific host and port in argument
if len(sys.argv) > 1:
    ip = sys.argv[1]
    splitted = ip.split(':')
    host = splitted[0]
    if len(splitted) > 1: # have specified port
        port = int(splitted[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make socket instance, AF_INET = address family ipv4. SOCK_STREAM = connection oriented TCP protocol.
s.bind((host, port)) # bind server to configured host and port
s.listen() # start listen for incomming message
print('Started listining at \'' + host + ':' + str(port) + '\'')

# wait for connection forever
while True:
    connection, address = s.accept() # wait for new connection
    print('Established connection from ' + str(address[0]) + ':' + str(address[1]))
    threading.Thread(target=handle_message, args=(connection, address)).start() # start new thread and new loop again

s.close() # close the socket