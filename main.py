import subprocess
import sys
from pathlib import Path

import pydantic_ai
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)

agent = pydantic_ai.Agent(
    "google:gemini-2.5-flash", instructions="You are an AI assistant"
)


@agent.tool_plain(description="Search for content pattern in files using ripgrep.")
def ripgrep_search(pattern: str, path: str) -> str:
    result = subprocess.run(
        ["rg", pattern, path], capture_output=True, encoding="utf-8", errors="replace"
    )
    return result.stdout or result.stderr


@agent.tool_plain(description="Find files matching name pattern using fd-find.")
def fd_find(pattern: str, path: str) -> str:
    result = subprocess.run(
        ["fd", pattern, path], capture_output=True, encoding="utf-8", errors="replace"
    )
    return result.stdout or result.stderr


@agent.tool_plain(description="Read entire file")
def read_file(path: str) -> str:
    return open(path, encoding="utf8").read()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [target_dir] <prompt>")
        sys.exit(1)

    target_dir = (
        Path(sys.argv[1]) if len(sys.argv) > 1 and Path(sys.argv[1]).is_dir() else None
    )
    prompt_args = sys.argv[2:] if target_dir else sys.argv[1:]

    if not prompt_args:
        print("Usage: python main.py [target_dir] <prompt>")
        sys.exit(1)

    prompt = " ".join(prompt_args)
    if target_dir:
        prompt = f"Use files in directory {target_dir} to response\n\n{prompt}"

    result = agent.run_sync(prompt)
    messages = result.all_messages()
    counters = {"user": 0, "ai": 0, "call": 0, "output": 0}

    for msg in messages:
        for part in msg.parts:
            part_type = type(part).__name__
            if isinstance(part, UserPromptPart):
                print(f"[{part_type}]\n<Input>:\n{part.content}\n")
            elif isinstance(part, TextPart):
                print(f"[{part_type}]\n<Output>:\n{part.content}\n")
            elif isinstance(part, ToolCallPart):
                print(
                    f"[{part_type}]\n<Output>:\ntool={part.tool_name} args={part.args!r}\n"
                )
            elif isinstance(part, ToolReturnPart):
                print(f"[{part_type}]\n<Input>:\ntool={part.tool_name}")
                print(part.content)
            elif isinstance(part, ModelRequest):
                print(f"[{part_type}]\n<Input>:\n{part.parts!r}\n")
            elif isinstance(part, ModelResponse):
                print(f"[{part_type}]\n")
                print(part.parts)

    print("# Final Output\n")
    print(result.output)
