# Same as the upload_csv.py, but this time we added scrolledtext for log display
import tkinter as tk
import os
import pandas as pd
from tkinter import filedialog, messagebox, scrolledtext

# Here is : importing the functions for image preprocessing and OCR

from processing.image_preprocessing import preprocess_image
from processing.ocr_re import perform_ocr, extract_cin_id

# Here is : ensuring the "data/" directory exists before saving the file

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_folder = os.path.join(project_root, 'data')

os.makedirs(data_folder, exist_ok=True)

# Here is : the function that will save extracted CINs to data/extracted_cin.csv

def save_cin_to_csv(cin_id):

    file_path = os.path.join(data_folder, "extracted_cin.csv")

    # Here is : check if the CIN ID already exists in the CSV file

    if os.path.isfile(file_path):

        # If the file exists, read it into a DataFrame

        existing_data = pd.read_csv(file_path)

        # Here is : check if the CIN ID already exists in the CSV file

        if cin_id in existing_data['CIN'].values:

            print(f"CIN ID {cin_id} already exists in the CSV file. Skipping save.")  # Optional log in console

            return  # If the CIN already exists, don't save it again

    # Here is : create a DataFrame for the new CIN ID

    new_data = pd.DataFrame([[cin_id]], columns=["CIN"])

    # Here is : if the file doesn't exist, create it with a header, otherwise append

    if os.path.isfile(file_path):

        # Here is : if the file exists, append the new CIN ID

        new_data.to_csv(file_path, mode="a", header=False, index=False)  # Here is : appending to the file without the header

    else:
        # Here is : if the file doesn't exist, create it with a header

        new_data.to_csv(file_path, mode="w", header=True, index=False)  # Here is : creating the file with the header

# Here is : the function that will process the selected images

def process_images(image_paths, log_widget):

    # Here is : iterating through each image file path in the list

    for image_path in image_paths:

        # Here is : checking if the image file exists; if not, print an error message

        if not os.path.exists(image_path):

            log_widget.config(state="normal")  # Here is : enabling log widget to insert text

            log_widget.insert(tk.END, f"Error: The file {image_path} does not exist.\n", "error")  # Here is : displaying an error message in red

            log_widget.config(state="disabled")  # Here is : disabling log widget after inserting text

            log_widget.see(tk.END)  # Here is : scrolling to the latest message

            continue  # Here is : skipping to the next image if the current one doesn't exist

        image_file = os.path.basename(image_path)  # Here is : getting the base name of the image file
        
        log_widget.config(state="normal")

        log_widget.insert(tk.END, f"Processing image: {image_file}...\n", "info")  # Here is : displaying that the image is being processed

        log_widget.config(state="disabled")

        log_widget.see(tk.END)

        # Here is : preprocessing the image

        processed_image_path = preprocess_image(image_path)

        
        # Here is : performing OCR on the image to extract text

        ocr_result = perform_ocr(image_path)
        
        # Here is : extracting the CIN ID from the OCR result

        cin_id = extract_cin_id(ocr_result)

        # Here is : checking if a CIN ID was successfully extracted and print the result

        log_widget.config(state="normal")
        
        if cin_id:

            log_widget.insert(tk.END, f"CIN ID found in {image_file}: {cin_id}\n", "success")  # Here is : displaying the CIN ID in green

            # Here is : saving the extracted CIN ID to the CSV file

            save_cin_to_csv(cin_id)

        else:

            log_widget.insert(tk.END, f"No CIN ID found in {image_file}.\n", "warning")  # Here is : displaying a warning in orange

        log_widget.config(state="disabled")

        log_widget.see(tk.END)  # Here is : making sure the latest message is visible

    log_widget.config(state="normal")

    log_widget.insert(tk.END, "Processing completed.\n", "done")  # Here is : indicating that all images have been processed

    log_widget.config(state="disabled")

    log_widget.see(tk.END)

# Here is : the function that opens the window (interface)

def open_image_upload_interface():

    global image_paths  # Here is : declaring the image_paths variable globally

    image_paths = []  # Here is : initializing an empty list to store the selected image paths

    # Here is : Creating the window

    folder_root = tk.Tk()

    folder_root.title("Upload Images")  # Here is : the title again

    folder_root.geometry("500x300")  # Here is : the size again

    # Same as the last interface

    label = tk.Label(folder_root, text="Upload images to process", font=("Arial", 12))

    label.pack(pady=10)

    # Here is : creating a text box with a scrollbar to display logs

    log_widget = scrolledtext.ScrolledText(folder_root, height=10, width=60, wrap=tk.WORD)

    log_widget.pack(pady=10)

    # Here is : making the text box read-only

    log_widget.config(state="disabled")

    # Here is : the function that will handle the image upload process

    def upload_images():

        # Here is : opening a file dialog to allow the user to select one or more image files

        selected_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        
        if not selected_files:

            messagebox.showwarning("Warning", "No images selected.")  # Here is : showing a warning message if no files have been selected

            return

        # Here is : adding the selected image paths to the image_paths (variable) list

        image_paths.extend(selected_files)
        
        # Here is : disabling the button to prevent multiple uploads

        button.config(state=tk.DISABLED)
        
        # Here is : processing the selected images

        process_images(image_paths, log_widget)

    # Here is : creating the button

    button = tk.Button(folder_root, text="Select Images", command=upload_images)

    button.pack(pady=10)

    folder_root.mainloop()  # And finally, here is : starting the Tkinter event loop to keep the window open