from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext

def update_checklist_status(tool_context: ToolContext, category: str, task: str, is_complete: bool) -> Dict[str, Any]:
    """
    Updates the status of a specific task within a category in the user:checklist state.
    
    Args:
        tool_context: ADK session context.
        category: The checklist category (e.g., 'HR', 'IT', 'ENGINEERING').
        task: The specific task name (e.g., 'Assign laptop to staff').
        is_complete: Boolean status (True for done, False for pending).
    
    Returns:
        A status dictionary.
    """
    state = tool_context.state
    checklist = state.get("user:checklist")

    if not checklist:
        return {"status": "error", "message": "Onboarding checklist does not exist."}
    
    category_key = category.upper()
    
    if category_key not in checklist:
        return {"status": "error", "message": f"Checklist category '{category_key}' not found."}

    if task not in checklist[category_key]:
        return {"status": "error", "message": f"Task '{task}' not found in category '{category_key}'."}

    # 1. Simulate Confirmation (In a real scenario, this would call an HR/IT API)
    # Since we are simulating, we just update the state directly.
    checklist[category_key][task] = is_complete

    # 2. Store the updated checklist back into the state
    state["user:checklist"] = checklist
    
    return {
        "status": "success",
        "message": f"Task '{task}' in {category_key} confirmed as {'Complete' if is_complete else 'Pending'}."
    }

def verify_asset_assignment(tool_context: ToolContext, employee_id: str) -> Dict[str, Any]:
    """Simulates checking an IT asset management system for laptop assignment."""
    # Logic: Assumes success if the employee ID exists
    if tool_context.state.get("user:profile", {}).get("employee_id") == employee_id:
        # After successful verification, the IT agent would then call update_checklist_status
        return {"status": "verified", "asset_tag": "LT-5021", "message": "Laptop assignment confirmed in asset database."}
    return {
        "status": "unverified", 
        "message": "Laptop not found in system."
    }