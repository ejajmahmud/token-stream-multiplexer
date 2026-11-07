"""CLI for token-stream-multiplexer."""
import sys
import argparse
from .multiplexer import TokenStreamMultiplexer, StreamPacket


def main():
    parser = argparse.ArgumentParser(description="Token Stream Multiplexer")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        mux = TokenStreamMultiplexer()
        f1 = mux.push_chunk("agent_1", "Generating code...")
        f2 = mux.push_chunk("agent_2", "Validating tests...")
        f3 = mux.push_chunk("agent_1", " Done!", is_final=True)
        print("Encoded frames:")
        print(f1)
        print(f2)
        print(f3)
        p = StreamPacket.decode(f1)
        print(f"Decoded frame 1: Channel={p.channel_id}, Chunk={p.chunk}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
