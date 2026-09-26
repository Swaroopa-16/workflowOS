"""
WorkFlowOS - Autonomous Workflow Agent
Coordinates AI reasoning, step planning, tool execution, and self-correction.
"""

import sys
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Reconfigure Windows stdout to UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.ai.grok import GrokClient, default_grok_client
from backend.ai.prompts import SYSTEM_PROMPT, build_step_prompt
from backend.agent.executor import Executor

# Load environment
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=root_dir / ".env")


# ============================================================
# MOCK TOOLS
# ============================================================

class MockTools:
    """Mock implementations for Gmail, CRM, and Slack integrations."""

    def gmail_read_email(self) -> Dict[str, Any]:
        print("\n[Gmail] Reading customer email...")
        return {
            "success": True,
            "customer": "ABC Ltd",
            "email": "customer@abc.com",
            "request": "New quotation required",
            "attachment": "quotation.pdf"
        }

    def gmail_download_attachment(self, filename: str) -> Dict[str, Any]:
        print(f"\n[Gmail] Downloading attachment: {filename}...")
        return {
            "success": True,
            "file": filename
        }

    def crm_search_customer(self, customer: str) -> Dict[str, Any]:
        print(f"\n[CRM] Searching for customer: {customer}...")
        if customer == "ABC Ltd":
            return {
                "success": True,
                "customer_id": "CRM-001",
                "customer": customer
            }
        return {
            "success": False,
            "error": "Customer not found"
        }

    def crm_update_customer(self, customer_id: str, request: str, attachment: str) -> Dict[str, Any]:
        print(f"\n[CRM] Updating customer {customer_id}...")
        return {
            "success": True,
            "message": "Customer record updated"
        }

    def slack_send_message(self, channel: str, message: str) -> Dict[str, Any]:
        print(f"\n[Slack] Sending message to {channel}...")
        print(f"        {message}")
        return {
            "success": True,
            "message": "Slack notification sent"
        }


# ============================================================
# WORKFLOW AGENT
# ============================================================

class WorkFlowAgent:
    """Autonomous agent that reasons through workflows and executes tools."""

    def __init__(self, ai_client: Optional[GrokClient] = None, tools: Optional[Any] = None):
        self.ai_client = ai_client or default_grok_client
        self.tools = tools or MockTools()
        self.executor = Executor(self.tools)
        self.history = []
        self.completed = False

    def ask_ai(self, workflow: dict, history: list) -> Dict[str, Any]:
        """Queries the AI reasoning engine for the next atomic action."""
        step_prompt = build_step_prompt(workflow, history)
        return self.ai_client.chat_json(SYSTEM_PROMPT, step_prompt)

    def run(self, workflow: dict, max_steps: int = 15) -> Dict[str, Any]:
        """Runs the autonomous workflow execution loop."""
        print("\n===================================")
        print("[AGENT] WorkFlowOS Agent Started")
        print(f"[AI] Provider: {self.ai_client.provider} (Model: {self.ai_client.model})")
        print("===================================")
        print("\nDetected workflow:")
        print(json.dumps(workflow, indent=2))

        context = {
            "workflow": workflow,
            "history": []
        }

        for step in range(max_steps):
            print(f"\n\n========== AGENT STEP {step + 1} ==========")

            try:
                decision = self.ask_ai(workflow, context["history"])
            except Exception as e:
                print(f"[ERROR] During AI reasoning: {e}")
                return {
                    "status": "error",
                    "error": str(e),
                    "history": context["history"]
                }

            print("\n[DECISION] AI Decision:")
            print(json.dumps(decision, indent=2))

            action = decision.get("action")
            parameters = decision.get("parameters", {})

            # Handle Complete
            if action == "complete":
                print("\n[OK] WORKFLOW COMPLETED SUCCESSFULLY")
                self.completed = True
                return {
                    "status": "completed",
                    "reason": decision.get("reason"),
                    "history": context["history"]
                }

            # Handle Human Intervention Required
            if action == "ask_user":
                print("\n[PAUSE] Agent needs human intervention")
                return {
                    "status": "needs_user",
                    "reason": decision.get("reason"),
                    "history": context["history"]
                }

            # Execute Tool via Executor
            result = self.executor.execute(action, parameters)
            print("\n[RESULT] Tool Execution Result:")
            print(json.dumps(result, indent=2))

            # Record history
            context["history"].append({
                "action": action,
                "parameters": parameters,
                "result": result,
                "reason": decision.get("reason")
            })

        return {
            "status": "failed",
            "reason": "Maximum agent steps reached",
            "history": context["history"]
        }


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    discovered_workflow = {
        "name": "Process Customer Request",
        "trigger": "New customer request in Gmail",
        "actions": [
            "Read customer email",
            "Download attachment",
            "Find customer in CRM",
            "Update customer record",
            "Notify team in Slack"
        ],
        "condition": "If customer cannot be found, ask user"
    }

    agent = WorkFlowAgent()
    result = agent.run(discovered_workflow)

    print("\n\n===================================")
    print("FINAL RESULT")
    print("===================================")
    print(json.dumps(result, indent=2))