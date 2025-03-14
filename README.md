## Project Overview

This is a Final Year Project (FYP) for the SMI department at "La Faculté Polydisciplinaire de Ouarzazate" - Ouarzazate - Morocco.
The system is intended for educational use only.

## Features

- **CSV Upload**: Upload a CSV file with student data (ID, First Name, Last Name, Exam Number).
- **Image Folder Upload**: Upload CIN card images for processing.
- **Attendance Tracking**: Automatically compare extracted IDs with the CSV data and display attendance status as a table.

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