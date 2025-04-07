""" This script is the 2nd OCR one using PaddleOCR.
It is the same as the previous one but with some modifications to the OCR engine and image processing techniques.
You can use this module and test it on the system by modifing: ##from processing.ocr_re_process import ocr_, extracting_cin
line in each file that used in to: ##from processing.ocr_re_process_pytesseract import ppocr_, extracting_cin`` """


from paddleocr import PaddleOCR
import re
import cv2

ocr_reader = None

def ppocr_(image_path):    # A function that performs OCR using PaddleOCR
    global ocr_reader
    
    if ocr_reader is None:
        ocr_reader = PaddleOCR(use_angle_cls=True, lang='en')  # Initializing if not already done to avoid multiple initializations
          
    image = cv2.imread(image_path)  # Loading the image from the given file path using OpenCV
    graysc_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converting the image from color to grayscale
    
    ocr_results = ocr_reader.ocr(graysc_image, cls=True)  # Performing the OCR on the grayscale image and returning detailed results (text, confidence, box) using cls
    
    ocr_results = [line[1][0] for line in ocr_results[0]]  # Extracting only the recognized text from each detected line in the first results
    return ocr_results

def extracting_cin(ocr_result):
    ocr_result_combined = ' '.join(ocr_result)
    
    cin_regex = r"\b([A-Z]{1,2}\s*\d{4,8})\b"
    
    re_match = re.search(cin_regex, ocr_result_combined)
    
    if re_match:
        cin_id = re_match.group().replace(" ", "")
        logging.info(f"Potential CIN ID Found: {cin_id}")
        return cin_id
    
    logging.warning("No CIN ID found in the extracted text.")
    return None


if __name__ == "__main__":   # Testing the functions by direct execution

    import logging
    import tkinter as tk
    from tkinter import filedialog, messagebox
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [ %(levelname)s ] - %(message)s')
    
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
                    selected_lang = 'ar'
                    logging.debug("User chose Arabic (ar).\n")
                    break
                
                elif lang_choice == "2":
                    selected_lang = 'en'
                    logging.debug("User chose English (en).\n")
                    break
                
                elif lang_choice == "3":
                    selected_lang = 'fr'
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
        
        ocr_results = ppocr_(image_path)

        combined_result = ' '.join(ocr_results)
        total_characters = len(combined_result)
        print("\n")
        if choice == "1":
            logging.info(f"OCR Result:\n\n{combined_result}\n\n\nTotal Characters: {total_characters}\n")
            print(f"OCR Result:\n\n{combined_result}\n\n\nTotal Characters: {total_characters}\n")
        else:
            cin_id = extracting_cin(ocr_results)
            logging.info(f"OCR Result:\n\n{combined_result}\n\n\nExtracted CIN ID: {cin_id if cin_id else 'None'}\n")
            logging.info(f"Total Characters: {total_characters}\n")
            print(f"OCR Result:\n\n{combined_result}\n\n\nExtracted CIN ID: {cin_id if cin_id else 'None'}\n")
            print(f"Total Characters: {total_characters}\n")

    except KeyboardInterrupt:
        logging.warning("Program interrupted by the user. Exiting gracefully...\n")
        
    except FileNotFoundError as e:
        logging.error(f"Error: {e}\n")
        
    except cv2.error as e:
        logging.error(f"OpenCV Error: {e}\n")
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}\n")
        
        
    print("------------------------- The OCR Test Ends -------------------------\n\n")