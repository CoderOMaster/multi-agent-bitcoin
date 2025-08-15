import os
from agno.tools.tavily import TavilyTools
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from memory_manager import MemoryManager
import asyncio
import re
from textwrap import dedent
from groq_cli import client_groq

load_dotenv()


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

async def run_web_search_agent(message: str) -> None:
    """Run the web search agent with the given message, using shared memory."""
    memory_manager = MemoryManager()

    # Get memory and create instructions
    memory_context = memory_manager.get_memory()
    instructions = dedent(f"""\
        Major focus should be on using stackoverflow,github, forums,etc to retrieve information about code errors and depreciation.

        Here is the conversation history for your reference:
        {memory_context}
    """)

    web_agent = Agent(
        name="Web Search Agent",
        role="Handle web search requests and general research for code errors and depreciation",
        model=Groq(id="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY")),
        tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
        instructions=instructions,
    )

    
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    await web_agent.aprint_response(message, stream=True)

    sys.stdout = old_stdout
    response = captured_output.getvalue()
    # print(response)

    # Clean the response and add the interaction to memory
    # cleaned_response = clean_response(response)
    summarised_response = client_groq(response)
    print(summarised_response)

    # Clean the response and add the interaction to memory
    cleaned_response = clean_response(summarised_response)
    memory_manager.add_entry("WebSearchAgent", f"User Query: {message}\nResponse: {cleaned_response}")

# Example usage
if __name__ == "__main__":
    asyncio.run(run_web_search_agent("How to solve numpy<2 not supported"))