import cv2
import pytesseract
import matplotlib.pyplot as plt
import numpy as np

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR_5.3.3\tesseract.exe'

def preprocess_and_ocr(image_path):
    # Read the image using cv2
    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Error: Unable to load the image at path: {image_path}")
        return

    # Separate color channels using color deconvolution
    deconvolution_matrix = np.array([[0.0, 0.0, 1.0],
                                     [0.0, 1.0, 0.0],
                                     [1.0, 0.0, 0.0]])
    shadows = cv2.transform(original_image, deconvolution_matrix)
    shadow_channel = cv2.split(shadows)[0]

    # Perform OCR on the shadow channel
    text = pytesseract.image_to_string(shadow_channel)

    # Display the images and OCR result using matplotlib
    plt.figure(figsize=(8, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(original_image[...,::-1])
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(shadow_channel, cmap='gray')
    plt.title('Shadow Channel')
    plt.axis('off')

    plt.show()

    print("OCR Result:", text)

    return text

# Example usage
image_path = "targetText.png"
result_text = preprocess_and_ocr(image_path)
print("OCR Result:", result_text)
