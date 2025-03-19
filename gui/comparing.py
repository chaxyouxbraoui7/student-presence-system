import tkinter as tk
from tkinter import messagebox
import pandas as pd
import cv2
import easyocr

def extract_cin_from_image(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path, detail=0)
    extracted_cins = [word for word in results if word.isdigit()]
    return set(extracted_cins)

def compare_cin():
    # Load CINs from database (CSV file)
    df = pd.read_csv("database.csv")
    database_cins = set(df["CIN"].astype(str))
    
    # Extract CINs from image (update with actual path)
    extracted_cins = extract_cin_from_image("cin_image.jpg")
    
    # Compare
    matched_cins = database_cins.intersection(extracted_cins)
    if matched_cins:
        messagebox.showinfo("Result", f"Matched CINs: {', '.join(matched_cins)}")
    else:
        messagebox.showwarning("Result", "No matches found.")

# Create GUI window
root = tk.Tk()
root.title("CIN Comparator")
root.geometry("300x150")

button = tk.Button(root, text="Go for it", command=compare_cin, font=("Arial", 14))
button.pack(pady=20)

root.mainloop()
