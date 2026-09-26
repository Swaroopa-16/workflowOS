from backend.ai.grok import GrokClient


class WorkflowPlanner:

    def __init__(self, grok_client=None):
        self.grok = grok_client or GrokClient()

    def create_plan(self, workflow, memory=None):

        actions = workflow.get("actions", [])

        if not actions:
            raise ValueError(
                "Approved workflow contains no actions."
            )

        steps = []

        for index, action in enumerate(actions, start=1):

            tool = action.get(
                "action",
                action.get("tool")
            )

            if not tool:
                raise ValueError(
                    f"Workflow action {index} has no action/tool."
                )

            parameters = self._default_parameters(
                tool,
                action
            )

            steps.append({
                "step": index,
                "tool": tool,
                "parameters": parameters,
                "depends_on": (
                    []
                    if index == 1
                    else [index - 1]
                ),
                "description": action.get(
                    "purpose",
                    f"Execute {tool}"
                )
            })

        plan = {
            "workflow_name": workflow.get(
                "workflow_name",
                "Unnamed Workflow"
            ),

            "goal": workflow.get(
                "intent",
                workflow.get(
                    "summary",
                    "Execute approved workflow"
                )
            ),

            "steps": steps,

            "failure_policy": {
                "action": "ask_user",
                "condition": (
                    "Customer cannot be found in CRM "
                    "or a workflow step fails."
                )
            }
        }

        self._validate_plan(plan)

        return plan

    def _default_parameters(self, tool, action):

        if tool == "gmail_read_email":
            return {}

        if tool == "gmail_download_attachment":
            return {
                "filename": "quotation.pdf"
            }

        if tool == "crm_search_customer":
            return {
                "customer": "ABC Ltd"
            }

        if tool == "crm_update_customer":
            return {
                "customer_id": "CRM-001",
                "request": "New quotation required",
                "attachment": "quotation.pdf"
            }

        if tool == "slack_send_message":
            return {
                "channel": "#customer-ops",
                "message": (
                    "Processed quotation request "
                    "for customer ABC Ltd."
                )
            }

        return {}

    def _validate_plan(self, plan):

        required_fields = [
            "workflow_name",
            "goal",
            "steps",
            "failure_policy"
        ]

        for field in required_fields:

            if field not in plan:
                raise ValueError(
                    f"Planner output missing field: {field}"
                )

        if not isinstance(plan["steps"], list):
            raise ValueError(
                "Planner steps must be a list."
            )

        for step in plan["steps"]:

            required_step_fields = [
                "step",
                "tool",
                "parameters",
                "depends_on",
                "description"
            ]

            for field in required_step_fields:

                if field not in step:
                    raise ValueError(
                        f"Planner step missing field: {field}"
                    )

        return True

    def display_plan(self, plan):

        print("\n" + "=" * 60)
        print("🧠 EXECUTION PLAN")
        print("=" * 60)

        print(
            f"\nWorkflow: "
            f"{plan['workflow_name']}"
        )

        print(
            f"\nGoal:\n"
            f"{plan['goal']}"
        )

        print("\nExecution Steps:")

        for step in plan["steps"]:

            print(
                f"\n[{step['step']}] "
                f"{step['tool']}"
            )

            print(
                f"    Description: "
                f"{step['description']}"
            )

            print(
                f"    Parameters: "
                f"{step['parameters']}"
            )

            print(
                f"    Depends on: "
                f"{step['depends_on']}"
            )

        policy = plan["failure_policy"]

        print("\nFailure Policy:")

        print(
            f"    Action: "
            f"{policy['action']}"
        )

        print(
            f"    Condition: "
            f"{policy['condition']}"
        )

        print("=" * 60)