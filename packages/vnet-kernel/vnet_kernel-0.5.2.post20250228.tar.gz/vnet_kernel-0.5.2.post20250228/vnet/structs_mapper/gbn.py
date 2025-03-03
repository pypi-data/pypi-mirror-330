from ctypes import Structure, c_char, c_uint8, c_uint16

from .common import MAX_PACKET_SIZE


# 数据包结构
class Packet(Structure):
    _fields_ = [("seq", c_uint8), ("len", c_uint16), ("data", c_char * MAX_PACKET_SIZE)]


# ACK数据包结构
class ACKPacket(Structure):
    _fields_ = [("ack", c_uint8)]
