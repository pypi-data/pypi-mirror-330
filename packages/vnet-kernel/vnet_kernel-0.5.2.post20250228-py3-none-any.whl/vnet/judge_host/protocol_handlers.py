import socket
from abc import ABC, abstractmethod
from ctypes import pointer
from typing import Any

from vnet.structs_mapper.common import WINDOW_SIZE, Connection, sockaddr_in
from vnet.structs_mapper.rdup_struct import ACK, RUDPPacket, SenderWnd


class ProtocolHandler(ABC):
    """协议处理器抽象基类"""

    @abstractmethod
    def process_packet(self, data: bytes, addr: tuple[str, int], send_callback):
        """处理接收到的数据包"""
        pass

    @abstractmethod
    def create_connection(self, socket_fd: int, peer_addr: tuple[str, int], **kwargs) -> Any:
        """创建连接对象"""
        pass


class RUDPProtocolHandler(ProtocolHandler):
    """Reliable UDP协议处理器"""

    def __init__(self, logger):
        self.logger = logger

    def process_packet(self, data: bytes, addr: tuple[str, int], send_callback):
        """处理RUDP数据包"""
        self.logger.info(f"[RUDP] 处理来自 {addr} 的数据包，长度: {len(data) - 6} 字节")

        # RUDP协议特定的处理
        ack_packet = RUDPPacket()
        ack_packet.header.flag = ACK
        ack_packet.header.ack_num = data[1]  # 假设序列号在第二个字节
        ack_packet.header.rwnd = WINDOW_SIZE

        ack_bytes = bytes(ack_packet)
        send_callback(ack_bytes, addr)
        self.logger.info(f"[RUDP] 发送 ACK {ack_packet.header.ack_num}")

    def create_connection(self, socket_fd: int, peer_addr: tuple[str, int], **kwargs) -> Any:
        """创建RUDP连接对象"""
        init_base_seq = kwargs.get("init_base_seq", 0)
        next_seq = kwargs.get("next_seq", 0)
        unacked_packet_count = kwargs.get("unacked_packet_count", 0)
        peer_rwnd = kwargs.get("peer_rwnd", WINDOW_SIZE)

        # 创建Connection对象
        conn = Connection()
        conn.sockfd = socket_fd

        # 设置目标地址
        conn.dest_addr = sockaddr_in()
        conn.dest_addr.sin_family = socket.AF_INET
        conn.dest_addr.sin_port = socket.htons(peer_addr[1])

        # 将IP地址转换为网络字节序
        if peer_addr[0] == "localhost" or peer_addr[0] == "127.0.0.1":
            conn.dest_addr.sin_addr.s_addr = socket.htonl(socket.INADDR_LOOPBACK)
        else:
            conn.dest_addr.sin_addr.s_addr = socket.htonl(
                int.from_bytes(socket.inet_aton(peer_addr[0]), "big")
            )

        self.logger.info(f"[RUDP] 创建连接到 {peer_addr}")

        # 对于RUDP协议，我们可能需要在其他地方存储发送窗口信息，
        # 因为Connection结构不再包含send_window字段
        window = SenderWnd(init_base_seq, next_seq, unacked_packet_count, peer_rwnd)
        self.logger.info(
            f"[RUDP] 初始化发送窗口: base_seq={window.base_seq}, next_seq={window.next_seq}, unacked={window.unacked_packet_count}, peer_rwnd={window.peer_rwnd}"
        )

        # 在这里，我们可以将窗口信息存储在协议处理器中或其他地方
        # 这里简单地将窗口对象保存在协议处理器实例中
        self.window = window

        return pointer(conn)


