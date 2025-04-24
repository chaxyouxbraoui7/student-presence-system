""" This module provides utility functions for common tasks such as generating an incremental counter and centering application windows.
It also includes a test section that demonstrates these functions by creating a simple Tkinter-based GUI, 
which displays an odd number counter in a centered window with logging for debugging. """

import tkinter as tk
import cv2


def counter():    # A function that counts upwards indefinitely
    # Used to count the number of messages in the logwidget, the number of absent and present students in the list, the tracking progress for the attendace report.
    i = 1
    while True:  # A infinite loop
        yield i  # Returning the current counter value 'i' by pausing with 'yield'
        i += 1

def window_centering(window, width_ratio=1, height_ratio=1):    # A function to center the windows on the screen based on specified width and height ratios.

    # Fetching the width & the height of the screen in pixels
    screen_width = window.winfo_screenwidth() 
    screen_height = window.winfo_screenheight()
    
    # Calculating the width and height of the window based on "screen_width" & "screen_height"
    width = int(screen_width * width_ratio)
    height = int(screen_height * height_ratio)
    
    # Calculating the horizontal & vertical coordinates (x & y)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")    # Setting the geometry of the window
    
def center_camera_wndw(win_nm, win_width=640, win_height=480): # A function to center the camera window display
    camera_wndw = tk.Tk()
    camera_wndw.withdraw()
    screen_width = camera_wndw.winfo_screenwidth()
    screen_height = camera_wndw.winfo_screenheight()
    
    x = (screen_width - win_width) // 2
    y = (screen_height - win_height) // 2

    cv2.namedWindow(win_nm, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_nm, win_width, win_height)
    cv2.moveWindow(win_nm, x, y)


if __name__ == "__main__":     # A direct execution of the file to test the functions before using them in other places


    import logging
    import tkinter as gui
    from tkinter import PhotoImage
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

    def update_count():   # A function that updates the label of the window with the next odd number
        while True:    # A infinite loop
            nxt_odd_num = next(odd_num)  # Geting the next number from the counter
            
            if nxt_odd_num % 2 != 0:
                counting.config(text=str(nxt_odd_num))  # Updating the counting
                break
            
        odd.after(750, update_count)  # Scheduling the next update after 750 ms


    print("\n\n------------------------- Functions Test Starts -------------------------\n")

    try:
        odd_num = counter()
        logging.info("Creating the Odd window\n")

        odd = gui.Tk()
        
        odd.lift()
        
        odd.attributes("-topmost", True)

        odd.title("Odd")

        odd.configure(bg="black")

        window_centering(odd, width_ratio=0.3, height_ratio=0.15)

        img = PhotoImage(file = r"gui\images&logo\logo.png")    # Loading the PNG image as a PhotoImage object with the help of tk

        odd.iconphoto(True, img)    # Setting the window icon to the PNG image

        frame = gui.Frame(odd, bg="black")
        frame.pack(expand=True)  # Centering the frame

        title = gui.Label(frame, text="Odd Number Counter", font=("Times New Roman", 25, "bold"), fg="white", bg="black", padx=10, pady=10)
        title.pack(anchor="center")  # Center the title label

        counting = gui.Label(frame, text="0", font=("Times New Roman", 25, "bold"), fg="lightgreen", bg="black")
        counting.pack(anchor="center")

        update_count()

        odd.mainloop()
        logging.info("The Odd window was created and displayed successfully.")

    except Exception as e:
        logging.error(f"An error occurred while creating or displaying the Odd window: {e}")

    
    print("\n------------------------- Functions Test Ends -------------------------\n\n")