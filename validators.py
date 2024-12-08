# validators.py

class InputValidator:
    @staticmethod
    def is_number(value, check_positive=False, check_negative=False):
        """Check if the value is a number (int or float)."""
        try:
            value = float(value)  # Attempt to convert to float
        except ValueError:
            return False

        if check_positive and value > 0:
            return True

        if check_negative and value < 0:
            return True

        return True

    @staticmethod
    def is_int(value, check_positive=False, check_negative=False):
        """Check if the value is an integer."""
        try:
            value = int(value)  # Attempt to convert to int
        except ValueError:
            return False

        if check_positive and value > 0:
            return True

        if check_negative and value < 0:
            return True

        return True

    @staticmethod
    def is_float(value, check_positive=False, check_negative=False):
        """Check if the value is a float."""
        try:
            value = float(value)  # Attempt to convert to float
            if '.' not in str(value):  # Ensure it's a float, not an int
                return False
        except ValueError:
            return False

        if check_positive and value > 0:
            return True

        if check_negative and value < 0:
            return True

        return True

    @staticmethod
    def is_non_empty_string(value):
        """Check if the value is a non-empty string."""
        return isinstance(value, str) and bool(value.strip())
