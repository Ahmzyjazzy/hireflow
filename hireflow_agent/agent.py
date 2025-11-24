import os
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

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

hireflow_mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params = StdioServerParameters(
            command='python3', # Command to run MCP server script
            args=["-m", "hireflow_agent.mcp_server.server"], # Argument is the path to the script
        ),
    ),
    tool_filter=['employee_lookup', 'get_onboarding_checklist'] # Optional: ensure only specific tools are loaded
)

# Define base tools
agent_tools = [
    hireflow_mcp_toolset, #employee_lookup, get_onboarding_checklist
    AgentTool(agent=hr_agent),
    AgentTool(agent=it_agent),
    AgentTool(agent=engineering_agent),
    AgentTool(agent=finance_agent),
    AgentTool(agent=assessment_agent),
]

# Conditionally add Notion MCP if API key is present
if os.environ.get("NOTION_API_KEY"):
    notion_mcp_toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@notionhq/notion-mcp-server"],
                env={
                    "NOTION_TOKEN": os.environ.get("NOTION_API_KEY"),
                    **os.environ # Optional: Inherit system environment variables so npx can find 'node' and other tools
                }
            ),
            timeout=120 # Optional: Increase timeout for npx installation
        ),
        tool_filter=['API-post-search', 'API-retrieve-a-page']
    )
    agent_tools.append(notion_mcp_toolset)

root_agent = LlmAgent(
    name="hireflow_agent",
    description="The Automated New-Hire Onboarding Agent",
    instruction=ROOT_AGENT_INSTRUCTION,
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    tools=agent_tools,
    after_tool_callback=update_session_after_tool_callback
)