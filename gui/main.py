""" You can think of this script as the entry point for the Student Presence System application.
It initializes the program, displays a splash screen, and then launches the main GUI interface for uploading the CSV file containing student information. """


import os
import sys
import logging
import tkinter as gui

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gui.csv_gui import csv_upld_interface
from utils.utils_defs import window_centering

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

main_project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

imgs_logo_folder = os.path.join(main_project_directory, "gui", "images&logo")

logo_path = os.path.join(imgs_logo_folder, "logo.ico")

def wlcm_splash_screen():      # A function used to display the starting splash screen
    
    logging.debug("Starting show_splash_screen function.\n")
    
    splash = gui.Tk()
    splash.lift()  
    splash.attributes("-topmost", True)  
    
    splash.title("Student • Presence • System")
    
    splash.configure(bg="black")  # Setting the splash's bg color

    logging.debug("Setting the logo.\n")
    if os.path.exists(logo_path):
        splash.iconbitmap(logo_path)
        
    else:
        logging.warning("Logo icon not found. Proceeding without it (Default tk logo).\n")
        
    
    welcome_label = gui.Label(splash, text="Welcome to « Student Presence System »", 
                              font=("Georgia", 25, "bold"), 
                              fg="white", 
                              bg="black")
    welcome_label.pack(expand=True)  # Centering the label in the window

    
    description_label = gui.Label(splash, text="A Moroccan student attendance system.", 
                                  font=("Merriweather", 11, "bold", "italic"), 
                                  fg="white", 
                                  bg="black")
    description_label.pack(pady=7)
    
    window_centering(splash, 0.7, 0.1)  # Set the splash screen size to 45% width and 10% height of the screen
    
    splash.update()  # Updating the splash screen to reflect changes

    splash.after(2500, splash.destroy)  # Destroying (closing) the splash screen after 2.5 seconds
    
    logging.debug(f"Setting up the main window with title: `{splash.title()}`\n")
    splash.mainloop()

def main_program():   # The function that starts our program from the start
    
    wlcm_splash_screen()
     
    csv_upld_interface()

    logging.debug("Main program closed.\n")


if __name__ == "__main__":     # The direct execution ...
    
    
    print("\n------------------------- Main Run (main.py) -------------------------\n")
    
    
    main_program()