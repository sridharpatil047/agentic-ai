from IPython.utils.PyColorize import pride_theme
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient
from docker_sandbox import DockerSandbox
import csv
import io
import docker
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

# 1. Start a persistent Docker container
# We use 'tail -f /dev/null' to keep the container running in the background
docker_client = docker.from_env()
container = docker_client.containers.run(
    image="python:3.12-slim",
    command=["tail", "-f", "/dev/null"],
    detach=True,
    remove=True, # Automatically cleans up the volume when stopped
    working_dir="/workspace"
)
backend = DockerSandbox(container=container,work_dir="/workspace")

# sandbox = SandboxClient().create_sandbox(name="data-analysis-agent", snapshot_name="test")
# backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model=model,
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)

rows = [
    ["Date", "Product", "Units", "Revenue"],
    ["2025-08-01", "Widget A", 10, 250],
    ["2025-08-02", "Widget B", 5, 125],
    ["2025-08-03", "Widget A", 7, 175],
    ["2025-08-04", "Widget C", 3, 90],
]
buf = io.StringIO()
csv.writer(buf).writerows(rows)
backend.upload_files([("/sales.csv", buf.getvalue().encode())])

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user", 
                "content": "Read /workspace/sales.csv and summarize total revenue by product in one sentence. Do not run shell commands."
            }
        ]
    },
    config={"recursion_limit": 8},
)

print(response["messages"][-1].content[-1].get("text"))

container.stop()
