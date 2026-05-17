import json
import subprocess
import sys
from pathlib import Path

import pydantic_ai
from dotenv import load_dotenv

load_dotenv()

agent = pydantic_ai.Agent(
    "google:gemini-2.5-flash", instructions="You are an AI assistant"
)


@agent.tool_plain(description="Search for content pattern in files using ripgrep.")
def ripgrep_search(pattern: str, path: str) -> str:
    result = subprocess.run(["rg", pattern, path], capture_output=True, text=True)
    return result.stdout or result.stderr


@agent.tool_plain(description="Find files matching name pattern using fd-find.")
def fd_find(pattern: str, path: str) -> str:
    result = subprocess.run(["fd", pattern, path], capture_output=True, text=True)
    return result.stdout or result.stderr


@agent.tool_plain(description="Read entire file")
def read_file(path: str) -> str:
    return open(path).read()


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
    all_msg_json = result.all_messages_json()
    messages = json.loads(all_msg_json)
    counters = {"user": 0, "ai": 0, "call": 0, "output": 0}

    for msg in messages:
        for part in msg.get("parts", []):
            kind = part.get("part_kind")
            content = part.get("content", "")

            if kind == "user-prompt":
                counters["user"] += 1
                print(f"[User Prompt #{counters['user']}]\n{content}\n")
            elif kind == "text":
                counters["ai"] += 1
                print(f"[AI Message #{counters['ai']}]\n{content}\n")
            elif kind == "tool-call":
                counters["call"] += 1
                tool_name = part.get("tool_name", "")
                args = part.get("args", {})
                print(f"[Tool Call #{counters['call']}]\n{tool_name}({args})\n")
            elif kind == "tool-return":
                counters["output"] += 1
                tool_name = part.get("tool_name", "")
                print(
                    f"[Tool Output #{counters['output']}]\n{tool_name} -> {content}\n"
                )

    print("# Final Output\n")
    print(result.output)
