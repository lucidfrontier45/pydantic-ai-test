from pydantic_ai import Agent

agent = Agent(
    "google:gemini-3.1-flash-lite",
    instructions="Respond concisely.",
)

resp = agent.run_sync("What is Pydantic AI?")

print(resp.output)
