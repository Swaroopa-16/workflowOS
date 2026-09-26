from backend.main import WorkFlowOS


app = WorkFlowOS()

# -------------------------------------------------
# Simulated repeated user activity
# -------------------------------------------------

sessions = [

    {
        "session_id": "session-001",
        "activities": [
            {
                "application": "Gmail",
                "action": "gmail_read_email"
            },
            {
                "application": "Gmail",
                "action": "gmail_download_attachment"
            },
            {
                "application": "CRM",
                "action": "crm_search_customer"
            },
            {
                "application": "CRM",
                "action": "crm_update_customer"
            },
            {
                "application": "Slack",
                "action": "slack_send_message"
            }
        ]
    },

    {
        "session_id": "session-002",
        "activities": [
            {
                "application": "Gmail",
                "action": "gmail_read_email"
            },
            {
                "application": "Gmail",
                "action": "gmail_download_attachment"
            },
            {
                "application": "CRM",
                "action": "crm_search_customer"
            },
            {
                "application": "CRM",
                "action": "crm_update_customer"
            },
            {
                "application": "Slack",
                "action": "slack_send_message"
            }
        ]
    }

]


print("\n")
print("=" * 70)
print("🧪 WORKFLOWOS END-TO-END TEST")
print("=" * 70)


result = app.run(sessions)


print("\n")
print("=" * 70)
print("🏁 FINAL RESULT")
print("=" * 70)

print(result)