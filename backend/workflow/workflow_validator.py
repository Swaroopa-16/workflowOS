class WorkflowValidator:

    ALLOWED_ACTIONS = {
        "gmail_read_email",
        "gmail_download_attachment",
        "crm_search_customer",
        "crm_update_customer",
        "slack_send_message",
    }

    REQUIRED_FIELDS = {
        "workflow_name",
        "intent",
        "summary",
        "trigger",
        "actions",
        "conditions",
        "failure_handling",
        "confidence",
    }

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate(self, workflow):

        self.errors = []
        self.warnings = []

        if not isinstance(workflow, dict):

            self.errors.append(
                "Workflow must be a dictionary."
            )

            return self._result()

        self._validate_required_fields(workflow)
        self._validate_basic_fields(workflow)
        self._validate_trigger(workflow)
        self._validate_actions(workflow)
        self._validate_conditions(workflow)
        self._validate_failure_handling(workflow)
        self._validate_confidence(workflow)

        return self._result()

    def _validate_required_fields(self, workflow):

        for field in self.REQUIRED_FIELDS:

            if field not in workflow:

                self.errors.append(
                    f"Missing required field: {field}"
                )

    def _validate_basic_fields(self, workflow):

        for field in [
            "workflow_name",
            "intent",
            "summary"
        ]:

            value = workflow.get(field)

            if not isinstance(value, str):

                self.errors.append(
                    f"{field} must be a string."
                )

            elif not value.strip():

                self.errors.append(
                    f"{field} cannot be empty."
                )

    def _validate_trigger(self, workflow):

        trigger = workflow.get("trigger")

        if not isinstance(trigger, dict):

            self.errors.append(
                "Trigger must be an object."
            )

            return

        if not trigger.get("type"):

            self.errors.append(
                "Trigger type is missing."
            )

        if not trigger.get("description"):

            self.errors.append(
                "Trigger description is missing."
            )

    def _validate_actions(self, workflow):

        actions = workflow.get("actions")

        if not isinstance(actions, list):

            self.errors.append(
                "Actions must be a list."
            )

            return

        if len(actions) == 0:

            self.errors.append(
                "Workflow must contain at least one action."
            )

            return

        for index, action in enumerate(
            actions,
            start=1
        ):

            if not isinstance(action, dict):

                self.errors.append(
                    f"Action {index} must be an object."
                )

                continue

            required = [
                "step",
                "application",
                "action",
                "purpose"
            ]

            for field in required:

                if field not in action:

                    self.errors.append(
                        f"Action {index} is missing "
                        f"'{field}'."
                    )

            action_name = action.get("action")

            if action_name not in self.ALLOWED_ACTIONS:

                self.errors.append(
                    f"Unsupported action in step "
                    f"{index}: {action_name}"
                )

    def _validate_conditions(self, workflow):

        conditions = workflow.get("conditions")

        if not isinstance(conditions, list):

            self.errors.append(
                "Conditions must be a list."
            )

            return

        for index, condition in enumerate(
            conditions,
            start=1
        ):

            if not isinstance(condition, dict):

                self.errors.append(
                    f"Condition {index} must be an object."
                )

                continue

            if not condition.get("condition"):

                self.errors.append(
                    f"Condition {index} is missing condition."
                )

            if not condition.get("behavior"):

                self.errors.append(
                    f"Condition {index} is missing behavior."
                )

    def _validate_failure_handling(self, workflow):

        failures = workflow.get("failure_handling")

        if not isinstance(failures, list):

            self.errors.append(
                "failure_handling must be a list."
            )

            return

        for index, failure in enumerate(
            failures,
            start=1
        ):

            if not isinstance(failure, dict):

                self.errors.append(
                    f"Failure {index} must be an object."
                )

                continue

            if not failure.get("failure"):

                self.errors.append(
                    f"Failure {index} is missing failure."
                )

            if not failure.get("behavior"):

                self.errors.append(
                    f"Failure {index} is missing behavior."
                )

    def _validate_confidence(self, workflow):

        confidence = workflow.get("confidence")

        if not isinstance(
            confidence,
            (int, float)
        ):

            self.errors.append(
                "Confidence must be a number."
            )

            return

        if not 0 <= confidence <= 1:

            self.errors.append(
                "Confidence must be between 0.0 and 1.0."
            )

        elif confidence < 0.70:

            self.warnings.append(
                "Workflow confidence is below 70%."
            )

    def _result(self):

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }

    def validate_or_raise(self, workflow):

        result = self.validate(workflow)

        if not result["valid"]:

            message = "\n".join(
                f"- {error}"
                for error in result["errors"]
            )

            raise ValueError(
                "Workflow validation failed:\n"
                + message
            )

        return workflow

    def display_result(self, result):

        print("\n" + "=" * 55)
        print("🔍 WORKFLOW VALIDATION")
        print("=" * 55)

        if result["valid"]:

            print("\n✅ Workflow is VALID.")

        else:

            print("\n❌ Workflow is INVALID.")

            print("\nErrors:")

            for error in result["errors"]:

                print(f"  ❌ {error}")

        if result["warnings"]:

            print("\nWarnings:")

            for warning in result["warnings"]:

                print(f"  ⚠️ {warning}")

        print("\n" + "=" * 55)