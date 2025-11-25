from typing import Any
import mcp.types as types
from mcp.server.fastmcp import FastMCP

from .data import NEW_STAFF_DATABASE, CHECKLISTS

# Initialize FastMCP server
mcp = FastMCP("hireflow-mcp")

@mcp.tool()
def employee_lookup(email: str) -> dict:
    """
    Lookup staff info using email only.
    
    Args:
        email (str): Staff email (used as lookup key).
        
    Returns:
        dict with user info on success, or error message on failure.
    """
    # 1. Ensure email domain is allowed
    if not email.lower().endswith("@xyz.com"):
        return {
            "status": "error",
            "error_message": "Invalid email domain. Only @xyz.com emails are allowed."
        }

    # 2. Lookup staff by email only
    staff_info = NEW_STAFF_DATABASE.get(email.lower())

    if staff_info is None:
        return {
            "status": "error",
            "error_message": f"No staff found with email: {email}"
        }

    # 3. set user info to store
    user_info_to_store = {
        "name": staff_info["name"],
        "email": email, # Use the validated email
        "department": staff_info["department"],
        "start_date": staff_info["start_date"],
        "employee_id": staff_info["employee_id"],
        "verified": True # Add verification flag
    }
    
    # 4. Return success response with data
    return {
        "status": "success",
        "result": user_info_to_store
    }

@mcp.tool()
def get_onboarding_checklist(department: str) -> dict:
    """
    Generates the full, consolidated onboarding checklist for a department.
    
    Args:
        department (str): The department to generate the checklist for.
        
    Returns:
        dict containing the full checklist structure.
    """
    user_dept = department.lower()

    # Consolidate the Full Checklist
    # HR and IT tasks are MANDATORY for all staff
    full_checklist = {
        "HR": {task: False for task in CHECKLISTS["hr"]},
        "IT": {task: False for task in CHECKLISTS["it"]},
    }
    
    # Assessment tasks are general but grouped separately for tracking
    full_checklist["Assessment"] = {task: False for task in CHECKLISTS["assessment"]}

    # Add department-specific tasks
    if user_dept in CHECKLISTS:
        full_checklist[user_dept.upper()] = {
            task: False for task in CHECKLISTS[user_dept]
        }
    
    # Return the generated checklist
    if full_checklist:
        return {
            "status": "success",
            "message": "Checklist generated.",
            "result": full_checklist
        }
    else:
        return {
            "status": "error",
            "error_message": "Invalid checklist data from MCP server"
        }

if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\nMCP server (studio) stopped by user")
    except Exception as e:
        print(f"\nMCP server (studio) encountered an error: {e}")
    finally:
        print("\nMCP server (studio) process exiting.")
