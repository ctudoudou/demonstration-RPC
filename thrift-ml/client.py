import sys
import time

sys.path.append('./gen-py')

from ml import Filebuff
from ml.ttypes import *
from ml.constants import *

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
    client = Filebuff.Client(protocol)

    # Connect!
    transport.open()

    a = FileData('0.gif', open('0.gif', 'rb').read())
    a = client.predict(a)
    print(a)

    transport.close()

except Thrift.TException as tx:
    print("%s" % (tx.message))
