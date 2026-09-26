from backend.ai.grok import GrokClient
from backend.agent.planner import WorkflowPlanner


workflow = {
    "workflow_name": "Process Customer Request",

    "intent": "Process customer quotation requests",

    "summary": (
        "Read customer email, download quotation, "
        "update CRM and notify the team."
    ),

    "actions": [
        {
            "step": 1,
            "application": "Gmail",
            "action": "gmail_read_email",
            "purpose": "Read the customer request"
        },
        {
            "step": 2,
            "application": "Gmail",
            "action": "gmail_download_attachment",
            "purpose": "Download quotation attachment"
        },
        {
            "step": 3,
            "application": "CRM",
            "action": "crm_search_customer",
            "purpose": "Find customer in CRM"
        },
        {
            "step": 4,
            "application": "CRM",
            "action": "crm_update_customer",
            "purpose": "Update customer record"
        },
        {
            "step": 5,
            "application": "Slack",
            "action": "slack_send_message",
            "purpose": "Notify customer operations team"
        }
    ],

    "confidence": 0.98
}


grok = GrokClient()

planner = WorkflowPlanner(grok)

plan = planner.create_plan(workflow)

planner.display_plan(plan)