import time
import zmq

def publisher1():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    while True:
        count = 99

        while True:
            time.sleep(1)
            socket.send_string('publisher1 pushes event %d' % count)
            print('push event %d' % count)
            count += 1

if __name__ == "__main__":
    publisher1()