class GBNProtocolHandler(ProtocolHandler):
    """Go-Back-N协议处理器，模拟GBN服务器行为"""

    def __init__(self, logger, window_size=WINDOW_SIZE):
        self.logger = logger
        self.window_size = window_size
        self.expected_seq_num = 0  # GBN协议中期望接收的下一个序列号
        self.window = None  # 存储窗口信息

        # 存储接收到的最大序列号，用于累计确认
        self.last_ack_sent = -1

        # 跟踪已接收的包，用于检测乱序和丢包
        self.received_packets = {}
        self.received_seqs = []  # 记录接收顺序，用于重传检测

        # 用于测试的特性
        self.specific_drops = set()  # 特定要丢弃的序列号
        self.ack_drops = set()  # 特定要丢弃的ACK的序列号

        # 序列号最大值（模拟序列号回绕）
        self.max_seq_num = 256  # 8位序列号，最大值为255

    def _is_in_order(self, seq_num: int) -> bool:
        """检查序列号是否按顺序到达"""
        if seq_num == self.expected_seq_num:
            return True
        return False

    def _update_expected_seq_num(self):
        """更新期望的下一个序列号"""
        self.expected_seq_num = (self.expected_seq_num + 1) % self.max_seq_num

    def _get_cumulative_ack(self) -> int:
        """获取累计确认的序列号"""
        return self.expected_seq_num - 1 if self.expected_seq_num > 0 else self.max_seq_num - 1

    def process_packet(self, data: bytes, addr: tuple[str, int], send_callback):
        """处理GBN数据包，实现GBN服务器的行为"""
        self.logger.info(f"[GBN] 处理来自 {addr} 的数据包，长度: {len(data) - 6} 字节")

        # 假设序列号在数据的第二个字节
        packet_seq_num = data[1]
        self.logger.info(f"[GBN] 收到序列号 {packet_seq_num}，期望序列号 {self.expected_seq_num}")

        # 记录收到的序列号，用于重传检测
        self.received_seqs.append(packet_seq_num)

        # 测试特性：如果序列号在丢弃列表中，模拟包丢失
        if packet_seq_num in self.specific_drops:
            self.logger.info(f"[GBN] 故意丢弃序列号 {packet_seq_num}")
            return

        # 记录收到的包数据
        packet_data = data[6 : 6 + data[2]]  # 假设数据长度在第3个字节
        self.received_packets[packet_seq_num] = packet_data

        # GBN协议只接受按序列号顺序到达的包
        if self._is_in_order(packet_seq_num):
            # 收到期望的序列号，更新期望序列号
            self._update_expected_seq_num()

            # 检查是否有连续包已经收到
            while self.expected_seq_num in self.received_packets:
                self._update_expected_seq_num()

            # 发送累计确认
            cumulative_ack = self._get_cumulative_ack()
            self.last_ack_sent = cumulative_ack

            # 测试特性：如果ACK序列号在丢弃列表中，模拟ACK丢失
            if cumulative_ack in self.ack_drops:
                self.logger.info(f"[GBN] 故意丢弃ACK {cumulative_ack}")
                return

            ack_packet = RUDPPacket()
            ack_packet.header.flag = ACK
            ack_packet.header.ack_num = cumulative_ack
            ack_packet.header.rwnd = self.window_size

            ack_bytes = bytes(ack_packet)
            send_callback(ack_bytes, addr)
            self.logger.info(f"[GBN] 发送累计ACK {cumulative_ack}")
        else:
            # 收到乱序包，GBN协议会忽略乱序包，重新发送最后一个ACK

            # 测试特性：如果ACK序列号在丢弃列表中，模拟ACK丢失
            if self.last_ack_sent in self.ack_drops:
                self.logger.info(f"[GBN] 故意丢弃乱序ACK {self.last_ack_sent}")
                return

            ack_packet = RUDPPacket()
            ack_packet.header.flag = ACK
            ack_packet.header.ack_num = self.last_ack_sent
            ack_packet.header.rwnd = self.window_size

            ack_bytes = bytes(ack_packet)
            send_callback(ack_bytes, addr)
            self.logger.info(f"[GBN] 收到乱序包 {packet_seq_num}，重发ACK {self.last_ack_sent}")

    def create_connection(self, socket_fd: int, peer_addr: tuple[str, int], **kwargs) -> Any:
        """创建GBN连接对象"""
        init_base_seq = kwargs.get("init_base_seq", 0)
        next_seq = kwargs.get("next_seq", 0)
        unacked_packet_count = kwargs.get("unacked_packet_count", 0)
        peer_rwnd = kwargs.get("peer_rwnd", self.window_size)

        # 创建Connection对象
        conn = Connection()
        conn.sockfd = socket_fd

        # 设置目标地址
        conn.dest_addr = sockaddr_in()
        conn.dest_addr.sin_family = socket.AF_INET
        conn.dest_addr.sin_port = socket.htons(peer_addr[1])

        # 将IP地址转换为网络字节序
        if peer_addr[0] == "localhost" or peer_addr[0] == "127.0.0.1":
            conn.dest_addr.sin_addr.s_addr = socket.htonl(socket.INADDR_LOOPBACK)
        else:
            conn.dest_addr.sin_addr.s_addr = socket.htonl(
                int.from_bytes(socket.inet_aton(peer_addr[0]), "big")
            )

        self.logger.info(f"[GBN] 创建连接到 {peer_addr}")

        # 创建发送窗口
        window = SenderWnd(init_base_seq, next_seq, unacked_packet_count, peer_rwnd)
        self.logger.info(
            f"[GBN] 初始化发送窗口: base_seq={window.base_seq}, next_seq={window.next_seq}, unacked={window.unacked_packet_count}, peer_rwnd={window.peer_rwnd}"
        )
        self.window = window

        return pointer(conn)

    def reset(self):
        """重置GBN协议状态"""
        self.expected_seq_num = 0
        self.last_ack_sent = -1
        self.received_packets.clear()
        self.received_seqs.clear()
        self.specific_drops.clear()
        self.ack_drops.clear()

        # 如果需要，也可以重置窗口状态
        if self.window:
            self.window.base_seq = 0
            self.window.next_seq = 0
            self.window.unacked_packet_count = 0
