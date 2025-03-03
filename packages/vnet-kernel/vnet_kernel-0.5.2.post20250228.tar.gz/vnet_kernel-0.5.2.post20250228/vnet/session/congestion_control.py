"""Congestion Control，存储实现TCP拥塞控制算法所需的状态信息，包括拥塞窗口、慢启动阈值、重复ACK计数和拥塞阶段。

Typical usage example:

    congestion = CongestionControl()
        # TODO
"""

import logging
from enum import Enum, auto


class CongestionPhase(Enum):
    SLOW_START = auto()
    CONGESTION_AVOIDANCE = auto()
    FAST_RECOVERY = auto()


class CongestionControl:
    congestion_window: int = 1460  # Initial congestion window size
    ssthresh: int = 64  # Slow start threshold
    duplicate_ack_count: int = 0  # Counter for duplicate ACKs
    congestion_phase: CongestionPhase = CongestionPhase.SLOW_START  # Initial phase
    mss: int = 1460  # Maximum segment size (MSS)

    def reset(self):
        """
        Reset the congestion window and phase to their initial values.
        """
        self.congestion_window = 1
        self.congestion_phase = CongestionPhase.SLOW_START
        logging.debug("Congestion control reset.")

    def increase_window(self):
        """
        Increase the congestion window size based on the current congestion phase.
        """
        if self.congestion_phase == CongestionPhase.SLOW_START:
            self.congestion_window += 1
            if self.congestion_window >= self.ssthresh:
                self.congestion_phase = CongestionPhase.CONGESTION_AVOIDANCE
        elif self.congestion_phase == CongestionPhase.CONGESTION_AVOIDANCE:
            self.congestion_window += max(1, int(1 / self.congestion_window))

    def handle_duplicate_ack(self):
        """
        Handle duplicate acknowledgments to trigger fast recovery if necessary.
        """
        self.duplicate_ack_count += 1
        if self.duplicate_ack_count >= 3:
            self.ssthresh = max(self.congestion_window // 2, 2)
            self.congestion_window = self.ssthresh + 3
            self.congestion_phase = CongestionPhase.FAST_RECOVERY
            logging.debug("Fast recovery triggered.")

    def ack_received(self, ack_num: int, current_ack: int):
        """
        Process a received ACK number and adjust congestion window and phase accordingly.

        Args:
                ack_num (int): The acknowledgment number received.
                current_ack (int): The current acknowledgment number.
        """
        if ack_num > current_ack:
            self.duplicate_ack_count = 0
            self.increase_window()
        elif ack_num == current_ack:
            self.handle_duplicate_ack()
