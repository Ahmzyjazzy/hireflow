from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool

from config import config
from .prompt import ROOT_AGENT_INSTRUCTION
from .tools.employee_lookup import employee_lookup
from .tools.get_onboarding_checklist import get_onboarding_checklist
from .sub_agents import hr_agent, it_agent, engineering_agent, finance_agent

root_agent = LlmAgent(
    name="hireflow_agent",
    description="The Automated New-Hire Onboarding Agent",
    instruction=ROOT_AGENT_INSTRUCTION,
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    tools=[
        employee_lookup,
        get_onboarding_checklist,
        AgentTool(agent=it_agent),
        AgentTool(agent=hr_agent),
        AgentTool(agent=engineering_agent),
        AgentTool(agent=finance_agent),
    ]
)