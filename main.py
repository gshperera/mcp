from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

# from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import asyncio

load_dotenv()

# MCP_SERVERS = {
#     "file-service": {
#         "transport": "stdio",  # Since we run all things (ex: servers) locally
#         "command": "uv",
#         "args": ["run", "mcp_file_service.py"],
#         "cwd": ".",
#     }
# }
MCP_SERVERS = {
    "file-service": {
        "url": "http://localhost:8000/mcp",  # hosted server url
        "transport": "http",
    },
    "calc-service": {
        "url": "http://localhost:8001/mcp",  # hosted server url
        "transport": "http",
    },
}


async def run_chat():
    client = MultiServerMCPClient(MCP_SERVERS)

    tools = await client.get_tools()

    model = ChatOpenAI(model="gpt-4.1-mini")
    agent = create_agent(model, tools)

    while True:
        user_text = input("You: ").strip()

        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_text}]}
        )

        assistant_text = result["messages"][-1].content
        print(f"AI: {assistant_text}\n")


if __name__ == "__main__":
    asyncio.run(run_chat())
