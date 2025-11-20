from typing import Dict, List
from datetime import datetime, timedelta

# --- Datetime Calculation ---
# Calculate the mock start date: one day before today
today = datetime.now().date()
yesterday = today - timedelta(days=1)
CALCULATED_START_DATE = yesterday.strftime("%Y-%m-%d")

# --- Mock Employee Database ---
# (in production, this would be an API call)
NEW_STAFF_DATABASE: Dict[str, Dict[str, str]] = {
    "john.doe@xyz.com": {
        "name": "John Doe",
        "department": "Engineering",
        "start_date": CALCULATED_START_DATE,
        "employee_id": "EMP1021",
    },
    "sarah.daniels@xyz.com": {
        "name": "Sarah Daniels",
        "department": "Finance",
        "start_date": CALCULATED_START_DATE,
        "employee_id": "EMP3092",
    }
}

# --- Mock Onboarding Checklists ---
# Ordered checklists per department
CHECKLISTS: Dict[str, List[str]] = {
   "it": [
        "Create official email",
        "Assign laptop to staff",
    ],
    "hr": [
        "Complete personal information form",
        "Sign employee handbook",
        "Complete benefits enrollment",
        "Attend HR orientation",
    ],
    "assessment": [
        "Take HR assessment quiz",
        "Complete security training",
    ],
    "engineering": [
        "Setup dev workstation",
        "Request repo access",
        "Setup and run project locally",
        "Meet with tech lead",
    ],
    "finance": [
        "Complete finance onboarding form",
        "Setup expense account",
        "Attend finance orientation",
        "Meet with finance manager",
    ],
}