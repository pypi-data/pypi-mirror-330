from datetime import datetime


def generate_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")

    return current_date
