import argparse
import os
from .process import process_image


def main():
    parser = argparse.ArgumentParser(
        description="Convert pen drawings to transparent PNGs."
    )
    parser.add_argument("input", type=str, help="Path to the input image")
    parser.add_argument("output", type=str, help="Path to save the output PNG")

    args = parser.parse_args()

    # validate input file
    if not os.path.isfile(args.input):
        print(f"Error: The input file '{args.input}' does not exist.")
        return

    # validate output directory
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: The output directory '{output_dir}' does not exist.")
        return

    try:
        process_image(args.input, args.output)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
