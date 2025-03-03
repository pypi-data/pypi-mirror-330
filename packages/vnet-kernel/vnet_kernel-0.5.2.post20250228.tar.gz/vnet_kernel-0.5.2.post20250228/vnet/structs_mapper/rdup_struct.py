from ctypes import Structure, c_char, c_uint8, c_uint16, c_uint32

from .common import MAX_PACKET_SIZE

# Constants matching C implementation
BUFFER_SIZE = 256
# Packet flags
SYN = 0x01
ACK = 0x02
FIN = 0x04


class RUDPHeader(Structure):
    _fields_ = [
        ("flag", c_uint8),
        ("seq_num", c_uint8),
        ("ack_num", c_uint8),
        ("rwnd", c_uint8),
        ("data_len", c_uint16),
    ]


class RUDPPacket(Structure):
    _fields_ = [("header", RUDPHeader), ("data", c_char * MAX_PACKET_SIZE)]


class WindowSlot(Structure):
    _fields_ = [
        ("packet", RUDPPacket),
        ("send_time", c_uint32),
        ("retries", c_uint8),
    ]


class SenderWnd(Structure):
    _fields_ = [
        ("packets_buffer", WindowSlot * BUFFER_SIZE),
        ("base_seq", c_uint8),
        ("next_seq", c_uint8),
        ("unacked_packet_count", c_uint8),
        ("peer_rwnd", c_uint8),
    ]

    def __init__(self, base_seq: int, next_seq: int, unacked_packet_count: int, peer_rwnd: int) -> None:
        self.base_seq = base_seq
        self.next_seq = next_seq
        self.unacked_packet_count = unacked_packet_count
        self.peer_rwnd = peer_rwnd
