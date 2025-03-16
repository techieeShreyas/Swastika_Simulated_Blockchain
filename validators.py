import re

def validate_name(name):
    """Validate the name field."""
    if not name or len(name) > 100:
        return "Name must be between 1 and 100 characters."
    return None

def validate_age(age):
    """Validate the age field."""
    try:
        age = int(age)
        if age < 0 or age > 120:
            return "Age must be between 0 and 120."
    except ValueError:
        return "Age must be a valid number."
    return None

def validate_blood_type(blood_type):
    """Validate the blood type field."""
    valid_blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if blood_type not in valid_blood_types:
        return f"Blood type must be one of: {', '.join(valid_blood_types)}."
    return None

def validate_medical_urgency(medical_urgency):
    """Validate the medical urgency field."""
    if not medical_urgency or len(medical_urgency) > 200:
        return "Medical urgency must be between 1 and 200 characters."
    return None

def validate_hospital_name(hospital_name):
    """Validate the hospital name field."""
    if not hospital_name or len(hospital_name) > 100:
        return "Hospital name must be between 1 and 100 characters."
    return None