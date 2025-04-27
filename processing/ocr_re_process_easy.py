""" This script is the one that performs Optical Character Recognition (OCR) on images using EasyOCR, 
with a specific focus on extracting CIN IDs from text.
It includes functions for OCR processing and regex-based CIN extraction, 
along with a test section that allows users to interactively select images and specify OCR preferences via a Tkinter-based interface, 
while logging relevant details for debugging. """


import easyocr
import re
import cv2
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [ %(levelname)s ] - %(message)s')

ocr_reader = None

def ocr_easy(image_path):    # A function that performs OCR using EasyOCR
    global ocr_reader
    
    if ocr_reader is None: #this can be also the pro
        ocr_reader = easyocr.Reader(['ar', 'en'])  # Initializing if not already done to avoid multipl initializations
          
    image = cv2.imread(image_path)  # Loading the image from the given file path using OpenCV
    graysc_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converting the image from color to grayscale
    
    ocr_results = ocr_reader.readtext(graysc_image, detail=0, paragraph=True)  # Performing OCR and returning only the detected text as a list of strings
    # 'detail=1' for returning detailed information, including the bounding box coordinates, text, and confidence score for each detected text region.
    
    return ocr_results

def extracting_cin(ocr_result):    # A function that extracts the CIN ID from the OCR results
    ocr_result_combined = ' '.join(ocr_result)  # Joining all extracted text into a single string for better CIN ID extraction
    
    cin_regex = r"\b([A-Z]{1,2}\s*\d{4,8})\b"  # Defining a regex pattern for matching CIN ID formats
    
    # `[A-Z]{1,2}` for letters (for example: A1234 or AB1234) and `\d{4,8}` for digits (for example: AB1234 or AB123456 or A1234 or AB123456)
    # \b is a word boundary anchor that ensures the matched CIN ID is isolated from surrounding text."
    # It helps avoid matching CIN IDs that are part of a longer string for ex "startAB123456end".
    
    re_match = re.search(cin_regex, ocr_result_combined)    # Searching for the CIN ID in the results using regex
    
    if re_match:  # Checking if a match
        cin_id = re_match.group().replace(" ", "")  # Extracting the matched CIN ID & removing the spaces if found
        logging.info(f"Potential CIN ID Found: {cin_id}")
        return cin_id
    
    logging.warning("No CIN ID found in the extracted text.")
    return None


if __name__ == "__main__":   # Testing the functions by direct execution

    
    print("\n\n------------------------- The OCR Test Starts -------------------------\n")
    
    try:
        while True:
            logging.info("Choose the type of OCR to perform:\n")
            print("1. Normal Text Extraction")
            print("2. CIN Card ID Extraction\n")
            choice = input("\nEnter your choice: ").strip()
            print("\n")

            if choice == "1":
                logging.debug("User chose Normal Text Extraction.\n")
                break
            
            elif choice == "2":
                logging.debug("User chose CIN Card ID Extraction.\n")
                break
            
            else:
                logging.error("Invalid choice. Please enter 1 or 2.\n")

        if choice == "1":
            
            while True:
                logging.info("Choose the language for OCR:\n")
                print("1. Arabic (ar)")
                print("2. English (en)")
                print("3. French (fr)\n")
                lang_choice = input("\nEnter your choice: ").strip()
                print("\n")

                if lang_choice == "1":
                    selected_lang = ['ar']
                    logging.debug("User chose Arabic (ar).\n")
                    break
                
                elif lang_choice == "2":
                    selected_lang = ['en']
                    logging.debug("User chose English (en).\n")
                    break
                
                elif lang_choice == "3":
                    selected_lang = ['fr']
                    logging.debug("User chose French (fr).\n")
                    break
                
                else:
                    logging.error("Invalid choice. Please enter 1, 2, or 3.\n")
      
        print("--------------------------------------------------------------------------")

        print("\nPlease select the image file for OCR...\n")
        
        ocr_tst = tk.Tk()
        ocr_tst.lift()  
        ocr_tst.attributes("-topmost", True)  
        ocr_tst.withdraw()

        image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")])

        if not image_path:
            messagebox.showwarning("No image selected", "Exiting Program!")
            logging.warning("No image selected.\n")
            exit()

        if not image_path.lower().endswith((".png", ".jpg", ".jpeg")):
            messagebox.showwarning("Invalid file type", "Exiting Program!")
            logging.warning(f"Invalid file selected: {image_path}\n")
            exit()

        logging.info(f"Performing OCR on: {image_path}\n")
        
        ocr_results = ocr_easy(image_path)

        combined_result = ' '.join(ocr_results)
        total_characters = len(combined_result)
        print("\n")
        if choice == "1":
            logging.info(f"OCR Result:\n\n{combined_result}\n\n\nTotal Characters: {total_characters}\n")
        else:
            cin_id = extracting_cin(ocr_results)
            logging.info(f"OCR Result:\n\n{combined_result}\n\n\nExtracted CIN ID: {cin_id if cin_id else 'None'}\n")
            logging.info(f"Total Characters: {total_characters}\n")

    except KeyboardInterrupt:
        logging.warning("Program interrupted by the user. Exiting gracefully...\n")
        
    except FileNotFoundError as e:
        logging.error(f"Error: {e}\n")
        
    except cv2.error as e:
        logging.error(f"OpenCV Error: {e}\n")
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}\n")
        
        
    print("------------------------- The OCR Test Ends -------------------------\n\n")