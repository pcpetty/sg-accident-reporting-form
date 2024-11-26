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

def save_to_database(accident_data):
    try:
        conn = sqlite3.connect('accident_reports.db')
        cursor = conn.cursor()
        
        # Insert data into the table
        cursor.execute("""
        INSERT INTO accident_reports (date, location, weather, police_involved, tow_required)
        VALUES (?, ?, ?, ?, ?)
        """, (
            accident_data["date"],
            accident_data["location"],
            accident_data["weather"],
            accident_data["police_involved"],
            accident_data["tow_required"]
        ))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False


# Police Involvement
self.police_label = QLabel("Police involved?")
self.police_dropdown = QComboBox()
self.police_dropdown.addItems(["Yes", "No"])
self.layout.addWidget(self.police_label)
self.layout.addWidget(self.police_dropdown)

# Tow Required
self.tow_label = QLabel("Tow required?")
self.tow_dropdown = QComboBox()
self.tow_dropdown.addItems(["Yes", "No"])
self.layout.addWidget(self.tow_label)
self.layout.addWidget(self.tow_dropdown)

def fetch_all_records():
    conn = sqlite3.connect('accident_reports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accident_reports")
    records = cursor.fetchall()
    conn.close()
    return records


def view_records(self):
    records = fetch_all_records()
    if not records:
        QMessageBox.information(self, "No Records", "No accident reports found.")
        return

    record_text = "\n".join(
        f"ID: {r[0]}, Date: {r[1]}, Location: {r[2]}, Weather: {r[3]}, Police: {r[4]}, Tow: {r[5]}"
        for r in records
    )
    QMessageBox.information(self, "Accident Records", record_text)
