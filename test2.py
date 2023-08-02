def get_user_input():
    while True:
        user_input = input("Enter a number: ")
        if user_input.isdigit():
            number = int(user_input)
            return number
        else:
            error_message = f"Invalid input: '{user_input}'. Please enter a valid number."
            return error_message

# Example usage
result = get_user_input()
print(result)