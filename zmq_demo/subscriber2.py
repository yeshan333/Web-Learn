import zmq

def subscriber2():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:5555')
    socket.connect('tcp://127.0.0.1:5556')
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        message = socket.recv()
        print('message: %s' % message)

if __name__ == "__main__":
    subscriber2()