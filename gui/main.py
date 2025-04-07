# Importing all the necessary libraries & absolute importing of functions and variables

import tkinter as tk
import os
import sys

# Adding the parent directory to the system path for module importing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importing the 'upload_csv' function from the 'upload_csv' file in the 'gui' folder

from gui.upload_csv import upload_csv

# The function that initializes and starts the application

def start_program():
    
    # Creating the main app window
    
    root = tk.Tk()

    # Setting the window's title
    
    root.title("Student • Presence • System")
    
    # Calling the 'upload_csv' function to set up the CSV upload interface
    
    upload_csv(root)

    # Starting the tkinter event loop to keep the app interactive
    
    root.mainloop()

# Checking if the script is being executed directly

if __name__ == "__main__":
    
    # If true, the function can be called to launch the application
    
    start_program()