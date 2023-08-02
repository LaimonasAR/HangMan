def get_user_input():
    valid_input = False
    error_message = ""
    while not valid_input:
        user_input = input("Enter a number: ")
        if user_input.isdigit():
            number = int(user_input)
            valid_input = True
        else:
            error_message = f"Invalid input: '{user_input}'. Please enter a valid number."

    if valid_input:
        return number
    else:
        return error_message

# Example usage
result = get_user_input()
print(result)