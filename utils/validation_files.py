import os

def validate_csv(file_path):
    """Validate if the file is a valid CSV"""
    if not file_path.endswith(".csv"):
        raise ValueError("The uploaded file is not a valid CSV file.")
    return True

def validate_image_folder(folder_path):
    """Validate if the folder contains images"""
    if not os.path.isdir(folder_path):
        raise ValueError("The selected folder is not valid.")

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        raise ValueError("The folder contains no valid image files.")

    return image_files
