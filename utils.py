from blockchain import Blockchain

# Initialize the three blockchains
donor_chain = Blockchain("Donor")
recipient_chain = Blockchain("Recipient")
transplant_chain = Blockchain("Transplant")

def get_blockchain(name):
    """
    Get the blockchain instance by name.
    """
    if name == "donor":
        return donor_chain
    elif name == "recipient":
        return recipient_chain
    elif name == "transplant":
        return transplant_chain
    else:
        raise ValueError("Invalid blockchain name")

def find_match(recipient, donor_chain):
    """
    Find a matching donor for the given recipient.

    Args:
        recipient (dict): The recipient's data (name, age, blood_type, medical_urgency).
        donor_chain (Blockchain): The donor blockchain to search for a match.

    Returns:
        dict: The matching donor's data, or None if no match is found.
    """
    for block in donor_chain.get_all_blocks():
        donor = block.get_data()  # Deserialize the data

        # Ensure the donor data is valid and not already used
        if not isinstance(donor, dict) or "used" in donor:
            continue

        # Check if the donor's blood type matches the recipient's blood type
        if donor.get("blood_type") != recipient.get("blood_type"):
            continue

        # Check if the donor meets the age requirement (e.g., at least 18 years old)
        if donor.get("age", 0) < 18:  # Default to 0 if age is missing
            continue

        # If all conditions are met, return the matching donor
        return donor

    # If no match is found, return None
    return None

def notify_hospital(hospital_name, recipient_name):
    """
    Notify the hospital that a match has been found.
    """
    print(f"Notification sent to {hospital_name}: A match has been found for {recipient_name}.")

def notify_recipient(recipient_name):
    """
    Notify the recipient that a donor has been found.
    """
    print(f"Notification sent to {recipient_name}: A donor has been found for you.")