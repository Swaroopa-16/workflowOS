from backend.ai.grok import GrokClient
from backend.agent.replanner import WorkflowReplanner


workflow = {

    "workflow_name":
        "Process Customer Request",

    "intent":
        "Process customer quotation requests",

    "summary":
        "Read email, download quotation, "
        "update CRM and notify the team.",

    "actions": [
        {
            "step": 1,
            "action": "gmail_read_email"
        },
        {
            "step": 2,
            "action":
                "gmail_download_attachment"
        },
        {
            "step": 3,
            "action":
                "crm_search_customer"
        },
        {
            "step": 4,
            "action":
                "crm_update_customer"
        },
        {
            "step": 5,
            "action":
                "slack_send_message"
        }
    ]
}


current_plan = {

    "workflow_name":
        "Process Customer Request",

    "goal":
        "Process customer quotation request",

    "steps": [
        {
            "step": 3,
            "tool":
                "crm_search_customer",

            "parameters": {
                "customer":
                    "ABC Ltd"
            },

            "depends_on": [2],

            "description":
                "Search customer in CRM"
        }
    ],

    "failure_policy": {
        "action":
            "ask_user",

        "condition":
            "Customer cannot be found"
    }
}


failed_step = {

    "step": 3,

    "tool":
        "crm_search_customer",

    "parameters": {
        "customer":
            "ABC Ltd"
    }
}


tool_result = {

    "success": False,

    "tool":
        "crm_search_customer",

    "error":
        "Customer ABC Ltd was not found in CRM."
}


execution_history = [
    {
        "step": 1,
        "tool":
            "gmail_read_email",
        "success": True
    },
    {
        "step": 2,
        "tool":
            "gmail_download_attachment",
        "success": True
    }
]


grok = GrokClient()

replanner = WorkflowReplanner(grok)


decision = replanner.replan(

    workflow=workflow,

    current_plan=current_plan,

    failed_step=failed_step,

    tool_result=tool_result,

    execution_history=execution_history
)


print("\nFINAL REPLANNER DECISION:")
print(decision)