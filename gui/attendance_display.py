""" This file provides the last (3rd) GUI-based interface, for displaying the attendance table. 
It loads the attendance data, displays it in a table format using Tkinter's Treeview widget, 
and provides counters for students marked as "Present" or "Absent".
It also includes error handling and window management features to ensure smooth interaction with the user. """


import os
import sys
import logging
import pandas as pnds
import tkinter as gui

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

from tkinter import ttk
from tkinter import messagebox
from utils.utils_defs import window_centering, counter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

data_folder = os.path.join(project_directory, "data")
attendance_path = os.path.join(data_folder, 'attendance.csv')

logo_path = os.path.join(project_directory, "gui", "images&logo", "logo.ico")

def attendance_table_display(previous_window=None, direct_run=False): # A function that displays the attendance table, has 2 parmeters as Boolean; one for indicating the previous window and the other for indicating if the script is run directly
    logging.debug("Starting the attendance_table_display function.\n")
    
    if previous_window is None:    # Creating a new main window, if no previous one's provided
        previous_window = gui.Tk()
        previous_window.withdraw()
        previous_window.lift()
        
    if not os.path.exists(attendance_path):    # Checking if the attendance file exists before proceeding
        messagebox.showwarning("No Updated Table Yet", "Attendance table is not updated yet!\nUpload some images to update it.")
        logging.error("Attendance table not found.\n") 
        
        if direct_run:
            previous_window.destroy()
            
        return

    logging.debug("Attendance table found. Proceeding to display the table...\n")
    
    table_window = gui.Toplevel(previous_window)    # Creating a window (Toplevel) to display the table

    table_window.iconbitmap(logo_path)

    table_window.title("Student • Presence • System | Attendance Table")

    window_centering(table_window, width_ratio=0.9, height_ratio=0.8)

    try:
        attendance_df = pnds.read_csv(attendance_path)
        logging.debug("Attendance table successfully loaded.\n")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load attendance table:\n{e}")
        logging.error(f"Failed to load attendance table: {e}\n")
        
        if direct_run:
            previous_window.destroy()
            
        return
    
    # Creating a styling object to customize the table
    tab_style = ttk.Style()
    
    tab_style.configure("Treeview.Heading", font=("Calibri", 15, "bold"))
    tab_style.configure("Treeview", font=("Verdana", 11))
    
    # Creating a frame to contain the table with a border
    tab_frame = gui.Frame(table_window, borderwidth=7, relief="ridge")
    tab_frame.pack(expand=True, fill="both")
    
    tab_tree = ttk.Treeview(tab_frame, columns=list(attendance_df.columns), show="headings", height=22)    # Creating a Treeview widget to display the attendance table
    
    tab_tree.tag_configure("present", background="lightgreen")    # Defining a tag for rows where students are marked "Present"
            
    for col in attendance_df.columns:    # Looping through each column in the DataFrame and set up table headers
        tab_tree.heading(col, text=col, anchor="center")  # Setting the column heading text
        tab_tree.column(col, anchor="center", width=100)  # Centering align content and setting the column width
    
    ids_count = counter()    # Initializing a counter for unique IDs
    
    # Initializing counters for students marked "Present" and "Absent"
    present_count = 0
    absent_count = 0
    
    for _, i_row in attendance_df.iterrows():    # Looping through each row in the DataFrame and insert it into the table
        values = list(i_row)
    
        if "Present" in values:
            tag_present = "present"
            present_count += 1
        else:
            tag_present = ""
            absent_count += 1
    
        tab_tree.insert("", "end", iid=next(ids_count), values=values, tags=(tag_present,))
    
    logging.debug("Attendance table displayed successfully!\n")
    
    tab_tree.pack(expand=True, fill="both")    # Adding the table widget to the frame and expanding it
    
    # Creating a frame to display the counters (Present & Absent)
    counter_frame = gui.Frame(table_window, bg="white", borderwidth=7, relief="groove")
    counter_frame.place(anchor="se", relx=1.0, rely=1.0, x=-counter_frame.winfo_width(), y=-counter_frame.winfo_height())
    
    present_label = gui.Label(counter_frame, text=f"Present: {present_count}", font=("Calibri", 14, "bold"), fg="lightgreen", bg="white")
    present_label.pack(side="bottom", anchor="e", padx=3, pady=1)
    
    absent_label = gui.Label(counter_frame, text=f"Absent: {absent_count}", font=("Calibri", 14, "bold"), fg="red", bg="white")
    absent_label.pack(side="bottom", anchor="e", padx=3, pady=1)
    
    table_window.update_idletasks()    # Forcing the window to refresh its layout
    
    def close_table_window():    # A function that handls the closing of the table window
        logging.debug("Srarting close_table_window function...\n")
        
        table_window.destroy()
        
        logging.debug("The attendance table window closed!\n\n")

        if direct_run:
            previous_window.destroy()
            sys.exit(0)  # Exiting the entire program

    table_window.protocol("WM_DELETE_WINDOW", close_table_window)    # A protocol that attachs the close function to the window close event
    
    
    if previous_window and isinstance(previous_window, gui.Tk):# Starting the main event loop, if the script created the main window, 
        previous_window.mainloop()


if __name__ == "__main__":       # The test with a direct execution
    
    
    print("\n\n------------------------- Direct Run (attendance_display.py) -------------------------\n")
    
    
    attendance_table_display(direct_run=True)