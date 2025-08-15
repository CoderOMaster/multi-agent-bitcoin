# Multi-Agent Code Generation

This project is a multi-agent system designed for code generation and related tasks. It leverages multiple specialized agents, each with a specific function, to provide a comprehensive and powerful coding assistant. The system is orchestrated by a meta-agent that routes user queries to the most appropriate agent based on the nature of the request.

## Features

- **Multi-Agent Architecture**: The system uses a modular, multi-agent approach, with specialized agents for:
  - **Code Execution**: Running Python code in a sandboxed environment.
  - **Web Search**: Searching the web for information.
  - **Knowledge Graph**: Storing and retrieving information from a knowledge graph.
- **Intelligent Routing**: A meta-agent intelligently routes user queries to the most suitable agent.
- **Contextual Memory**: The system maintains a conversational log in `chat.md` and a summarized memory of agent responses in `memory.md`. This provides rich context for interactions and serves as a simple implementation of an agent-to-agent communication protocol.
- **Extensible**: The architecture is designed to be easily extensible with new agents and capabilities.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7+
- Pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/multi-agent-bitcoin.git
   cd multi-agent-bitcoin
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**
   - Create a `.env` file in the root directory of the project.
   - Add your API keys to the `.env` file:
     ```
     GROQ_API_KEY=your_groq_api_key
     ```

## Usage

To start the multi-agent system, run the orchestrator:

```bash
python orchestrator.py
```

You can then interact with the system by typing your queries into the console.

## Project Structure

- `orchestrator.py`: The main entry point of the application. It initializes and coordinates the agents.
- `memory_manager.py`: Manages the conversation history and memory of the system.
- `python_code_runner.py`: The agent responsible for executing Python code.
- `web_search.py`: The agent that performs web searches.
- `deepgraph_mcp.py`: The agent that interacts with the knowledge graph.
- `groq_cli.py`: A command-line interface for interacting with the Groq API.
- `requirements.txt`: A list of the Python packages required by the project.
- `.env`: A file for storing environment variables (not included in the repository).
- `memory.md`: Stores a summarized log of responses from each agent, providing a memory of past actions and outcomes.
- `chat.md`: A log of the conversation between the user and the system.

