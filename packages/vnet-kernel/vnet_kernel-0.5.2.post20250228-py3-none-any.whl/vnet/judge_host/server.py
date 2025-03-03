import logging

from .network_simulator import NetworkSimulator
from .protocol_handlers import GBNProtocolHandler, ProtocolHandler, RUDPProtocolHandler
from .socket_manager import SocketManager


def setup_logger(name, log_file=None):
    """设置并返回日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class UDPServer:
    def __init__(self, ipv4_addr: str, host_name="Reliable_Server", port=8000, packet_loss_rate=0.0, delay_ms=0, protocol_type="rudp", protocol_params=None):
        self.ipv4_addr = ipv4_addr
        self.host_name = host_name
        self.logger = setup_logger(f"{host_name}", f"{host_name.lower()}.log")
        self.network_simulator = NetworkSimulator(packet_loss_rate, delay_ms)
        self.socket_manager = SocketManager(ipv4_addr, port, self.logger)
        protocol_params = protocol_params or {}
        self.protocol_handler = self._create_protocol_handler(protocol_type, protocol_params)
        self.socket_manager.set_packet_handler(self._handle_packet)

    def _create_protocol_handler(self, protocol_type, params) -> ProtocolHandler:
        """创建协议处理器"""
        if protocol_type.lower() == "rudp":
            return RUDPProtocolHandler(self.logger)
        elif protocol_type.lower() == "gbn":
            window_size = params.get("window_size", 4)
            return GBNProtocolHandler(self.logger, window_size)
        else:
            raise ValueError(f"不支持的协议类型: {protocol_type}")

    def start(self):
        """启动服务器"""
        self.socket_manager.initialize()
        self.socket_manager.start_listening()
        self.logger.info(f"{self.host_name} 服务器已启动")

    def stop(self):
        """停止服务器"""
        self.socket_manager.stop_listening()
        self.socket_manager.cleanup()
        self.logger.info(f"{self.host_name} 服务器已停止")

    def set_network_conditions(self, packet_loss_rate=None, delay_ms=None):
        """设置网络条件"""
        self.network_simulator.set_conditions(packet_loss_rate, delay_ms)
        self.logger.info(f"网络条件已更新: 丢包率={self.network_simulator.packet_loss_rate}, 延迟={self.network_simulator.delay_ms}ms")

    def _handle_packet(self, data: bytes, addr: tuple):
        """处理接收到的数据包"""
        self.logger.info(f"接收到来自 {addr} 的数据包")

        # 检查是否应该丢弃数据包
        if self.network_simulator.should_drop_packet():
            return

        # 应用网络延迟
        self.network_simulator.apply_delay()

        # 使用协议处理器处理数据包
        self.protocol_handler.process_packet(data, addr, self.socket_manager.send_packet)

    def create_conn_with_srv(self, srv_port=8000, **kwargs):
        """创建与服务器的连接"""
        # 创建客户端套接字
        sock, fd = self.socket_manager.create_client_socket()

        # 创建连接对象
        peer_addr = ("127.0.0.1", srv_port)
        conn = self.protocol_handler.create_connection(fd, peer_addr, **kwargs)

        return conn
