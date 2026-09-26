class ApprovalManager:

    def __init__(self):
        self.pending_workflow = None

    def request_approval(self, workflow):

        self.pending_workflow = workflow

        print("\n" + "=" * 60)
        print("🔔 REPEATED WORKFLOW DETECTED")
        print("=" * 60)

        print(
            f"\nWorkflow: {workflow.get('workflow_name', 'Unnamed Workflow')}"
        )

        print(
            f"\nIntent:\n"
            f"{workflow.get('intent', 'Not specified')}"
        )

        print(
            f"\nSummary:\n"
            f"{workflow.get('summary', 'Not specified')}"
        )

        print("\nExecution Steps:")

        for action in workflow.get("actions", []):

            print(
                f"  [{action.get('step', '?')}] "
                f"{action.get('application', 'Unknown')} → "
                f"{action.get('action', 'Unknown')}"
            )

            purpose = action.get("purpose")

            if purpose:
                print(f"      → {purpose}")

        confidence = workflow.get(
            "confidence",
            0
        )

        print(
            f"\nConfidence: "
            f"{confidence * 100:.0f}%"
        )

        print("\n" + "-" * 60)

        while True:

            choice = input(
                "\nWould you like me to automate this? "
                "[A]utomate / [N]ot Now: "
            ).strip().lower()

            if choice in ["a", "automate", "yes", "y"]:

                print("\n✅ Workflow approved.")

                return True

            if choice in [
                "n",
                "no",
                "not now"
            ]:

                print(
                    "\n⏸️ Workflow postponed."
                )

                return False

            print(
                "\nPlease enter A for Automate "
                "or N for Not Now."
            )

    def get_pending_workflow(self):

        return self.pending_workflow

    def clear_pending_workflow(self):

        self.pending_workflow = None