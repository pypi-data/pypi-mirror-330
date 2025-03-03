from __future__ import annotations

import re
import socket
import struct

import vnet.lib.exceptions
from vnet.lib.constants import IP4_ADDRESS_LEN, IP4_REGEX


class Ip4Address:
    """
    IPv4 address support class.
    """

    version: int = 4
    address: int

    def __init__(
        self,
        address: Ip4Address | str | bytes | bytearray | memoryview | int,
    ) -> None:
        """
        Initialize an Ip4Address instance.

        Args:
            address (Ip4Address | str | bytes | bytearray | memoryview | int):
                The address to initialize. Can be:
                - An Ip4Address instance
                - A string in dotted-decimal format, e.g., '192.168.1.1'
                - Bytes, bytearray, or memoryview of length 4
                - An integer representing the address

        Raises:
            vnet.net_addr.errors.Ip4AddressFormatError: If the address format is invalid.
        """

        match address:
            case int() if address & 0xFF_FF_FF_FF == address:
                self.address = address
            case memoryview() | bytes() | bytearray() if len(address) == 4:
                self.address = struct.unpack("!L", address)[0]
            case str() if re.search(IP4_REGEX, address):
                try:
                    self.address = int.from_bytes(socket.inet_aton(address), "big")
                except OSError:
                    raise vnet.lib.exceptions.Ip4AddressFormatError(address)
            case Ip4Address():
                self.address = int(address)
            case _:
                raise vnet.lib.exceptions.Ip4AddressFormatError(address)

    def __str__(self) -> str:
        """
        Return the string representation of the IP address.

        Returns:
            str: The IP address in dotted-decimal format.
        """
        return socket.inet_ntoa(bytes(self))

    def __int__(self) -> int:
        """
        Convert the IP address to an integer.

        Returns:
            int: The IP address as a 32-bit integer.
        """
        return self.address

    def __eq__(self, other: object) -> bool:
        """
        Compare two Ip4Address instances for equality.

        Args:
            other (object): The other object to compare.

        Returns:
            bool: True if both IP addresses are equal, False otherwise.
        """
        return repr(self) == repr(other)

    def __repr__(self) -> str:
        """
        Return the official string representation of the Ip4Address.

        Returns:
            str: The representation in the format "Ip4Address('192.168.1.1')".
        """
        return f"Ip4Address('{str(self)}')"

    def __hash__(self) -> int:
        """
        Return the hash of the Ip4Address.

        Returns:
            int: The hash based on the address integer value.
        """
        return self.address

    def __bytes__(self) -> bytes:
        """
        Convert the IP address to bytes.

        Returns:
            bytes: The IP address as a 4-byte sequence.
        """
        return self.address.to_bytes(IP4_ADDRESS_LEN)

    @property
    def is_global(self) -> bool:
        """
        Determine if the IP address is a global (public) address.

        Returns:
            bool: True if the address is global, False otherwise.
        """
        return not any(
            (
                self.is_unspecified,
                self.is_invalid,
                self.is_link_local,
                self.is_loopback,
                self.is_multicast,
                self.is_private,
                self.is_reserved,
                self.is_limited_broadcast,
            )
        )

    @property
    def is_link_local(self) -> bool:
        """
        Check if the IPv4 address is link-local.

        Returns:
            bool: True if link-local, False otherwise.
        """
        return self.address & 0xFF_FF_00_00 == 0xA9_FE_00_00  # 169.254.0.0 - 169.254.255.255

    @property
    def is_loopback(self) -> bool:
        """
        Check if the IPv4 address is a loopback address.

        Returns:
            bool: True if loopback, False otherwise.
        """
        return self.address & 0xFF_00_00_00 == 0x7F_00_00_00  # 127.0.0.0 - 127.255.255.255

    @property
    def is_multicast(self) -> bool:
        """
        Check if the IPv4 address is a multicast address.

        Returns:
            bool: True if multicast, False otherwise.
        """
        return self.address & 0xF0_00_00_00 == 0xE0_00_00_00  # 224.0.0.0 - 239.255.255.255

    @property
    def is_private(self) -> bool:
        """
        Check if the IPv4 address is a private address.

        Returns:
            bool: True if private, False otherwise.
        """
        return (
            self.address & 0xFF_00_00_00 == 0x0A_00_00_00  # 10.0.0.0 - 10.255.255.255
            or self.address & 0xFF_F0_00_00 == 0xAC_10_00_00  # 172.16.0.0 - 172.31.255.255
            or self.address & 0xFF_FF_00_00 == 0xC0_A8_00_00  # 192.168.0.0 - 192.168.255.255
        )

    @property
    def is_reserved(self) -> bool:
        """
        Check if the IPv4 address is reserved.

        Returns:
            bool: True if reserved, False otherwise.
        """
        return self.address & 0xF0_00_00_01 == 0xF0_00_00_00  # 240.0.0.0 - 255.255.255.254

    @property
    def is_limited_broadcast(self) -> bool:
        """
        Check if the IPv4 address is a limited broadcast address.

        Returns:
            bool: True if limited broadcast, False otherwise.
        """
        return self.address == 0xFF_FF_FF_FF  # 255.255.255.255

    @property
    def is_invalid(self) -> bool:
        """
        Check if the IPv4 address is invalid.

        Returns:
            bool: True if invalid, False otherwise.
        """
        return (
            self.address != 0x00_00_00_00 and self.address & 0xFF_00_00_00 == 0x00_00_00_00
        )  # 0.0.0.1 - 0.255.255.255

    @property
    def unspecified(self) -> Ip4Address:
        """
        Get the unspecified IPv4 address (0.0.0.0).

        Returns:
            Ip4Address: The unspecified IPv4 address.
        """
        return Ip4Address(0)

    @property
    def is_unspecified(self) -> bool:
        """
        Check if the IP address is unspecified (0.0.0.0).

        Returns:
            bool: True if unspecified, False otherwise.
        """
        return self.address == 0

    @property
    def is_unicast(self) -> bool:
        """
        Check if the IP address is a unicast address.

        Returns:
            bool: True if unicast, False otherwise.
        """
        return any(
            (
                self.is_global,
                self.is_private,
                self.is_link_local,
                self.is_loopback,
            )
        )
