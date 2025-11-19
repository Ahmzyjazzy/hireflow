from google.adk.agents import LlmAgent

from config import config
from .tools.employee_lookup_tool import employee_lookup
from .prompt import ROOT_AGENT_INSTR

root_agent = LlmAgent(
    model=config.model_name,
    name="hireflow_agent",
    description="The Automated New-Hire Onboarding Agent",
    instruction=ROOT_AGENT_INSTR,
    tools=[employee_lookup]
)