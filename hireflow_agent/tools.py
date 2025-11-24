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
        # Try fuzzy matching (token-based)
        matched_task = None
        task_tokens = set(task.lower().split())
        
        best_match = None
        max_overlap = 0
        
        for existing_task in checklist[category_key]:
            existing_tokens = set(existing_task.lower().split())
            overlap = len(task_tokens.intersection(existing_tokens))
            
            # We require at least some significant overlap (e.g., > 50% of tokens or at least 2 tokens)
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = existing_task
        
        # Threshold: arbitrary, but let's say at least 2 tokens match or 50% of the query
        if best_match and (max_overlap >= 2 or max_overlap >= len(task_tokens) * 0.5):
            task = best_match
        else:
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