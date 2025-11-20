import re
import keyword
import sys
import os

RESERVED_KEYWORDS = set(keyword.kwlist)

PYTHON_VAR_REGEX = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

def validate_manual(var_name):
    if var_name in RESERVED_KEYWORDS:
        return False, f"FAILED: '{var_name}' is a reserved Python keyword."
    if var_name and var_name[0].isdigit():
        return False, f"FAILED: '{var_name}' cannot start with a digit."
    for char in var_name:
        if not (char.isalnum() or char == '_'):
            return False, f"FAILED: '{var_name}' contains an invalid character: '{char}'."
    return True, f"PASSED: '{var_name}' appears valid based on manual rules."

def validate_regex(var_name):
    if var_name in RESERVED_KEYWORDS:
        return False, f"FAILED: '{var_name}' is a reserved Python keyword."
    if re.match(PYTHON_VAR_REGEX, var_name):
        return True, f"PASSED: '{var_name}' matches the Python variable regex pattern."
    else:
        if not var_name:
            reason = "Variable name is empty."
        elif var_name[0].isdigit():
            reason = "Cannot start with a digit."
        else:
            reason = "Contains invalid characters or structure."
        return False, f"FAILED: '{var_name}' does not match the regex pattern. Reason: {reason}"

def validate_hands_on(var_name):
    temp_file_name = f"test_var_name.py"
    
    test_code = f"# Test file for variable name: {var_name}\n\n{var_name} = 10\nprint('Test variable assignment was successful!')"
    
    try:
        with open(temp_file_name, 'w') as f:
            f.write(test_code)
        print(f"ACTION: Wrote test code to '{temp_file_name}' in the current directory.")
        print(f"File Content:\n---\n{test_code}\n---")
    except Exception as e:
        print(f"ERROR: Could not create file. {e}")
        return False, "File creation failed."

    print(f"ACTION: Executing file with: {sys.executable} {temp_file_name}")
    exit_code = os.system(f"{sys.executable} {temp_file_name}")

    if exit_code == 0:
        result = (True, f"HANDS-ON RESULT: GOOD. '{var_name}' executed successfully (Exit Code: {exit_code}).")
    else:
        result = (False, f"HANDS-ON RESULT: BAD. '{var_name}' failed to execute (Exit Code: {exit_code}). Check console output for error.")

    print("\n-----------------------------------")
    print(result[1])
    print("\n-----------------------------------")
    
    delete_choice = input(f"QUESTION: The test is complete. Should we delete the test file '{temp_file_name}'? (Y/N): ").strip().upper()
    
    if delete_choice == 'Y':
        try:
            os.remove(temp_file_name)
            print(f"ACTION: Successfully deleted '{temp_file_name}'. Workspace clean.")
        except Exception as e:
            print(f"ERROR: Could not delete file. {e}")
    else:
        print(f"ACTION: File '{temp_file_name}' remains. Remember to clean up your workspace.")
        
    return result

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n========================================")
        print("PYTHON VARIABLE VALIDATOR MENU")
        print("========================================")
        print("1. Simple Manual Check")
        print("2. Complex Regex Check")
        print("3. Hands-On Syntax Test (Requires real file I/O & Execution)")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '4':
            print("Exiting validator. Goodbye!")
            break

        if choice in ('1', '2', '3'):
            var_name = input("Enter the variable name to test: ").strip()
            if not var_name:
                print("Input cannot be empty. Please try again.")
                input("Press Enter to continue...")
                continue
            
            result = (False, "Invalid choice.")
            
            if choice == '1':
                result = validate_manual(var_name)
                print(f"\n--- Manual Check Result ---")
                print(result[1])
            elif choice == '2':
                result = validate_regex(var_name)
                print(f"\n--- Regex Check Result ---")
                print(result[1])
            elif choice == '3':
                validate_hands_on(var_name)
                
            if choice != '3':
                input("\nPress Enter to continue...")
                
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
            input("Press Enter to continue...")