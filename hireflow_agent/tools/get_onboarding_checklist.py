from typing import Dict, List, Any
from google.adk.tools.tool_context import ToolContext

from ..data import CHECKLISTS

def get_onboarding_checklist(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Initializes or retrieves the user's full, consolidated onboarding checklist 
    from the session state.

    Args:
        tool_context (ToolContext): ADK session context.

    Returns:
        A dictionary containing the full checklist structure or an error message.
    """
    state = tool_context.state
    
    # 1. Check if checklist already exists in the session state
    existing_checklist = state.get("user:checklist")
    if existing_checklist:
        return {
            "status": "success",
            "message": "Onboarding checklist retrieved from session state.",
            "checklist": existing_checklist
        }

    # 2. Checklist does NOT exist, so create it
    # Ensure 'user:profile' exists before proceeding
    user_profile = state.get("user:profile")
    if not user_profile:
        return {
            "status": "error",
            "error_message": "User profile not found in state. Please run employee_lookup first."
        }
        
    user_dept = user_profile.get("department", "").lower()

    # 3. Consolidate the Full Checklist

    # HR and IT tasks are MANDATORY for all staff
    full_checklist = {
        "HR": {task: False for task in CHECKLISTS["hr"]},
        "IT": {task: False for task in CHECKLISTS["it"]},
    }
    
    # Assessment tasks are general but grouped separately for tracking
    full_checklist["General_Assessment"] = {task: False for task in CHECKLISTS["assessment"]}

    # Add department-specific tasks
    if user_dept in CHECKLISTS:
        # Include the department's specific tasks
        full_checklist[user_dept.upper()] = {
            task: False for task in CHECKLISTS[user_dept]
        }
    
    # 4. Store the newly generated checklist in the session state
    state["user:checklist"] = full_checklist
    
    return {
        "status": "success",
        "message": f"Full consolidated checklist generated for {user_dept.upper()} staff.",
        "checklist": full_checklist
    }