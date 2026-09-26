"""
WorkFlowOS - Grok / AI Integration Verification Test
Tests environment variables, Grok AI client connectivity, response parsing, and agent loop.
"""

import sys
import os
import json
from pathlib import Path

# Fix Windows console UTF-8 output encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.ai.grok import GrokClient
from backend.ai.parser import parse_ai_json_response
from backend.ai.prompts import SYSTEM_PROMPT
from backend.agent.agent import WorkFlowAgent


def print_banner(title: str):
    print("\n" + "=" * 60)
    print(f"[*] {title}")
    print("=" * 60)


def test_parser():
    print_banner("1. Testing AI JSON Parser")
    sample_outputs = [
        '{"action": "crm_search_customer", "parameters": {"customer": "ABC Ltd"}, "reason": "Lookup"}',
        '```json\n{"action": "complete", "parameters": {}, "reason": "Done"}\n```',
        'Here is the JSON you requested:\n{"action": "slack_send_message", "parameters": {"channel": "#general", "message": "Hi"}, "reason": "Notify"}'
    ]

    for idx, text in enumerate(sample_outputs, 1):
        parsed = parse_ai_json_response(text)
        assert isinstance(parsed, dict) and "action" in parsed, f"Failed on sample {idx}"
        print(f"  [OK] Sample {idx} parsed successfully: action = '{parsed['action']}'")


def test_ai_client():
    print_banner("2. Testing AI Client & Provider Detection")
    client = GrokClient()
    print(f"  Active Provider: {client.provider}")
    print(f"  Active Model:    {client.model}")
    print(f"  Is Mock Mode:    {client.is_mock}")

    if client.is_mock:
        print("  [INFO] No API key found in .env. Running in Mock/Simulation Mode.")
        print("         To use real Grok/Groq/OpenAI, set XAI_API_KEY or GROQ_API_KEY in .env.")

    test_user_prompt = "Initial trigger: Read new customer email in Gmail. History: []"
    result = client.chat_json(SYSTEM_PROMPT, test_user_prompt)
    print(f"  [OK] AI Decision Output:\n{json.dumps(result, indent=4)}")
    assert "action" in result, "AI output missing 'action' key"


def test_agent_execution():
    print_banner("3. Testing End-to-End WorkFlowAgent Execution")
    workflow = {
        "name": "Process Customer Request",
        "trigger": "New customer request in Gmail",
        "actions": [
            "Read customer email",
            "Download attachment",
            "Find customer in CRM",
            "Update customer record",
            "Notify team in Slack"
        ]
    }

    agent = WorkFlowAgent()
    result = agent.run(workflow, max_steps=10)

    print("\n  Workflow Execution Result Status:", result.get("status"))
    assert result.get("status") == "completed", f"Expected completed status, got {result.get('status')}"
    print(f"  [OK] Workflow completed in {len(result['history'])} steps.")


def main():
    print("============================================================")
    print(">> Running WorkFlowOS AI & Grok Test Suite")
    print("============================================================")
    
    try:
        test_parser()
        test_ai_client()
        test_agent_execution()
        print("\n" + "=" * 60)
        print("[SUCCESS] ALL TESTS PASSED SUCCESSFULLY! No errors detected.")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()