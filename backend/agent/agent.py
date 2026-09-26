import os
import json
from groq import Groq


# ============================================================
# GROK CLIENT
# ============================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# MOCK TOOLS
# These will later be replaced with real Gmail / CRM / Slack
# ============================================================

class MockTools:

    def gmail_read_email(self):
        print("\n📧 Gmail: Reading customer email...")

        return {
            "success": True,
            "customer": "ABC Ltd",
            "email": "customer@abc.com",
            "request": "New quotation required",
            "attachment": "quotation.pdf"
        }

    def gmail_download_attachment(self, filename):
        print(f"\n📎 Gmail: Downloading {filename}...")

        return {
            "success": True,
            "file": filename
        }

    def crm_search_customer(self, customer):
        print(f"\n🏢 CRM: Searching for {customer}...")

        # Change to False to test agent recovery
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

    def crm_update_customer(self, customer_id, request, attachment):
        print(f"\n🏢 CRM: Updating customer {customer_id}...")

        return {
            "success": True,
            "message": "Customer record updated"
        }

    def slack_send_message(self, channel, message):
        print(f"\n💬 Slack: Sending message to {channel}...")
        print(f"   {message}")

        return {
            "success": True,
            "message": "Slack notification sent"
        }


tools = MockTools()


# ============================================================
# TOOL DEFINITIONS FOR GROK
# ============================================================

TOOL_DEFINITIONS = {
    "gmail_read_email": {
        "description": "Read the latest customer email",
        "parameters": {}
    },

    "gmail_download_attachment": {
        "description": "Download an email attachment",
        "parameters": {
            "filename": "string"
        }
    },

    "crm_search_customer": {
        "description": "Search for a customer in the CRM",
        "parameters": {
            "customer": "string"
        }
    },

    "crm_update_customer": {
        "description": "Update a customer record",
        "parameters": {
            "customer_id": "string",
            "request": "string",
            "attachment": "string"
        }
    },

    "slack_send_message": {
        "description": "Send a notification to Slack",
        "parameters": {
            "channel": "string",
            "message": "string"
        }
    }
}


# ============================================================
# GROK AGENT
# ============================================================

class WorkFlowAgent:

    def __init__(self):
        self.history = []
        self.completed = False

    def ask_grok(self, instruction):

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": """
You are the reasoning engine of WorkFlowOS.

You are an agentic workflow automation agent.

Your job is to:

1. Understand the discovered workflow.
2. Decide the next action.
3. Select an available tool.
4. Examine the tool result.
5. Decide what to do next.
6. Recover from failures when possible.
7. Stop and request human intervention when necessary.

IMPORTANT:
- Never invent tool results.
- Only use available tools.
- Do not execute multiple actions at once.
- After every tool result, reason about the next action.
- Return ONLY valid JSON.

Available tools:

gmail_read_email
gmail_download_attachment
crm_search_customer
crm_update_customer
slack_send_message

JSON format:

{
    "action": "tool_name | complete | ask_user",
    "parameters": {},
    "reason": "short explanation"
}
"""
                },

                {
                    "role": "user",
                    "content": instruction
                }
            ],

            temperature=0.1
        )

        content = response.choices[0].message.content

        # Remove markdown code fences if Grok returns them
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        return json.loads(content)

    # --------------------------------------------------------

    def execute_tool(self, action, parameters):

        if action == "gmail_read_email":
            return tools.gmail_read_email()

        elif action == "gmail_download_attachment":
            return tools.gmail_download_attachment(
                parameters["filename"]
            )

        elif action == "crm_search_customer":
            return tools.crm_search_customer(
                parameters["customer"]
            )

        elif action == "crm_update_customer":
            return tools.crm_update_customer(
                parameters["customer_id"],
                parameters["request"],
                parameters["attachment"]
            )

        elif action == "slack_send_message":
            return tools.slack_send_message(
                parameters["channel"],
                parameters["message"]
            )

        return {
            "success": False,
            "error": "Unknown tool"
        }

    # --------------------------------------------------------

    def run(self, workflow):

        print("\n===================================")
        print("🤖 WorkFlowOS Agent Started")
        print("===================================")

        print("\nDetected workflow:")
        print(workflow)

        context = {
            "workflow": workflow,
            "history": []
        }

        max_steps = 15

        for step in range(max_steps):

            print(f"\n\n========== AGENT STEP {step + 1} ==========")

            instruction = f"""
A repeated workflow has been detected.

Workflow:

{json.dumps(workflow, indent=2)}

Previous execution history:

{json.dumps(context["history"], indent=2)}

Determine the NEXT action.

Remember:
- Execute only one tool.
- Examine previous results.
- If the workflow is successfully completed, return "complete".
- If you cannot safely continue, return "ask_user".
"""

            decision = self.ask_grok(instruction)

            print("\n🧠 Grok decision:")
            print(json.dumps(decision, indent=2))

            action = decision.get("action")
            parameters = decision.get("parameters", {})

            # -----------------------------------------------
            # COMPLETE
            # -----------------------------------------------

            if action == "complete":

                print("\n✅ WORKFLOW COMPLETED")

                self.completed = True

                return {
                    "status": "completed",
                    "history": context["history"]
                }

            # -----------------------------------------------
            # ASK USER
            # -----------------------------------------------

            if action == "ask_user":

                print("\n⚠️ Agent needs human intervention")

                return {
                    "status": "needs_user",
                    "reason": decision.get("reason"),
                    "history": context["history"]
                }

            # -----------------------------------------------
            # EXECUTE TOOL
            # -----------------------------------------------

            print(f"\n🔧 Executing: {action}")

            result = self.execute_tool(
                action,
                parameters
            )

            print("\n📊 Tool result:")
            print(json.dumps(result, indent=2))

            # -----------------------------------------------
            # SAVE OBSERVATION
            # -----------------------------------------------

            context["history"].append({
                "action": action,
                "parameters": parameters,
                "result": result
            })

        return {
            "status": "failed",
            "reason": "Maximum agent steps reached",
            "history": context["history"]
        }


# ============================================================
# EXAMPLE DISCOVERED WORKFLOW
# In the real application this comes from repetition_detector
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

    result = agent.run(
        discovered_workflow
    )

    print("\n\n===================================")
    print("FINAL RESULT")
    print("===================================")

    print(json.dumps(
        result,
        indent=2
    ))