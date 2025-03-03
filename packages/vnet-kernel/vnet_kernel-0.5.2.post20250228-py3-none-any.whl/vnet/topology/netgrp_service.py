from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv4Network

from vnet.lib.ip4_host import Ip4Host, Ip4HostFactory
from vnet.lib.status_logger import Status, service_logger


@dataclass
class NetGroup:
    """
    NetGroup用于表示一个网段内的主机，

    Attributes:
        - `network: IPv4Address`: 通过Ip4Network表示网段号,`192.168.0.0/24` e.g；
        - `hosts: list[Ip4Host]`: 该网段内的主机

    Methods:
        - `add(self, host: Ip4Host)`: 添加主机
        - `remove(self, host: Ip4Host)`: 删除主机
        - `find_host(self, host: str | IPv4Address | Ip4Host) -> Ip4Host`: 查找主机
    """

    network: IPv4Network
    hosts: list[Ip4Host] = field(default_factory=list)

    def add(self, host: Ip4Host):
        """Add a host to the network group."""
        if host not in self.hosts:
            self.hosts.append(host)

    def remove(self, host: Ip4Host):
        """Remove a host from the network group."""
        self.hosts.remove(host)

    def find(self, host_address: str) -> Ip4Host | None:
        """
        Find a host in the network group by IP.

        Args:
            host (str): 192.168.1.1 e.g.

        Returns:
            Ip4Host | None: The found host or None if not found.
        """
        return next((h for h in self.hosts if str(h.ip_address) == host_address), None)


class NetGroupService:
    """
    Manage network groups.

    networks_dict:
        - str: 网络组的标识符，e.g. lan1,192.168.0.0/24,wan1 etc.
        - list[NetGroup]: 网络组，形如{IPv4Network,[Ip4Host1,Ip4Host2...]}
    """

    def __init__(self):
        self.networks_dict: dict[str, NetGroup] = {}

    @service_logger
    def add_netgrp(self, gid: str, network: str) -> Status:
        """
        Add a new network group.

        Args:
            gid (str): Network group identifier.
            network (str): Network range (e.g., '192.168.1.0/24').

        Returns:
            Status: NGRP_ALREADY_EXISTS or SUCCESS.
        """
        if gid in self.networks_dict:
            return Status.NGRP_ALREADY_EXISTS
        self.networks_dict[gid] = NetGroup(IPv4Network(network))
        return Status.SUCCESS

    @service_logger
    def rm_netgrp(self, gid: str) -> Status:
        """
        Remove a network group by its identifier.

        Args:
            gid (str): Network group identifier.

        Returns:
            Status: NGRP_NOT_FOUND or SUCCESS.
        """
        if gid in self.networks_dict:
            del self.networks_dict[gid]
            return Status.SUCCESS
        return Status.NGRP_NOT_FOUND

    # ================================
    # *     host manage
    # ================================

    @service_logger
    def add_host_to_netgrp(self, host_address: str | Ip4Host, netgrp_id: str) -> Status:
        """
        Add a host to a specified network group.

        Args:
            host_address (str): IP address of the host to remove. 192.168.1.1 e.g.
            netgrp_id (str): Network group identifier.

        Returns:
            Status: NGRP_NOT_FOUND or SUCCESS.
        """
        net_grp = self._get_netgrp_by_id(netgrp_id)
        if not net_grp:
            return Status.NGRP_NOT_FOUND

        match host_address:
            case Ip4Host():
                net_grp.add(host_address)
            case str():
                net_grp.add(Ip4HostFactory.from_address_and_network(host_address, net_grp.network))
        return Status.SUCCESS

    @service_logger
    def rm_host_from_netgrp(self, host_address: str, netgrp_id: str) -> Status:
        """
        Remove a single host from a specified network group.

        Args:
            host_address (str): IP address of the host to remove. 192.168.1.1 e.g.
            netgrp_id (str): Network group identifier.

        Returns:
            Status: NGRP_NOT_FOUND, HOST_NOT_FOUND, or SUCCESS.
        """
        net_grp = self._get_netgrp_by_id(netgrp_id)
        if not net_grp:
            return Status.NGRP_NOT_FOUND
        host = net_grp.find(host_address)
        if host:
            net_grp.remove(host)
            return Status.SUCCESS
        else:
            return Status.HOST_NOT_FOUND

    @service_logger
    def get_hosts_in_netgrp(self, netgrp_id: str) -> tuple[Status, list[Ip4Host]]:
        """
        List all hosts in a specified network group.

        Args:
            netgrp_id (str): Network group identifier.

        Returns:
            tuple(Status, Statuslist[Ip4Host]): NGRP_NOT_FOUND or SUCCESS, list of hosts.
        """
        net_grp = self._get_netgrp_by_id(netgrp_id)
        if not net_grp:
            return Status.NGRP_NOT_FOUND, []
        return Status.SUCCESS, net_grp.hosts

    @service_logger
    def find_host_in_netgrp(
        self, host_address: str | IPv4Address | Ip4Host, netgrp_id: str
    ) -> tuple[Status, Ip4Host | None]:
        """
        Find a host in a network group by IP address.

        Args:
            host_address (str | IPv4Address | Ip4Host): IP address of the host to find.
            netgrp_id (str): Network group identifier.

        Returns:
            tuple(Status, Ip4Host): SUCCESS | NGRP_NOT_FOUND, HOST_NOT_FOUND, or the host.
        """
        net_grp = self._get_netgrp_by_id(netgrp_id)
        if not net_grp:
            return Status.NGRP_NOT_FOUND, None
        match host_address:
            case Ip4Host():
                ip_addr = str(host_address.ip_address)
                host = net_grp.find(ip_addr)
            case IPv4Address():
                host = net_grp.find(str(host_address))
            case str():
                host = net_grp.find(host_address)
        return (Status.SUCCESS, host) if host else (Status.HOST_NOT_FOUND, None)

    def _get_netgrp_by_id(self, gid: str) -> NetGroup | None:
        """
        Retrieve a network group by its identifier.

        Args:
            gid (str): Network group identifier.

        Returns:
            NetGroup | None: The network group or None if not found.
        """
        return self.networks_dict.get(gid, None)

    @staticmethod
    def _validate_network_and_gid(gid: str, network: str) -> None:
        """
        Validate that network and group identifier are not empty.

        Args:
            gid (str): Group identifier.
            network (str): Network range.

        Raises:
            ValueError: If either network or gid is empty.
        """
        if not network or not gid:
            raise ValueError("Network and gid cannot be empty")
