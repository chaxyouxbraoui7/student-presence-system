import tkinter as tk
from tkinter import filedialog, messagebox
from upload_images import open_image_upload_interface

def upload_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path.endswith(".csv"):
        messagebox.showerror("Error", "Please select a valid CSV file.")
        return

    # Close the CSV upload window
    root.destroy()

    # After successful CSV upload, open the image upload interface
    open_image_upload_interface()
    
# Main window for CSV upload
root = tk.Tk()
root.title("CSV & Image Upload")
root.geometry("400x200")

label = tk.Label(root, text="Upload your CSV file", font=("Arial", 12))
label.pack(pady=20)

button = tk.Button(root, text="Select CSV File", command=upload_csv)
button.pack()

root.mainloop()
