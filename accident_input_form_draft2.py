def main():
    print("Safety Generalist Accident Report Form")
    
    # Ask if user wants the SOP tutorial
    accident_reporting_procedure = get_yes_no("Would you like an accident reporting SOP tutorial? (y/n): ")
    
    if accident_reporting_procedure:
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
            if not get_yes_no("Do you want to continue the tutorial? (y/n): "):
                print("\nTutorial skipped. Proceeding to the form...")
                break
        else:
            print("\nTutorial Complete. Proceeding to the form...")
    else:
        print("\nSkipping SOP tutorial. Proceeding to the form...")
    
#     # Proceed to collect accident data
# def collect_accident_data():
#     # Basic Accident Info
#     accident_date = get_date()
#     accident_time = get_time()
#     accident_location = input("Enter accident location or address: ").strip()
#     hazmat = get_yes_no("Hazmat? (y/n): ")
#     collect_accident_data()


# ------------------------------------------------------------------------
# Import Libraries and Modules
import datetime
import inquirer
# ------------------------------------------------------------------------
# Create an empty dictionary to store the form data
accident_data = {}
# ------------------------------------------------------------------------

# Date input function
def get_date():
    while True:
        date_str = input("Enter date (mm/dd/yyyy): ")
        try:
            date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
            return date
        except ValueError:
            print("Invalid date format. Please try again.")

# Time input function
def get_time():
    while True:
        time_str = input("Enter accident time (HH:MM): ")
        try:
            time = datetime.datetime.strptime(time_str, "%H:%M").time()
            return time_str
        except ValueError:
            print("Invalid time format. Please try again.")

# Yes/No input function for better validation
def get_yes_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

# ------------------------------------------------------------------------
# Collect User Input
# ------------------------------------------------------------------------

# Basic Accident Info
accident_date = get_date()
accident_time = get_time()
accident_location = input("Enter accident location or address: ").strip()
hazmat = get_yes_no("Hazmat? (y/n): ")

# Fuel Spill
fuel_spill = get_yes_no("Has the accident or incident resulted in a fuel spill? (y/n)")
if fuel_spill:
    print("Reminder to call claims adjuster on call to report fuel spill for environmental cleanup")
else:
    fuel_spill = None

# Police Involvement
police_involvement = get_yes_no("Police involved? (y/n): ")
if police_involvement:
    police_department = input("Enter name of police department: ").strip()
    police_officer = input("Enter name of officer: ").strip()
    police_badge = input("Enter badge number or None: ").strip()
    police_report = input("Enter police report number or case number: ").strip()
else:
    police_department = police_officer = police_badge = police_report = None

# Tow Company Involvement
tow_required = get_yes_no("Is a tow service required? (y/n): ")
if tow_required:
    tow_disabling = get_yes_no("Is one or more vehicles considered disabled? (y/n): ")
    tow_company_name = input("Enter tow company name: ").strip()
    tow_company_phone = input("Enter tow company phone number: ").strip()
    tow_company_address = input("Enter tow company yard address: ").strip()
else:
    tow_disabling = tow_company_name = tow_company_phone = tow_company_address = None

# Fire Department
fire_department = get_yes_no("Is fire department on the scene? (y/n): ")

# Situational Factors
safe_location = get_yes_no("Is vehicle stopped in a safe location? (y/n): )")

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
        
        # Handle the custom input
        if answers[condition_type] == "Custom":
            custom_condition = input(f"Enter custom {condition_type.replace('_', ' ')}: ").strip()
            return custom_condition
        else:
            return answers[condition_type]
    except Exception as e:
        print(f"An error occurred while selecting {condition_type}: {e}")
        return None
    
# V1 Driver Info + Co-Driver (y/n)
def v1_driver(v1_driver_name, v1_driver_phone, v1_driver_injury):
    v1_driver_name = input("Enter V1 name: ")
    v1_driver_phone = input("V1 driver phone number: ")
    v1_driver_injury = get_yes_no(f"Is {v1_driver_name} injured? (y/n): ")
    return {
        "v1_driver_name": v1_driver_name,
        "v1_driver_phone": v1_driver_phone,
        "v1_driver_injury": v1_driver_injury
    }
    
