from backend.agent.approval import ApprovalManager


workflow = {

    "workflow_name": "Process Customer Request",

    "intent": (
        "Process incoming customer requests "
        "and update the CRM."
    ),

    "summary": (
        "Read the email, download the attachment, "
        "update the CRM and notify Slack."
    ),

    "confidence": 0.98,

    "actions": [

        {
            "step": 1,
            "application": "Gmail",
            "action": "gmail_read_email"
        },

        {
            "step": 2,
            "application": "Gmail",
            "action": "gmail_download_attachment"
        },

        {
            "step": 3,
            "application": "CRM",
            "action": "crm_search_customer"
        },

        {
            "step": 4,
            "application": "CRM",
            "action": "crm_update_customer"
        },

        {
            "step": 5,
            "application": "Slack",
            "action": "slack_send_message"
        }
    ]
}


approval = ApprovalManager()

approved = approval.request_approval(
    workflow
)

print("\nApproval result:", approved)
