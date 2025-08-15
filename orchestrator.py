import asyncio
import os
from textwrap import dedent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up necessary API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

from agno.agent import Agent
from memory_manager import MemoryManager
from agno.models.groq import Groq
from python_code_runner import run_mcp_agent
from web_search import run_web_search_agent
from deepgraph_mcp import run_codex
from pydantic import BaseModel, Field

class AgentName(BaseModel):
    symbol: str = Field(..., description="Agent Name")

class MetaAgent:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.agents = {
            "python_code_runner": run_mcp_agent,
            "web_search": run_web_search_agent,
            "knowledge_graph": run_codex,
        }

        self.router_agent = Agent(
            model=Groq(id='openai/gpt-oss-20b', api_key=os.getenv("GROQ_API_KEY")),
            instructions="You are a router agent. Your job is to route the user's query to the appropriate agent. The available agents are: python_code_runner, web_search, knowledge_graph. Return the name of the agent to use without any additional text, symbols like ** etc",
            markdown=True,
            response_model=AgentName,
            show_tool_calls=True,
        )

    async def route_query(self, query):
        # Add the user query to memory
      
        response_object = self.router_agent.run(query)
        agent_name_str = response_object.content.symbol.strip().strip('`')
        print(agent_name_str)
        agent = self.agents.get(agent_name_str)
        self.memory_manager.add_memory_chat_convo(query, agent_name_str)
        if agent:
            # Run the selected agent with the query
            response = await agent(query)
            self.memory_manager.add_entry(agent_name_str,response)
            return response
        else:
            return "Could not find an appropriate agent to handle your query."


async def main():
    # Initialize the memory manager
    memory_manager = MemoryManager()

    # Initialize the meta agent
    meta_agent = MetaAgent(memory_manager)

    # Start the conversation loop
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        response = await meta_agent.route_query(query)
        print(f"AI: {response}")


if __name__ == "__main__":
    asyncio.run(main())
