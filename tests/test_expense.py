import pytest
from pathlib import Path
import tempfile
import shutil
from src.expense import ExpenseTracker, DIRECTORY
from factories.product import ProductFactory


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_directory = tempfile.mkdtemp()
    yield temp_directory
    # Cleanup after test
    shutil.rmtree(temp_directory)


@pytest.fixture
def tracker(temp_dir):
    """Create an ExpenseTracker instance with a temporary directory"""
    return ExpenseTracker(file_path="test_expense.txt", directory=temp_dir)


@pytest.fixture
def tracker_with_files(tracker: ExpenseTracker):
    """Create an ExpenseTracker instance with a temporary directory"""
    [tracker.add_expense(f"{product.name} - {product.price} - {product.stock}")
     for product in ProductFactory.create_batch(10)]
    return tracker


class TestExpenseTrackerInit:
    """Test initialization of ExpenseTracker"""

    def test_init_creates_file_if_not_exists(self, temp_dir):
        """Test that initialization creates a file if it doesn't exist"""
        tracker = ExpenseTracker(file_path="new_file.txt", directory=temp_dir)
        assert tracker._file_path.exists()
        assert tracker.get_total_lines() == 0

    def test_init_with_default_filename(self, temp_dir):
        """Test initialization with default filename"""
        tracker = ExpenseTracker(directory=temp_dir)
        assert tracker._file_path.name == "expense.txt"
        assert tracker._file_path.exists()

    def test_init_adds_txt_extension(self, temp_dir):
        """Test that .txt extension is added if not provided"""
        tracker = ExpenseTracker(file_path="myfile", directory=temp_dir)
        assert tracker._file_path.name == "myfile.txt"

    def test_init_with_existing_file(self, temp_dir):
        """Test initialization with an existing file that has content"""
        file_path = Path(temp_dir) / "existing.txt"
        file_path.write_text("expense1\nexpense2\nexpense3\n")

        tracker = ExpenseTracker(file_path="existing.txt", directory=temp_dir)
        assert tracker.get_total_lines() == 3

    def test_init_creates_directory_if_not_exists(self):
        """Test that initialization creates the directory structure"""
        temp_dir = tempfile.mkdtemp()
        try:
            nested_dir = Path(temp_dir) / "nested" / "path"
            tracker = ExpenseTracker(
                file_path="test.txt", directory=str(nested_dir))
            assert tracker._file_path.parent.exists()
            assert tracker._file_path.exists()
        finally:
            shutil.rmtree(temp_dir)

class TestExpenseStr:
    """Check if the __str__ given the proper result"""

    def test_expense__str__(self, tracker: ExpenseTracker):
        assert str(
            tracker) == f"ExpenseTracker(file_path={tracker._file_path}, total_lines={tracker._total_lines})"


class TestExpenseFind:
    """Test find function of ExpenseTracker"""

    def test_expense_find(self, tracker: ExpenseTracker):
        """Find the line with correspondent id"""
        list_products = [
            f"{product.name} - {product.price} - {product.stock}" for product in ProductFactory.create_batch(10)]
        [tracker.add_expense(product) for product in list_products]
        assert tracker._total_lines == 10
        assert tracker.find_expense(10) == list_products[9]

    def test_expense_find_not_in_range_then_added(self, tracker: ExpenseTracker):
        """Find the line with an id that is not in the range given"""
        [tracker.add_expense(f"{product.name} - {product.price} - {product.stock}")
         for product in ProductFactory.create_batch(10)]
        assert tracker._total_lines == 10
        error_str = "Number given is not in the range of values added"
        with pytest.raises(ValueError, match=error_str):
            tracker.find_expense(20)
        with pytest.raises(ValueError, match=error_str):
            tracker.find_expense(-20)


