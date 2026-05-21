from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic_ai import Agent


class AnalysisAndOutput(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_intention: Annotated[
        str, Field(description="The true intention behind the user question")
    ]
    reasoning: Annotated[str, Field(description="Reasoning text of the model")]
    response: Annotated[str, Field(description="Final response of the question")]


agent = Agent(
    "google:gemini-3.1-flash-lite",
    instructions="Respond concisely.",
    output_type=AnalysisAndOutput,
)

resp = agent.run_sync("What is Pydantic AI?")

print(resp.output.model_dump_json(indent=2))
