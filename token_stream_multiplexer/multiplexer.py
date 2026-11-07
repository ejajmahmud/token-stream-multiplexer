"""Core Token Stream Multiplexer implementation."""
from typing import Dict, List, Optional, Tuple


class StreamPacket:
    def __init__(self, channel_id: str, chunk: str, is_final: bool = False):
        self.channel_id = channel_id
        self.chunk = chunk
        self.is_final = is_final

    def encode(self) -> str:
        flag = "F" if self.is_final else "C"
        return f"[{self.channel_id}:{flag}:{len(self.chunk)}:{self.chunk}]"

    @classmethod
    def decode(cls, frame: str) -> "StreamPacket":
        if not (frame.startswith("[") and frame.endswith("]")):
            raise ValueError(f"Malformed frame: {frame}")
        parts = frame[1:-1].split(":", 3)
        if len(parts) != 4:
            raise ValueError(f"Invalid frame format: {frame}")
        ch_id, flag, length, chunk = parts
        return cls(channel_id=ch_id, chunk=chunk, is_final=(flag == "F"))


class TokenStreamMultiplexer:
    def __init__(self):
        self._channels: Dict[str, List[str]] = {}
        self._closed_channels: set = set()

    def push_chunk(self, channel_id: str, chunk: str, is_final: bool = False) -> str:
        packet = StreamPacket(channel_id, chunk, is_final)
        if channel_id not in self._channels:
            self._channels[channel_id] = []
        self._channels[channel_id].append(chunk)
        if is_final:
            self._closed_channels.add(channel_id)
        return packet.encode()

    def get_channel_output(self, channel_id: str) -> str:
        return "".join(self._channels.get(channel_id, []))

    def active_channels(self) -> List[str]:
        return [ch for ch in self._channels if ch not in self._closed_channels]
