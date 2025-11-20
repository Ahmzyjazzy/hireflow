from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from config import config
from .tools.shared_onboarding_tools import update_checklist_status, verify_asset_assignment

hr_agent = LlmAgent(
    name="hr_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Manages HR onboarding tasks. Can confirm completion of HR forms, handbook signing, and scheduling HR orientation.",
    instruction="Your primary task is to confirm and update the status of HR-related checklist items in the session state.",
    tools=[update_checklist_status] 
)

it_agent = LlmAgent(
    name="it_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Manages IT setup, email creation, and asset provisioning. Can verify laptop assignment in the system.",
    instruction="""Your primary task is to verify and update IT-related checklist items. 
    Use verify_asset_assignment to check if a laptop is assigned.
    Then, update the checklist status accordingly.
    """,
    tools=[update_checklist_status, verify_asset_assignment] 
)

engineering_agent = LlmAgent(
    name="engineering_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Guides and confirms setup of development environments, repository access, and local project setup.",
    instruction="Your primary task is to confirm and update the status of Engineering checklist items.",
    tools=[update_checklist_status]
)