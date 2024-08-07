# -*- coding: utf-8 -*-
import asyncio
import aioquic.asyncio
from datetime import datetime
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol

class QuicPlayer:
    async def send_quic_traffic(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send quic traffic for effect verification.", flush=True)
        configuration = QuicConfiguration(is_client=True)
        # protocol = QuicConnectionProtocol("quic")
        try:
            async with aioquic.asyncio.connect(
                host=traffic_data["host"],
                port=traffic_data["port"],
                configuration=configuration,
                # create_protocol=protocol
            ) as quic_instance:
                await quic_instance.connect(host=traffic_data["host"], port=traffic_data["port"])
                stream = quic_instance.create_stream(False)
                writer = asyncio.StreamWriter(stream)
                writer.write("headers")
                await writer.drain()
            # await asyncio.sleep(10)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Error: {e}.", flush=True)
            return f"Error: No handshake operation.."
  
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "quic",
            "host": "www.youtube.com",
            "port": 443
        }
    }
    traffic_data = test_data["traffic"]
    quic_player = QuicPlayer()
    asyncio.run(quic_player.send_quic_traffic(traffic_data, "ui", False))