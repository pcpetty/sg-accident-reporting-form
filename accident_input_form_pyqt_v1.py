import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
import datetime

class AccidentReportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window Title
        self.setWindowTitle("Accident Report Form")

        # Layout
        self.layout = QVBoxLayout()

        # Accident Date
        self.date_label = QLabel("Enter accident date (mm/dd/yyyy):")
        self.date_input = QLineEdit()
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_input)

        # Accident Location
        self.location_label = QLabel("Enter accident location:")
        self.location_input = QLineEdit()
        self.layout.addWidget(self.location_label)
        self.layout.addWidget(self.location_input)

        # Weather Conditions
        self.weather_label = QLabel("Select weather conditions:")
        self.weather_dropdown = QComboBox()
        self.weather_dropdown.addItems(["Clear", "Overcast", "Sunny", "Rainy", "Windy", "Stormy"])
        self.layout.addWidget(self.weather_label)
        self.layout.addWidget(self.weather_dropdown)
        
                # Police Involvement
        self.police_label = QLabel("Police involved?")
        self.police_dropdown = QComboBox()
        self.police_dropdown.addItems(["Yes", "No"])
        self.layout.addWidget(self.police_label)
        self.layout.addWidget(self.police_dropdown)


        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)  # Connect button to form submission
        self.layout.addWidget(self.submit_button)

        # Set the layout
        self.setLayout(self.layout)

    def submit_form(self):
        # Collect user input
        date_str = self.date_input.text()
        location = self.location_input.text()
        weather = self.weather_dropdown.currentText()

        # Process inputs
        accident_date = get_date(date_str)
        if accident_date is None:
            QMessageBox.warning(self, "Input Error", "Invalid date format. Please use mm/dd/yyyy.")
            return

        # Display collected data
        QMessageBox.information(
            self,
            "Form Submitted",
            f"Accident Date: {accident_date}\nLocation: {location}\nWeather: {weather}"
        )

def get_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
    except ValueError:
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccidentReportApp()
    window.show()
    sys.exit(app.exec())


def collect_accident_data(date_str, location, weather):
    accident_data = {}

    # Process the data
    accident_date = get_date(date_str)
    if not accident_date:
        return {"error": "Invalid date format."}

    accident_data["accident_date"] = accident_date
    accident_data["accident_location"] = location
    accident_data["weather_info"] = weather

    return accident_data

def submit_form(self):
        # Collect user input
        date_str = self.date_input.text()
        location = self.location_input.text()
        weather = self.weather_dropdown.currentText()

        # Use the backend function
        accident_data = collect_accident_data(date_str, location, weather)

        if "error" in accident_data:
            QMessageBox.warning(self, "Input Error", accident_data["error"])
            return

        # Display collected data
        QMessageBox.information(
            self,
            "Form Submitted",
            f"Accident Date: {accident_data['accident_date']}\n"
            f"Location: {accident_data['accident_location']}\n"
            f"Weather: {accident_data['weather_info']}"
        )

