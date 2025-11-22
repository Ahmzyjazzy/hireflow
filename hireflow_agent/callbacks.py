import json
from typing import Dict, Any, Optional
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

def update_session_after_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """Inspects the tool result after execution to update session state."""
    agent_name = tool_context.agent_name
    tool_name = tool.name

    print(f"[Callback] After tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Args used: {args}")
    print(f"[Callback] Original tool_response: {tool_response}")

    # MCP tools return content as a list of blocks, usually JSON in the text block
    try:
        content = tool_response.get("content", [])
        if content and isinstance(content, list) and "text" in content[0]:
            response_text = content[0]["text"]
            parsed_response = json.loads(response_text)
            
            result = parsed_response.get("result", "")
            status = parsed_response.get("status", "")
        else:
            # Fallback for non-MCP tools or different structure
            result = tool_response.get("result", "")
            status = tool_response.get("status", "")
            
    except json.JSONDecodeError:
        print("[Callback] Failed to parse tool response as JSON")
        result = ""
        status = ""
    except Exception as e:
        print(f"[Callback] Error processing tool response: {e}")
        result = ""
        status = ""

    print(f"[Callback] Result: {result}")
    print(f"[Callback] Status: {status}")

    if tool_name == 'employee_lookup' and status == "success":
        tool_context.state["user:profile"] = result
        # We don't necessarily need to return tool_response if we just want to update state
        # But returning it keeps the flow going
        return tool_response

    if tool_name == 'get_onboarding_checklist' and status == "success":
        tool_context.state["user:checklist"] = result
        return tool_response

    print("[Callback] Passing original tool response through.")
    # Return None to use the original tool_response
    return None