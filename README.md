# Pydantic AI: A Comprehensive Overview

Pydantic AI is a modern Python framework designed to build type-safe AI agents with structured outputs, tool integration, and dependency injection capabilities. Built on top of Pydantic's robust data validation system, it provides a developer-friendly approach to creating reliable and maintainable AI applications.

## Development Setup

- Pyright or Pyrefly are recommended for LSP. Ty still has unsupported feature at 2026-05.
- There are [official skills](https://pydantic.dev/docs/ai/overview/coding-agent-skills/). You can add them by `npx/bunx skills add pydantic/skills`.

## Core Features

### 1. Simple Agent Creation

Getting started with Pydantic AI is straightforward. You can create an agent with just a few lines of code:

```python
from pydantic_ai import Agent

agent = Agent(
    "google:gemini-3.1-flash-lite",
    instructions="Respond concisely.",
)

resp = agent.run_sync("What is Pydantic AI?")
print(resp.output)
```

The framework supports multiple language model providers, including Google's Gemini models, and offers both synchronous and asynchronous execution methods.

### 2. Structured Output

One of Pydantic AI's most powerful features is its ability to enforce structured outputs using Pydantic models. This ensures type safety and predictable responses from your AI agents:

```python
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
```

This structured approach allows you to:

- Define precise output schemas
- Get JSON-serializable responses
- Maintain type safety throughout your application
- Document expected outputs clearly

### 3. Tool Integration

Pydantic AI allows you to extend agent capabilities by integrating custom tools. Tools enable agents to perform specific actions or access external data:

```python
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
```

The framework supports both plain tools (`@agent.tool_plain`) and context-aware tools (`@agent.tool`), providing flexibility in how agents interact with external functionality.

### 4. Dependency Injection

For more complex scenarios, Pydantic AI supports dependency injection, allowing agents to access contextual information and services:

```python
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
```

This pattern enables:

- User-specific context and personalization
- Service integration (databases, APIs, etc.)
- Multi-tenant applications
- Complex workflow orchestration

## Key Advantages

### Type Safety

Built on Pydantic's foundation, the framework ensures type safety at every level, from agent inputs to structured outputs. This reduces runtime errors and improves code reliability.

### Developer Experience

The framework provides:

- Intuitive API design
- Clear documentation through type hints
- Easy debugging with predictable structures
- Integration with modern Python development practices

### Flexibility

Support for various LLM providers, synchronous and asynchronous operations, and extensible tool systems makes Pydantic AI adaptable to diverse use cases.

### Maintainability

Structured outputs and dependency injection patterns promote clean, testable, and maintainable codebases, essential for production AI applications.

## Use Cases

Pydantic AI is particularly well-suited for:

- **Customer Support Agents**: With structured responses and user context
- **Data Analysis Systems**: Requiring structured output formats
- **Workflow Automation**: Through tool integration and dependency management
- **Multi-tenant Applications**: Leveraging dependency injection for user-specific behavior
