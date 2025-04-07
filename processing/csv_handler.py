""" This module handles CSV file operations for the student attendance system, including validation, uploading, processing, and generating attendance reports. 
It ensures data consistency and integrates with the GUI for user interactions. """


import os
import sys
import logging
import pandas as pnds

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Adding the project root directory to sys.path to allow module imports from the project
sys.path.append(project_directory)

from tkinter import filedialog, messagebox
from utils.utils_defs import counter  

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

print("\n\n")

logging.debug("Starting CSV handling...\n")

print("\n\n------------------------- Our CSV Database :) -------------------------\n\n")

logging.debug("Checking data folder existence\n")
data_folder = os.path.join(project_directory, 'data') # Checking the existence of `data` folder
students_path = os.path.join(data_folder, "students.csv")  # ... `students.csv` file
extracted_path = os.path.join(data_folder, "cin_list.csv")  # ... `cin_list.csv` ...
attendance_path = os.path.join(data_folder, "attendance.csv")  # ... `attendance.csv` ...

os.makedirs(data_folder, exist_ok=True) # Creating the folder if it does not exist
if not data_folder:
    logging.debug(f"Creating data folder at: {data_folder}")
else:
    logging.debug(f"Data folder already existe at: {data_folder}")
    
def file_validation(): # A function to validate the existence of all the required `.csv` files in the `data` folder
        
    # Checking the existence of the required files
    students_exists = os.path.exists(students_path)  # True if `students.csv` exists
    extracted_exists = os.path.exists(extracted_path)  # True if c`in_list.csv` exists

    # Loging debugs and errors, If either of the required files is missing
    if not students_exists or not extracted_exists:
        logging.error("One or more required files are missing.\n")
        logging.debug(f"students.csv exists: {'Yes' if students_exists else 'No'}\n")
        logging.debug(f"cin_list.csv exists: {'Yes' if extracted_exists else 'No'}\n")
        return None, None, None  # Return None for all paths

    return students_path, extracted_path, attendance_path  # Returning the paths to each file

