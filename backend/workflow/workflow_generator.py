"""
WorkFlowOS - Workflow Generator
Uses AI reasoning to synthesize structured, automated workflows from detected user activity patterns.
"""

import sys
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Fix Windows console UTF-8 output encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure project root in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.ai.grok import GrokClient, default_grok_client


WORKFLOW_GENERATION_PROMPT = """
You are the Workflow Synthesizer engine of WorkFlowOS.
Your job is to analyze a detected repetitive sequence of tool interactions and convert it into a structured, production-ready autonomous workflow template.

Output ONLY a valid JSON object matching this schema:
{
    "name": "<Descriptive Name of Workflow>",
    "description": "<Concise summary of what this workflow automates>",
    "trigger": "<Trigger event that initiates this workflow>",
    "actions": [
        "<Action 1 name>",
        "<Action 2 name>",
        ...
    ],
    "steps": [
        {
            "step": 1,
            "action": "<tool_function_name>",
            "name": "<User friendly step title>",
            "description": "<What this step accomplishes>"
        }
    ],
    "condition": "<Safety / human-in-the-loop fallback condition>",
    "confidence": <float between 0.0 and 1.0>,
    "estimated_time_saved_minutes": <integer>
}
"""


class WorkflowGenerator:
    """
    Generates high-level workflow definitions and blueprints using AI analysis.
    """

    def __init__(self, ai_client: Optional[GrokClient] = None):
        self.ai_client = ai_client or default_grok_client

    def generate(self, detected_workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a complete structured workflow specification from detected sequence data.
        """
        user_prompt = f"""Synthesize an autonomous workflow from this detected activity pattern:

Detected Pattern Data:
{json.dumps(detected_workflow, indent=2)}

Generate the complete workflow specification in JSON format."""

        try:
            workflow = self.ai_client.chat_json(WORKFLOW_GENERATION_PROMPT, user_prompt)
        except Exception as e:
            print(f"⚠️ Error during AI workflow generation: {e}. Falling back to default template.")
            workflow = self._fallback_template(detected_workflow)

        # Merge metadata from detection if not provided
        if "occurrences" not in workflow and "occurrences" in detected_workflow:
            workflow["occurrences"] = detected_workflow["occurrences"]

        return workflow

    def _fallback_template(self, detected: Dict[str, Any]) -> Dict[str, Any]:
        sequence = detected.get("sequence", [])
        return {
            "name": "Automated Multi-Step Workflow",
            "description": "Automatically executes sequential actions based on detected repeating pattern.",
            "trigger": "Triggered by initial sequence event",
            "actions": sequence,
            "steps": [
                {"step": i + 1, "action": act, "name": act.replace("_", " ").title(), "description": f"Execute {act}"}
                for i, act in enumerate(sequence)
            ],
            "condition": "If any step fails, escalate to human supervisor",
            "confidence": detected.get("average_similarity", 0.9),
            "estimated_time_saved_minutes": 10
        }

    def display_workflow(self, workflow: Dict[str, Any]):
        """
        Renders a cleanly formatted representation of the generated workflow in terminal.
        """
        print("\n" + "=" * 65)
        print("  WORKFLOW DEFINITION BLUEPRINT")
        print("=" * 65)
        print(f"  Name:        {workflow.get('name', 'Untitled Workflow')}")
        print(f"  Trigger:     {workflow.get('trigger', 'Manual')}")
        print(f"  Condition:   {workflow.get('condition', 'None')}")
        if "confidence" in workflow:
            print(f"  Confidence:  {workflow.get('confidence') * 100:.1f}%")
        if "estimated_time_saved_minutes" in workflow:
            print(f"  Time Saved:  ~{workflow.get('estimated_time_saved_minutes')} minutes / run")
        print("-" * 65)
        print("  Execution Steps:")

        steps = workflow.get("steps", [])
        if steps:
            for s in steps:
                step_num = s.get("step", "#")
                name = s.get("name", s.get("action", "Step"))
                action = s.get("action", "")
                desc = s.get("description", "")
                print(f"    [{step_num}] {name} ({action})")
                if desc:
                    print(f"        -> {desc}")
        else:
            for idx, action in enumerate(workflow.get("actions", []), 1):
                print(f"    [{idx}] {action}")

        print("=" * 65 + "\n")
