from typing import Dict, List
from datetime import datetime, timedelta

# --- Datetime Calculation ---
# Calculate the mock start date: one day before today
today = datetime.now().date()
yesterday = today - timedelta(days=1)
CALCULATED_START_DATE = yesterday.strftime("%Y-%m-%d")

# --- Mock Employee Database ---
# (in production, this would be an API call/DB query)
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
# (in production, this would be an API call/DB query for pre-configured company wide onboarding checklist)
CHECKLISTS: Dict[str, List[str]] = {
    "hr": [
        "Complete employee profile form",
        "Read the employee handbook",
        "Sign employee handbook form",
        "Attend HR orientation",
    ],
   "it": [
        "Confirm worktools received",
        "Confirm profile on staff portal",
    ],
    "assessment": [
        "Complete security training",
        "Take Assessment Quiz",
    ],
    "engineering": [
        "Setup dev workstation",
        "Meet with tech lead",
    ],
    "finance": [
        "Attend finance orientation",
        "Meet with finance manager",
    ],
}
