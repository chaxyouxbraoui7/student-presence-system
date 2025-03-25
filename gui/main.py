import tkinter as tk
from tkinter import messagebox
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from gui.upload_csv import upload_csv  # Use absolute import instead of relative
#my branch

# geeneral func

def start_program():
    root = tk.Tk()
    root.title("CSV & Image Upload")
    root.geometry("400x200")

    label = tk.Label(root, text="Upload your CSV file", font=("Arial", 12))
    label.pack(pady=20)

    button = tk.Button(root, text="Select CSV File", command=upload_csv)
    button.pack()

if __name__ == "__main__":
    start_program()