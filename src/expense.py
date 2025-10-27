from pathlib import Path

DIRECTORY = "expenses/"
class ExpenseTracker:
    _file_path = None
    _total_lines = 0

    def __init__(self, file_path=None, directory=DIRECTORY):
        if not file_path:
            file_path = "expense.txt"  # Default filename if not provided
        if "." not in file_path:
            file_path += ".txt"  # Ensure file extension is .txt
        # Set up the file path using the directory if provided
        self._file_path = Path(directory) / file_path
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        # Check if the file exists; if not, create it
        if not self._file_path.exists():
            self._file_path.touch()  # Create an empty file if it doesn't exist
            print(f"File {self._file_path} created.")
        else:
            # Count lines in the file if it already exists
            with self._file_path.open('r') as f:
                self._total_lines = len(f.readlines())
    
    def get_total_lines(self):
        """Get total lines on file"""
        return self._total_lines

    def get_expenses(self):
        """Get all expenses from the file"""
        # Read and return all the expenses
        with self._file_path.open('r') as f:
            return f.readlines()

    def add_expense(self, expense: str):
        """Add expense to the file"""
        # line = self._total_lines + 1
        with self._file_path.open(mode="a") as f:
            # f.write(str(line) + "\t" + "\"" + expense + "\"" + "\n")
            f.write(expense + "\n")
        self._total_lines += 1
        return self._total_lines
    
    def clear_expenses(self):
        """Clear all expenses from the file"""
        with self._file_path.open(mode="w") as f:
            f.truncate(0)
        self._total_lines = 0

    def remove_expense(self, line_number: int):
        """Remove an expense by line number (1-indexed)"""
        expenses = self.get_expenses()
        if 1 <= line_number <= len(expenses):
            del expenses[line_number - 1]
            with self._file_path.open(mode="w") as f:
                f.writelines(expenses)
            self._total_lines -= 1
            return True
        return False