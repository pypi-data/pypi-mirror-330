import errno
import logging
import select
import socket
import threading
from collections.abc import Callable
from typing import Any


class SocketManager:
    """
    套接字管理器，负责创建、管理和监听UDP套接字
    """

    def __init__(self, ipv4_addr: str, port: int, logger: logging.Logger):
        self.ipv4_addr = ipv4_addr
        self.port = port
        self.sock = None
        self.running = False
        self.thread = None
        self.socket_registry: dict[int, socket.socket] = {}
        self.packet_handler = None
        self.logger = logger

    def initialize(self):
        """初始化UDP套接字"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ipv4_addr, self.port))
        self.sock.setblocking(False)
        self.logger.info(f"套接字初始化完成，监听于 {self.ipv4_addr}:{self.port}")

    def set_packet_handler(self, handler: Callable[[bytes, tuple], Any]):
        """设置数据包处理函数"""
        self.packet_handler = handler

    def start_listening(self):
        """开始监听数据包"""
        if self.sock is None:
            self.initialize()

        self.running = True
        self.thread = threading.Thread(target=self._listen_loop)
        self.thread.daemon = True
        self.thread.start()
        self.logger.info("开始监听数据包")

    def stop_listening(self):
        """停止监听数据包"""
        self.running = False
        if self.thread:
            self.thread.join()
        if self.sock:
            self.sock.close()
            self.sock = None
        self.logger.info("停止监听数据包")

    def _listen_loop(self):
        """监听循环，接收数据包并调用处理函数"""
        while self.running:
            try:
                readable, _, _ = select.select([self.sock], [], [], 0.1)
                if not readable:
                    continue

                data, addr = self.sock.recvfrom(2048)
                self.logger.info(f"接收到来自 {addr} 的数据包，大小: {len(data)} 字节")

                if self.packet_handler:
                    self.packet_handler(data, addr)

            except Exception as e:
                if isinstance(e, socket.error) and e.errno == errno.EWOULDBLOCK:
                    continue
                self.logger.error(f"监听循环错误: {e}")

    def send_packet(self, data: bytes, addr: tuple):
        """发送数据包到指定地址"""
        if not self.sock:
            self.logger.error("套接字未初始化，无法发送数据包")
            return False

        try:
            self.sock.sendto(data, addr)
            self.logger.info(f"发送数据包到 {addr}，大小: {len(data)} 字节")
            return True
        except Exception as e:
            self.logger.error(f"发送数据包错误: {e}")
            return False

    def register_socket(self, sock: socket.socket) -> int:
        """注册套接字并返回文件描述符"""
        fd = sock.fileno()
        self.socket_registry[fd] = sock
        return fd

    def get_socket(self, fd: int) -> socket.socket:
        """根据文件描述符获取套接字"""
        return self.socket_registry.get(fd)  # type: ignore

    def create_client_socket(self):
        """创建客户端套接字"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ipv4_addr, 0))  # 随机端口
        fd = self.register_socket(sock)
        self.logger.info(f"创建客户端套接字，本地地址: {sock.getsockname()}")
        return sock, fd

    def cleanup(self):
        """清理所有套接字资源"""
        self.stop_listening()
        for sock in self.socket_registry.values():
            sock.close()
        self.socket_registry.clear()
        self.logger.info("清理所有套接字资源完成")
