# <img src="gui/images&logo/logo.png" alt="icon" height="25" style="vertical-align: middle;"/> **Student Attendance System**

## Project Overview

This is a Final Year Project (FYP) for the SMI department at "La Faculté Polydisciplinaire de Ouarzazate" - Ouarzazate - Morocco.

# It Features  

four key functionalities:  

- **Student Data Import:** Upload a CSV file containing student details (**CIN, Numero, Nom, Prenom**). This file is stored as `students.csv`.

- **CIN Card Processing:** Upload images of CIN cards, which are processed to extract CIN numbers using Optical Character Recognition (OCR) and regex. The extracted CINs are saved in `extracted_cin.csv`.

- **Capture Card Feature (Experimental):** Capture images of CIN cards using your laptop's camera. While this feature is still under development, please note that OCR accuracy may be limited due to the camera quality. Low-quality images can cause difficulties with CIN extraction, but we are actively working on improving this feature, insh'allah.

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

## Troubleshooting

- **Issue :** `pip install` doesn't work.

  **Solution :** Ensure you have activated the virtual environment before running `pip install`.

- **Issue :** The program doesn't run or shows an error when starting.

  **Solution 1 :** Ensure you have the correct Python version installed (3.12.9).

  **Solution 2 :** Ensure you have navigated to the project directory by running `cd .\student-presence-system\`

- **Issue :** The libraries don't install when running `pip install -r requirements.txt`.

  **Solution :** Try installing them one by one.

## Notes

- The project is intended for educational purposes only and cannot be used commercially!

- For optimal accuracy in extracting CIN IDs, the uploaded images should be and clear and of a reasonable quality (or at least of mid-quality), since the system relies on a pre-trained OCR model rather than a custom-trained one, poor-quality images may lead to incorrect extractions.

- **Contributions are welcome!** and we really encourage pull requests or suggestions to help improve the system, especially for the CIN card capture feature or other new ideas!