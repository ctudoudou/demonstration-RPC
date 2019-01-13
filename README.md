# RPC 演示仓库

**注：本仓库演示的是基于`gRPC`和`Thrift`框架的Python语言版本简单应用。**

## gRPC演示

### 0x00 安装环境
因为本案例仅演示Python版本，所以只需要安装一个`grpcio-tools`库就可以啦。
执行命令
```bash
pip install grpcio-tools
```

### 0x01 编写一个结构数据序列化文件
新建一个文件`Hello.proto`。写入内容
```protobuf
syntax = "proto3";

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

使用`grpcio-tools`将这个文件转成Python版本，执行命令。
```bash
python3 -m grpc_tools.protoc --proto_path=.  --python_out=. --grpc_python_out=. Hello.proto
```

### 0x03 编写客户端和服务端

```python
# client.py

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

```

```python
# server.py

from concurrent import futures
import time
import logging

import grpc

from . import Hello_pb2
from . import Hello_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(Hello_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print(request.name)
        return Hello_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()

```

### 0x04 运行它！

文件树如下
```
.
├── Hello.proto
├── Hello_pb2.py
├── Hello_pb2_grpc.py
├── clinet.py
└── server.py
```


OK，到此，我们来执行一下吧。
```bash
python server.py
```
```bash
# 另起一个终端
python clinet.py
```

## Thrift演示

### 0x00 准备一下环境
```bash
# Ubuntu下执行
sudo apt install thrift-compiler
# OS X 下执行
brew install thrift
```
emmmm，就这一句话就可以啦

### 0x01 再编写一个结构数据序列化文件
gRPC和Thrift的框架序列化文件不通用哦

```thrift
const string HELLO_YK = "yk"
service HelloWorld {
    void ping(),
    string sayHello(),
    string sayMsg(1:string msg)
}
```
（PS：感觉好像简单很多的样子）

执行命令，将文件转成Python语言版本
```bash
thrift -r --gen py Hello.thrift 
# 如果转C++语言的话，将py修改成cpp即可，其他语言皆可。
thrift -r --gen cpp Hello.thrift 
thrift -r --gen go Hello.thrift 
```

### 0x02 编写客户端和服务端
```python
# client.py

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
```

```python
# server.py

import sys

sys.path.append('./gen-py')

from Hello import HelloWorld
from Hello.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import socket


class HelloWorldHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        print("ping()")

    def sayHello(self):
        print("sayHello()")

        return "say hello from " + socket.gethostname()

    def sayMsg(self, msg):
        print("sayMsg(" + msg + ")")
        return "say " + msg + " from " + socket.gethostname()


handler = HelloWorldHandler()
processor = HelloWorld.Processor(handler)
transport = TSocket.TServerSocket('127.0.0.1', 8000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Starting python server...")
server.serve()
print("done!")

```

### 0x04 运行它！

文件树如下
```
├── Hello.thrift
├── client.py
├── gen-py
│   ├── Hello
│   │   ├── HelloWorld-remote
│   │   ├── HelloWorld.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── constants.py
│   │   └── ttypes.py
│   └── __init__.py
└── server.py

```


OK，到此，我们来执行一下吧。
```bash
python server.py
```
```bash
# 另起一个终端
python clinet.py
```
代码均在仓库中可以找到。

**土豆豆，写于2019年1月13日**
