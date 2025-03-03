from abc import ABC
from dataclasses import dataclass
from ipaddress import IPv4Address


@dataclass
class VSession(ABC):
    local_ip: IPv4Address
    local_port: int
    remote_ip: IPv4Address
    remote_port: int

    def __str__(self):
        return f"{self.local_ip}:{self.local_port} -> {self.remote_ip}:{self.remote_port}"
