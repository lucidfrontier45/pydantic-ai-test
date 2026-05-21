from dataclasses import dataclass

from pydantic_ai import Agent, RunContext


@dataclass(frozen=True)
class User:
    name: str
    email: str


agent = Agent(
    "google:gemini-3.1-flash-lite",
    instructions="Respond concisely. The response must also be sent to user's email address too.",
    deps_type=User,
)


@agent.tool
async def send_email(ctx: RunContext[User], msg: str) -> None:
    mail_msg = f"""--------------------------------------------
TO: {ctx.deps.email}

Hello {ctx.deps.name}. Here is the response to your question.
{msg}
---------------------------------------------
"""
    print(mail_msg)


user = User(name="James", email="jjj@dummymail.com")

resp = agent.run_sync("What is Pydantic AI?", deps=user)
print("--------OUTPUT--------------")
print(resp.output)
