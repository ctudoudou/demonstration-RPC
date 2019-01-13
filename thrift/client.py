import sys
import time

sys.path.append('./gen-py')

from Hello import HelloWorld
from Hello.ttypes import *
from Hello.constants import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
    # Make socket
    transport = TSocket.TSocket('127.0.0.1', 8000)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = HelloWorld.Client(protocol)

    # Connect!
    transport.open()

    client.ping()
    print("ping()")

    msg = client.sayHello()
    print(msg)
    msg = client.sayMsg(HELLO_YK)
    print(msg)

    transport.close()

except Thrift.TException as tx:
    print("%s" % (tx.message))
