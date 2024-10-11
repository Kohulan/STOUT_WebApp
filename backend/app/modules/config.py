import tensorflow as tf
import efficientnet.tfkeras as efn
from PIL import Image, ImageEnhance
from pillow_heif import register_heif_opener
import numpy as np
import io
import cv2


def resize_by_ratio(image, max_size=512):
    """
    This function takes a Pillow Image object and will resize the image to a maximum dimension of 512x512
    To upscale or to downscale the image LANCZOS resampling method is used.
    With the new pillow version the antialias is turned on when using LANCZOS.
    Args: PIL.Image
    Returns: PIL.Image
    """
    ratio = max_size / max(image.size)
    new_size = tuple(int(dim * ratio) for dim in image.size)
    return image.resize(new_size, resample=Image.LANCZOS)


def central_square_image(image, padding_color="white"):
    """
    This function takes a Pillow Image object and will add white padding
    so that the image has a square shape with the width/height of the longest side
    of the original image.
    Args: PIL.Image
    Returns: PIL.Image
    """
    max_dim = max(int(1.2 * max(image.size)), 512)
    new_im = Image.new(image.mode, (max_dim, max_dim), padding_color)
    paste_pos = tuple((max_dim - dim) // 2 for dim in image.size)
    new_im.paste(image, paste_pos)
    return new_im


def delete_empty_borders(image):
    """
    This function takes a Pillow Image object, converts it to grayscale and
    deletes white space at the borders.
    Args: PIL.Image
    Returns: PIL.Image
    """
    gray_image = np.array(image.convert("L"))
    mask = gray_image > 200
    rows, cols = np.where(~mask)
    return Image.fromarray(
        gray_image[rows.min() : rows.max() + 1, cols.min() : cols.max() + 1]
    )


def pil_image_to_bytes(image):
    """
    Convert pillow image to bytes
    Args: PIL.Image
    Returns: bytes object with the image data
    """
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        return output.getvalue()


def heif_to_pillow(image_path: str):
    """
    Converts Apple's HEIF format to useful pillow object
    Args: image_path (str): path of input image
    Returns: PIL.Image
    """
    register_heif_opener()
    return Image.open(image_path).convert("RGBA")


def remove_transparent(image_path: str):
    """
    Removes the transparent layer from a PNG image with an alpha channel
    Args: image_path (str): path of input image
    Returns: PIL.Image
    """
    try:
        img = Image.open(image_path).convert("RGBA")
    except Image.UnidentifiedImageError:
        img = heif_to_pillow(image_path)

    background = Image.new("RGBA", img.size, (255, 255, 255))
    return Image.alpha_composite(background, img)


def get_bnw_image(image):
    """
    converts images to black and white
    Args: PIL.Image
    Returns: PIL.Image
    """
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    pil_image = Image.fromarray(gray_image)
    enhancer = ImageEnhance.Contrast(pil_image)
    return enhancer.enhance(1.8)


def increase_contrast(image):
    """
    This function increases the contrast of an image input.
    Args: PIL.Image
    Returns: PIL.Image
    """
    img_array = np.array(image)
    min_val, max_val = np.min(img_array), np.max(img_array)
    lut = np.linspace(0, 255, max_val - min_val + 1, dtype=np.uint8)
    return Image.fromarray(lut[img_array - min_val])


def get_resize(image, target_size=512):
    """
    This function used to decide how to resize a given image without losing much information.
    Args: PIL.Image
    Returns: PIL.Image
    """
    if max(image.size) < target_size:
        return image.resize((target_size, target_size), resample=Image.LANCZOS)
    return (
        resize_by_ratio(image, target_size) if max(image.size) > target_size else image
    )


def increase_brightness(image, factor=1.6):
    """
    This function adjusts the brightness of the given image.
    Args: PIL.Image
    Returns: PIL.Image
    """
    return ImageEnhance.Brightness(image).enhance(factor)


def decode_image(image_path: str):
    """
    Loads an image and preprocesses the input image in several steps to get the image ready for DECIMER input.

    Args:
        image_path (str): path of input image

    Returns:
        Processed image
    """
    img = remove_transparent(image_path)
    img = increase_contrast(img)
    img = get_bnw_image(img)
    img = get_resize(img)
    img = central_square_image(img)
    img = increase_brightness(img)
    img_bytes = pil_image_to_bytes(img)
    img_tensor = tf.image.decode_png(img_bytes, channels=3)
    img_tensor = tf.image.resize(
        img_tensor, (512, 512), method="gaussian", antialias=True
    )
    return efn.preprocess_input(img_tensor)
