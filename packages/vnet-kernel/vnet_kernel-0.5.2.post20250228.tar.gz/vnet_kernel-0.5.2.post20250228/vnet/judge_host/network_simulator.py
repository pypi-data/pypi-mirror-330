import random
import time
import logging


class NetworkSimulator:
    """
    网络模拟器，用于模拟网络条件（丢包、延迟）
    """

    def __init__(self, packet_loss_rate=0.0, delay_ms=0):
        self.packet_loss_rate = packet_loss_rate
        self.delay_ms = delay_ms
        self.logger = logging.getLogger("network_simulator")

    def set_conditions(self, packet_loss_rate=None, delay_ms=None):
        """设置网络条件"""
        if packet_loss_rate is not None:
            self.packet_loss_rate = packet_loss_rate
        if delay_ms is not None:
            self.delay_ms = delay_ms

    def should_drop_packet(self):
        """根据丢包率决定是否丢弃数据包"""
        drop = random.random() < self.packet_loss_rate
        if drop:
            self.logger.info("模拟丢包")
        return drop

    def apply_delay(self):
        """应用网络延迟"""
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)
