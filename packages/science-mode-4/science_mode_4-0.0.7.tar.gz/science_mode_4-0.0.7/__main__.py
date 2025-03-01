"""Test program how to use library without installing the library"""

import sys
import asyncio

from src.science_mode_4.device_p24 import DeviceP24
from src.science_mode_4.low_level.low_level_layer import LayerLowLevel
from src.science_mode_4.low_level.low_level_types import LowLevelHighVoltageSource, LowLevelMode
from src.science_mode_4.mid_level.mid_level_types import MidLevelChannelConfiguration
from src.science_mode_4.protocol.channel_point import ChannelPoint
from src.science_mode_4.protocol.types import Channel, Connector
from src.science_mode_4.utils.serial_port_connection import SerialPortConnection


# print(science_mode_4.__version__)

def send_channel_config(low_level_layer: LayerLowLevel, connector: Connector):
    """Sends channel update"""
    # device can store up to 10 channel config commands
    for channel in Channel:
        # send_channel_config does not wait for an acknowledge
        low_level_layer.send_channel_config(True, channel, connector,
                                            [ChannelPoint(4000, 20), ChannelPoint(4000, -20),
                                            ChannelPoint(4000, 0)])
        
async def main() -> int:
    """Main function"""

    connection = SerialPortConnection('COM3')
    # connection = NullConnection()
    connection.open()

    device = DeviceP24(connection)
    await device.initialize()
    general = device.get_layer_general()
    print(f"device id: {general.device_id}")
    print(f"firmware version: {general.firmware_version}")
    print(f"science mode version: {general.science_mode_version}")

    # c1p1: ChannelPoint = ChannelPoint(200, 20)
    # c1p2: ChannelPoint = ChannelPoint(100, 0)
    # c1p3: ChannelPoint = ChannelPoint(200, -20)
    # cc1 = MidLevelChannelConfiguration(True, 3, 20, [c1p1, c1p2, c1p3])

    # c2p1: ChannelPoint = ChannelPoint(100, 100)
    # c2p2: ChannelPoint = ChannelPoint(100, 0)
    # c2p3: ChannelPoint = ChannelPoint(100, -100)
    # cc2 = MidLevelChannelConfiguration(True, 3, 10, [c2p1, c2p2, c2p3])

    # mid_level = device.get_layer_mid_level()
    # await mid_level.init(False)
    # await mid_level.update([cc1, cc2])
    # for _ in range(100):
    #     update = await mid_level.get_current_data()
    #     print(update)

    #     await asyncio.sleep(1)

    # await mid_level.stop()

    # get low level layer to call low level commands
    low_level_layer = device.get_layer_low_level()

    # call init low level
    await low_level_layer.init(LowLevelMode.NO_MEASUREMENT, LowLevelHighVoltageSource.STANDARD)

    # now we can start stimulation
    counter = 0
    while counter < 100:
        # get new data from connection
        # both append_bytes_to_buffer and get_packet_from_buffer should be called regulary
        new_buffer_data = device.connection.read()
        if len(new_buffer_data) > 0:
            low_level_layer.packet_buffer.append_bytes_to_buffer(new_buffer_data)
            # we added new data to buffer, so there may be new valid acknowledges
            packet_ack = low_level_layer.packet_buffer.get_packet_from_buffer()
            # do something with packet ack
            # here we print that an acknowledge arrived
            # print(packet_ack)

        if counter % 10 == 0:
            send_channel_config(low_level_layer, Connector.GREEN)
        elif counter % 10 == 5:
            send_channel_config(low_level_layer, Connector.YELLOW)

        await asyncio.sleep(0.1)
        counter += 1

    # call stop low level
    await low_level_layer.stop()

    connection.close()
    return 0


if __name__ == '__main__':
    res = asyncio.run(main())
    sys.exit(res)
