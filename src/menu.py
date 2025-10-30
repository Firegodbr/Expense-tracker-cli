import os
import datetime
from .expense import ExpenseTracker

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("Welcome to the Expense Tracker CLI!")
    
    # Prompt the user for the file name and initialize the ExpenseTracker
    while True:
        file_path = input("Enter the name of the file for expenses (leave blank for 'expense.txt'): ").strip()
        if not file_path:
            file_path = "expense.txt"
        try:
            obj_expense = ExpenseTracker(file_path)
            break  # If no error, break the loop
        except Exception as e:
            print(f"Error initializing Expense Tracker: {e}. Please try again.")
    
    while True:
        # Display the menu options
        print("\nOptions available:")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. Remove an expense")
        print("4. Update an expense")
        print("5. Clear all expenses")
        print("6. Search expenses")
        print("7. Exit\n")
        
        try:
            action = input("Please select an option (1-7): ").strip()
            # clear_console()  # Clear console after user selection
            
            if action == "1":
                # Add an expense with category and amount
                category = input("Enter the expense category (e.g., 'Food', 'Transport'): ").strip()
                amount = float(input("Enter the expense amount (e.g., 25.50): ").strip())
                description = input("Enter a brief description of the expense: ").strip()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                expense = f"{timestamp}\t{category}\t${amount:.2f}\t{description}"
                obj_expense.add_expense(expense)
                # Print confirmation after adding the expense
                print(f"Expense added: {timestamp} - {category} - ${amount:.2f} - {description}")
            
            elif action == "2":
                # View all expenses
                expenses = obj_expense.get_expenses()
                if expenses:
                    print("\nExpenses:")
                    for idx, expense in enumerate(expenses, 1):
                        print(f"{idx}. {expense.strip()}")
                else:
                    print("No expenses found.")
            
            elif action == "3":
                # Remove an expense
                line_number = int(input("Enter the line number of the expense to remove: "))
                if obj_expense.remove_expense(line_number):
                    print(f"Expense at line {line_number} removed.")
                else:
                    print("Invalid line number.")
            
            elif action == "4":
                # Update an expense
                line_number = int(input("Enter the line number of the expense to update: "))
                if obj_expense.find_expense(line_number):  # To check if line exists
                    print(f"Current expense: {obj_expense.find_expense(line_number)}")
                    print("Enter new details for the expense:")
                    category = input("Enter the expense category (e.g., 'Food', 'Transport'): ").strip()
                    amount = float(input("Enter the expense amount (e.g., 25.50): ").strip())
                    description = input("Enter a brief description of the expense: ").strip()
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_value = f"{timestamp}\t{category}\t${amount:.2f}\t{description}"
                    if obj_expense.update_expense(line_number, new_value):
                        print(f"Expense at line {line_number} updated to: {new_value}")
                else:
                    print("Invalid line number.")
            
            elif action == "5":
                # Clear all expenses
                obj_expense.clear_expenses()
                print("All expenses cleared.")
            
            elif action == "6":
                # Search expenses by category, amount or description
                search_term = input("Enter a keyword to search for (category, description, or amount): ").strip().lower()
                expenses = obj_expense.get_expenses()
                results = [expense for expense in expenses if search_term in expense.lower()]
                
                if results:
                    print("\nSearch Results:")
                    for idx, result in enumerate(results, 1):
                        print(f"{idx}. {result.strip()}")
                else:
                    print("No matching expenses found.")
            
            elif action == "7":
                # Exit the program
                print("Exiting the Expense Tracker. Goodbye!")
                break  # Exit the loop and end the program
            
            else:
                print("Invalid option, please select between 1 and 7.")
        
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