def csv_fl_upload(csv_wndw):   # A function that handls the logic for uploading the CSV file
    logging.debug("Starting csv_fl_upload function.\n")
    
    from gui.capt_imgs_gui import images_interface

    file_path = filedialog.askopenfilename(title="Select a CSV File", filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")])
    
    logging.debug("Checking if a file was selected...\n")
    if not file_path:
        messagebox.showwarning("No File Selected", "Please select a file!")
        logging.warning("No file selected!\n")
        return
    #messagebox.showinfo("CSV File Selected", f"File selected successfully from:\n{file_path}\nYou can now proceed.")
    logging.debug(f"File selected successfully from: {file_path}\n")

    logging.debug("Validating the file's extension...\n")
    if not file_path.lower().endswith(".csv"):
        messagebox.showwarning("Invalid File Type", "The selected file is not a CSV.\nPlease select a valid file!\n")
        logging.error("Invalid file type selected!\n")
        return
    
    logging.debug("File type validated successfully.\n")

    # Reading the CSV file into a pandas DataFrame
    logging.debug("Reading the CSV file into a DataFrame...\n")
    students_df = pnds.read_csv(file_path)
    
    # Defining the target path where the CSV file will be saved
    students_path = os.path.join(data_folder, "students.csv")
    
    # Saving the DataFrame to the target path as 'students.csv'
    logging.debug(f"Saving the DataFrame to {students_path}...\n")
    students_df.to_csv(students_path, index=False)
    
    logging.debug("CSV file saved successfully.\n")
    
    csv_wndw.destroy()
    logging.debug("CSV window closed.\n")
          
    images_interface()
    logging.debug("Images interface opened.\n")
    
def cin_list_save(cin_id):# A function that makes the saving of the extracted CIN ID as a CSV file
    logging.debug("Starting the cin_list_save function.\n")
    
    file_path = os.path.join(data_folder, "cin_list.csv")

    logging.debug(f"Saving CIN ID: {cin_id} to the list.\n")
    
    try:  # Checking if the file already exists in the directory then reading its content to check if the CIN ID already in there so we can skip its saving
        file_existence = os.path.isfile(file_path)
        logging.debug(f"Checking if cin_list.csv exists at: {file_path}\n")
        
        if file_existence:
            logging.debug(f"File |{file_path}| exists. Reading it.\n")
            existing_extracted_fl = pnds.read_csv(file_path)
            
            if cin_id in existing_extracted_fl['CIN'].values: 
                logging.debug(f"CIN ID `{cin_id}` already exists in the file. Skipping save.\n")
                return   # Exiting if the CIN ID already exists
            
            logging.debug(f"CIN ID {cin_id} does not exist in the file. Proceeding to save.\n")
            
        # Creating a new DataFrame to save the CIN ID
        new_extracted_fl = pnds.DataFrame([[cin_id]], columns=["CIN"])
        logging.debug(f"New DataFrame created:\n{new_extracted_fl}\n")
        
        if file_existence:  # Appending the file if it exists
            new_extracted_fl.to_csv(file_path, mode="a", header=False, index=False) # Appending instead of overwriting | Avoiding the repeat of column names | Avoiding the default index of Pandas
            logging.debug(f"New CIN ID appended to {file_path}.\n")
            
        else:  # Creating a new file if it doesn't exist
            new_extracted_fl.to_csv(file_path, mode="w", header=True, index=False)  # Creating this time instead of writing | Reading the column header | Avoiding the default index of Pandas
            logging.debug("Successfully created the new list.\n")
            
        logging.debug(f"Successfully saved CIN ID: {cin_id} to {file_path}.\n")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save CIN ID to CSV: {e}")
        logging.error(f"Error occurred while saving CIN ID: {cin_id} to CSV file.\n")
        
def attendance_report_table_gen():  # A function that generates the attendance report by comparing CIN numbers from `students.csv` & `cin_list.csv`
    students_path, extracted_path, attendance_path = file_validation()  # Validation of the required files
    
    report_start_time = pnds.Timestamp.now()  # Recording the start time of the report generation using pandas
    logging.info("Generating attendance report...\n")
    logging.debug(f"Attendance report generation started at: {report_start_time}\n")
    
    if not students_path or not extracted_path:
        return  # Exiting if so

    try:
        students_df = pnds.read_csv(students_path)  # Reading `students.csv`
        logging.debug("Successfully read students.csv.\n")
        
    except Exception as e:
        logging.error(f"Error reading students.csv: {e}\n")
        return

    try:
        extracted_df = pnds.read_csv(extracted_path, header=None, names=["CIN"])  # Reading `cin_list.csv`
        logging.debug("Successfully read cin_list.csv.\n")
        
    except Exception as e:
        logging.error(f"Error reading cin_list.csv: {e}\n")
        return

    if "CIN" not in students_df.columns:  # Ensuring thst the `students.csv` has a CIN column
        logging.error("'CIN' column is missing in students.csv.\n")
        messagebox.showwarning("Warning", "'CIN' column is missing in the list of students.\nPlease check the file format.")
        return

    progress_count = counter()  # Initializing a counter for tracking student CIN progress
    
    students_df["Attendance Status"] = students_df["CIN"].apply(lambda cin: "Present" if cin in extracted_df["CIN"].values else "Absent ⨉")
    
    # Logging the processing of each student's CIN along with the attendance status
    for i_cin, j_status in zip(students_df["CIN"], students_df["Attendance Status"]):
        logging.debug(f"Processing student #{next(progress_count)} - |{i_cin}| - Attendance statue: {j_status}...\n")

    try:
        students_df.to_csv(attendance_path, index=False)  # Saving attendance table report to `attendance.csv`
        #messagebox.showinfo("Success", "Attendance report generated successfully!\n You can now viww the report.")
        logging.debug(f"Attendance report generated successfully at: {attendance_path}\n")
        
    except Exception as e:
        logging.error(f"Error saving attendance.csv: {e}\n")
        return
    
    report_end_time = pnds.Timestamp.now()  # The end time of the report generation
    logging.debug(f"Attendance report generation completed at: {report_end_time}\n")
    
def csv_reupload(new_csv_path): # A function that checks if the newly uploaded CSV file is different from the existing one    
    
    logging.debug("Checking for existing students.csv...\n")
    
    if os.path.exists(students_path):    # If students.csv already exists, compare it with the newly uploaded file
        logging.debug(f"Existing students.csv found at: {students_path}\n")
        
        try:
            students_df = pnds.read_csv(students_path)
            new_students_df = pnds.read_csv(new_csv_path)

            if students_df.equals(new_students_df):  # Checking if both DataFrames are identical
                #messagebox.showinfo("No Changes", "The uploaded CSV file is identical to the existing one.")
                logging.debug("The uploaded CSV file is identical to the existing one.")
                
            else:
                logging.debug("A different CSV file has been uploaded.")
                
        except Exception as e:
            logging.error(f"Error comparing CSV files: {e}")
            messagebox.showwarning("Please check the file format or the columns of the file (CIN, Numero, Nom, Prenom).")
            
    else:
        logging.debug("No existing CSV file found. This is the first uploaded one.")
    
    
if __name__ == "__main__":  # Testing the functions by executing of this module directly
    
    
    print("\n\n------------------------- Attendance Report Generator Starts -------------------------\n")
    
    
    logging.debug("Checking required files in the 'data' folder...\n")
    students_path, extracted_path, attendance_path = file_validation()  # Validating the files
    
    if not students_path or not extracted_path:
        logging.warning("One or both CSV files are not present in the `data` folder.\n")
        
    else:
        logging.debug("All required files are present. Generating attendance report...\n")
        attendance_report_table_gen()

        # Displaying attendance statistics, if `attendance.csv` was successfully generated, 
        if os.path.exists(attendance_path):
            
            try:
                attendance_df = pnds.read_csv(attendance_path)
                
                total_students = len(attendance_df)
                
                present_count = attendance_df["Attendance Status"].value_counts().get("Present", 0)  # Counting present students with `value_counts()` from Pandas
                absent_count = attendance_df["Attendance Status"].value_counts().get("Absent ⨉", 0)  # ... absent ...

                print("Attendance Report Summary:\n")
                
                logging.info(f"Total Students: {total_students}\n")
                logging.info(f"Present: {present_count}\n")
                logging.info(f"Absent: {absent_count}\n")
                
            except Exception as e:
                logging.error(f"Error reading attendance.csv: {e}\n")
                
        else:
            logging.error("Failed to generate attendance report.\n")
            
            
    print("------------------------- Attendance Report Generator Ends -------------------------\n\n")