# HireFlow - Automated New-Hire Onboarding Agent

**Automating the employee onboarding journey with Multi-Agent Systems and MCP.**

## Overview
HireFlow is an intelligent multi-agent system designed to streamline and automate the new-hire onboarding process. Built as a capstone project for the [Kaggle Agents Intensive](https://www.kaggle.com/competitions/agents-intensive-capstone-project/overview), it leverages Google's Agent Development Kit (ADK) and the Model Context Protocol (MCP) to create a seamless, efficient, and interactive onboarding experience.

By orchestrating specialized sub-agents and integrating with external data sources via MCP, HireFlow reduces the administrative burden on HR and IT teams while ensuring new employees have everything they need from day one.

## Value Proposition
*   **Efficiency**: Reduces manual coordination time by automating checklist tracking.
*   **Consistency**: Ensures every new hire goes through a standardized, error-free onboarding process.
*   **Interactivity**: Provides a conversational interface for new hires to check their status and complete tasks.
*   **Scalability**: Modular multi-agent architecture allows for easy addition of new departments or tasks.

## Architecture
HireFlow uses a **Multi-Agent LLM Orchestrator** pattern. The main `HireFlow Agent` acts as the orchestrator, delegating specific tasks to specialized sub-agents based on the user's intent. It also connects to an **MCP Server** to securely access employee data, generate dynamic onboarding checklists and access to internal company documents on notion (if notion is configured).

![HireFlow Architecture](/docs/images/architecture/hireflow_architecture.png)

### Core Components
1.  **HireFlow Agent (Orchestrator)**: The entry point for the user. It understands the user's request and routes it to the appropriate sub-agent or tool.
2.  **MCP Server**: A dedicated server implementing the Model Context Protocol to provide safe, standardized access to:
    *   `employee_lookup`: Retrieves employee details from the staff database.
    *   `get_onboarding_checklist`: Generates department-specific onboarding checklists.
    *   `API-post-search(query:, sort, filter, start_cursor, page_size)`: it is use to search Notion pages/documents by title (if notion is configured)
    *   `API-retrieve-a-page( page_id: str)`: it is use to retrieve a specific page/document by page_id (if notion is configured)
3.  **Sub-Agents**: Specialized agents focused on specific domains (HR, IT, Engineering, etc.).

## Agents

### Main Agent
*   **HireFlow Agent**: The central controller. It initializes the session, authenticates the user via the MCP `employee_lookup` tool, and manages the overall conversation flow.

### Sub-Agents
*   **HR Agent**: Hireflow HR Agent: Manages HR onboarding tasks.
*   **IT Agent**: Hireflow IT Agent: Manages IT onboarding tasks.
*   **Engineering Agent**: Hireflow Engineering Agent: Manages Engineering onboarding tasks.
*   **Finance Agent**: Hireflow Finance Agent: Manages Finance onboarding tasks.
*   **Assessment Agent**: Hireflow Assessment Agent: Manages Assessment onboarding tasks.

## Tools

### MCP Tools (Data Layer)
These tools are served via the MCP server and provide data to the agents.
*   `employee_lookup(email: str)`: Looks up an employee by email to retrieve their profile, department, and ID.
*   `get_onboarding_checklist(department: str)`: Generates a consolidated checklist containing mandatory HR/IT tasks and department-specific items.

Some other tools use from Notion MCP Server
* `API-post-search(query:, sort, filter, start_cursor, page_size)`: it is use to search Notion pages/documents by title
* `API-retrieve-a-page( page_id: str)`: it is use to retrieve a specific page/document by page_id

### Agent Tools (Action Layer)
These tools are used by the agents to modify the session state and track progress.
*   `update_checklist_status(category, task, is_complete)`: Updates the status of a specific checklist item (e.g., marking "Sign employee handbook" as complete).

## Workflow
1.  **Authentication**: The user provides their email. The **HireFlow Agent** calls the `employee_lookup` MCP tool to verify identity and load the user's profile. 
> Note: For realife scenario, this agent would be access with staff portal ensuring user is already authenticated
2.  **Initialization**: Based on the user's department, the agent calls `get_onboarding_checklist` (MCP) to generate a personalized onboarding checklist.
3.  **Orchestration**: The user interacts with the agent (e.g., "I've signed my handbook").
4.  **Delegation**: The **HireFlow Agent** routes the request to the relevant sub-agent (e.g., **HR Agent**).
5.  **Execution**: The sub-agent uses tools like `update_checklist_status` to mark the task as complete in the session state.
6.  **Feedback**: The agent confirms the action to the user and suggests the next steps.

See sample screenshots in the [Demo folder](docs/images/demo) folder below.
- [Adk web UI](docs/images/demo/1-adk-chat.png)
- [Adk web UI- Notion MCP](docs/images/demo/2-adk-chat.png)
- [Session State](docs/images/demo/3-adk-state.png)
- [Tool call](docs/images/demo/4-adk-tool-call.png)
- [Tool response](docs/images/demo/4-adk-tool-response.png)
- [Tool response](docs/images/demo/5-notion-tools-all.png)

![HireFlow User Floe](/docs/images/architecture/hireflow_user_flow.png)

## Setup & Usage

### Prerequisites
*   Python 3.11+
*   `uv` package manager
*   Clone the repository
*   Configure your Gemini API Key
*   Configure your Notion API Key

### Configure your Gemini API Key

This project uses the [Gemini API](https://ai.google.dev/gemini-api/), which requires an API key.

1.  **Get your API key**: If you don't have one already, create an [API key in Google AI Studio](https://aistudio.google.com/app/api-keys).

### 3. Configure Environment Variables

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open `.env` and add your API keys:
    ```bash
    GOOGLE_API_KEY=your_google_api_key_here
    NOTION_API_KEY=your_notion_api_key_here #optional
    ```

### 4. Notion Integration Setup (Optional)

To enable the agent to access your Notion workspace (for employee handbook, company policies, etc.), you need to set up a Notion Integration.

👉 **[Read the Notion Setup Guide](/docs/NOTION.md)** for step-by-step instructions.

### Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    make install
    ```
3.  Set up environment variables in `.env`. as described under the Configure your Gemini API Key section.

### Running the Agent
1.  Start the MCP server in a separate terminal
    ```bash
    make mcp
    ```
2.  Start the Agent playground (i.e adk web UI):
    ```bash
    make playground
    ```
3.  Open the provided URL in your browser to interact with HireFlow.

## Test Data
Use the following sample emails to authenticate as different users:

| Name | Email | Department |
| :--- | :--- | :--- |
| **John Doe** | `john.doe@xyz.com` | Engineering |
| **Sarah Daniels** | `sarah.daniels@xyz.com` | Finance |
