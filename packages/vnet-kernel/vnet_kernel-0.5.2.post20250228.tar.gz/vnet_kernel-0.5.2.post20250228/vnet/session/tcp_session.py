"""TCP Session 用于存储 TCP 对话的状态信息，包括本地和远程 IP 地址和端口、序列号、确认号、发送和接收的数据包等。

Typical usage example:

        session = TcpSession(local_ip, local_port, remote_ip, remote_port)
        # TODO 设计完了再补充
"""

import ipaddress
import logging
import random
from dataclasses import dataclass, field
from enum import Enum, auto

from scapy.all import send, sr1
from scapy.layers.inet import IP, TCP


# Enums for TCP State and Congestion Control Phase
class TcpState(Enum):
    CLOSED = auto()  # 1
    LISTEN = auto()
    SYN_SENT = auto()
    SYN_RECEIVED = auto()
    ESTABLISHED = auto()
    FIN_WAIT_1 = auto()
    FIN_WAIT_2 = auto()
    CLOSE_WAIT = auto()
    CLOSING = auto()
    LAST_ACK = auto()
    TIME_WAIT = auto()  # 11


@dataclass
class TcpSession:
    local_ip: ipaddress.IPv4Address
    local_port: int
    remote_ip: ipaddress.IPv4Address
    remote_port: int
    state: TcpState = TcpState.CLOSED
    state_changes: list = field(default_factory=list)
    seq_num: int = field(default_factory=lambda: random.randint(0, 0xFFFFFFFF))
    ack_num: int = 0
    packets_sent: list = field(default_factory=list)
    packets_received: list = field(default_factory=list)

    def __post_init__(self):
        self.state_changes.append(self.state)

    def change_state(self, new_state: TcpState):
        logging.debug(f"State transition: {self.state} -> {new_state}")
        self.state = new_state
        self.state_changes.append(new_state)

    def create_packet(self, flags="", data=b""):
        pkt = (
            IP(src=str(self.local_ip), dst=str(self.remote_ip))
            / TCP(
                sport=self.local_port,
                dport=self.remote_port,
                seq=self.seq_num,
                ack=self.ack_num,
                flags=flags,
            )
            / data
        )
        return pkt

    def send_packet(self, pkt):
        send(pkt)
        self.packets_sent.append(pkt)
        logging.info(f"Packet sent: {pkt.summary()}")

    def receive_packet(self):
        response = sr1(
            IP(dst=self.remote_ip) / TCP(sport=self.local_port, dport=self.remote_port),
            timeout=1,
            verbose=0,
        )
        if response:
            self.packets_received.append(response)
            logging.info(f"Packet received: {response.summary()}")
            return response
        else:
            logging.warning("No response received.")
            return None

    def handle_ack(self, ack_num):
        self.ack_num = ack_num
        logging.info(f"ACK received: {ack_num}")

    @property
    def state_change_log(self):
        return " -> ".join(str(state) for state in self.state_changes)
