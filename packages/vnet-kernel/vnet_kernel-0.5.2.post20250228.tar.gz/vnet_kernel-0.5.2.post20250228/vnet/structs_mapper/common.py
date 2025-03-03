import ipaddress
import socket
import struct
from ctypes import Structure, c_char, c_int, c_uint16, c_uint32, c_ushort

TIMEOUT_SEC = 1
MAX_PACKET_SIZE = 512
WINDOW_SIZE = 16


class in_addr(Structure):
    _fields_ = [("s_addr", c_uint32)]


class sockaddr_in(Structure):
    _fields_ = [
        ("sin_family", c_ushort),
        ("sin_port", c_uint16),
        ("sin_addr", in_addr),
        ("sin_zero", c_char * 8),
    ]

    def __init__(self, srv_port=8000, ip_addr="127.0.0.1"):
        """
        初始化 sockaddr_in 结构体

        参数:
            srv_port: 服务端口号，默认为8000
        """
        super(sockaddr_in, self).__init__()

        self.sin_zero = (c_char * 8)()  # 初始化为全0
        self.sin_family = socket.AF_INET
        self.sin_port = socket.htons(srv_port)
        self.sin_addr.s_addr = socket.htonl(socket.INADDR_LOOPBACK)  # 使用localhost (127.0.0.1)

        # 处理IP地址
        ip = ipaddress.IPv4Address(ip_addr)
        # 将IPv4Address对象转换为网络字节序的整数
        self.sin_addr.s_addr = struct.unpack("!I", ip.packed)[0]


class Connection(Structure):
    _fields_ = [("sockfd", c_int), ("dest_addr", sockaddr_in)]
