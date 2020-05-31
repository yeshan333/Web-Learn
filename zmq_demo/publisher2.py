import time
import zmq

def publisher2():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

    while True:
        count = 1

        while True:
            time.sleep(1)
            socket.send_string('publisher2 pushes event %d' % count)
            print('push event %d' % count)
            count += 1

if __name__ == "__main__":
    publisher2()