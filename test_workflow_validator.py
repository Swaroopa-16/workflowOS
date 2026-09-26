print("TEST FILE STARTED")

from backend.workflow.workflow_validator import WorkflowValidator

print("IMPORT SUCCESS")

validator = WorkflowValidator()

print("VALIDATOR CREATED")

workflow = {
    "workflow_name": "Test Workflow",
    "intent": "Test workflow validation",
    "summary": "Testing the WorkFlowOS validator",

    "trigger": {
        "type": "event",
        "description": "Test event"
    },

    "actions": [
        {
            "step": 1,
            "application": "Gmail",
            "action": "gmail_read_email",
            "purpose": "Read email"
        }
    ],

    "conditions": [],

    "failure_handling": [],

    "confidence": 0.98
}

print("RUNNING VALIDATION")

result = validator.validate(workflow)

print("RESULT:")
print(result)

print("TEST FILE FINISHED")