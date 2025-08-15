from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.groq import Groq
import os
from dotenv import load_dotenv
from memory_manager import MemoryManager
import asyncio
from textwrap import dedent
from agno.tools.mcp import StdioServerParameters
import re
from io import StringIO
from groq_cli import client_groq
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

server_params = StdioServerParameters(
    command="/home/keshav/anaconda3/bin/mcp-proxy",
    args=["http://localhost:6000/sse"],
)

async def run_mcp_agent(message: str) -> None:
    """Run the filesystem agent with the given message, using shared memory."""
    memory_manager = MemoryManager()

    async with MCPTools(server_params=server_params) as mcp_tools:
        # Get memory and create instructions
        memory_context = memory_manager.get_memory()
        instructions = dedent(f"""\
            You are a python code executor assistant. Run the code provided by user strictly by using mcp tools provided to you. First create a sandbox environment by calling the tool then use the execute code tool to run the code. If its already created use existing one.
            Strictly calculate using tool and not your reasoning.

            Here is the conversation history for your reference:
            {memory_context}
        """)

        # Use the MCP tools with an Agent
        agent = Agent(
            model=Groq(id='openai/gpt-oss-20b', api_key=os.getenv("GROQ_API_KEY")),
            tools=[mcp_tools],
            instructions=instructions,
            markdown=True,
            show_tool_calls=False,
        )

        # Run the agent and get the response
        # response = await agent.run_response(message)

        def clean_response(text):
            """Removes ANSI escape codes and other terminal formatting from a string."""
            # Remove ANSI escape codes
            text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)
            # Remove box-drawing characters and other symbols
            text = re.sub(r'[┏━┃┗┛┓│─•]', '', text)
            # Remove the headers
            text = re.sub(r' (Message|Tool Calls|Response \(\d+\.\d+s\)) ', '', text)
            # Remove lines that are just whitespace and strip leading/trailing whitespace from all lines
            text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
            return text

        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        await agent.aprint_response(message, stream=True)

    sys.stdout = old_stdout
    response = captured_output.getvalue()
    print(response)
    summarised_response = client_groq(response)

    # Clean the response and add the interaction to memory
    # cleaned_response = clean_response(response)
    memory_manager.add_entry("CodeRunnerAgent", f"User Query: {message}\nResponse: {summarised_response}")

# Example usage
if __name__ == "__main__":
    # Basic example - exploring project license
    asyncio.run(run_mcp_agent("print(1 ^ 2 + 2 * 3**10)"))