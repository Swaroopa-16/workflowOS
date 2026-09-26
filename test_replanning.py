from backend.ai.grok import GrokClient
from backend.agent.agent import WorkFlowAgent
from backend.tools.gmail_tool import GmailTool
from backend.tools.crm_tool import CRMTool
from backend.tools.slack_tool import SlackTool


# -------------------------------------------------
# Initialize tools
# -------------------------------------------------

gmail = GmailTool()
crm = CRMTool()
slack = SlackTool()


# -------------------------------------------------
# Create a failing CRM tool
# -------------------------------------------------

original_search = crm.search_customer


def failing_search(customer):
    print("\n🔴 TEST MODE: Simulating CRM failure")

    return {
        "success": False,
        "found": False,
        "customer": customer,
        "error": "CRM service temporarily unavailable."
    }


crm.search_customer = failing_search


# -------------------------------------------------
# Register tools
# -------------------------------------------------

tools = {
    "gmail_read_email": gmail.read_email,
    "gmail_download_attachment": gmail.download_attachment,
    "crm_search_customer": crm.search_customer,
    "crm_update_customer": crm.update_customer,
    "slack_send_message": slack.send_message
}


# -------------------------------------------------
# Workflow
# -------------------------------------------------

workflow = {

    "workflow_name": "Process Customer Request",

    "intent": (
        "Automatically process customer quotation requests."
    ),

    "summary": (
        "Read customer email, download attachment, "
        "find customer in CRM, update CRM, and notify Slack."
    ),

    "actions": [

        {
            "step": 1,
            "application": "Gmail",
            "action": "gmail_read_email",
            "purpose": "Read the customer email"
        },

        {
            "step": 2,
            "application": "Gmail",
            "action": "gmail_download_attachment",
            "purpose": "Download the quotation attachment"
        },

        {
            "step": 3,
            "application": "CRM",
            "action": "crm_search_customer",
            "purpose": "Find the customer in CRM"
        },

        {
            "step": 4,
            "application": "CRM",
            "action": "crm_update_customer",
            "purpose": "Update the customer record"
        },

        {
            "step": 5,
            "application": "Slack",
            "action": "slack_send_message",
            "purpose": "Notify the customer operations team"
        }

    ],

    "conditions": [
        {
            "condition": "Customer cannot be found in CRM",
            "behavior": (
                "Pause and request human intervention."
            )
        }
    ],

    "failure_handling": [
        {
            "failure": "Any workflow step fails",
            "behavior": (
                "Ask the user for guidance before continuing."
            )
        }
    ],

    "confidence": 0.98
}


# -------------------------------------------------
# Start Agent
# -------------------------------------------------

print("\n")
print("=" * 70)
print("🧪 REPLANNING TEST")
print("=" * 70)

grok = GrokClient()

agent = WorkFlowAgent(
    tools=tools,
    grok_client=grok
)


result = agent.run(workflow)


# -------------------------------------------------
# Result
# -------------------------------------------------

print("\n")
print("=" * 70)
print("🏁 REPLANNING TEST RESULT")
print("=" * 70)

print(result)