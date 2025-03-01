"""Provides a paket factory class"""

from ..protocol.packet import Packet, PacketAck

class PacketFactory():
    """Packet factory class"""


    def __init__(self):
        self.data: dict[int, Packet] = {}

        for x in Packet.__subclasses__():
            # we will not register subclasses of PacketAck here, it will be done in following loop
            # if (type(x) is PacketAck) or (x not in PacketAck.__subclasses__()):
            if not isinstance(x, type(PacketAck)):
                # print(f"Register type {x.__name__}")
                # disable linter warning, that a parameter is missing, which seems to be wrong
                # pylint: disable = no-value-for-parameter
                self.register_packet(x())

        for x in PacketAck.__subclasses__():
            # print(f"Register type {x.__name__}")
            self.register_packet(x(None))


    def register_packet(self, packet: Packet):
        """Register a packet"""
        self.data[packet.command] = packet


    def create_packet(self, command: int) -> Packet:
        """Create a packet based on command number"""
        copy = self.data[command].create_copy()
        return copy


    def create_packet_with_data(self, command: int, number: int, data: bytes) -> PacketAck:
        """Create a acknowledge packet based on command number with data"""
        proto: PacketAck = self.data[command]
        copy = proto.create_copy_with_data(data)
        copy.number = number
        return copy
