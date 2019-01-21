import sys

# sys.path.append('./gen-py')

from ml import Filebuff
from ml.ttypes import *

from keras.models import load_model
from PIL import Image
import numpy as np

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import socket

boxs = [(5, 1, 17, 21), (17, 1, 29, 21), (29, 1, 41, 21), (41, 1, 53, 21)]
app = load_model('net.h5')
dic_ = {0: 'r', 1: 'u', 2: '9', 3: '0', 4: '7', 5: 'i', 6: 'n', 7: 'g', 8: '6', 9: 'z', 10: '1', 11: '8', 12: 't',
        13: 's', 14: 'a', 15: 'f', 16: 'o', 17: 'h', 18: 'm', 19: 'j', 20: 'c', 21: 'd', 22: 'v', 23: 'q', 24: '4',
        25: 'x', 26: '3', 27: 'e', 28: 'b', 29: 'k', 30: 'l', 31: '2', 32: 'y', 33: '5', 34: 'p', 35: 'w'}


class FilebuffHandler:
    def __init__(self):
        self.log = {}

    def predict(self, data):
        open('./tmp/{}'.format(data.name), 'wb+').write(data.buff)
        img = Image.open('./tmp/{}'.format(data.name)).convert('L').convert('1')
        name = ''
        for x in range(len(boxs)):
            aaa = []
            roi = img.crop(boxs[x])
            roi = np.array(roi)
            aaa.append([roi])
            aaa = np.array(aaa)
            aaa = app.predict(aaa)
            name += dic_[np.argmax(aaa)]
        return name


handler = FilebuffHandler()
processor = Filebuff.Processor(handler)
transport = TSocket.TServerSocket('127.0.0.1', 8000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Starting python server...")
server.serve()
print("done!")
