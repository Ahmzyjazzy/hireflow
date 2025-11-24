from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from config import config
from hireflow_agent.tools import update_checklist_status

hr_agent = LlmAgent(
    name="hr_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Hireflow HR Agent: Manages HR onboarding tasks.",
    instruction="""You are an HR agent, focus on HR tasks from the user:checklist state only.
    - Your primary task is to interpret the user's request if it falls within HR tasks.
    - Get the HR tasks from the user:checklist state and retrieve the matching task from the checklist.
    - Use semantic matching to find the closest task in the checklist that corresponds to the user's request.
    - Only pass the retrieved task to the update_checklist_status tool if it does.
    - Use the update_checklist_status tool to update the task
    """,
    tools=[update_checklist_status] 
)

it_agent = LlmAgent(
    name="it_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Hireflow IT Agent: Manages IT onboarding tasks.",
    instruction="""You are an IT agent, focus on IT tasks from the user:checklist state only.
    - Your primary task is to interpret the user's request if it falls within IT tasks.
    - Get the IT tasks from the user:checklist state and retrieve the matching task from the checklist.
    - Use semantic matching to find the closest task in the checklist that corresponds to the user's request.
    - Only pass the retrieved task to the update_checklist_status tool if it does.
    - Use the update_checklist_status tool to update the task
    """,
    tools=[update_checklist_status] 
)

engineering_agent = LlmAgent(
    name="engineering_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Hireflow Engineering Agent: Manages Engineering onboarding tasks.",
    instruction="""You are an Engineering agent, focus on Engineering tasks from the user:checklist state only.
    - Your primary task is to interpret the user's request if it falls within Engineering tasks.
    - Get the Engineering tasks from the user:checklist state and retrieve the matching task from the checklist.
    - Use semantic matching to find the closest task in the checklist that corresponds to the user's request.
    - Only pass the retrieved task to the update_checklist_status tool if it does.
    - Use the update_checklist_status tool to update the task
    """,
    tools=[update_checklist_status]
)

finance_agent = LlmAgent(
    name="finance_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Hireflow Finance Agent: Manages Finance onboarding tasks.",
    instruction="""You are a Finance agent, focus on Finance tasks from the user:checklist state only.
    - Your primary task is to interpret the user's request if it falls within Finance tasks.
    - Get the Finance tasks from the user:checklist state and retrieve the matching task from the checklist.
    - Use semantic matching to find the closest task in the checklist that corresponds to the user's request.
    - Only pass the retrieved task to the update_checklist_status tool if it does.
    - Use the update_checklist_status tool to update the task
    """,
    tools=[update_checklist_status]
)

assessment_agent = LlmAgent(
    name="assessment_agent",
    model=Gemini(
        model_name=config.model_name,
        retry_options=config.retry_config
    ),
    description="Hireflow Assessment Agent: Manages Assessment onboarding tasks.",
    instruction="""You are an Assessment agent, focus on Assessment tasks from the user:checklist state only.
    - Your primary task is to interpret the user's request if it falls within Assessment tasks.
    - Get the Assessment tasks from the user:checklist state and retrieve the matching task from the checklist.
    - Use semantic matching to find the closest task in the checklist that corresponds to the user's request.
    - Only pass the retrieved task to the update_checklist_status tool if it does.
    - Use the update_checklist_status tool to update the task
    """,
    tools=[update_checklist_status] 
)