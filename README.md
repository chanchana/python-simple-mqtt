# Simple-MQTT
Simple MQTT python program including Broker, Subscriber, Publisher. Support wildcard matching.

### Requirement
- python3

## Broker Usage

    python3 broker.py [BROKER HOST]:[BROKER PORT]

Run with default port(80):

    sudo python3 broker.py [BROKER IP]

## Subscriber Usage

    python3 subscriber.py [BROKER IP] [TOPIC NAME]
    
## Publisher Usage

    python3 publisher.py [BROKER IP] [TOPIC NAME] [DATA TO PUBLISH]


### Example
#### Broker
    python3 broker.py localhost:8080
#### Subscriber
    python3 subscriber.py localhost:8080 /kitchen/light
    python3 subscriber.py localhost:8080 /bedroom/light
    python3 subscriber.py localhost:8080 /kitchen/fan
#### Subscriber
    python3 publisher.py localhost:8080 /bedroom/light value=on
    python3 publisher.py localhost:8080 /+/light value=on
    python3 publisher.py localhost:8080 /kitchen/# value=off