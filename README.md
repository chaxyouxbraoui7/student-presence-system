# **Student Attendance System**

## Project Overview

This is a Final Year Project (FYP) for the SMI department at "La Faculté Polydisciplinaire de Ouarzazate" - Ouarzazate - Morocco.

The system is intended for educational use only.

## Features  

This system provides three key functionalities:  

- **Student Data Import:** Upload a CSV file containing student details (**CIN, Numero, Nom, Prenom**). This file is stored as `students.csv`.

- **CIN Card Processing:** Upload images of CIN cards, which are processed to extract CIN numbers using Optical Character Recognition (OCR) and regex. The extracted CINs are saved in `extracted_cin.csv`.

> **Note:** For optimal accuracy in extracting CIN numbers, the uploaded images should be at least of mid-quality.  
> Since this system relies on a pre-trained OCR model rather than a custom-trained one, poor-quality images may lead to incorrect extractions.

- **Automated Attendance Tracking:** The system compares the extracted CINs with the student CSV file, generates an attendance report, and saves it as `attendance.csv`. The attendance is displayed as a table in the GUI.


## Project Code Installation

To set up the project on a local machine, follow the steps below :

**Python Version :**

This project is compatible with :

```bash
Python 3.12.9
```

Ensure you have this version installed before proceeding.

1. **Verify your Python version :**

- To check your Python version, you can run : 

```bash
python --version
```

- If you have multiple Python versions, you can use :

```bash
python3 --version
```

2. **Clone the repository :**

```bash
   git clone https://github.com/chaxyouxbraoui7/student-presence-system.git
```

3. **Navigate to the project directory :**

```bash
cd student-presence-system
```

4. **Create a virtual environment :**

```bash
python -m venv venv
```

5. **Activate the virtual environment :**

- On Windows:

```bash
.\venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

6. **Upgrade pip (Important) :**

```bash
python.exe -m pip install --upgrade pip
```

7. **Install the required dependencies :**

```bash
python -m pip install -r requirements.txt
```

**If the above fails, you can try :**

```bash
pip install --no-cache-dir -r requirements.txt
```

8. **Then finally run the system :**

```bash
python gui/main.py
```

**Libraries Version :**

```bash
easyocr==1.7.2
opencv-python==4.11.0.86
pandas==2.2.3
regex==2024.11.6
```

## Troubleshooting

- **Issue :** `pip install` doesn't work.

  **Solution :** Ensure you have activated the virtual environment before running `pip install`.

- **Issue :** The program doesn't run or shows an error when starting.

  **Solution 1 :** Ensure you have the correct Python version installed (3.12.9).

  **Solution 2 :** Ensure you have navigated to the project directory by running `cd .\student-presence-system\`

- **Issue :** The libraries don't install when running `pip install -r requirements.txt`.

  **Solution :** Try installing them one by one, or run `pip install pandas opencv-python easyocr regex` or `pip install pandas opencv-python easyocr regex torch torchvision`.

## License

This project is intended for educational purposes only and cannot be used commercially.

Feel free to modify it for personal or academic use.

**Contributions are welcome!** Feel free to submit **pull requests** or open an **issue** if you find a bug or have suggestions.