class TestExpenseUpdate:
    """Test update function of ExpenseTracker"""

    def test_expense_update(self, tracker: ExpenseTracker):
        """Test update value of a expense"""
        product = ProductFactory()
        product_expense = f"{product.name}- {product.price} - {product.price}"
        line = tracker.add_expense(product_expense)
        assert tracker.find_expense(line) == product_expense
        new_product = ProductFactory()
        new_product_expense = f"{new_product.name}- {new_product.price} - {new_product.price}"
        assert tracker.update_expense(line, new_product_expense)
        assert tracker.find_expense(line) == new_product_expense

    def test_expense_update_not_found(self, tracker_with_files: ExpenseTracker):
        """Test update value of a expense that does not exist"""
        error_str = "Line out of range"
        with pytest.raises(ValueError, match=error_str):
            tracker_with_files.update_expense(15, "test")
        with pytest.raises(ValueError, match=error_str):
            tracker_with_files.update_expense(-15, "test")


class TestGetExpenses:
    """Test getting expenses"""

    def test_get_expenses_empty_file(self, tracker):
        """Test getting expenses from an empty file"""
        expenses = tracker.get_expenses()
        assert expenses == []

    def test_get_expenses_with_content(self, tracker):
        """Test getting expenses from a file with content"""
        tracker.add_expense("Coffee")
        tracker.add_expense("Lunch")
        tracker.add_expense("Gas")

        expenses = tracker.get_expenses()
        assert len(expenses) == 3
        assert "Coffee\n" in expenses
        assert "Lunch\n" in expenses
        assert "Gas\n" in expenses


class TestAddExpense:
    """Test adding expenses"""

    def test_add_single_expense(self, tracker):
        """Test adding a single expense"""
        result = tracker.add_expense("Coffee $5")
        assert result == 1
        assert tracker.get_total_lines() == 1

        expenses = tracker.get_expenses()
        assert expenses[0] == "Coffee $5\n"

    def test_add_multiple_expenses(self, tracker):
        """Test adding multiple expenses"""
        tracker.add_expense("Coffee $5")
        tracker.add_expense("Lunch $12")
        result = tracker.add_expense("Dinner $20")

        assert result == 3
        assert tracker.get_total_lines() == 3

        expenses = tracker.get_expenses()
        assert len(expenses) == 3

    def test_add_expense_increments_total_lines(self, tracker):
        """Test that adding expenses correctly increments total_lines"""
        assert tracker.get_total_lines() == 0
        tracker.add_expense("Item 1")
        assert tracker.get_total_lines() == 1
        tracker.add_expense("Item 2")
        assert tracker.get_total_lines() == 2

    def test_add_expense_with_special_characters(self, tracker):
        """Test adding expenses with special characters"""
        special_expense = "Coffee @ Café: $5.50 (10% tip)"
        tracker.add_expense(special_expense)

        expenses = tracker.get_expenses()
        assert expenses[0] == special_expense + "\n"


class TestClearExpenses:
    """Test clearing expenses"""

    def test_clear_empty_file(self, tracker):
        """Test clearing an already empty file"""
        tracker.clear_expenses()
        assert tracker.get_total_lines() == 0
        assert tracker.get_expenses() == []

    def test_clear_file_with_content(self, tracker):
        """Test clearing a file with content"""
        tracker.add_expense("Coffee")
        tracker.add_expense("Lunch")
        tracker.add_expense("Dinner")

        assert tracker.get_total_lines() == 3

        tracker.clear_expenses()
        assert tracker.get_total_lines() == 0
        assert tracker.get_expenses() == []

    def test_clear_and_add_again(self, tracker):
        """Test that we can add expenses after clearing"""
        tracker.add_expense("Before clear")
        tracker.clear_expenses()
        tracker.add_expense("After clear")

        assert tracker.get_total_lines() == 1
        expenses = tracker.get_expenses()
        assert expenses[0] == "After clear\n"


