# Import Libraries and Modules
import datetime
import inquirer
import json
import PyQt6
import re
import json

# ----- SQL DB Integration ----- # 
import psycopg2
from psycopg2.extras import Json

# Connect to PostgreSQL
def connect_postgresql():
    try:
        conn = psycopg2.connect(
            dbname="accident_reports_db",
            user="safety_generalist",
            password="SierraDecember1997@",
            host="localhost",  # Adjust if using a remote database
            port="5432"        # Default PostgreSQL port
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Insert Report into PostgreSQL
def insert_into_postgresql(data):
    def custom_serializer(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    conn = connect_postgresql()
    if conn is None:
        print("Failed to connect to PostgreSQL. Data not saved.")
        return

    try:
        with conn.cursor() as cursor:
            # Ensure data is JSON-serializable
            json_data = json.dumps(data, default=custom_serializer)

            # Insert into the database
            cursor.execute(
                """
                INSERT INTO accident_reports (reference_key, report_data)
                VALUES (%s, %s)
                """,
                (data["reference_key"], Json(json.loads(json_data)))
            )
        conn.commit()
        print("Data successfully saved to PostgreSQL.")
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
    finally:
        conn.close()


# ---- File Management ---- # 

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
        
# ---- CLEAN UP SQL FORMAT ---- #
def clean_field(value, default="Not Provided"):
    return value if value else default


# ---- FLT---- #

def get_next_flt_number():
    conn = connect_postgresql()
    if conn is None:
        print("Failed to connect to PostgreSQL for FLT number generation.")
        return None

    try:
        with conn.cursor() as cursor:
            # Retrieve the last number
            cursor.execute("SELECT last_number FROM flt_sequence LIMIT 1;")
            last_number = cursor.fetchone()[0]

            # Increment the number
            next_number = last_number + 1

            # Update the sequence table
            cursor.execute("UPDATE flt_sequence SET last_number = %s;", (next_number,))

            # Commit the change
            conn.commit()

            # Format the number as FLT########
            return f"FLT{next_number:07d}"
    except psycopg2.errors.InsufficientPrivilege as e:
        print(f"Permission error: {e}")
        print("Ensure the user has SELECT and UPDATE privileges on the flt_sequence table.")
        return None
    except Exception as e:
        print(f"Error generating FLT number: {e}")
        return None
    finally:
        conn.close()

# ---- EDIT REPORT FUNCTIONS ---- # 

# Load a report by FLT number
def load_report(flt_number, filename="accident_report.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)

        # Find the report by FLT number
        for report in data:
            if report.get("reference_key") == flt_number:
                return report
        print(f"No report found with reference number: {flt_number}")
        return None
    except FileNotFoundError:
        print("No existing reports found.")
        return None

# Edit a specific field in the report
def edit_report_field(report):
    print("\nEditing Report:")
    for key, value in report.items():
        print(f"{key}: {value}")
        new_value = input_with_default(f"Enter new value for {key} or press Enter to keep the current value", value)
        if new_value != value:
            report[key] = new_value
    return report

# ---- SOP TUTORIAL ---- # 
def display_sop_tutorial():
    print("\nAccident Reporting SOP Tutorial:")
    steps = [
        "First determine if anyone is injured.",
        "Ask for the basic vehicle information before taking a statement from the driver.",
        "Once a statement is obtained, determine if this is an accident or an incident.",
        "Ask for pictures of all vehicles involved from all four sides from a wide angle.",
        "Obtain other motorists' contact and insurance information.",
        "If police are involved, determine if a citation has been issued.",
        "If a citation has been issued, proceed with the post-accident testing SOP.",
        "If any injuries are sustained, determine if EMS will transport anyone from the scene. If so, where are they being transported?",
        "If a tow is required, determine if the vehicle is disabled. If it is being towed, obtain the tow company information.",
    ]
    for i, step in enumerate(steps, start=1):
        print(f"{i}. {step}")
        if not get_yes_no("Do you want to continue the tutorial? (y/n)", "yes"):
            print("\nTutorial skipped.")
            return
    print("\nTutorial Complete.")

# ----- Regex Functions ----- # 

# Regex validation for phone numbers
def validate_phone(prompt):
    while True:
        phone = input(prompt).strip()
        if re.match(r'^\+?1?\d{10,15}$', phone):  # Allows international format or 10-15 digits
            return phone
        print("Invalid phone number. Please enter a valid phone number (e.g., 1234567890 or +11234567890).")

# Regex validation for license plate
def validate_license_plate(prompt):
    while True:
        plate = input(prompt).strip()
        if re.match(r'^[A-Z0-9]{1,8}$', plate):  # Allows up to 8 alphanumeric characters
            return plate
        print("Invalid license plate. Please enter a valid license plate (e.g., ABC1234).")

# Regex validation for date (MM/DD/YYYY)
def validate_date(prompt):
    while True:
        date_str = input(prompt).strip()
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            try:
                return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                pass
        print("Invalid date format. Please use MM/DD/YYYY.")

# Regex validation for email
def validate_email(prompt):
    while True:
        email = input(prompt).strip()
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):  # Basic email validation
            return email
        print("Invalid email address. Please enter a valid email address.")

# ------ Begin Accident Info Collection ------ # 

# Determine Company Details
def get_company_info():
    is_faf = get_yes_no("Is this an FAF (Forward Air) accident? (y/n): ")
    if is_faf:
        faf_branch = get_condition("FAF Branch", ['FAF', 'TQL', 'PLC', 'OMNI'])
        return {"is_faf": True, "faf_branch": faf_branch}
    else:
        return {"is_faf": False, "carrier": input("Enter brokered third-party carrier name: ").strip()}

# Date input function with default pass
def get_date(prompt):
    while True:
        date_str = input(f"{prompt} (Press Enter to skip): ").strip()
        if not date_str:  # Allow skipping
            return None
        try:
            return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY or press Enter to skip.")

# Time input function with default pass
def get_time():
    while True:
        time_str = input("Enter time (HH:MM) or press Enter to skip: ").strip()
        if not time_str:  # Allow skipping
            return None
        try:
            return datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print("Invalid time format. Please use HH:MM or press Enter to skip.")

# Input with Default
def input_with_default(prompt, default):
    response = input(f"{prompt} (Press Enter to default to '{default}'): ").strip()
    return response if response else default

# Yes/No Input with Default
def get_yes_no(prompt, default="no"):
    while True:
        response = input_with_default(prompt, default).lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n', or press Enter to skip.")

# Reusable function for selecting conditions
def get_condition(condition_type, choices):
    try:
        questions = [
            inquirer.List(
                condition_type,
                message=f"Choose {condition_type.replace('_', ' ')}:",
                choices=choices + ['Custom'],
            ),
        ]
        answers = inquirer.prompt(questions)
        if answers[condition_type] == "Custom":
            return input(f"Enter custom {condition_type.replace('_', ' ')}: ").strip()
        return answers[condition_type]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Truck Information
def get_truck():
    truck_number = input("Enter truck number: ")
    truck_type = get_condition("truck_type", ['Tractor Trailer', 'Straight Truck', 'Van'])
    truck_cameras = get_yes_no("Does the truck have cameras? (y/n): ")
    return {
        "truck_number": truck_number,
        "truck_type": truck_type,
        "truck_cameras": truck_cameras,
    }

# Trailer Information
def get_trailer():
    trailer_connected = get_yes_no("Is a trailer connected? (y/n): ")
    if trailer_connected:
        trailer_type = get_condition("trailer_type", ['Dry Van', 'Refrigerated', 'Bobtail/None', 'Straight Truck'])
        trailer_number = input("Enter trailer number: ")
        return {
            "trailer_connected": trailer_connected,
            "trailer_type": trailer_type,
            "trailer_number": trailer_number,
        }
    return {"trailer_connected": False}

# Load Information
def load_information():
    manifest_number = input("Enter manifest number: ")
    if manifest_number:
        origin = input("Enter load origin: ")
        destination = input("Enter load destination: ")
        return {
            "manifest_number": manifest_number,
            "origin": origin,
            "destination": destination,
        }
    return {"manifest_number: False"}

# V1 Driver Information
def get_v1_driver():
    driver_name = input("Enter V1 driver name: ").strip()
    driver_phone = input("Enter V1 driver phone number: ").strip()
    driver_injury = get_yes_no(f"Is {driver_name} injured? (y/n): ")
    return {
        "driver_name": driver_name,
        "driver_phone": driver_phone,
        "driver_injury": driver_injury,
    }

# # Co-Driver Information
def get_v1_codriver():
    codriver_present = get_yes_no("Does V1 have a co-driver? (y/n): ")
    if codriver_present:
        codriver_name = input("Enter co-driver name: ").strip()
        codriver_phone = input("Enter co-driver phone number: ").strip()
        codriver_injury = get_yes_no(f"Is {codriver_name} injured? (y/n): ")
        return {
            "codriver_name": codriver_name,
            "codriver_phone": codriver_phone,
            "codriver_injury": codriver_injury,
        }
    return {
        "codriver_present": False
    }
    
# V2 Driver Information
def get_v2_driver():
    v2_name = input("Enter V2 driver name: ").strip()
    v2_phone = input("Enter V2 phone number: ").strip()
    driver_license = input("Enter V2 driver license number: ").strip()
    license_state = input("Enter issuing state for driver license: ").strip()
    license_expiry = input("Enter driver license expiry date (mm/dd/yyyy): ")
    insurance_company = input("Enter V2 insurance company name: ").strip()
    insurance_policy = input("Enter V2 insurance policy number: ").strip()
    v2_injuries = get_yes_no("Is the driver or passenger(s) reporting injury? (y/n): ")
    if v2_injuries:
        injury_description = input("Describe V2 driver or passenger injury: ").strip()
    else:
        injury_description = None

    return {
        "v2_name": v2_name,
        "v2_phone": v2_phone,
        "driver_license": driver_license,
        "license_state": license_state,
        "license_expiry": license_expiry,
        "insurance_company": insurance_company,
        "insurance_policy": insurance_policy,
        "v2_injuries": v2_injuries,
        "injury_description": injury_description,
    }
    
# Get V2 Passenger Information
def get_v2_passengers():
    has_passengers = get_yes_no("Does V2 have passengers? (y/n)", "no")
    passengers = []
    if has_passengers:
        num_passengers = input_with_default("How many passengers are there?", "0")
        try:
            num_passengers = int(num_passengers)
        except ValueError:
            num_passengers = 0
        for i in range(num_passengers):
            print(f"Passenger {i + 1}:")
            passenger_name = input_with_default("Enter passenger name", "N/A")
            passenger_injury = get_yes_no(f"Is {passenger_name} injured? (y/n)", "no")
            passengers.append({"name": passenger_name, "injured": passenger_injury})
    return {"has_passengers": has_passengers, "passengers": passengers}

# V2 Vehicle Information
def get_v2_vehicle():
    v2_plate_number = input("Enter V2 license plate number: ").strip()
    v2_plate_state = input("Enter V2 license plate issuing state: ").strip()
    v2_make = input("Enter V2 vehicle make (e.g., Toyota, Ford): ").strip()
    v2_model = input("Enter V2 vehicle model (e.g., Camry, F-150): ").strip()
    v2_year = input("Enter V2 vehicle year: ").strip()
    v2_color = input("Enter V2 vehicle color: ").strip()
    v2_damage_description = input("Describe damage to V2 vehicle: ").strip()
    v2_tow_required = get_yes_no("Does V2 require towing? (y/n): ")
    if v2_tow_required:
        v2_tow_company = input("Enter towing company name: ").strip()
        v2_tow_phone = input("Enter towing company phone number: ").strip()
    else:
        v2_tow_company = None
        v2_tow_phone = None

    return {
        "v2_plate_number": v2_plate_number,
        "v2_plate_state": v2_plate_state,
        "v2_make": v2_make,
        "v2_model": v2_model,
        "v2_year": v2_year,
        "v2_color": v2_color,
        "v2_damage_description": v2_damage_description,
        "v2_tow_required": v2_tow_required,
        "v2_tow_company": v2_tow_company,
        "v2_tow_phone": v2_tow_phone,
    }

# Additional Remarks Section
def get_additional_remarks():
    remarks = input("Enter any additional remarks or observations (Press Enter to skip): ").strip()
    return remarks if remarks else "No additional remarks provided."

# Collect Accident Data
def collect_accident_data():
    accident_data = {}

    # Company Information
    accident_data["company_info"] = get_company_info()
    # Basic Accident Info
    accident_data["accident_date"] = get_date("Enter accident date (MM/DD/YYYY): ")
    accident_data["accident_time"] = get_time()  # Existing time validation
    accident_data["accident_location"] = input("Enter accident location or address: ").strip()
    accident_data["hazmat"] = get_yes_no("Hazmat? (y/n): ")
    accident_data["v1_driver"] = get_v1_driver()
    accident_data["v1_codriver"] = get_v1_codriver()
    accident_data["v2_driver"] = get_v2_driver()
    accident_data["v2_vehicle"] = get_v2_vehicle()

    # V2 Passenger Information
    accident_data["v2_passengers"] = get_v2_passengers()

    # Weather and Road Conditions
    accident_data["weather_info"] = get_condition("weather_conditions", ['Clear', 'Overcast', 'Sunny', 'Rainy', 'Windy', 'Stormy'])
    accident_data["road_conditions"] = get_condition("road_conditions", ['Wet', 'Dry', 'Snowy', 'Icy'])

    # Police Information
    accident_data["police_involvement"] = get_yes_no("Police involved? (y/n): ")
    if accident_data["police_involvement"]:
        accident_data["police_department"] = input("Enter name of police department: ").strip()
        accident_data["police_officer"] = input("Enter name of officer: ").strip()
        accident_data["police_badge"] = input("Enter badge number or None: ").strip()
        accident_data["police_report"] = input("Enter police report number or case number: ").strip()
    else:
        accident_data["police_department"] = None
        accident_data["police_officer"] = None
        accident_data["police_badge"] = None
        accident_data["police_report"] = None

    # Tow Company Information
    accident_data["tow_required"] = get_yes_no("Is a tow service required? (y/n): ")
    if accident_data["tow_required"]:
        accident_data["tow_disabling"] = get_yes_no("Is one or more vehicles considered disabled? (y/n): ")
        accident_data["tow_company_name"] = input("Enter tow company name: ").strip()
        accident_data["tow_company_phone"] = validate_phone("Enter tow company phone number: ")
        accident_data["tow_company_address"] = input("Enter tow company yard address: ").strip()
    else:
        accident_data["tow_disabling"] = None
        accident_data["tow_company_name"] = None
        accident_data["tow_company_phone"] = None
        accident_data["tow_company_address"] = None

    # Truck and Trailer Information
    accident_data["truck_info"] = get_truck()
    accident_data["trailer_info"] = get_trailer()

    # Load Information
    accident_data["load_info"] = load_information()
    accident_data["additional_remarks"] = get_additional_remarks()

    return accident_data

def main():
    try:
        print("Safety Generalist Accident Report Form")

        while True:  # Main menu loop
            print("\nOptions:")
            print("1. Create a new report")
            print("2. Edit an existing report")
            print("3. Exit")

            choice = input_with_default("Choose an option (1/2/3)", "3")

            if choice == "1":
                # Optional SOP Tutorial
                if get_yes_no("Would you like an accident reporting SOP tutorial? (y/n)", "no"):
                    display_sop_tutorial()

                # Collect new accident data
                accident_data = collect_accident_data()

                # Retry mechanism for FLT number generation and submission
                while True:
                    reference_key = get_next_flt_number()
                    if reference_key:
                        accident_data["reference_key"] = reference_key

                        # Save data
                        save_to_json(accident_data)
                        insert_into_postgresql(accident_data)

                        print("\nForm Submitted Successfully!")
                        print(f"Your reference number is: {reference_key}")
                        print("Please save this number for future reference.")
                        break  # Exit retry loop
                    else:
                        print("\nError: Unable to generate a reference number. Form not submitted.")
                        retry = get_yes_no("Would you like to retry submitting the form? (y/n)", "yes")
                        if not retry:
                            print("\nSubmission failed. Returning to the main menu.")
                            break

            elif choice == "2":
                # Edit existing report
                flt_number = input("Enter the FLT number of the report to edit: ").strip()
                report = load_report(flt_number)
                if report:
                    updated_report = edit_report_field(report)
                    save_to_json(updated_report)
                    insert_into_postgresql(updated_report)
                    print("\nReport updated successfully.")
                else:
                    print("\nReport not found. Returning to the main menu.")

            elif choice == "3":
                print("\nThank you for using the Safety Generalist Accident Report Form. Goodbye!")
                break  # Exit the program

            else:
                print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting gracefully. Goodbye!")

if __name__ == "__main__":
    main()
#-------------------------------------------------------------------------------------
# -- SG Accident Reporting Overhaul --
# Needs:
# - Fully functioning input program
# -- All standard accident into collected and formatted
# - Ability to upload photos and documents
# - Expand to collect V2 info and insurance information
# --- Expand into PyQt6 for graphical user interface
# - Convert stored info from GUI into database (SQL, Excel) for analysis and visualization
# - Ability to edit entered information for corrections. Bug testing for repeated mistakes.
# - With thought to queries and sorting, ability to connect with driver and asset database to pull records and make profile history
# Wants:
# - Accident Reporting Tutorial for new Safety Generalists
# -- Fully equipped to advise on post accident drug testing, making trucks or drivers unavailable, dot-recordable or not
# -- Provides my mastered script and procedure, to prevent overwhelming new S.G. ... 
# -- Define full tutorial function acting as documentation for the job as a whole. Ability to select SOP sections
# - Ability to mass email initial report to email group.
# - Make the a program that would beat the John Henry of Safety Generalists. Bulletproof. Safety Director approved.
# ----------------------------------------------------------------------------------

# Revert Dates When Loading JSON
# If I  need to load this JSON and revert the strings back to date objects, use this:
# def load_from_json(filename):
#     with open(filename, "r") as file:
#         data = json.load(file)

#     # Convert date strings back to `datetime.date`
#     for key, value in data.items():
#         if isinstance(value, str) and value.count("-") == 2:  # Check for ISO format
#             try:
#                 data[key] = datetime.date.fromisoformat(value)
#             except ValueError:
#                 pass

#     return data
