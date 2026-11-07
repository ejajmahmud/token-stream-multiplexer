"""Tests for token-stream-multiplexer."""
import unittest
from token_stream_multiplexer.multiplexer import TokenStreamMultiplexer, StreamPacket


class TestMultiplexer(unittest.TestCase):
    def setUp(self):
        self.mux = TokenStreamMultiplexer()

    def test_encode_decode(self):
        packet = StreamPacket("ch1", "Hello World!", is_final=False)
        frame = packet.encode()
        decoded = StreamPacket.decode(frame)
        self.assertEqual(decoded.channel_id, "ch1")
        self.assertEqual(decoded.chunk, "Hello World!")
        self.assertFalse(decoded.is_final)

    def test_channel_aggregation(self):
        self.mux.push_chunk("worker", "Part 1 ")
        self.mux.push_chunk("worker", "Part 2", is_final=True)
        self.assertEqual(self.mux.get_channel_output("worker"), "Part 1 Part 2")
        self.assertEqual(len(self.mux.active_channels()), 0)