class TestRemoveExpense:
    """Test removing expenses"""

    def test_remove_expense_valid_line(self, tracker):
        """Test removing an expense with a valid line number"""
        tracker.add_expense("Coffee")
        tracker.add_expense("Lunch")
        tracker.add_expense("Dinner")

        result = tracker.remove_expense(2)  # Remove "Lunch"
        assert result is True
        assert tracker.get_total_lines() == 2

        expenses = tracker.get_expenses()
        assert len(expenses) == 2
        assert "Coffee\n" in expenses
        assert "Dinner\n" in expenses
        assert "Lunch\n" not in expenses

    def test_remove_first_expense(self, tracker):
        """Test removing the first expense"""
        tracker.add_expense("First")
        tracker.add_expense("Second")
        tracker.add_expense("Third")

        result = tracker.remove_expense(1)
        assert result is True
        assert tracker.get_total_lines() == 2

        expenses = tracker.get_expenses()
        assert "First\n" not in expenses
        assert "Second\n" in expenses

    def test_remove_last_expense(self, tracker):
        """Test removing the last expense"""
        tracker.add_expense("First")
        tracker.add_expense("Second")
        tracker.add_expense("Third")

        result = tracker.remove_expense(3)
        assert result is True
        assert tracker.get_total_lines() == 2

        expenses = tracker.get_expenses()
        assert "Third\n" not in expenses

    def test_remove_expense_invalid_line_number_too_high(self, tracker):
        """Test removing with line number too high"""
        tracker.add_expense("Coffee")

        result = tracker.remove_expense(5)
        assert result is False
        assert tracker.get_total_lines() == 1

    def test_remove_expense_invalid_line_number_zero(self, tracker):
        """Test removing with line number zero"""
        tracker.add_expense("Coffee")

        result = tracker.remove_expense(0)
        assert result is False
        assert tracker.get_total_lines() == 1

    def test_remove_expense_invalid_line_number_negative(self, tracker):
        """Test removing with negative line number"""
        tracker.add_expense("Coffee")

        result = tracker.remove_expense(-1)
        assert result is False
        assert tracker.get_total_lines() == 1

    def test_remove_from_empty_file(self, tracker):
        """Test removing from an empty file"""
        result = tracker.remove_expense(1)
        assert result is False
        assert tracker.get_total_lines() == 0


class TestGetTotalLines:
    """Test getting total lines"""

    def test_get_total_lines_empty(self, tracker):
        """Test total lines for empty file"""
        assert tracker.get_total_lines() == 0

    def test_get_total_lines_after_adds(self, tracker):
        """Test total lines after adding expenses"""
        tracker.add_expense("Item 1")
        tracker.add_expense("Item 2")
        assert tracker.get_total_lines() == 2

    def test_get_total_lines_after_remove(self, tracker):
        """Test total lines after removing an expense"""
        tracker.add_expense("Item 1")
        tracker.add_expense("Item 2")
        tracker.add_expense("Item 3")
        tracker.remove_expense(2)
        assert tracker.get_total_lines() == 2

    def test_get_total_lines_after_clear(self, tracker):
        """Test total lines after clearing"""
        tracker.add_expense("Item 1")
        tracker.add_expense("Item 2")
        tracker.clear_expenses()
        assert tracker.get_total_lines() == 0


class TestEdgeCases:
    """Test edge cases and integration scenarios"""

    def test_empty_expense_string(self, tracker):
        """Test adding an empty expense string"""
        tracker.add_expense("")
        assert tracker.get_total_lines() == 1
        expenses = tracker.get_expenses()
        assert expenses[0] == "\n"

    def test_expense_with_newlines(self, tracker):
        """Test expense containing newline characters"""
        tracker.add_expense("Multi\nline\nexpense")
        expenses = tracker.get_expenses()
        # This will create multiple lines in the file
        assert len(expenses) > 1

    def test_multiple_trackers_same_file(self, temp_dir):
        """Test multiple tracker instances with the same file"""
        tracker1 = ExpenseTracker(file_path="shared.txt", directory=temp_dir)
        tracker1.add_expense("From tracker 1")

        tracker2 = ExpenseTracker(file_path="shared.txt", directory=temp_dir)
        assert tracker2.get_total_lines() == 1

        expenses = tracker2.get_expenses()
        assert "From tracker 1\n" in expenses

    def test_sequential_operations(self, tracker):
        """Test a sequence of operations"""
        # Add some expenses
        tracker.add_expense("Coffee $5")
        tracker.add_expense("Lunch $12")
        tracker.add_expense("Snack $3")
        tracker.add_expense("Dinner $20")

        # Remove one
        tracker.remove_expense(3)

        # Add another
        tracker.add_expense("Dessert $8")

        # Clear and start over
        tracker.clear_expenses()
        tracker.add_expense("New expense")

        assert tracker.get_total_lines() == 1
        expenses = tracker.get_expenses()
        assert expenses == ["New expense\n"]
