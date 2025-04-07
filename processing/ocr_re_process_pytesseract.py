""" This script is the last OCR one using Tesseract this time.
It is the same as the previous one but with some modifications to the OCR engine and image processing techniques.
Import modification: 
##from processing.ocr_re_process import ocr_, extracting_cin >>>> ##from processing.ocr_re_process_pytesseract import ocr_pytss, extracting_cin`` """


import pytesseract
import re
import cv2    
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [ %(levelname)s ] - %(message)s')

ocr_reader = None

def ocr_pytss(image_path):
    global ocr_reader
    
    if ocr_reader is None:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Setting the path to the Tesseract executable 

    # The default path Windows
    # For Linux & macOS, Tesseract is usually installed globally and is accessible in your system's PATH
    # Unless you installed it in a different location, the can change it to your own path
    # Just make sure Tesseract is installed and the path is correct!
    
    image = cv2.imread(image_path)
    if image is None:
        logging.error(f"Failed to load image: {image_path}")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    resized_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR) # Resizing the image for better OCR accuracy (works better for Tesseract)
    
    bin_image = cv2.adaptiveThreshold(resized_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Applying adaptive thresholding to improve contrast between text and background | max value=255, method=Gaussian, type=Binary, block size=11 and the constant C=2
    
    morph = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))   # Performing morphological operations to remove small noise (closing: dilation followed by erosion)
    denoised_image = cv2.morphologyEx(bin_image, cv2.MORPH_CLOSE, morph) # Applying the closing by filling the tiny gaps (dilation) then removing outer noise (erosion)
    # All that to help clean small defects and connect broken letters before OCR

    try:    # The extractions try...
        
        logging.info("Performing OCR using Tesseract...")
        ocr_config = r'--oem 1 --psm 6'        # Configuring Tesseract with high accuracy, and assuming a single uniform block of text
        
        # --oem: OCR Engine Mode ~ 0. Lagacy egine only (The OG engine - Tesseract 3)
        # 1. LSTM (Long short-term memory engien - Tesseract 4/5)
        # 2. Legacy & LSTM
        # 3. Default (It auto chooses the best engine based on the structure given)
        
        ## --psm: Page Segmentation Mode ~ 0. OCD only (Orientation & script detection)
        ## 1. Automatic page segmentation along with OSD
        ## 2. Same as `1` but no OCD and no OCR this time lol
        ## 3. Same as `2` but this time there is OCR and the segmentation is fully auto
        ## 4. Assumes a single column of text of variable sizes
        ## 5. Assumes a single uniform block of vertically aligned text
        ## 6. Assumes a single uniform block of text (we used it because ID cards usually have well-structured text)
        ## 7. Treats the image as a single text line
        ## 8. Treats the image as a single word
        ## 9. Treats the image as a single word in a circle
        ## 10. Treats the image as a single character
        ## 11. Sparses text and finds as much text as possible in no particular order (no OSD, and most used form random scattered text)
        ## 12. Sparses text with OSD (handles documents with sparse, scattered text and irregular layouts, unlike PSM 3)
        ## 13. Raw line, bypasses most layout analysis (used for simple lines)
        
        ### REFERENCE: [Pytesseract | Page Segmentation Modes (PSMs) | Kaggle](https://www.kaggle.com/code/dhorvay/pytesseract-page-segmentation-modes-psms)
        ### [Tesseract OCR | Page Segmentation Modes (PSMs) | Tesseract](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html#page-segmentation-methods)
        
        """ So the most suitable configuration for our case is [1/3 & 6]"""

        ocr_results = pytesseract.image_to_string(denoised_image, lang='eng+fra+ara', config=ocr_config) #this can be also the pro
        logging.info(f"OCR Result:\n{ocr_results}")
        
        return ocr_results.splitlines()  # Returning the results as a list of lines
    
    except Exception as e:
        logging.error(f"Error during OCR: {e}")
        return []
    
def extracting_cin(ocr_result):
    logging.info(f"Extracted OCR Text: {ocr_result}")

    ocr_result_combined = ' '.join(ocr_result)
    
    cin_regex = r'\b[A-Z]{2}\d{4,6}\b'

    logging.info(f"Combined OCR Text for Regex Matching: {ocr_result_combined}")

    re_match = re.search(cin_regex, ocr_result_combined)
    if re_match:
        cin_id = re_match.group().replace(" ", "")
        logging.info(f"Potential CIN ID Found: {cin_id}")
        return cin_id
    
    logging.warning("No CIN ID found in the extracted text.")
    return None


if __name__ == "__main__":
    
    
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
        
        ocr_results = ocr_pytss(image_path)

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