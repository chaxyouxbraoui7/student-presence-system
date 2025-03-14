import tkinter as tk
import os
from tkinter import filedialog, messagebox
from processing.image_preprocessing import preprocess_image  # Updated import
from processing.ocr_re import perform_ocr, extract_cin_id  # Updated import

def process_images(image_paths):
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"Error: The file {image_path} does not exist.")
            continue

        image_file = os.path.basename(image_path)
        print(f"Processing image: {image_file}")

        processed_image_path = preprocess_image(image_path)
        ocr_result = perform_ocr(image_path)
        cin_id = extract_cin_id(ocr_result)

        if cin_id:
            print(f"CIN ID found in {image_file}: {cin_id}")
        else:
            print(f"No CIN ID found in {image_file}.")

    print("Processed images.")

def open_image_upload_interface():
    global image_paths
    image_paths = []

    folder_root = tk.Tk()
    folder_root.title("Upload Images")
    folder_root.geometry("400x200")

    label = tk.Label(folder_root, text="Upload images to process", font=("Arial", 12))
    label.pack(pady=20)

    def upload_images():
        selected_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not selected_files:
            messagebox.showwarning("Warning", "No images selected.")
            return

        image_paths.extend(selected_files)
        folder_root.destroy()
        process_images(image_paths)

    button = tk.Button(folder_root, text="Select Images", command=upload_images)
    button.pack()

    folder_root.mainloop()
