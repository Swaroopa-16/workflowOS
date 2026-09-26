import json

from backend.workflow.workflow_validator import WorkflowValidator


class WorkflowGenerator:

    def __init__(self, grok_client):
        self.grok = grok_client
        self.validator = WorkflowValidator()

    def generate(self, detected_workflow):

        sequence = detected_workflow.get("sequence", [])

        if not sequence:
            raise ValueError(
                "No repeated workflow sequence detected."
            )

        # -------------------------------------------------
        # Ask Grok to understand the repeated workflow
        # -------------------------------------------------

        system_prompt = """
You are the Workflow Understanding Engine of WorkFlowOS.

Your job is to convert a repeated sequence of user actions
into a structured automation workflow.

Return ONLY valid JSON.

The "action" field MUST contain the exact tool name.

Allowed actions:

gmail_read_email
gmail_download_attachment
crm_search_customer
crm_update_customer
slack_send_message

Required JSON structure:

{
    "workflow_name": "Process Customer Request",

    "trigger": {
        "type": "repeated_workflow_detected",
        "description": "..."
    },

    "intent": "...",

    "summary": "...",

    "actions": [
        {
            "step": 1,
            "application": "Gmail",
            "action": "gmail_read_email",
            "purpose": "Read the customer email"
        }
    ],

    "conditions": [
        {
            "condition": "...",
            "behavior": "..."
        }
    ],

    "failure_handling": [
        {
            "failure": "...",
            "behavior": "..."
        }
    ],

    "confidence": 0.98
}

IMPORTANT:

conditions MUST contain:
- condition
- behavior

failure_handling MUST contain:
- failure
- behavior
"""

        user_prompt = f"""
A repeated workflow was detected.

Detected workflow:

{json.dumps(detected_workflow, indent=2)}

Repeated action sequence:

{json.dumps(sequence, indent=2)}

Understand this workflow and generate an automation workflow.

Use the exact action names from the sequence.

Return ONLY valid JSON.
"""

        # -------------------------------------------------
        # Get AI interpretation
        # -------------------------------------------------

        workflow = self.grok.chat_json(
            system_prompt,
            user_prompt
        )

        if not isinstance(workflow, dict):
            workflow = {}

        # -------------------------------------------------
        # Workflow name
        # -------------------------------------------------

        workflow["workflow_name"] = (
            workflow.get("workflow_name")
            or "Process Customer Request"
        )

        # -------------------------------------------------
        # Trigger
        # -------------------------------------------------

        workflow["trigger"] = {
            "type": "repeated_workflow_detected",
            "description": (
                "WorkFlowOS detected a repeated sequence "
                "of user actions."
            )
        }

        # -------------------------------------------------
        # Intent
        # -------------------------------------------------

        workflow["intent"] = (
            workflow.get("intent")
            or (
                "Automatically execute the repeated "
                "customer request workflow."
            )
        )

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        workflow["summary"] = (
            workflow.get("summary")
            or (
                "Read the customer email, download the "
                "attachment, update the CRM record, "
                "and notify the team."
            )
        )

        # -------------------------------------------------
        # Build reliable actions from detected sequence
        #
        # We intentionally use the detected sequence here
        # instead of trusting Grok to rename the tools.
        # -------------------------------------------------

        actions = []

        for index, action in enumerate(
            sequence,
            start=1
        ):

            actions.append(
                self._build_action(
                    action,
                    index
                )
            )

        workflow["actions"] = actions

        # -------------------------------------------------
        # Conditions
        #
        # Validator requires:
        # condition + behavior
        # -------------------------------------------------

        workflow["conditions"] = [
            {
                "condition": (
                    "Customer cannot be found in CRM"
                ),
                "behavior": (
                    "Pause the workflow and request "
                    "human intervention."
                )
            }
        ]

        # -------------------------------------------------
        # Failure handling
        #
        # Validator requires:
        # failure + behavior
        # -------------------------------------------------

        workflow["failure_handling"] = [
            {
                "failure": (
                    "Any workflow step fails"
                ),
                "behavior": (
                    "Ask the user for guidance "
                    "before continuing."
                )
            }
        ]

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        workflow["confidence"] = workflow.get(
            "confidence",
            detected_workflow.get(
                "average_similarity",
                0.0
            )
        )

        # Make sure confidence is numeric
        try:
            workflow["confidence"] = float(
                workflow["confidence"]
            )
        except (TypeError, ValueError):
            workflow["confidence"] = float(
                detected_workflow.get(
                    "average_similarity",
                    0.0
                )
            )

        # -------------------------------------------------
        # Validate final workflow
        # -------------------------------------------------

        validation = self.validator.validate(
            workflow
        )

        if not validation["valid"]:

            raise ValueError(
                "Generated workflow failed validation: "
                + str(validation)
            )

        # -------------------------------------------------
        # Display generated workflow
        # -------------------------------------------------

        self.display_workflow(workflow)

        return workflow

    # =====================================================
    # ACTION BUILDER
    # =====================================================

    def _build_action(
        self,
        action,
        step
    ):

        action_info = {

            "gmail_read_email": {
                "application": "Gmail",
                "purpose": (
                    "Read the customer email"
                )
            },

            "gmail_download_attachment": {
                "application": "Gmail",
                "purpose": (
                    "Download the quotation attachment"
                )
            },

            "crm_search_customer": {
                "application": "CRM",
                "purpose": (
                    "Find the customer in CRM"
                )
            },

            "crm_update_customer": {
                "application": "CRM",
                "purpose": (
                    "Update the customer record"
                )
            },

            "slack_send_message": {
                "application": "Slack",
                "purpose": (
                    "Notify the customer operations team"
                )
            }

        }

        info = action_info.get(
            action,
            {
                "application": "Application",
                "purpose": f"Execute {action}"
            }
        )

        return {
            "step": step,
            "application": info["application"],
            "action": action,
            "purpose": info["purpose"]
        }

    # =====================================================
    # DISPLAY WORKFLOW
    # =====================================================

    def display_workflow(self, workflow):

        print("\n" + "=" * 60)
        print("🧠 GENERATED AUTOMATION WORKFLOW")
        print("=" * 60)

        print(
            f"\nWorkflow: "
            f"{workflow.get('workflow_name')}"
        )

        print(
            f"\nIntent:\n"
            f"{workflow.get('intent')}"
        )

        print(
            f"\nSummary:\n"
            f"{workflow.get('summary')}"
        )

        print("\nExecution Steps:")

        for action in workflow.get(
            "actions",
            []
        ):

            print(
                f"  [{action.get('step')}] "
                f"{action.get('application')} → "
                f"{action.get('action')}"
            )

            print(
                f"      → "
                f"{action.get('purpose')}"
            )

        print("\nConditions:")

        for condition in workflow.get(
            "conditions",
            []
        ):

            print(
                f"  • {condition.get('condition')}"
            )

            print(
                f"    → {condition.get('behavior')}"
            )

        print("\nFailure Handling:")

        for failure in workflow.get(
            "failure_handling",
            []
        ):

            print(
                f"  • {failure.get('failure')}"
            )

            print(
                f"    → {failure.get('behavior')}"
            )

        print(
            f"\nConfidence: "
            f"{workflow.get('confidence', 0) * 100:.1f}%"
        )

        print("=" * 60)