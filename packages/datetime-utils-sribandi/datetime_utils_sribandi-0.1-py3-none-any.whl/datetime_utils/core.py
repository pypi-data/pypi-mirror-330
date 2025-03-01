from datetime import datetime, timedelta
import pytz

def get_current_time(timezone='UTC'):
    """Returns the current time in the given timezone."""
    tz = pytz.timezone(timezone)
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def format_date(date_obj, current_format='%Y-%m-%d', new_format='%d-%m-%Y'):
    """Converts a date (string or datetime object) to a different format."""
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, current_format)  # Convert string to datetime
    return date_obj.strftime(new_format)

def days_between(date1, date2, date_format='%Y-%m-%d'):
    """Returns the number of days between two dates."""
    if isinstance(date1, str):  
        date1 = datetime.strptime(date1, date_format)  # Convert string to datetime
    if isinstance(date2, str):  
        date2 = datetime.strptime(date2, date_format)  # Convert string to datetime
    
    return abs((date2 - date1).days)

from datetime import datetime, timedelta

def add_days(date, days, date_format='%Y-%m-%d'):
    """Adds or subtracts days from a given date."""
    if isinstance(date, str):  # ✅ Corrected indentation
        date = datetime.strptime(date, date_format)  # Convert string to datetime
    new_date = date + timedelta(days=days)  # Add/subtract days
    return new_date.strftime(date_format)  # Return formatted string
