import json
from backend.ai.grok import GrokClient


class WorkflowReplanner:

    def __init__(self, grok_client=None):
        self.grok = grok_client or GrokClient()

    def replan(
        self,
        workflow,
        current_plan,
        failed_step,
        tool_result,
        execution_history=None
    ):

        system_prompt = """
You are the Replanning Engine of WorkFlowOS.

Analyze the workflow execution result and decide what
the agent should do next.

Allowed decisions:

retry
alternative
continue
ask_user
complete

Return ONLY valid JSON.

Format:

{
    "decision": "retry",
    "reason": "Why this decision was selected",
    "next_action": {
        "tool": "tool_name",
        "parameters": {}
    },
    "message": "Message for the user"
}
"""

        user_prompt = f"""
Original Workflow:
{json.dumps(workflow, indent=2)}

Current Plan:
{json.dumps(current_plan, indent=2)}

Failed Step:
{json.dumps(failed_step, indent=2)}

Tool Result:
{json.dumps(tool_result, indent=2)}

Execution History:
{json.dumps(
    execution_history or [],
    indent=2
)}

Decide what the agent should do next.

Return ONLY JSON.
"""

        decision = self.grok.chat_json(
            system_prompt,
            user_prompt
        )

        # If the AI response is not in the expected
        # replanner format, create a safe fallback.
        if "decision" not in decision:

            decision = {
                "decision": "ask_user",

                "reason": (
                    "The workflow step failed and "
                    "the agent requires human guidance."
                ),

                "next_action": {},

                "message": (
                    "I could not safely continue "
                    "the workflow. Please check the "
                    "failed step."
                )
            }

        self._validate_decision(decision)

        self.display_decision(decision)

        return decision

    def _validate_decision(self, decision):

        valid_decisions = {
            "retry",
            "alternative",
            "continue",
            "ask_user",
            "complete"
        }

        if not isinstance(decision, dict):

            raise ValueError(
                "Replanner response must be a dictionary."
            )

        if "decision" not in decision:

            raise ValueError(
                "Replanner response missing 'decision'."
            )

        if decision["decision"] not in valid_decisions:

            raise ValueError(
                f"Invalid replanner decision: "
                f"{decision['decision']}"
            )

        if "reason" not in decision:

            decision["reason"] = (
                "No reason provided."
            )

        if "next_action" not in decision:

            decision["next_action"] = {}

        if "message" not in decision:

            decision["message"] = ""

        return True

    def display_decision(self, decision):

        print("\n" + "=" * 60)
        print("🧠 AGENT REPLANNING")
        print("=" * 60)

        print(
            f"\nDecision: "
            f"{decision['decision']}"
        )

        print(
            f"\nReason:\n"
            f"{decision['reason']}"
        )

        next_action = decision.get(
            "next_action",
            {}
        )

        if next_action:

            print("\nNext Action:")

            print(
                f"    Tool: "
                f"{next_action.get('tool')}"
            )

            print(
                f"    Parameters: "
                f"{next_action.get('parameters', {})}"
            )

        if decision.get("message"):

            print(
                f"\nAgent Message:\n"
                f"{decision['message']}"
            )

        print("=" * 60)