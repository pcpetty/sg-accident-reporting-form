# SG Accident Report Generation

# Import Libraries and Modules
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import json
from openpyxl.chart import BarChart, Reference
import datetime


def export_to_excel(data, filename="Accident_Report.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Accident Report"

    # Add headers
    headers = ["Reference Key", "Accident Date", "Accident Time", "Location", "Hazmat", "Driver Name", "Vehicle Plate"]
    ws.append(headers)

    # Add data
    ws.append([
        data["reference_key"],
        data["accident_date"],
        data["accident_time"],
        data["accident_location"],
        "Yes" if data["hazmat"] else "No",
        data["driver_id"],  # Replace with a query to fetch driver name
        data["vehicle_id"]  # Replace with a query to fetch vehicle plate
    ])

    # Style headers
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Add chart (example: Hazmat incidents)
    chart = BarChart()
    chart.title = "Hazmat Incidents"
    chart.x_axis.title = "Reference Key"
    chart.y_axis.title = "Count"
    data = Reference(ws, min_col=5, min_row=1, max_row=ws.max_row, max_col=5)
    chart.add_data(data, titles_from_data=True)
    ws.add_chart(chart, "H10")

    wb.save(filename)
    print(f"Excel report saved as {filename}.")

# ---- EXPORT TO PDF ----#

from fpdf import FPDF

def export_to_pdf(data, filename="Accident_Report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Accident Report", ln=True, align="C")

    # Report Details
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.output(filename)
    print(f"PDF report saved as {filename}.")

# ---- ---- # 

def save_to_json(data, filename="accident_report.json"):
    def custom_serializer(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()  # Convert date/datetime to ISO 8601 string
        elif isinstance(obj, set):
            return list(obj)  # Convert sets to lists
        raise TypeError(f"Type {type(obj)} not serializable")

    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4, default=custom_serializer)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")
