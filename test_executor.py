from backend.agent.executor import WorkflowExecutor


# Mock tools for testing
def gmail_read_email():
    return {
        "email_id": "EMAIL-001",
        "customer": "ABC Ltd",
        "subject": "Quotation Request",
        "attachment": "quotation.pdf"
    }


def gmail_download_attachment(filename):
    return {
        "filename": filename,
        "status": "downloaded"
    }


def crm_search_customer(customer):
    return {
        "customer_id": "CRM-001",
        "customer": customer,
        "found": True
    }


def crm_update_customer(
    customer_id,
    request,
    attachment
):
    return {
        "customer_id": customer_id,
        "status": "updated",
        "request": request,
        "attachment": attachment
    }


def slack_send_message(
    channel,
    message
):
    return {
        "channel": channel,
        "status": "sent",
        "message": message
    }


# Register tools
tools = {

    "gmail_read_email":
        gmail_read_email,

    "gmail_download_attachment":
        gmail_download_attachment,

    "crm_search_customer":
        crm_search_customer,

    "crm_update_customer":
        crm_update_customer,

    "slack_send_message":
        slack_send_message
}


# Create executor
executor = WorkflowExecutor(tools)


# Test plan
plan = {

    "workflow_name":
        "Process Customer Request",

    "goal":
        "Process customer quotation request",

    "steps": [

        {
            "step": 1,
            "tool": "gmail_read_email",
            "parameters": {},
            "depends_on": [],
            "description":
                "Read customer email"
        },

        {
            "step": 2,
            "tool":
                "gmail_download_attachment",
            "parameters": {
                "filename":
                    "quotation.pdf"
            },
            "depends_on": [1],
            "description":
                "Download quotation"
        },

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
        },

        {
            "step": 4,
            "tool":
                "crm_update_customer",
            "parameters": {
                "customer_id":
                    "CRM-001",
                "request":
                    "New quotation required",
                "attachment":
                    "quotation.pdf"
            },
            "depends_on": [3],
            "description":
                "Update CRM"
        },

        {
            "step": 5,
            "tool":
                "slack_send_message",
            "parameters": {
                "channel":
                    "#customer-ops",
                "message":
                    "Processed quotation request for ABC Ltd."
            },
            "depends_on": [4],
            "description":
                "Notify team"
        }
    ]
}


# Execute
result = executor.execute_plan(plan)


print("\nFINAL RESULT:")
print(result)