# length constraint
def get_limited_input(prompt, max_length):
    while True:
        user_input = input(prompt)
        if len(user_input) <= max_length:
            return user_input
        else:
            print(f"Input must be {max_length} characters or fewer. Try again.")

# Example
name = get_limited_input("Enter your name (max 10 characters): ", max_length=10)
print(f"Name entered: {name}")

# numeric restraint
def get_numeric_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():  # Check if input is numeric
            return int(user_input)
        else:
            print("Invalid input. Please enter a number.")

# Example
age = get_numeric_input("Enter your age: ")
print(f"Age entered: {age}")
