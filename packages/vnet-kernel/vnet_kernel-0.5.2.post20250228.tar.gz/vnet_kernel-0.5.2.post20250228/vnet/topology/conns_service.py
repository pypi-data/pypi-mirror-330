"""用于表示互联网上两台主机是否连通"""

from __future__ import annotations

from dataclasses import dataclass

from vnet.lib.status_logger import Status, service_logger
from vnet.net_addr import Ip4Host


@dataclass
class Connection:
    """
    表示网络连接的类，包含源主机、目标主机

    Connection只负责通用的连接管理，不涉及协议状态或传输控制
    各协议的细节逻辑由Session子类处理。

    Properties:
            - `cli_host`
            - `srv_host`
            - `cli_addr`
            - `srv_addr`

    Methods:
            - `init_sessions`
            - `send_packet`
    """

    cli_host: Ip4Host
    srv_host: Ip4Host

    def __init__(
        self,
        cli_host: Ip4Host,
        srv_host: Ip4Host,
    ):
        """
        Initialize a new Connection instance.

        Args:
                cli_host (Ip4Host): Client host.
                srv_host (Ip4Host): Server host.
                cli_port (int): Client port.
                srv_port (int): Server port.
        """
        self.cli_host = cli_host
        self.srv_host = srv_host

    @property
    def cli_addr(self):
        """Get the client's IP address."""
        return self.cli_host.ip_address

    @property
    def srv_addr(self):
        """Get the server's IP address."""
        return self.srv_host.ip_address


class ConnectionsService:
    connections: dict[str, Connection]

    def __init__(self):
        self.connections = {}

    @service_logger
    def add_conn(
        self,
        conn_id: str,
        cli_host: Ip4Host,
        srv_host: Ip4Host,
    ) -> Status:
        """
        Add a new connection to the manager.

        Args:
                conn_id (str): Connection identifier.
                cli_host (Ip4Host): cli host.
                srv_host (Ip4Host): srv host.

        Returns:
                Status: SUCCESS | CONN_ALREADY_EXISTS.
        """
        if conn_id in self.connections:
            return Status.CONN_ALREADY_EXISTS
        # 创建并添加新连接
        conn = Connection(cli_host, srv_host)
        self.connections[conn_id] = conn
        return Status.SUCCESS

    @service_logger
    def rm_conn(self, conn_id: str) -> Status:
        """
        Remove a connection by its identifier.

        Args:
                conn_id (str): Connection identifier.

        Returns:
                Status: SUCCESS | CONN_NOT_FOUND.
        """
        if conn_id in self.connections:
            del self.connections[conn_id]
            return Status.SUCCESS
        return Status.CONN_NOT_FOUND

    @service_logger
    def get_conn_by_id(self, conn_id: str) -> Connection | Status:
        """
        Retrieve a connection by its identifier.

        Args:
                conn_id (str): Connection identifier.

        Returns:
                Connection | Status: The connection object or status if not found.
        """
        return self.connections.get(conn_id, Status.CONN_NOT_FOUND)
