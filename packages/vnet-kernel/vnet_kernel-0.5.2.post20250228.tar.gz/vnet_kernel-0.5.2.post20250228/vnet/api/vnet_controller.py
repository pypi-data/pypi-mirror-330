import ipaddress
import logging
import random
from typing import Any

from scapy.layers.inet import IP

from vnet.lib.inet_cksum import calc_inet_cksum
from vnet.lib.status_logger import Status, controller_logger
from vnet.topology import VNet

from .response_vo import ResponseVO
from .router import RequestMapper
from .validation import validate_inet_addr

logging.basicConfig(
    filename="vnet_controller.log",  # 日志文件名
    filemode="a",  # 追加模式
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class VNetController:
    """VNet请求控制器，处理不同的请求"""

    def __init__(self, vnet: VNet):
        self.vnet = vnet
        self.netgrp_service = vnet.netgrp_service
        self.conns_service = vnet.conns_service
        logger.info("VNet Controller 初始化完成")

    # ===============================================
    # Request Handler
    # ===============================================

    def process_request(self, request: dict[str, Any]) -> ResponseVO:
        """处理传入的请求并返回响应对象。

        此方法从请求中提取 `action` 字段，该字段应包含 HTTP 方法和资源，
        格式如 "METHOD PATH"（例如 "POST /api/v1/netgroup"）。还可能包含其他参数字段，
        以键值对形式提供，如 "netgrp_id": "net1"。

        Args:
                request (dict[str, Any]): 包含请求数据的字典。

        Returns:
                ResponseVO: 构建的响应对象。
        """
        action = request.get("action", "")
        method, path = action.split(" ")[0], action.split(" ")[1]
        logger.info("[Process Request] METHOD=%s, URL=%s", method, path)
        routes = RequestMapper.routes.get(method, {})
        route_handler = routes.get(path)

        if route_handler:
            # 提取请求中的参数
            try:
                params = {
                    k: request.get(k)
                    for k in route_handler.__code__.co_varnames[
                        1 : route_handler.__code__.co_argcount
                    ]
                    if k in request
                }
                logger.info(
                    "[Process Request] 调用函数: %s 请求参数为: %s",
                    route_handler.__name__,
                    params,
                )
                return route_handler(self, **params)
            except ValueError as ve:
                logger.exception(
                    "[Process Request]处理请求时发生未预期的错误，vnet_controller.process_request"
                )
                return ResponseVO("[ERROR]", str(ve))

        return ResponseVO.unknown_action()

    # ===============================================
    # Network Group APIs
    # ===============================================

    @controller_logger
    @validate_inet_addr("network_address", param_type="IPv4Network")
    @RequestMapper.route("POST", "/api/v1/netgroup")
    def create_network_group(self, netgrp_id: str, network_address: str) -> ResponseVO:
        """创建网络组"""
        status = self.netgrp_service.add_netgrp(netgrp_id, network_address)
        if status == Status.NGRP_ALREADY_EXISTS:
            return ResponseVO("[ERROR]", "Network group already exists")
        return ResponseVO("[DONE]", f"Network {netgrp_id} created")

    @controller_logger
    @RequestMapper.route("DELETE", "/api/v1/netgroup")
    def remove_network_group(self, netgrp_id: str) -> ResponseVO:
        """删除网络组"""
        status = self.netgrp_service.rm_netgrp(netgrp_id)
        if status == Status.NGRP_NOT_FOUND:
            return ResponseVO("[ERROR]", "Network group " + netgrp_id + " not found")
        return ResponseVO("[DONE]", f"Network {netgrp_id} deleted")

    # ===============================================
    # Host APIs
    # ===============================================

    @controller_logger
    @validate_inet_addr("host_address")
    @RequestMapper.route("POST", "/api/v1/host")
    def add_host_to_netgroup(self, netgrp_id: str, host_address: str) -> ResponseVO:
        """添加主机到网络组"""
        try:
            ipaddress.IPv4Address(host_address)
        except ValueError:
            return ResponseVO("[ERROR]", "请检查地址格式" + host_address)

        status = self.netgrp_service.add_host_to_netgrp(host_address, netgrp_id)
        if status == Status.NGRP_NOT_FOUND:
            return ResponseVO("[ERROR]", "Network group " + netgrp_id + " not found")
        return ResponseVO("[DONE]", f"Host {host_address} added to network group {netgrp_id}")

    @controller_logger
    @validate_inet_addr("host_address")
    @RequestMapper.route("DELETE", "/api/v1/host")
    def remove_host_from_netgroup(self, netgrp_id: str, host_address: str) -> ResponseVO:
        """从网络组中移除主机"""
        status = self.netgrp_service.rm_host_from_netgrp(host_address, netgrp_id)
        match status:
            case Status.NGRP_NOT_FOUND:
                return ResponseVO("[ERROR]", "Network group " + netgrp_id + " not found")
            case Status.HOST_NOT_FOUND:
                return ResponseVO("[ERROR]", "Host " + host_address + "does not exist")
            # case SUCCESS
        return ResponseVO("[DONE]", f"Host {host_address} removed from network group {netgrp_id}")

    @controller_logger
    @RequestMapper.route("GET", "/api/v1/netgroup/hosts")
    def get_hosts_in_netgroup(self, netgrp_id: str) -> ResponseVO:
        """获取网络组中的主机"""
        status, hosts = self.netgrp_service.get_hosts_in_netgrp(netgrp_id)
        if status == Status.NGRP_NOT_FOUND:
            return ResponseVO("[ERROR]", "Network group " + netgrp_id + " not found")
        return ResponseVO("[DONE]", str(hosts))

    @validate_inet_addr("host_address")
    @controller_logger
    @RequestMapper.route("GET", "/api/v1/netgroup/hosts/host")
    def find_host_in_netgroup(self, netgrp_id: str, host_address: str) -> ResponseVO:
        """查找网络组中的特定主机"""
        status, host = self.netgrp_service.find_host_in_netgrp(host_address, netgrp_id)
        match status:
            case Status.SUCCESS:
                return ResponseVO("[DONE]", f"Find Host In Netgroup: {host}")
            case Status.NGRP_NOT_FOUND:
                return ResponseVO("[ERROR]", "Network group " + netgrp_id + " not found")
            case Status.HOST_NOT_FOUND:
                return ResponseVO("[ERROR]", "Host " + host_address + " not found")
            case _:
                return ResponseVO("[ERROR]", "Server Error")

    # ===============================================
    # Ip Datagram APIs
    # ===============================================

    @controller_logger
    @RequestMapper.route("GET", "/network/ip4header")
    def get_random_ip4_header_bytes(self) -> ResponseVO:
        """构造IP数据包"""

        def _generate_random_ipv4_string() -> str:
            return ".".join(str(random.randint(0, 255)) for _ in range(4))

        random_ip4_header = IP(
            src=_generate_random_ipv4_string(), dst=_generate_random_ipv4_string()
        )
        header_bytes = bytes(random_ip4_header)
        checksum = calc_inet_cksum(header_bytes)
        # int->hex str
        hex_checksum = str(hex(checksum))
        return ResponseVO(
            status=hex_checksum,
            message=header_bytes.hex(),  # Convert dict to JSON string
        )
