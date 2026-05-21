import logging
import subprocess
import sys
from pathlib import Path

import pydantic_ai

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger("tools")

agent = pydantic_ai.Agent(
    "google:gemini-3.1-flash-lite", instructions="You are an AI assistant"
)


@agent.tool_plain(description="Search for content pattern in files using ripgrep.")
def ripgrep_search(pattern: str, path: str) -> str:
    logger.info("RG_TOOL: INPUT pattern=%r path=%r", pattern, path)
    result = subprocess.run(
        ["rg", pattern, path], capture_output=True, encoding="utf-8", errors="replace"
    )
    output = result.stdout or result.stderr
    logger.info(f"OUTPUT: {output}")
    return output


@agent.tool_plain(description="Find files matching name pattern using fd-find.")
def fd_find(pattern: str, path: str) -> str:
    logger.info("FD_TOOL: INPUT pattern=%r path=%r", pattern, path)
    result = subprocess.run(
        ["fd", pattern, path], capture_output=True, encoding="utf-8", errors="replace"
    )
    output = result.stdout or result.stderr
    logger.info(f"OUTPUT: {output}")
    return output


@agent.tool_plain(description="Read entire file")
def read_file(path: str) -> str:
    logger.info("READ_TOOL: INPUT path=%r", path)
    with open(path, encoding="utf8") as fp:
        output = fp.read()
    return output


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
        prompt = f"Use only files in directory {target_dir} to respond\n\n{prompt}"

    result = agent.run_sync(prompt)

    print("# Final Output\n")
    print(result.output)
