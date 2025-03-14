from PIL import Image
import imutils
import cv2

def resize_image(image_path, width=800):
    """Resize image using Pillow and imutils"""
    image = Image.open(image_path)
    image = imutils.resize(image, width=width)
    return image

def convert_to_pil_image(image_array):
    """Convert OpenCV image to PIL image"""
    return Image.fromarray(image_array)
