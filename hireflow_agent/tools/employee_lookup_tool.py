from datetime import datetime, timedelta

from google.adk.tools.tool_context import ToolContext

# Simulated new hire database  — indexed by email
# (in production, this would be an actual database or API)
# Calculate the required start date: one day before today (2025-11-18)
today = datetime.now().date()
yesterday = today - timedelta(days=1)
calculated_start_date = yesterday.strftime("%Y-%m-%d")

new_staff_database = {
    "john.doe@xyz.com": {
        "name": "John Doe",
        "department": "Engineering",
        "start_date": calculated_start_date,
        "employee_id": "EMP1021",
    },
    "sarah.daniels@xyz.com": {
        "name": "Sarah Daniels",
        "department": "Finance",
        "start_date": calculated_start_date,
        "employee_id": "EMP3092",
    }
}

def employee_lookup(tool_context: ToolContext, email: str) -> dict:
    """
    Lookup staff info using email only. Confirm that user exists, belongs to the correct
    department, and store their info in the session.

    Args:
        name (str): Staff name (not used for lookup).
        email (str): Staff email (used as lookup key).
        department (str): Department user claims to belong to.
        tool_context (ToolContext): ADK session context.

    Returns:
        dict with user info on success, or error message on failure:
        - On error, return dict with structure: {
            "status": "error",
            "error_message": "Description of the error"
        }
        - On success, return 
        dict with structure: {
            "status": "success",
            "user_department_info": session["user_info"]
        }
    """

    # 1. Ensure email domain is allowed
    if not email.lower().endswith("@xyz.com"):
        return {
            "status": "error",
            "error_message": "Invalid email domain. Only @xyz.com emails are allowed."
        }

    # 2. Lookup staff by email only
    staff_info = new_staff_database.get(email.lower())

    if staff_info is None:
        return {
            "status": "error",
            "error_message": f"No staff found with email: {email}"
        }

    # 3. Save staff info into the session
    state = tool_context.state

    user_info_to_store = {
        "name": staff_info["name"],
        "email": email, # Use the validated email
        "department": staff_info["department"],
        "start_date": staff_info["start_date"],
        "employee_id": staff_info["employee_id"],
        "verified": True # Add verification flag
    }
    
    tool_context.state["user:profile"] = user_info_to_store

    # 4. Return success response
    return {
        "status": "success",
        "user_department_info": state["user:profile"]
    }
