import cv2
import os

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image {image_path} not found.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Ensure we are referring to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the root directory
    processed_folder = os.path.join(project_root, 'data', 'processed')  # Folder inside the root

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    processed_image_path = os.path.join(processed_folder, f'preprocessed_{os.path.basename(image_path)}')
    cv2.imwrite(processed_image_path, thresholded)

    return processed_image_path
