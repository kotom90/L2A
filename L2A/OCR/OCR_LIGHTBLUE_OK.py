import cv2
import pytesseract
import matplotlib.pyplot as plt
import numpy as np

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR_5.3.3\tesseract.exe'

def preprocess_and_ocr(image_path, blur_radius=(0.6, 0.6), fixed_threshold=127):
    # Read the image using cv2
    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Error: Unable to load the image at path: {image_path}")
        return

    # Separate color channels using color deconvolution
    bgr_planes = cv2.split(original_image)
    deconvolution_matrix = np.array([[0.0, 0.0, 1.0],
                                     [0.0, 1.0, 0.0],
                                     [1.0, 0.0, 0.0]])
    shadows = cv2.transform(original_image, deconvolution_matrix)
    shadow_channel = cv2.split(shadows)[0]

    # Use fixed threshold
    _, thresh = cv2.threshold(shadow_channel, fixed_threshold, 255, cv2.THRESH_BINARY)

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(thresh, (0, 0), blur_radius[0], blur_radius[1])

    # Perform OCR on the blurred image
    text = pytesseract.image_to_string(original_image)

    # Display the images and OCR result using matplotlib
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(shadow_channel, cmap='gray')
    plt.title('Shadow Channel')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(thresh, cmap='gray')
    plt.title('Fixed Thresholding')
    plt.axis('off')

    """plt.subplot(1, 3, 3)
    plt.imshow(blurred_image, cmap='gray')
    plt.title(f'Blurred Image (Blur={blur_radius})')
    plt.axis('off')"""

    plt.show()

    print("OCR Result:", text)

    return text

# Example usage
image_path = "targetText.png"
result_text = preprocess_and_ocr(image_path)
print("OCR Result:", result_text)