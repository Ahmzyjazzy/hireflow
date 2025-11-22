from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from config import config
from hireflow_agent.prompt import ROOT_AGENT_INSTRUCTION
from hireflow_agent.sub_agents import (
    hr_agent, 
    it_agent, 
    engineering_agent, 
    finance_agent, 
    assessment_agent,
)
from hireflow_agent.callbacks import update_session_after_tool_callback

load_dotenv()

mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams( # Use StdioConnectionParams for local process communication
        server_params = StdioServerParameters(
            command='python3', # Command to run MCP server script
            args=["-m", "hireflow_agent.mcp_server.server"], # Argument is the path to the script
        ),
    ),
    tool_filter=['employee_lookup', 'get_onboarding_checklist'] # Optional: ensure only specific tools are loaded
)

root_agent = LlmAgent(
    name="hireflow_agent",
    description="The Automated New-Hire Onboarding Agent",
    instruction=ROOT_AGENT_INSTRUCTION,
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    tools=[
        mcp_toolset, #employee_lookup, get_onboarding_checklist
        AgentTool(agent=it_agent),
        AgentTool(agent=hr_agent),
        AgentTool(agent=engineering_agent),
        AgentTool(agent=finance_agent),
        AgentTool(agent=assessment_agent),
    ],
    after_tool_callback=update_session_after_tool_callback
)