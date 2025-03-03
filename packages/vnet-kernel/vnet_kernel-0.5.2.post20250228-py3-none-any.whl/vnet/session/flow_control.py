"""FlowControl class

当 TCP 连接接收到正确且顺序正确的字节时，它会将数据放入接收缓冲区(TCP data
        in buffer)。相关的应用程序进程(Application process )将从这个缓冲区读取数据
        进程从 buffer 中读取数据的时机是不确定的，可能在数据到达的瞬间读取，也可能
        在数据到达很久之后才尝试读取数据。如果应用程序读取数据的速度相对较慢，发送
        者很容易通过过快地发送过多的数据来溢出连接的接收缓冲区。

        ```ascii
                                                                        receive buffer diagram

                        | <----------------------  Recv  Buffer Size  -----------------------> |
                        +-----------------------+----------------------+-----------------------+
                        |  Bytes Already Read   |   Bytes in Buffer    |    Free Space         |
                        +-----------------------+----------------------+-----------------------+
                        ^                      ^                      ^                        ^
        index:  0              last_byte_read       last_byte_rcvd              buffer_size

        ```
"""

import logging
from collections import deque


class FlowControl:
    def __init__(self, buffer_size: int = 1024):
        """
        Initialize FlowControl with specified buffer size and metrics.

        Args:
                buffer_size (int, optional): Maximum size for send and receive buffers. Defaults to 1024.
        """
        self.recv_buffer = deque(maxlen=buffer_size)
        self.send_buffer = deque(maxlen=buffer_size)
        self._buffer_size = buffer_size
        self._last_byte_rcvd = 0  # Last byte received
        self._last_byte_read = 0  # Last byte read

        # Metrics for analysis
        self.total_bytes_written = 0
        self.total_bytes_read = 0
        self.max_buffer_usage = 0
        self.overflow_count = 0
        self.underflow_count = 0

    @property
    def recv_buffer_size(self) -> int:
        return len(self.recv_buffer)

    @property
    def send_buffer_size(self) -> int:
        return len(self.send_buffer)

    @property
    def recv_window(self) -> int:
        """Available space in the receive buffer."""
        return self._buffer_size - self.recv_buffer_size

    @property
    def buffer_usage(self) -> float:
        """Percentage of buffer usage."""
        return (self.recv_buffer_size / self._buffer_size) * 100

    def write_to_recv_buffer(self, data: bytes):
        """
        Write data to the receive buffer and update metrics.

        Args:
                data (bytes): Bytes to write to the buffer.

        Raises:
                BufferError: If there is not enough space in the receive buffer.
        """
        if len(data) > self.recv_window:
            self.overflow_count += 1
            logging.warning(f"Buffer overflow attempt with {len(data)} bytes.")
            raise BufferError("Not enough space in the receive buffer.")

        self.recv_buffer.extend(data)
        self._last_byte_rcvd += len(data)
        self.total_bytes_written += len(data)
        self.max_buffer_usage = max(self.max_buffer_usage, self.recv_buffer_size)

        logging.info(
            f"Data written to recv buffer. "
            f"Total bytes: {self.total_bytes_written}, Buffer usage: {self.buffer_usage:.2f}%."
        )

    def read_from_recv_buffer(self, read_len: int) -> bytes:
        """
        Read a specified number of bytes from the receive buffer.

        Args:
                read_len (int): Number of bytes to read.

        Returns:
                bytes: Data read from the buffer.

        Raises:
                BufferError: If the receive buffer is empty.
        """
        if self.recv_buffer_size == 0:
            self.underflow_count += 1
            logging.warning("Buffer underflow attempt.")
            raise BufferError("No data available in the receive buffer.")

        read_len = min(read_len, self.recv_buffer_size)
        data = b"".join(self.recv_buffer.popleft() for _ in range(read_len))
        self._last_byte_read += len(data)
        self.total_bytes_read += len(data)

        logging.info(
            f"Data read from recv buffer. "
            f"Total bytes: {self.total_bytes_read}, Buffer usage: {self.buffer_usage:.2f}%."
        )
        return data

    def write_to_send_buffer(self, data: bytes):
        """
        Write data to the send buffer.

        Args:
                data (bytes): Bytes to write to the send buffer.

        Raises:
                BufferError: If there is not enough space in the send buffer.
        """
        if len(data) > self._buffer_size - self.send_buffer_size:
            self.overflow_count += 1
            logging.warning(f"Send buffer overflow attempt with {len(data)} bytes.")
            raise BufferError("Not enough space in the send buffer.")

        self.send_buffer.extend(data)

    def read_from_send_buffer(self, read_len: int) -> bytes:
        """
        Read a specified number of bytes from the send buffer.

        Args:
                read_len (int): Number of bytes to read.

        Returns:
                bytes: Data read from the send buffer.

        Raises:
                BufferError: If the send buffer is empty.
        """
        if self.send_buffer_size == 0:
            self.underflow_count += 1
            logging.warning("Send buffer underflow attempt.")
            raise BufferError("No data available in the send buffer.")

        read_len = min(read_len, self.send_buffer_size)
        return b"".join(self.send_buffer.popleft() for _ in range(read_len))

    def simulate_slow_reader(self, delay: float, read_len: int):
        """
        Simulate a slow reader by introducing delays between reads.

        Args:
                delay (float): Delay in seconds between reads.
                read_len (int): Number of bytes to read at each interval.
        """
        import time

        while self.recv_buffer_size > 0:
            logging.info("Simulating slow reader...")
            self.read_from_recv_buffer(read_len)
            time.sleep(delay)

    def reset_buffers(self):
        """
        Reset both send and receive buffers to their initial empty state.
        """
        self.recv_buffer.clear()
        self.send_buffer.clear()
        self._last_byte_rcvd = 0
        self._last_byte_read = 0
        logging.info("Buffers reset to initial state.")

    def get_metrics(self):
        """
        Retrieve current buffer metrics.

        Returns:
                dict: Dictionary containing metrics like total bytes written/read, max buffer usage, overflow and underflow counts.
        """
        return {
            "total_bytes_written": self.total_bytes_written,
            "total_bytes_read": self.total_bytes_read,
            "max_buffer_usage": self.max_buffer_usage,
            "overflow_count": self.overflow_count,
            "underflow_count": self.underflow_count,
        }

    def __repr__(self):
        """
        Return a string representation of the FlowControl instance.

        Returns:
                str: Representation showing receive and send buffer sizes and receive window.
        """
        return (
            f"<FlowControl(recv_buffer={self.recv_buffer_size}, "
            f"send_buffer={self.send_buffer_size}, recv_window={self.recv_window})>"
        )
