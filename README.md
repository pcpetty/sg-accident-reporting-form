# Safety Generalist Accident Reporting System

The Safety Generalist Accident Reporting System is a Python-based tool designed to streamline accident data collection, storage, and reporting for safety professionals. With its modular design, the program efficiently handles driver and vehicle data, generates professional reports in multiple formats (Excel, PDF), and integrates seamlessly with PostgreSQL databases for long-term storage and analysis.

---

## **Features**
- **Accident Data Collection**: Collects detailed data about drivers, vehicles, weather conditions, and more.
- **Database Integration**: Stores and retrieves data from PostgreSQL.
- **Report Generation**: Exports reports in Excel and PDF formats.
- **Modular Design**: Clean separation of concerns for maintainability and scalability.
- **Editing Existing Reports**: Allows modification of stored reports.

---

## **File Structure**
sg_accident_form/
│
├── sg_accident_form/         # Package directory
│   ├── __init__.py           # Makes this a package
│   ├── main.py               # Entry point for the program
│   ├── data_collection.py    # Data collection functions
│   ├── db_operations.py      # PostgreSQL operations
│   ├── report_generation.py  # Report exporting functions
│   ├── utils.py              # Helper functions
│
├── tests/                    # Tests for the package
│   ├── __init__.py           # Makes this a package
│   ├── test_data_collection.py
│   ├── test_db_operations.py
│   ├── test_report_generation.py
│
├── requirements.txt          # List of dependencies
├── setup.py                  # Packaging configuration
└── README.md                 # Documentation

```