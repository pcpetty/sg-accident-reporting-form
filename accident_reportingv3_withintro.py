# Import Libraries and Modules
import datetime
import inquirer
import json
import PyQt6


# Date input function
def get_date():
    while True:
        date_str = input("Enter date (mm/dd/yyyy): ")
        try:
            return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
        except ValueError:
            print("Invalid date format. Please try again.")

# Time input function
def get_time():
    while True:
        time_str = input("Enter accident time (HH:MM): ")
        try:
            return datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print("Invalid time format. Please try again.")

# Yes/No input function
def get_yes_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

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
    origin = input("Enter load origin: ")
    destination = input("Enter load destination: ")
    return {
        "manifest_number": manifest_number,
        "origin": origin,
        "destination": destination,
    }
    
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

# Co-Driver Information
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

# Collect Accident Data
def collect_accident_data():
    accident_data = {}
    
    # Basic Accident Info
    accident_data["accident_date"] = get_date()
    accident_data["accident_time"] = get_time()
    accident_data["accident_location"] = input("Enter accident location or address: ")
    accident_data["hazmat"] = get_yes_no("Hazmat? (y/n): ")
    accident_data["V1 Driver"] = get_v1_driver()
    accident_data["V1 Co-Driver"] = get_v1_codriver()
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
        accident_data["tow_company_phone"] = input("Enter tow company phone number: ").strip()
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

    return accident_data

# Main Function
def main():
    print("Safety Generalist Accident Report Form")
    
    # Reporting SOP Tutorial
    if get_yes_no("Would you like an accident reporting SOP tutorial? (y/n): "):
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
    
    # Collect and display accident data
    accident_data = collect_accident_data()
    print("\nCollected Accident Data:")
    for key, value in accident_data.items():
        print(f"{key}: {value}")
        # print("\nCollected Accident Data:")
        # print(json.dumps(accident_data, indent=4))


# Run the Program
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