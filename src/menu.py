from .expense import ExpenseTracker

def display_menu():
    print("Welcome to the Expense tracker:")
    file_path = input("What is the name of the file for expenses? ")
    
    obj_expense = ExpenseTracker(file_path.strip())
    while True:
        action = input("Do you wanna add expenses? ")
        if "n" in action.lower():
            break
        else:
            expense = input("What do you wanna add to it?")
            obj_expense.add_expense(expense)