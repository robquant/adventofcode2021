from textwrap import indent
from functools import reduce
import operator


class BitStream:
    def __init__(self, hex_input):
        self.hex_string = list(reversed(hex_input))
        self.available_bits = 0
        self.number = 0

    def read_bits(self, nbits):
        while self.available_bits < nbits:
            self.number <<= 4
            self.number |= int(self.hex_string.pop(), 16)
            self.available_bits += 4
        keep_bits = self.available_bits - nbits
        extract = self.number >> keep_bits
        self.number = self.number & (2 ** keep_bits - 1)
        self.available_bits -= nbits
        return extract

    def read_varint(self):
        result = 0
        nibbles = 0
        while True:
            result <<= 4
            nibbles += 1
            number = self.read_bits(5)
            result |= number & (2 ** 4 - 1)
            if number & (2 ** 4) == 0:
                break
        return nibbles, result


class Packet:
    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id


class LiteralValue(Packet):
    def __init__(self, version, type_id, length, value):
        assert type_id == 4
        super().__init__(version, type_id)
        self.value = value
        self.length = length

    def version_sum(self):
        return self.version

    def eval(self):
        return self.value

    def __str__(self):
        return f"LiteralValue\n version: {self.version}\n PacketID: {self.type_id}\n Value: {self.value}\n"


class OperatorPacket(Packet):
    def __init__(self, version, type_id, length_type_id, sub_packets):
        assert type_id != 4
        super().__init__(version, type_id)
        self.length_type_id = length_type_id
        self.sub_packets = sub_packets

    @property
    def length(self):
        total = 7
        if self.length_type_id == 0:
            total += 15
        else:
            total += 11
        return total + sum(p.length for p in self.sub_packets)

    def version_sum(self):
        return self.version + sum(p.version_sum() for p in self.sub_packets)

    def eval(self):
        if self.type_id == 0:
            return sum(p.eval() for p in self.sub_packets)
        elif self.type_id == 1:
            return reduce(operator.mul, (p.eval() for p in self.sub_packets))
        elif self.type_id == 2:
            return min(p.eval() for p in self.sub_packets)
        elif self.type_id == 3:
            return max(p.eval() for p in self.sub_packets)
        elif self.type_id == 5:
            assert len(self.sub_packets) == 2
            if self.sub_packets[0].eval() > self.sub_packets[1].eval():
                return 1
            else:
                return 0
        elif self.type_id == 6:
            assert len(self.sub_packets) == 2
            if self.sub_packets[0].eval() < self.sub_packets[1].eval():
                return 1
            else:
                return 0
        elif self.type_id == 7:  # ==
            assert len(self.sub_packets) == 2
            if self.sub_packets[0].eval() == self.sub_packets[1].eval():
                return 1
            else:
                return 0

    def __str__(self):
        sub_packets = indent("".join(str(p) for p in self.sub_packets), "  ")
        return (
            f"OperatorPacket\n version: {self.version}\n PacketID: {self.type_id}\n"
            + sub_packets
        )


def parse_packet(stream):
    version = stream.read_bits(3)
    type_id = stream.read_bits(3)
    if type_id == 4:
        # parse LiteralValue
        nibbles, value = stream.read_varint()
        length = 6 + 5 * nibbles
        return LiteralValue(version, type_id, length, value)
    else:  # operator packet
        length_type_id = stream.read_bits(1)
        if length_type_id == 0:
            total_length = stream.read_bits(15)
            total_length_read = 0
            sub_packets = []
            while total_length_read < total_length:
                sub_packet = parse_packet(stream)
                sub_packets.append(sub_packet)
                total_length_read += sub_packet.length
            return OperatorPacket(version, type_id, length_type_id, sub_packets)
        else:
            total_subpackets = stream.read_bits(11)
            sub_packets = []
            for _ in range(total_subpackets):
                sub_packet = parse_packet(stream)
                sub_packets.append(sub_packet)
            return OperatorPacket(version, type_id, length_type_id, sub_packets)


# stream = BitStream("D2FE28")
# print(parse_packet(stream))

# stream = BitStream("EE00D40C823060")
# print(parse_packet(stream))
# stream = BitStream("38006F45291200")
# print(parse_packet(stream))

# stream = BitStream("620080001611562C8802118E34")
# print(parse_packet(stream))

# stream = BitStream("C0015000016115A2E0802F182340")
# p = parse_packet(stream)
# print(p)
# print(p.version_sum())

stream = BitStream(open("input.txt").read().rstrip("\n"))
p = parse_packet(stream)
print(p.version_sum())
print(p.eval())
