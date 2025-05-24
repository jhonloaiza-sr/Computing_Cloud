import re
from datetime import datetime

class ValidationUtils:
    @staticmethod
    def validate_email(email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_date(date_str, format='%Y-%m-%d'):
        """Valida formato de fecha"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_time(time_str, format='%H:%M'):
        """Valida formato de hora"""
        try:
            datetime.strptime(time_str, format)
            return True
        except ValueError:
            return False