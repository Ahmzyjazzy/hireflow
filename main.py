import asyncio
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.apps.app import App, EventsCompactionConfig
from hireflow_agent.agent import root_agent
from utils import call_agent_async, clear_db
from config import config

# clear_db() # Uncomment to clear the database

# 1. Define app with Events Compaction enabled
hireflow_app = App(
    name=config.app_name,
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=config.compaction_interval,
        overlap_size=config.compaction_overlap_size,
    ),
)

# 2. Initialize Persistent Session Service
# Usign SQLite as the database for persistence
db_url = "sqlite:///./hireflow.db"
session_service = DatabaseSessionService(db_url=db_url)

# 3. Initialize Initial State
initial_state = {}

async def main():
    # Setup constants
    APP_NAME = config.app_name
    USER_ID = "_DEFAULT_USER_ID"

    # 4. Session Management - Find or Create Session
    existing_sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
    
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME, 
            user_id=USER_ID, 
            state=initial_state
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    # 5. Agent Runner Setup
    hireflow_runner_compacting = Runner(
        app=hireflow_app, session_service=session_service
    )

    # 6. Run the agent
    print("\n Welcome to the HireFlow Agent Memory Chat!\n")
    print("Your profile and checklist will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.")

    while True:
        # Get user input
        user_input = input("\nYou: ")

        # Check if user wants to exit
        if user_input.lower() in ['exit', 'quit']:
            print("Ending conversation. Your data has been saved to the database.")
            break
        
        # Process the user query through the agent runner
        await call_agent_async(hireflow_runner_compacting, USER_ID, SESSION_ID, user_input)
        

if __name__ == "__main__":
    asyncio.run(main())
