# Here is : importing all the necessary libraries for Tkinter, file dialogs, message boxes, and OS operations
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd  # Here is : importing pandas for handling the CSV storing
from upload_images import open_image_upload_interface # Here is : importing the function to open the second interface which is the images uploader (from upload_images.py)

# Here is : the function responsible for uploading the CSV file

def upload_csv():
    
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Here is : opening the file dialog and allowing the user to select the CSV file
    
    if not file_path.endswith(".csv"):
        
        messagebox.showerror("Error", "Please select a CSV file to continue the processing.")  # Here is : alerting the user with an error message if the file is not a CSV
        
        return
    
    # Here is : setting the project root directory
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Here is : getting the root directory
    
    data_folder = os.path.join(project_root, 'data')  # Here is : setting the 'data/' folder path relative to the root
    
    os.makedirs(data_folder, exist_ok=True)  # Here is : ensuring that the 'data/' folder exists in the correct location

    # Here is : using pandas to read the CSV file and save it to "data/students.csv"
    
    df = pd.read_csv(file_path)  # Here is : reading the CSV file into a pandas DataFrame
    
    target_path = os.path.join(data_folder, "students.csv")
    
    df.to_csv(target_path, index=False)  # Here is : saving the DataFrame to the target path 
    
    # Here is : closing the window only after selecting a valid file
    
    root.destroy()

    # Here is : opening the second interface, after the CSV uploading is successfully completed
    
    open_image_upload_interface()

# Here is : creating the main interface or should we call it window for the CSV uploader interface

root = tk.Tk()

root.title("Student CSV Uploader")  # Here is : setting the window's title

root.geometry("400x200")  # Here is : setting the window's size

label = tk.Label(root, text="Select Your CSV for Attendance", font=("Arial", 12))  # Here is : creating a label widget, to mainly guide the user

label.pack(pady=20)  # Here is : adding the label to the window with vertical padding

button = tk.Button(root, text="Browse and Upload", command=upload_csv)  # Here is : creating a button widget that allows the user to browse and upload the CSV file

button.pack()  # Here is : adding the button to the window

root.mainloop()  # And finally, here is for : adding the Tkinter event loop so the window stays open and responsive