import os
import sys
import logging
import tkinter as gui

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

from tkinter import messagebox
from PIL import Image, ImageTk
from processing.csv_handler import csv_fl_upload
from utils.utils_defs import window_centering

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

students_path = os.path.join(project_directory, 'data', 'students.csv')

def csv_upld_interface(csv_wndw=None):  # A function for uploading the CSV file with an argument root
    logging.debug("Starting csv_wndw function.\n")
    
    created_csv_wndw = False    # Creating the window if not provided
    
    if csv_wndw is None:
        csv_wndw = gui.Tk()
        
        created_csv_wndw = True  # Marking the creation
        
        csv_wndw.withdraw()
    
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "images&logo", "logo.ico"))
    
    csv_wndw.iconbitmap(logo_path)
    
    csv_wndw.title("Student • Presence • System")
    
    window_centering(csv_wndw, width_ratio=0.75, height_ratio=0.75)
    
    logging.debug("Setting the CSV window's background image.\n")
    img_path = os.path.join("gui", "images&logo", "bg1.jpg")  # Pathing the background image
        
    if os.path.exists(img_path):
        og_img = Image.open(img_path)   # Opening the bg image with PIL
        
        # Getting the window size
        window_width = csv_wndw.winfo_screenwidth()
        window_height = csv_wndw.winfo_screenheight()
        
        # Resizing the image to fit the window
        bg_img = og_img.resize((window_width, window_height), Image.Resampling.LANCZOS)
        bg_img = ImageTk.PhotoImage(bg_img)  # Converting the image into a format that Tkinter understands
        
        bg_label = gui.Label(csv_wndw, image=bg_img)  # Create a label to hold the background image
        bg_label.image = bg_img # Keep a reference to the image to prevent garbage collection (prob with tk lol)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1) # Making sure the bg image covers the entire window
    
    
    wndw_title = gui.Label(csv_wndw, text="Upload your CSV file for attendance tracking", 
                           font=("Georgia", 33, "bold", "italic"), 
                           bg="black", 
                           fg="white", 
                           padx=10, 
                           pady=10)
    wndw_title.place(relx=0.5, rely=0.1, anchor="center")

    
    import_csv = gui.Button(csv_wndw, text="Import Student List (CSV)", 
                            command=lambda: csv_fl_upload(csv_wndw),
                            width=25, 
                            height=1, 
                            font=("Inter", 15, "bold"), 
                            bg="#4CAF50", 
                            fg="black",
                            borderwidth=3,
                            relief="raised")
    import_csv.place(relx=0.5, rely=0.5, anchor="center")

    
    skip_list = gui.Button(csv_wndw, text="Skip List Upload", 
                           command=lambda: skip_csv_upload(csv_wndw),
                           width=25, 
                           height=1, 
                           font=("Inter", 11, "bold"),
                           bg="#808080",
                           fg="black",
                           borderwidth=3,
                           relief="raised")
    skip_list.place(relx=0.5, rely=0.55, anchor="center")

    
    csv_note = gui.Label(csv_wndw, text="Please upload a CSV file containing the following columns: CIN, Numero, Nom, Prenom.", 
                         font=("Merriweather", 9, "bold"), 
                         fg="white", 
                         bg="#3a3a3a", 
                         justify="center",
                         borderwidth=1,
                         relief="solid")
    csv_note.place(relx=0.5, rely=0.75, anchor="center")

    logging.debug("CSV window created successfully!\n")
    
    csv_wndw.deiconify()

    
    if created_csv_wndw:
        logging.debug("CSV window initialized successfully.\n")
        logging.debug("Waiting for user to upload a CSV file or skip the upload.\n")
        csv_wndw.mainloop()
        
    
def skip_csv_upload(csv_wndw):# A function that provides the skipping of the CSV upload option and proceeds to the next interface
    logging.debug("Starting skip_csv_upload function.\n")
    
    from capt_imgs_gui import images_interface
    
    logging.debug("Skipping CSV upload...\n")
    
    logging.debug(f"Checking for existing CSV file at: {students_path}\n")
    
    if not os.path.exists(students_path): # Checking the file existence
        messagebox.showerror("Missing CSV File", "No student list found!\nPlease upload a valid CSV file before skipping.")
        logging.error("No student list found!")
        return
    
    logging.debug("CSV file found. Proceeding to the next interface.\n")
    
    csv_wndw.destroy()
    logging.debug("CSV window closed.\n")
    
    images_interface()
    logging.debug("Images interface closed.\n")


if __name__ == "__main__":   # Executing the script directly
    
    
    print("\n------------------------- Direct Run (upload_csv.py) -------------------------\n")
    
    
    csv_upld_interface()