"""Quick standalone connectivity test — run directly with venv python."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from conf.runner import MCPConversationRunner


async def main():
    print("[1] Creating runner...", flush=True)
    runner = MCPConversationRunner()
    print("[2] Entering context (connect + initialize + list_tools)...", flush=True)
    async with runner:
        print(f"[3] Connected! {len(runner.tools)} tools available.", flush=True)
        print("[4] Running a quick prompt...", flush=True)
        result = await runner.run("Who am I on CloudBees?")
        print(f"[5] Done. Final text: {result.final_text[:200]}", flush=True)
        print(f"    Tool calls: {[tc.name for tc in result.tool_calls]}", flush=True)
    print("[6] Disconnected cleanly.", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
