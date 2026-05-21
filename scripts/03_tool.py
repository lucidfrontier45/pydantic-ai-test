from datetime import UTC, datetime

from pydantic_ai import Agent

agent = Agent(
    "google:gemini-3-flash-preview",
    instructions=(
        "Respond concisely.",
        "Always append current timestamp at the beginning of the response.",
    ),
)


@agent.tool_plain
def get_current_timestamp() -> str:
    """Get the current timestamp in ISO format."""
    return datetime.now(tz=UTC).isoformat()


resp = agent.run_sync("What is Pydantic AI?")

print(resp.output)
