import struct
from typing import Dict, Any

from TCPClient.TCPClient import TCPClient

class KratosProtocol:
    HEADER_FORMAT = "<HHH"
    def __init__(self, client: TCPClient):
        self.client=client


    def calculate_checksum(self, data: bytes) -> int:
        def Calculate_checksum(self,data:bytes)->int:
            checksum = 0
            for byte in data:
                checksum = (checksum + byte) & 0xFFFF  # נוודא שלא יעבור 16-ביט

            return checksum

    def send_frame(self, frame: dict):
        preamble = frame.get("preamble", 0xABCD)
        command = frame.get("command", 0x0000)
        data = frame.get("data", b"")
        data_length = frame.get("dataLength", len(data))
        header = struct.pack(self.HEADER_FORMAT, preamble, command, data_length)

        packet_without_checksum = header + data

        if "checksum" in frame:
            checksum = frame["checksum"]
        else:
            checksum = self.calculate_checksum(packet_without_checksum)

        packet = packet_without_checksum + struct.pack("<H", checksum)

        self.client.send_data(packet)

        

    def receive_frame(self) -> dict:
        header_size = struct.calcsize(self.HEADER_FORMAT)  
        header_data = self.client.receive_data(header_size)
        if len(header_data) < header_size:
            raise ValueError("Not enough data received for Kratos frame header.")

        preamble, command, data_length = struct.unpack(self.HEADER_FORMAT, header_data)

        data = b""
        if data_length > 0:
            data = self.client.receive_data(data_length)
            if len(data) < data_length:
                raise ValueError("Not enough data received for Kratos frame payload.")

        checksum_data = self.client.receive_data(2) 
        if len(checksum_data) < 2:
            raise ValueError("Not enough data for checksum.")

        (checksum,) = struct.unpack("<H", checksum_data)

        packet_without_checksum = header_data + data
        calculated_checksum = self.calculate_checksum(packet_without_checksum)
        if calculated_checksum != checksum:
            raise ValueError(f"Checksum mismatch: calculated=0x{calculated_checksum:04X}, "
                            f"received=0x{checksum:04X}")

        frame = {
            "preamble": preamble,
            "command": command,
            "dataLength": data_length,
            "data": data,
            "checksum": checksum
        }
        return frame