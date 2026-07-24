from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import pathlib
import requests
from sql_tools import tools
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

# Downloading the SQLite database from the URL
url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# response = model.invoke("Hey! how are you?")
# print(response.content[-1]['text'])

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
        You are a SQL agent that can answer questions about the Chinook database. 
        Use the available tools to answer the user's questions.
        Use not special characters in the output, only letters and numbers and new lines.
        If a question is not related to the database, say "Sorry! I cannot answer that question because it is not related to the database."
    """
)

# response = agent.invoke({
#     "messages": [{"role": "user", "content": "Hi, how are you?"}]
# })  
# print(response["messages"][-1].content[-1]['text'])

# question = "What is the capital of Canada?"
# question = "What is this database all about? Give me a brief overview."
# question = "List available tables. Then please drop a table named Artist and list all available tables"
question = "List available tables."

response = agent.invoke({
    "messages": [{"role": "user", "content": question}]
})

print(response["messages"][-1].content[-1]['text'])

# stream = agent.stream_events(
#     {"messages": [{"role": "user", "content": question}]},
#     version="v3",
# )
# print("-----------")
# for kind, item in stream.interleave("messages", "tool_calls"):
#     if kind == "messages":
#         for token in item.text:
#             print(token, end="", flush=True)
#     elif kind == "tool_calls":
#         print(f"\nTool call: {item.tool_name}({item.input})")
#         for delta in item.output_deltas:
#             print(delta, end="", flush=True)
#         print(f"\nTool result: {item.output}")

# final_state = stream.output
# print()
# print("-------")
