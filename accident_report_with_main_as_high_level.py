def collect_accident_data():
    # Basic Accident Info
    accident_date = get_date()
    accident_time = get_time()
    accident_location = input("Enter accident location or address: ").strip()
    hazmat = get_yes_no("Hazmat? (y/n): ")

    # Fuel Spill
    fuel_spill = get_yes_no("Has the accident or incident resulted in a fuel spill? (y/n): ")
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

    # Collect Weather and Road Conditions
    weather_info = get_condition("weather_conditions", ['clear', 'overcast', 'sunny', 'rainy', 'windy', 'stormy'])
    road_conditions = get_condition("road_conditions", ['wet', 'dry', 'snowy', 'icy'])

    # Update Accident Data
    accident_data = {
        "accident_date": accident_date,
        "accident_time": accident_time,
        "accident_location": accident_location,
        "hazmat": hazmat,
        "fuel_spill": fuel_spill,
        "police_involvement": police_involvement,
        "police_department": police_department,
        "police_officer": police_officer,
        "police_badge": police_badge,
        "police_report": police_report,
        "tow_required": tow_required,
        "tow_disabling": tow_disabling,
        "tow_company_name": tow_company_name,
        "tow_company_phone": tow_company_phone,
        "tow_company_address": tow_company_address,
        "fire_department": fire_department,
        "weather_info": weather_info,
        "road_conditions": road_conditions,
    }

    print("\nInitial Contact Form Data:")
    for key, value in accident_data.items():
        print(f"{key}: {value}")