#!/usr/bin/env python3
"""
Picnic MCP client wrapper.
Calls mcp-picnic tools via stdio JSON-RPC.

Usage: picnic.py <tool_name> '<json_args>'

Examples:
  picnic.py picnic_search '{"query": "havermelk", "limit": 5}'
  picnic.py picnic_add_to_cart '{"productId": "s1010217", "count": 2}'
  picnic.py picnic_get_cart '{}'
  picnic.py picnic_remove_from_cart '{"productId": "s1010217", "count": 1}'
  picnic.py picnic_clear_cart '{}'
  picnic.py picnic_get_delivery_slots '{}'
  picnic.py picnic_get_user_details '{}'
"""

import json
import os
import subprocess
import sys
import threading

MCP_SERVER = "/data/.npm-global/lib/node_modules/mcp-picnic/dist/bundle.js"
SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/.secrets/picnic.env")


def load_env():
    """Load Picnic credentials from .env file into os.environ."""
    if not os.path.exists(SECRETS_FILE):
        return
    with open(SECRETS_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            if "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip('"').strip("'")
                os.environ[key] = val
    # Map env var names to what mcp-picnic expects
    if "PICNIC_EMAIL" in os.environ and "PICNIC_USERNAME" not in os.environ:
        os.environ["PICNIC_USERNAME"] = os.environ["PICNIC_EMAIL"]
    if "PICNIC_AUTH_TOKEN" in os.environ and "PICNIC_AUTH_KEY" not in os.environ:
        os.environ["PICNIC_AUTH_KEY"] = os.environ["PICNIC_AUTH_TOKEN"]


def call_tool(tool_name: str, args: dict) -> dict:
    """Call a Picnic MCP tool via stdio and return the result."""
    load_env()

    init_msg = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mickey", "version": "1.0"}
        }
    })
    tool_msg = json.dumps({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    })

    proc = subprocess.Popen(
        ["node", MCP_SERVER],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=os.environ.copy()
    )

    result_holder = {}
    stderr_lines = []

    def read_stdout():
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg.get("id") == 2:
                    result_holder["response"] = msg
                    proc.stdin.close()
                    proc.kill()
                    return
            except json.JSONDecodeError:
                pass

    def read_stderr():
        for line in proc.stderr:
            stderr_lines.append(line)

    t_out = threading.Thread(target=read_stdout, daemon=True)
    t_err = threading.Thread(target=read_stderr, daemon=True)
    t_out.start()
    t_err.start()

    # Send messages
    proc.stdin.write(init_msg + "\n")
    proc.stdin.flush()
    proc.stdin.write(tool_msg + "\n")
    proc.stdin.flush()

    # Wait for response (up to 20s)
    t_out.join(timeout=20)
    proc.kill()
    proc.wait()

    if "response" in result_holder:
        return result_holder["response"]

    stderr_text = "".join(stderr_lines)
    return {"error": f"No response from MCP server.\n{stderr_text[:500]}"}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    tool_name = sys.argv[1]
    args_raw = sys.argv[2] if len(sys.argv) > 2 else "{}"

    try:
        args = json.loads(args_raw)
    except json.JSONDecodeError as e:
        print(f"Error parsing args JSON: {e}", file=sys.stderr)
        sys.exit(1)

    result = call_tool(tool_name, args)

    if "result" in result:
        content = result["result"].get("content", [])
        is_error = result["result"].get("isError", False)
        for item in content:
            if item.get("type") == "text":
                text = item["text"]
                try:
                    parsed = json.loads(text)
                    print(json.dumps(parsed, indent=2, ensure_ascii=False))
                except json.JSONDecodeError:
                    print(text)
        if is_error:
            sys.exit(1)
    elif "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
