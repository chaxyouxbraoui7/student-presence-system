## Project Overview

This is a Final Year Project (FYP) for the SMI department at "La Faculté Polydisciplinaire de Ouarzazate" - Ouarzazate - Morocco.
The system is intended for educational use only.

## Features

- **CSV Upload**: Upload a CSV file with student data (ID, First Name, Last Name, Exam Number).
- **Image Folder Upload**: Upload CIN card images for processing.
- **Attendance Tracking**: Automatically compare extracted IDs with the CSV data and display attendance status as a table.

## Folder Structure Overview:

The project folder is structured as follows to maintain organization and clarity:

**database/:** Contains the database setup and CRUD operations:

- db_handler.py: Performs CRUD operations on the database.

**gui/:** Contains GUI-related files implemented using Tkinter:

- attendance_display.py: Displays the attendance table after processing.

- main.py: Main GUI script that manages the interfaces.

- upload_csv.py: Interface for uploading the student data (CSV file).

- upload_images_folder.py: Interface for uploading the images folder (CIN card images folder).

**processing/:** Contains the image processing and OCR-related functions:

- image_preprocessing.py: Handles OpenCV preprocessing of images.

- ocr.py: Handles EasyOCR and regex for extracting CIN IDs.

**utils/:** Contains utility functions:

- utils.py: Handles image preprocessing using Pillow and imutils.

- validate_files.py: Handles validation of CSV and images folder.

**.gitignore:** Git ignore files.

**requirements.txt:** List of all the required Python dependencies for the project.

**README.md:** Explanation of the project (how to use it, and the folder structure).

## Project Code Installation

To set up the project on a local machine, follow the steps below:

1. **Clone the repository:**

```bash
   git clone https://github.com/chaxyouxbraoui7/student-presence-system.git
```

2. **Create a virtual environment:**

```bash
python -m venv venv
```

3. **Activate the virtual environment:**

- On Windows:

```bash
.\venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install the required dependencies:**

```bash
pip install -r requirements.txt
```

5. **Then finally run the system:**

```bash
python gui/main.py
```

## License

This project is intended for educational purposes only and cannot be used commercially.
Feel free to modify it for personal or academic use.