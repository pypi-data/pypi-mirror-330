import json

from .conns_service import ConnectionsService
from .netgrp_service import NetGroupService

# +----------------+          +----------------+
# |     VNet       |          |  SessionManager|
# |----------------|          |----------------|
# | - connections  |<>--------| - sessions     |
# | - netgrp       |          | + manage_conn  |
# | - session_mgr  |          | + update_state |
# +----------------+          +----------------+
#         |
#         |
#         |
#         |
# +----------------+          +------------------+
# |  Connection    |<>--------|   TCPSession     |
# |----------------|          |------------------|
# | + id           |          | - state          |
# | + src_host     |          | - congestion_win |
# | + dst_host     |          | + establish      |
# | + send_packet  |          | + close          |
# | + recv_packet  |          | + handle_timeout |
# +----------------+          +------------------+


class VNet:
    """
    负责网络拓扑的管理

    Attributes:
            - `networks_dict: dict[str,NetGroup]`: 维护 id: NetGroup字典集合，其中id用于标识一个NetGroup；
            - `connections: Connections`: 维护连接，一个Connections形如`(src_host, dst_host, src_ip, dst_ip,proto)`
    """

    netgrp_service: NetGroupService = NetGroupService()
    conns_service: ConnectionsService = ConnectionsService()

    def __str__(self):
        """
        Return a JSON-formatted string representation of the VNet.

        Returns:
                str: JSON string containing networks and connections information.
        """
        networks_json = {k: str(v.network) for k, v in self.netgrp_service.networks_dict.items()}
        connections_json = {str(k): str(conn) for k, conn in self.conns_service.connections.items()}
        return json.dumps({"networks": networks_json, "connections": connections_json}, indent=2)

    def __repr__(self):
        """
        Return the string representation of the VNet.

        Returns:
                str: String representation of the VNet.
        """
        return str(self)
