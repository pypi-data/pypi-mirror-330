import struct


def calc_inet_cksum_bak(
    data: bytes | bytearray | memoryview,
    init: int = 0,
) -> int:
    """
    计算校验和

    当要计算IPv4报文首部校验和时，发送方先将其校验和字段置为全0，然后按16位逐一累加至IPv4报文首部结束，累加和保存于一个32位的数值中。
    如果总的字节数为奇数，则最后一个字节单独相加。累加完毕将结果中高16位再加到低16位上，重复这一过程直到高16位为全0。最后
    将结果取反存入首部校验和域。

    Args:
            data (bytes | bytearray | memoryview): 输入的二进制数据，如`data = b'\x45\x00\x00\x54\x00\x00\x40\x00\x40\x01\xff'`
            init (int = 0): 可选参数，初始化的校验和值，默认为 0。用于某些场景下在已有的校验和基础上继续计算(例如ttl值会在传输过程中递减，需要
            重新计算校验和)

    Returns:
            int: 计算得到的校验和
    """
    cksum = init

    # 每16位(2字节)一组进行解包并累加
    dlen = len(data)
    num_shorts = dlen // 2  # 16位即2字节

    # 使用struct解包为16位(2字节)的无符号short类型，并逐一累加
    cksum += sum(struct.unpack(f"!{num_shorts}H", data[: num_shorts * 2]))

    # 如果数据长度为奇数，则处理剩余的字节
    if dlen % 2:
        cksum += data[-1] << 8  # 将最后一个字节左移8位以填充高位

    # 将高位和低位相加，直到得到16位的校验和
    cksum = (cksum >> 16) + (cksum & 0xFFFF)
    cksum += cksum >> 16

    # 对结果取反并返回
    return ~cksum & 0xFFFF


def calc_inet_cksum(
    data: bytes | bytearray | memoryview,
    init: int = 0,
) -> int:
    """
    RFC-1071 [Page 3] Parallel Summation 中给出了一种并行计算校验和的方法，可以有效提高计算效率。
    Compute Internet Checksum used by IPv4/ICMPv4/ICMPv6/UDP/TCP protocols.
    """

    # 数据长度为 20 Bytes时，代码按 32 位（4 字节）一组，解包 5 个 unsigned long
    if (dlen := len(data)) == 20:
        cksum = init + int(sum(struct.unpack("!5L", data)))
    # 如果数据长度不是 20 字节,按 64 位（8 字节）一组，解包 dlen/8 个 unsigned long long
    else:
        cksum = init + int(sum(struct.unpack_from(f"!{dlen >> 3}Q", data)))

        if remainder := dlen & 7:  # 不是8的倍数
            cksum += int().from_bytes(data[-remainder:], byteorder="big") << ((8 - remainder) << 3)
        cksum = (cksum >> 64) + (cksum & 0xFFFFFFFFFFFFFFFF)

    cksum = (cksum >> 32) + (cksum & 0xFFFFFFFF)
    cksum = (cksum >> 16) + (cksum & 0xFFFF)
    cksum = ~(cksum + (cksum >> 16)) & 0xFFFF

    return cksum
