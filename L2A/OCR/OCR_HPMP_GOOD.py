import pytesseract
from PIL import Image
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR_5.3.3\tesseract.exe'

def resize_image(image, scale_factor):
    # Resize the image
    resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    return resized_image

def apply_ocr_and_display(image_path, scale_factor=5.0):
    # Open the image
    original_image = Image.open(image_path)

    # Convert the image to a NumPy array
    rgb_image = np.array(original_image)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)

    # Simple binary thresholding
    _, binary_image = cv2.threshold(gray_image, 145, 255, cv2.THRESH_BINARY_INV)

    # Set pixels to white (255) on the X axis from pixel 46 to 54
    binary_image[:, 46:54] = 255

    # Resize the thresholded image to make the letters appear larger
    resized_image = resize_image(binary_image, scale_factor)

    # Perform OCR on the resized image with configuration parameters
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(Image.fromarray(resized_image), custom_config)

    # Print the OCR result in the terminal
    print(f"OCR Result for {os.path.basename(image_path)}:\n{text}\n")

    # Display the original image, the thresholded image, and the resized image
    plt.figure(figsize=(18, 6))

    # Original image
    plt.subplot(1, 3, 1)
    plt.imshow(rgb_image)
    plt.title('Original Image')

    # Thresholded image
    plt.subplot(1, 3, 2)
    plt.imshow(binary_image, cmap='gray')
    plt.title('Thresholded Image')

    # Resized image
    plt.subplot(1, 3, 3)
    plt.imshow(resized_image, cmap='gray')
    plt.title('Resized Image')

    plt.show()

# Specify the path to the folder containing PNG images
folder_path = r'H:\.shortcut-targets-by-id\1VSD6Z7UK0SywHePIdMBlTFp54ESQUX9G\python raspberry project\PC\L2\OCR\for text reading'

# Loop through all PNG files in the folder
image_path = os.path.join(folder_path, "HPMP.png")
apply_ocr_and_display(image_path)
