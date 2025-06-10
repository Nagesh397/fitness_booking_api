from pytz import timezone
import logging

def convert_ist_to_tz(dt, tz_str):
    """
    Convert a datetime from IST (Asia/Kolkata) to a target timezone.

    Args:
        dt (datetime): The datetime object (naive or aware) in IST.
        tz_str (str): A string representing the target timezone (e.g., 'UTC', 'America/New_York').

    Returns:
        str: The ISO 8601 formatted datetime string in the target timezone.
    """
    ist = timezone('Asia/Kolkata')
    target = timezone(tz_str)

    # Ensure datetime is timezone-aware
    dt = dt if dt.tzinfo else ist.localize(dt)

    # Convert and return in ISO format
    return dt.astimezone(target).isoformat()

def get_logger(name=__name__, level=logging.INFO):
    """
    Returns a reusable logger instance with console output.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
