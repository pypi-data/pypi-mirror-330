import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError
import pillow_heif
import os


def load_image(input_path):
    """Loads an image, converting HEIC to a format OpenCV can process."""
    try:
        if input_path.lower().endswith(".heic"):
            heif_image = pillow_heif.open_heif(input_path)
            image = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
            image = image.convert("L")
        else:
            image = Image.open(input_path).convert("L")

        return np.array(image)

    except UnidentifiedImageError:
        raise ValueError(
            f"Error: Unable to load image '{input_path}'. Unsupported format or corrupted file."
        )


def calculate_otsu_threshold(image):
    """
    Computes the Otsu threshold for an image.

    1. Compute the histogram of pixel intensities.
    2. Iterate over all possible thresholds to find the one that minimizes intra-class variance.
    3. Return the optimal threshold value.
    """
    hist, bins = np.histogram(image.ravel(), bins=256, range=(0, 256))

    total_pixels = image.size  # total number of pixels in the image
    sum_all = np.dot(np.arange(256), hist)  # sum of all pixel intensities

    best_threshold = 0
    max_between_class_variance = 0
    weight_background = 0
    sum_background = 0

    # for each possible threshold
    for t in range(256):
        # find variance between threshold-seperated classes
        weight_background += hist[t]
        if weight_background == 0:
            continue

        weight_foreground = total_pixels - weight_background
        if weight_foreground == 0:
            break

        sum_background += t * hist[t]
        mean_background = sum_background / weight_background
        mean_foreground = (sum_all - sum_background) / weight_foreground

        between_class_variance = (
            weight_background
            * weight_foreground
            * (mean_background - mean_foreground) ** 2
        )

        # keep track of optimal treshold
        if between_class_variance > max_between_class_variance:
            max_between_class_variance = between_class_variance
            best_threshold = t

    return best_threshold


def process_image(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Error: Input file '{input_path}' not found.")

    # load image
    image = load_image(input_path)

    # gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # compute otsu's threshold manually
    otsu_threshold = calculate_otsu_threshold(blurred)

    # apply thresholding
    binary = np.where(blurred >= otsu_threshold, 255, 0).astype(np.uint8)

    # invert colors so ink is black and paper is white
    binary = cv2.bitwise_not(binary)

    # convert to rgba
    h, w = binary.shape
    result = np.zeros((h, w, 4), dtype=np.uint8)
    result[:, :, 0:3] = 0
    result[:, :, 3] = binary

    # save as transparent PNG
    try:
        final_image = Image.fromarray(result)
        final_image.save(output_path, format="PNG")
        print(f"Processed image saved to {output_path}")
    except Exception as e:
        raise ValueError(f"Error: Unable to save image '{output_path}'. {e}")
