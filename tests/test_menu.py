import pytest
from unittest import mock
import io
from src.expense import ExpenseTracker
from src.menu import display_menu  # Assuming your display_menu is in cli.py
import os

@pytest.fixture
def expense_tracker():
    return ExpenseTracker(file_path="test_expenses.txt")

@pytest.fixture
def clear_expenses(expense_tracker: ExpenseTracker):
    """Start with a clean expense file before each test"""
    # Clear expenses before each test
    expense_tracker.clear_expenses()
    yield
    # Clear expenses after each test
    os.remove(expense_tracker._file_path)


def test_add_expense_cli(clear_expenses):
    """Test adding an expense via the CLI menu"""
    # Mock user input to add an expense
    inputs = [
        "test_expenses.txt",  # Load default file name
        "1",  # Add an expense
        "Food",  # Category
        "20.00",  # Amount
        "Lunch",  # Description
        "7"  # Exit the menu
    ]
    
    with mock.patch("builtins.input", side_effect=inputs):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            display_menu()
            # Capture the output
            output = mock_stdout.getvalue()
            
            assert "Welcome" in output  # Ensure we have the welcome message
            assert "Expense added:" in output  # Ensure we have the expense confirmation
            assert "Food" in output  # Ensure category is correct
            assert "$20.00" in output  # Ensure the amount is correct
            assert "Lunch" in output  # Ensure description is correct

def test_view_expense_cli(clear_expenses):
    """Test viewing expenses via the CLI menu"""
    # Mock user input to add an expense
    inputs = [
        "test_expenses.txt",  # Load default file name
        "1",  # Add an expense
        "Food",  # Category
        "20.00",  # Amount
        "Lunch",  # Description
        "1",  # Add another expense
        "Transport",  # Category
        "15.00",  # Amount
        "Bus fare",  # Description
        "2",  # View all expenses
        "7"  # Exit the menu
    ]
    
    with mock.patch("builtins.input", side_effect=inputs):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            display_menu()
            # Capture the output
            output = mock_stdout.getvalue()
            
            assert "Expenses:" in output  # Ensure we have the expense confirmation
            assert "Food\t$20.00\tLunch" in output  # Ensure first product
            assert "Transport\t$15.00\tBus fare" in output  # Ensure second product

