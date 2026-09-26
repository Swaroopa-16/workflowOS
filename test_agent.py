from backend.ai.grok import GrokClient
from backend.agent.agent import WorkFlowAgent

from backend.tools.gmail_tool import GmailTool
from backend.tools.crm_tool import CRMTool
from backend.tools.slack_tool import SlackTool


# ==========================================================
# CREATE MOCK APPLICATIONS
# ==========================================================

gmail = GmailTool()
crm = CRMTool()
slack = SlackTool()


# ==========================================================
# REGISTER TOOLS FOR THE AGENT
# ==========================================================

tools = {

    "gmail_read_email":
        gmail.read_email,

    "gmail_download_attachment":
        gmail.download_attachment,

    "crm_search_customer":
        crm.search_customer,

    "crm_update_customer":
        crm.update_customer,

    "slack_send_message":
        slack.send_message
}


# ==========================================================
# APPROVED WORKFLOW
# ==========================================================

workflow = {

    "workflow_name":
        "Process Customer Request",

    "intent":
        "Automatically process customer quotation requests",

    "summary":
        (
            "Read the customer email, download the quotation, "
            "find the customer in CRM, update the customer "
            "record, and notify the team in Slack."
        ),

    "actions": [

        {
            "step": 1,
            "application": "Gmail",
            "action": "gmail_read_email",
            "purpose":
                "Read the customer email"
        },

        {
            "step": 2,
            "application": "Gmail",
            "action":
                "gmail_download_attachment",
            "purpose":
                "Download the quotation attachment"
        },

        {
            "step": 3,
            "application": "CRM",
            "action":
                "crm_search_customer",
            "purpose":
                "Find the customer in CRM"
        },

        {
            "step": 4,
            "application": "CRM",
            "action":
                "crm_update_customer",
            "purpose":
                "Update the customer record"
        },

        {
            "step": 5,
            "application": "Slack",
            "action":
                "slack_send_message",
            "purpose":
                "Notify the customer operations team"
        }
    ],

    "confidence": 0.98
}


# ==========================================================
# GROK
# ==========================================================

grok = GrokClient()


# ==========================================================
# WORKFLOW AGENT
# ==========================================================

agent = WorkFlowAgent(

    tools=tools,

    grok_client=grok
)


# ==========================================================
# RUN
# ==========================================================

print("\n")
print("=" * 70)
print("🚀 WORKFLOWOS FULL AGENT TEST")
print("=" * 70)

result = agent.run(
    workflow
)


# ==========================================================
# RESULT
# ==========================================================

print("\n")
print("=" * 70)
print("📊 FINAL RESULT")
print("=" * 70)

print(
    result
)