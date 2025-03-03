from __future__ import annotations

import re
import socket
import struct

from vnet.lib.constants import IP4_REGEX
from vnet.lib.exceptions import Ip4AddressFormatError, Ip4HostFormatError, Ip4NetworkFormatError
from vnet.net_addr.ip4_address import Ip4Address


class Ip4Mask:
    """
    IPv4 mask support class.
    """

    version: int = 4
    mask: int

    def __init__(
        self,
        mask: Ip4Mask | str | bytes | bytearray | memoryview | int,
    ) -> None:
        """
        Initialize an Ip4Mask instance.

        Args:
            mask (Ip4Mask | str | bytes | bytearray | memoryview | int):
                The mask to initialize. Can be:
                - An Ip4Mask instance
                - A string in formats like '/24' or '255.255.255.0'
                - Bytes, bytearray, or memoryview of length 4
                - An integer representing the mask

        Raises:
            Ip4MaskFormatError: If the mask format is invalid.
        """

        def _validate_bits() -> bool:
            """
            Validate that mask is made of consecutive bits.
            """

            bit_mask = f"{self.mask:032b}"
            try:
                return not bit_mask[bit_mask.index("0") :].count("1")
            except ValueError:
                return True

        if isinstance(mask, int):
            if mask & 0xFF_FF_FF_FF == mask:
                self.mask = mask
                if _validate_bits():
                    return

        if isinstance(mask, (memoryview, bytes, bytearray)):
            if len(mask) == 4:
                self.mask = struct.unpack("!L", mask)[0]
                if _validate_bits():
                    return

        if isinstance(mask, str) and re.search(r"^/\d{1,2}$", mask):
            bit_count = int(mask[1:])
            if bit_count in range(33):
                self.mask = int("1" * bit_count + "0" * (32 - bit_count), 2)
                return

        if isinstance(mask, str) and re.search(IP4_REGEX, mask):
            try:
                self.mask = struct.unpack("!L", socket.inet_aton(mask))[0]
                if _validate_bits():
                    return
            except OSError:
                pass

        if isinstance(mask, Ip4Mask):
            self.mask = mask.mask
            return

        raise Ip4HostFormatError(mask)

    def __bytes__(self) -> bytes:
        """
        Convert the mask to bytes.

        Returns:
            bytes: The mask as a 4-byte sequence.
        """

        return struct.pack("!L", self.mask)

    def __str__(self) -> str:
        """
        Return the string representation of the mask.

        Returns:
            str: The mask in '/24' format.
        """

        return f"/{len(self)}"

    def __repr__(self) -> str:
        """
        Return the official string representation of the Ip4Mask.

        Returns:
            str: The representation in the format "Ip4Mask('/24')".
        """

        return f"Ip4Mask('{str(self)}')"

    def __int__(self) -> int:
        """
        Convert the mask to an integer.

        Returns:
            int: The mask as a 32-bit integer.
        """

        return self.mask

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare two Ip4Mask instances for equality.

        Args:
            other (object): The other object to compare.

        Returns:
            bool: True if both masks are equal, False otherwise.
        """
        return repr(self) == repr(other)

    def __hash__(self) -> int:
        """
        Return the hash of the Ip4Mask.

        Returns:
            int: The hash based on the mask integer value.
        """
        return self.mask

    def __len__(self) -> int:
        """
        Get the number of bits set to '1' in the mask.

        Returns:
            int: The count of '1' bits representing the network prefix length.
        """

        return f"{self.mask:b}".count("1")


class Ip4Network:
    """
    IPv4 network support class.
    """

    address: Ip4Address
    mask: Ip4Mask
    version: int = 4

    def __init__(
        self,
        network: Ip4Network | tuple[Ip4Address, Ip4Mask] | str,
    ) -> None:
        """
        Initialize an Ip4Network instance.

        Args:
                network (Ip4Network | tuple[Ip4Address, Ip4Mask] | str):
                        The network to initialize. Can be:
                        - An Ip4Network instance
                        - A tuple of (Ip4Address, Ip4Mask)
                        - A string in the format '192.168.1.0/24'

        Raises:
                Ip4NetworkFormatError: If the network format is invalid.
        """
        if isinstance(network, Ip4Network):
            self.mask = network.mask
            self.address = Ip4Address(int(network.address) & int(network.mask))
            return

        if isinstance(network, tuple):  # (address, mask)
            if len(network) == 2:
                if isinstance(network[0], Ip4Address) and isinstance(network[1], Ip4Mask):
                    self.mask = network[1]
                    self.address = Ip4Address(int(network[0]) & int(network[1]))
                    return

        if isinstance(network, str):
            try:
                address, mask = network.split("/")
                bit_count = int(mask)
                self.mask = Ip4Mask(int("1" * bit_count + "0" * (32 - bit_count), 2))
                self.address = Ip4Address(int(Ip4Address(address)) & int(self.mask))
                return
            except (ValueError, Ip4AddressFormatError, Ip4HostFormatError):
                raise Ip4NetworkFormatError(network)

    def __contains__(self, other: Ip4Address | str) -> bool:
        """
        Determine if an IP address is within the network.

        Args:
                other (Ip4Address | str): The IP address to check. Can be an Ip4Address instance or a string.

        Returns:
                bool: True if the IP address is within the network, False otherwise.

        Raises:
                TypeError: If the provided type is not supported.
        """
        match other:
            case str():
                return self.__contains__(Ip4Address(other))
            case Ip4Address():
                return int(self.address) <= int(other.address) <= int(self.last)
            case _:
                raise TypeError

    def __str__(self) -> str:
        """
        Return the string representation of the network.

        Returns:
                str: The network in '192.168.1.0/24' format.
        """

        return str(self.address) + "/" + str(len(self.mask))

    def __repr__(self) -> str:
        """
        Return the official string representation of the Ip4Network.

        Returns:
                str: The representation in the format "Ip4Network('192.168.1.0/24')".
        """
        return f"Ip4Network('{str(self)}')"

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare two Ip4Network instances for equality.

        Args:
                other (object): The other object to compare.

        Returns:
                bool: True if both networks are equal, False otherwise.
        """
        return repr(self) == repr(other)

    def __hash__(self) -> int:
        """
        Return the hash of the Ip4Network.

        Returns:
                int: The hash based on the address and mask.
        """

        return hash(self.address) ^ hash(self.mask)

    @property
    def last(self) -> Ip4Address:
        """
        Get the last IP address in the network.

        Returns:
                Ip4Address: The last address in the network.
        """

        return Ip4Address(int(self.address) + (~int(self.mask) & 0xFFFFFFFF))

    @property
    def broadcast(self) -> Ip4Address:
        """
        Get the broadcast address of the network.

        Returns:
                Ip4Address: The broadcast address, same as the last address in the network.
        """

        return self.last