def v1_codriver(v1_codriver_status, v1_codriver_name, v1_codriver_phone, v1_codriver_injury):
    v1_codriver_status = get_yes_no(f"Does V1 have a co-driver? (y/n): ")
    if v1_codriver:
            v1_codriver_name = input("Enter co-driver name: ")
            v1_codriver_phone = input("Enter co-driver phone number: "),
            v1_codriver_injury = get_yes_no(f"Is {v1_codriver} injured? (y/n): ")
            return {
                "v1_codriver_name": v1_codriver_name,
                "v1_codriver_phone": v1_codriver_phone,
                "v1_codriver_injury": v1_codriver_injury,
            }
            
    return {"v1_codriver": False}


# def v2_info(v2_name, v2_phone, v2_type, v2_tow, v2_passengers, v2_injuries, v2_citation):
#     v2_name = input("Enter V2 name: ")
# V2 Driver and Vehicle Info
# Injuries, passengers, tow (y/n)

# ------------------------------------------------------------------------
# Get Weather Conditions
weather_info = get_condition("weather_conditions", ['clear', 'overcast', 'sunny', 'rainy', 'windy', 'stormy'])
print(f"Weather condition selected: {weather_info}")

# Get Road Conditions
road_conditions = get_condition("road_conditions", ['wet', 'dry', 'snowy', 'icy'])
print(f"Road condition selected: {road_conditions}")


#-------------------------------------------------------------------------
# Truck Information
def get_truck(truck_number, truck_type, truck_categories, truck_cameras):
    truck_number = input(f"Enter truck number: ")
    truck_categories = get_condition("truck_type", ['tractor_trailer', 'straight_truck', 'van'])
    truck_type = input(f"Select truck type: {truck_categories} ")
    truck_cameras = get_yes_no(f"Does the truck have cameras? (y/n): ")    
    return {
        "truck_number": truck_number,
        "truck_type": truck_type,
        "truck_cameras": truck_cameras,
    }

def get_trailer():
    trailer_connected = get_yes_no("Is a trailer connected? (y/n): ")
    if trailer_connected:
        trailer_type = get_condition("trailer_type", ['Dry Van', 'Refrigerated', 'Bobtail/None', 'Straight Truck'])
        trailer_number = input("Enter trailer number: ").strip()
        return {
            "trailer_connected": trailer_connected,
            "trailer_type": trailer_type,
            "trailer_number": trailer_number,
        }
    return {"trailer_connected": False}
    
# Load Information
def load_information(manifest_number, origin, destination):
    manifest_number = input(f"Enter manifest number: ")
    origin = input(f"Enter load origin: ")
    destination = input(f"Enter load destination: ")
    return {
        "manifest_number": manifest_number,
        "origin": origin,
        "destination": destination,
    }
    

# ------------------------------------------------------------------------
# Store Data in Dictionary
# ------------------------------------------------------------------------
# Accident Basic Info
accident_data["accident_date"] = accident_date
accident_data["accident_time"] = accident_time
accident_data["accident_location"] = accident_location
accident_data["hazmat"] = hazmat
accident_data["weather_info"] = weather_info
accident_data["road_conditions"] = road_conditions


# Police Info
accident_data["police_involvement"] = police_involvement
accident_data["police_department"] = police_department
accident_data["police_officer"] = police_officer
accident_data["police_badge"] = police_badge
accident_data["police_report"] = police_report

# Tow Company Info
accident_data["tow_required"] = tow_required
accident_data["tow_disabling"] = tow_disabling
accident_data["tow_company_name"] = tow_company_name
accident_data["tow_company_phone"] = tow_company_phone
accident_data["tow_company_address"] = tow_company_address

# Fire Department
accident_data["fire_department"] = fire_department

# Truck and Trailer Info 
accident_data["truck_info"] = get_truck()
accident_data["truck_info"] = get_trailer()

# Load information
accident_data["load_info"] = load_information()


# ------------------------------------------------------------------------
# Print the Form Data
print("\nInitial Contact Form Data:")
for key, value in accident_data.items():
    print(f"{key}: {value}")
