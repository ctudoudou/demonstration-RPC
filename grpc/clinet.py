import logging
import time
import grpc

from . import Hello_pb2
from . import Hello_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = Hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(Hello_pb2.HelloRequest(name='world'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    start = time.time()
    run()
