# pen2png

`pen2png` is a command-line tool that converts pen drawings on paper into transparent PNGs with smooth black ink lines.

- Supports HEIC, JPG, PNG, and other common formats.
- Removes background and makes paper transparent.

## Installation

You can install the package via pip:

```sh
pip install pen2png
```

## Usage

To convert an image:

```sh
pen2png <input_filepath> <output_filepath>
```

Example:

```sh
pen2png my_drawing.jpg drawing.png
```

**Note:** For best results, crop your image _before_ conversion and avoid using pencils/non-black pens.
