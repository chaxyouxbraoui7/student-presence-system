""" This file does also provide a the GUI-based interface (2nd one), for uploading images of CIN cards, processing them using OCR, and extracting CIN IDs.
The extracted CIN IDs are saved into a list as a CSV file in the data folder, and the user can view attendance records or re-upload a different student list. """


import os
import sys
import logging
import time
import datetime
import tkinter as gui
import cv2

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageEnhance
from gui.csv_gui import csv_upld_interface  
from processing.ocr_re_process import ocr_, extracting_cin  # OCR-related functions (EasyOCR in default, but you can use other models by changing the import)
from processing.csv_handler import cin_list_save, attendance_report_table_gen
from attendance_display import attendance_table_display
from utils.utils_defs import window_centering, counter

data_folder = os.path.join(project_directory, 'data') # Checking the existence of `data` folder

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

def images_interface():      # A function that opens the image upload interface
    logging.debug("Starting the images_interface function.\n")
    
    image_paths = []  # Initializing the image paths as a list
    
    images_wndw = gui.Tk()
    images_wndw.withdraw()
    images_wndw.lift()
        
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "images&logo", "logo.ico"))
    images_wndw.iconbitmap(logo_path)

    images_wndw.title("Student • Presence • System")
    
    window_centering(images_wndw, width_ratio=1, height_ratio=1)

    logging.debug("Setting the images window's background image.\n")
    
    img_path = os.path.join("gui", "images&logo", "bg2.jpg")
    
    if os.path.exists(img_path):
        og_img = Image.open(img_path)
        
        window_width = images_wndw.winfo_screenwidth()
        window_height = images_wndw.winfo_screenheight()
        
        bg_img = og_img.resize((window_width, window_height), Image.Resampling.LANCZOS)
        bg_img = ImageTk.PhotoImage(bg_img)
        
        bg_label = gui.Label(images_wndw, image=bg_img)
        bg_label.image = bg_img
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = gui.Label(images_wndw, text="Upload or capture some CIN cards images to extract IDs via OCR", font=("Georgia", 25, "bold", "italic"), padx=7, pady=7, fg="white", bg="black")
    title_label.pack(pady=10)

    log_title = gui.Label(images_wndw, text="Processing log", font=("Merriweather", 11, "bold"), fg="cyan", bg="black")
    log_title.pack(pady=(7))

    # Configuring the log widget to display processing messages
    log_widget = scrolledtext.ScrolledText(images_wndw, height=25, width=150, wrap=gui.WORD, bg="#3a3a3a", fg="white", font=("Merriweather", 11, "bold"))
    log_widget.tag_config("header", foreground="blue", font=("Georgia", 15, "bold"))
    log_widget.tag_config("info", foreground="white", font=("Merriweather", 11, "bold"))
    log_widget.tag_config("info_msg", foreground="white", font=("Merriweather", 11, "bold"))
    log_widget.tag_config("success", foreground="lightgreen", font=("Merriweather", 11, "bold"))
    log_widget.tag_config("warning", foreground="yellow", font=("Merriweather", 11, "bold"))
    log_widget.tag_config("error", foreground="red", font=("Merriweather", 11, "bold"))
    log_widget.pack(pady=15)
    log_widget.config(state="disabled")
    
    def processing_splash(): # A function that creates a splash screen for processing images
        process_splash = gui.Toplevel()
        process_splash.lift()
        process_splash.title("Processing Images")
        process_splash.configure(bg="#2e2e2e")
        
        if os.path.exists(logo_path):
            process_splash.iconbitmap(logo_path)
        
        window_centering(process_splash, 0.3, 0.15)
        
        progress_label = gui.Label(process_splash, 
                                 text="Processing images...\n\nProgress: 0%", 
                                 font=("Georgia", 14, "bold"), 
                                 fg="white", bg="#2e2e2e")
        progress_label.pack(expand=True)
        
        process_splash.update()
        return process_splash, progress_label  # Returning both window and label to use them later
    
    def upload_images():    # A function that handls the upload images behavior

        logging.debug("Starting the upload_images function.\n")
        
        nonlocal image_paths  # Using 'nonlocal' to modify 'image_paths' in the nearest enclosing function's scope (not global!)
        
        selected_files = filedialog.askopenfilenames(title="Select some images", filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")])
        
        logging.debug(f"Selected images: {selected_files}\n")
        
        if not selected_files:
            messagebox.showwarning("No images selected", "Please select at least one image!")
            logging.warning(f"No images selected: {selected_files}\n")
            return

        valid_extensions = (".png", ".jpg", ".jpeg")
        
        invalid_files = [file for file in selected_files if not file.lower().endswith(valid_extensions)]
        
        if invalid_files:
            messagebox.showwarning("Invalid file type", "Some selected files are not images.\nPlease select only PNG, JPG, or JPEG images!")
            logging.warning(f"Invalid files selected: {invalid_files}\n")
            return
        
        logging.debug(f"Valid images selected: {selected_files}\n")
        
        image_paths.clear()
        logging.debug("Clearing the image_paths list.\n")
        
        image_paths.extend(selected_files)
        logging.debug(f"Image paths updated: {image_paths}\n")
        
        success = process_ocr_on_images(image_paths, log_widget)
        logging.debug("Finished processing images.\n")
        
        attendance_report_table_gen()
        logging.debug("Attendance report table generated.\n")
        
        if not success:
            
            log_widget.config(state="normal")
            log_widget.insert(gui.END, "Please check the quality of the imported images and try again!\n", "warning")
            log_widget.config(state="disabled")
            log_widget.see(gui.END)
        
    def safe_call_def_schedl(window, delay_ms, func, *args): # A function that schedules a function to be called after a delay safely to avoid crashes
        if window.winfo_exists():  # Checking if the window does exists (or open)
            window.after(delay_ms, func, *args) # Scheduling the function to be called after delay_ms, if the window is still open

    def process_ocr_on_images(image_paths, log_widget):    # A function that processes the images and extracts CIN IDs
        
        logging.debug("Starting the process_ocr_on_images function.\n")
        
        logging.debug("Creating processing splash screen.\n")
        
        processing_wndw, progress_label = processing_splash()
        
        msg_count = counter()
        
        start_msg = "==================== Processing Started ====================\n\n"
        end_msg = "==================== Processing Completed ==================\n\n"
        info_msg = "You can now:\n\n• Import more images\n• Capture CIN cards\n• View the attendance table\n• Re-upload new lists\n\n"
        
        
        log_widget.config(state="normal")
        log_widget.insert(gui.END, f"\n{start_msg}\n", "header")
        log_widget.insert(gui.END, "The system is now processing the uploaded images to extract CIN IDs.\n\n", "info")
        log_widget.config(state="disabled")
        log_widget.see(gui.END)
        
        current_image = [0]
        success = True  # Tracking overall success
        
        logging.debug("Processing each image for OCR and CIN ID extraction.\n")
        def process_one_image(i_img):   # A function that processes one image at a time
            nonlocal success
            i_img = current_image[0]
            if i_img >= len(image_paths): # If all images have been processed
                progress_label.config(text="Complete! Closing...") # Update the label to indicate completion
                
                processing_wndw.update() # Update the window to show the message
                
                time.sleep(0.75) # Wait for a moment before closing
                
                processing_wndw.destroy() # And then close the process splash screen
                
                log_widget.config(state="normal")
                log_widget.insert(gui.END, f"\n{end_msg}\n", "header")
                log_widget.config(state="disabled")
                log_widget.see(gui.END)
                
                log_widget.config(state="normal")
                log_widget.insert(gui.END, f"\n{info_msg}\n", "info_msg")
                log_widget.config(state="disabled")
                log_widget.see(gui.END)
                
                return # Ending the function if all images are processed
            
            # Process up to 3 images starting from index i
            images_to_process = image_paths[i_img:i_img+3]
                        
            progress = int(min(i_img + 3, len(image_paths)) / len(image_paths) * 100) # Calculating the progress percentage
            progress_label.config(text=f"Processing... {progress}%") # Updating the label
            processing_wndw.update_idletasks() # Updating the window
    
            
            try: # Processing 3 images at a time
                
                for image_path in images_to_process:
                    image_file = os.path.basename(image_path)
                    message_count = next(msg_count)
                    
                    log_widget.config(state="normal")
                       
                    if not os.path.exists(image_path): # Checking if the image file exists
                        log_widget.insert(gui.END, f"\n{message_count} - Error: The file {image_path} does not exist.\n\n\n", "error")
                        logging.error(f"Error: The file {image_path} does not exist.\n")
                        log_widget.config(state="disabled")
                        log_widget.see(gui.END)
                        success = False
                        continue # Skipping to the next image if the file does not exist
                    
                    # Performing the extraction
                    logging.debug(f"Starting the OCR processing for image: {image_path}\n")
                    
                    ocr_start_time = time.time()
                    ocr_result = ocr_(image_path)
                    ocr_end_time = time.time()
                    
                    print("\n")
                    
                    logging.debug(f"OCR processing for {image_path} took {ocr_end_time - ocr_start_time:.2f} seconds.\n")
                    
                    logging.info(f"OCR result for {image_path}: \n\n{ocr_result}\n\n")
                    
                    logging.debug(f"Starting the regex (re) CIN ID search for image: {image_path}\n")
                    
                    cin_id_start_time = time.time()
                    cin_id = extracting_cin(ocr_result)
                    cin_id_end_time = time.time()
                    
                    logging.debug(f"regex took {cin_id_end_time - cin_id_start_time:.2f} seconds to find {cin_id} in {image_path}.")
                    
                    print("\n")
                    
                    logging.info(f"The CIN ID in {image_path}: {cin_id}\n\n")
                    
                    if cin_id:
                        log_widget.insert(gui.END, f"\n✓ {message_count} - Successfully extracted CIN ID from '{image_file}' ▶ | {cin_id} |\n\n\n", "success")
                        logging.debug(f"Successfully extracted CIN ID: {cin_id} from {image_file}\n")
                        
                        cin_list_save(cin_id)
                        
                    else:
                        log_widget.insert(gui.END, f"\n⨻ {message_count} - No CIN ID found in {image_file} (Check your actual list since the model might struggle!!!)\n\n\n", "warning")
                        logging.warning(f"No CIN ID found in {image_file}\n")
                        success = False
            except Exception as e:
                success = False
                error_msg = f"\n⚠ {message_count} - Failed to process {image_file}\n\n"
                log_widget.insert(gui.END, error_msg, "error")
                logging.error(f"CRASH in {image_path}", exc_info=True)
                logging.error(f"Error processing {image_path}: {str(e)}")
                
            
            finally:
                log_widget.config(state="disabled")
                log_widget.see(gui.END)
                current_image[0] += 3 # Incrementing the image index
                safe_call_def_schedl(processing_wndw, 1, process_one_image, current_image[0]) # Scheduling the next image processing after 1 ms delay
                
        process_one_image(current_image[0]) # Starting the processing the first image
        return success  # Return overall success
        
    def reupload_csv():    # A function that handls the re-upload of a new CSV file
        logging.debug("Starting the reupload_csv function.\n")
        
        logging.debug("Closing images window.\n")
        images_wndw.destroy()
        
        logging.debug("Re-opening the CSV window.\n")
        csv_upld_interface()
        
    def capture_card():    # A function that captures the card using the laptop camera with thw help of OpenCV
        logging.debug("Starting the capture_card function.\n")

        cap = cv2.VideoCapture(0)  # Opening & and holding the default camera (0 for built-in camera, 1 for external camera)
        cv2.namedWindow("Capture CIN Card") # Creating a window to display the camera feed

        while True: # Looping the to capture the image
            ret, frame = cap.read() # Reading the frame from the camera
            if not ret:
                logging.error("Failed to capture image from camera.\n")
                break # Exiting the loop if the camera is not available or fails to capture
            
            cv2.imshow("Capture CIN Card", frame) # Displaying the frame in the window
            
            key = cv2.waitKey(1) # Waiting for a key press
            if key % 256 == 27:  # ESC key to exit
                logging.debug("ESC key pressed. Closing camera.\n")
                break
            elif key % 256 == 32 or key % 256 == 13:  # SPACE or ENTER key to capture
                capture_imgs_folder = os.path.join(data_folder, "capture-imgs")
                os.makedirs(capture_imgs_folder, exist_ok=True)
                cap_card_tm = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # Getting the live time the image was captured in to name it
                img_nm = f"{cap_card_tm}_cin_card.png"
                img_nm_path = os.path.join(capture_imgs_folder, img_nm)
                cv2.imwrite(img_nm_path, frame) # Saving the captured image
                logging.debug(f"Captured image saved as {img_nm_path}\n")
                break

        cap.release() # Releasing the camera
        cv2.destroyAllWindows() # Closing the camera window

        if os.path.exists(img_nm_path):
            logging.debug(f"Enhancing the captured image quality: {img_nm_path}\n")
            captured_img = Image.open(img_nm_path)

            # Enhancing the image quality
            enhancer = ImageEnhance.Contrast(captured_img)
            enhanced_img = enhancer.enhance(2)

            enhancer = ImageEnhance.Sharpness(enhanced_img)
            enhanced_img = enhancer.enhance(2)

            enhanced_img.save(img_nm_path)
            logging.debug(f"Enhanced image saved as {img_nm_path}\n")

            # Processing the captured and enhanced image
            success = process_ocr_on_images([img_nm_path], log_widget)
            logging.debug("Finished processing captured image.\n")

            attendance_report_table_gen()

            if success:
                log_widget.config(state="normal")
                log_widget.insert(gui.END, "You can now:\n\n• Import images\n• Capture more cards\n• View the attendance table\n• Re-upload new lists\n\n", "info")
                log_widget.config(state="disabled")
                log_widget.see(gui.END)
            else:
                log_widget.config(state="normal")
                log_widget.insert(gui.END, "Please try importing or fix the CIN ID and try again!\n", "warning")
                log_widget.config(state="disabled")
                log_widget.see(gui.END)

    btn_frame = gui.Frame(images_wndw, bg="#3a3a3a")
    btn_frame.pack(pady=10)
    
    import_imgs = gui.Button(btn_frame, text="Import Images For Attendance", 
                            command=upload_images,
                            width=30, 
                            height=1, 
                            font=("Inter", 15, "bold"), 
                            bg="#4CAF50", 
                            fg="black",
                            borderwidth=3,
                            relief="raised")
    import_imgs.pack(side="left", padx=1)
    
    capture_img = gui.Button(btn_frame, text="Capture CIN Card",
                            command=capture_card,
                            width=30,
                            height=1, 
                            font=("Inter", 15, "bold"), 
                            bg="#FF0000", 
                            fg="black",
                            borderwidth=3,
                            relief="raised")
    capture_img.pack(side="left", padx=1)
    
    show_table = gui.Button(btn_frame, text="View Attendance Records (Table)",
                            command=lambda: attendance_table_display(images_wndw),
                            width=30,
                            height=1, 
                            font=("Inter", 15, "bold", "underline"), 
                            bg="#2196F3", 
                            fg="white",
                            borderwidth=3,
                            relief="raised")
    show_table.pack(side="left", padx=1)
    
    reupload = gui.Button(btn_frame, text="Upload Different Student List (CSV)",
                          command=reupload_csv,
                          width=30,
                          height=1,
                          font=("Inter", 15, "bold"), 
                          bg="#808080", 
                          fg="black",
                          borderwidth=3,
                          relief="raised")  
    reupload.pack(side="left", padx=1)
    
    note_label = gui.Label(images_wndw, text="> Note: Since this system relies on a pre-trained OCR model rather than a custom-trained one, for optimal accuracy in extracting CIN IDs, the uploaded images should be of at least medium quality. Poor-quality images may lead to incorrect extractions.\n>> Recommendation: If you're using a CPU (no GPU) with this machine, we recommend importing 1 to 3 images at a time (at most) to ensure the service runs efficiently (this is optional). Since this model is slower on a CPU, switching to a GPU, if available, is highly recommended.",
                            font=("Merriweather", 9), 
                            fg="white", 
                            bg="black", 
                            justify="center",
                            borderwidth=1,
                            relief="solid")
    note_label.pack(pady=15, padx=1)
    
    logging.debug("Images window created successfully!\n")
    logging.debug("Waiting for user to upload images file, capture cards, view attendance table or re-upload a new list.\n")
    
    images_wndw.deiconify()
    
    if images_wndw:
        images_wndw.mainloop()

if __name__ == "__main__":  # A direct run to text the script
    
    print("\n------------------------- Direct Run (upload_images.py) -------------------------\n")  # End message
    
    images_interface()