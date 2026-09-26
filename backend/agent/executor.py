"""
WorkFlowOS - Executor

Responsible for:
1. Receiving an action selected by the AI agent
2. Calling the correct tool
3. Returning a structured result
4. Handling tool errors safely

The executor does NOT decide what action should happen next.
That decision belongs to the Grok / AI-powered reasoning agent.
"""

from typing import Any, Dict


class Executor:
    """
    Executes actions selected by the WorkFlowOS agent.
    """

    def __init__(self, tools):
        self.tools = tools

        # Map agent action names to actual Python functions
        self.action_map = {
            "gmail_read_email": self._gmail_read_email,
            "gmail_download_attachment": self._gmail_download_attachment,
            "crm_search_customer": self._crm_search_customer,
            "crm_update_customer": self._crm_update_customer,
            "slack_send_message": self._slack_send_message,
        }

    # =========================================================
    # MAIN EXECUTOR
    # =========================================================

    def execute(
        self,
        action: str,
        parameters: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:

        parameters = parameters or {}

        print(f"\n[EXECUTOR] Executing: {action}")
        print(f"           Parameters: {parameters}")

        # Check whether action exists
        if action not in self.action_map:
            return {
                "success": False,
                "action": action,
                "error": f"Unknown action: {action}"
            }

        try:
            function = self.action_map[action]
            result = function(parameters)

            # Make sure every tool returns a dictionary
            if not isinstance(result, dict):
                result = {
                    "success": True,
                    "data": result
                }

            result["action"] = action
            return result

        except Exception as e:
            print(f"[ERROR] Executor exception: {e}")
            return {
                "success": False,
                "action": action,
                "error": str(e)
            }

    # =========================================================
    # GMAIL
    # =========================================================

    def _gmail_read_email(self, params):
        print("  -> [Gmail] Reading email")
        return self.tools.gmail_read_email()

    # ---------------------------------------------------------

    def _gmail_download_attachment(self, params):
        filename = params.get("filename")
        if not filename:
            return {
                "success": False,
                "error": "Attachment filename is required"
            }
        print(f"  -> [Gmail] Downloading: {filename}")
        return self.tools.gmail_download_attachment(filename)

    # =========================================================
    # CRM
    # =========================================================

    def _crm_search_customer(self, params):
        customer = params.get("customer")
        if not customer:
            return {
                "success": False,
                "error": "Customer name is required"
            }
        print(f"  -> [CRM] Searching: {customer}")
        return self.tools.crm_search_customer(customer)

    # ---------------------------------------------------------

    def _crm_update_customer(self, params):
        customer_id = params.get("customer_id")
        request = params.get("request")
        attachment = params.get("attachment")

        if not customer_id:
            return {
                "success": False,
                "error": "customer_id is required"
            }

        print(f"  -> [CRM] Updating customer: {customer_id}")
        return self.tools.crm_update_customer(
            customer_id=customer_id,
            request=request,
            attachment=attachment
        )

    # =========================================================
    # SLACK
    # =========================================================

    def _slack_send_message(self, params):
        channel = params.get("channel")
        message = params.get("message")

        if not channel:
            return {
                "success": False,
                "error": "Slack channel is required"
            }

        if not message:
            return {
                "success": False,
                "error": "Slack message is required"
            }

        print(f"  -> [Slack] Sending message to {channel}")
        return self.tools.slack_send_message(
            channel=channel,
            message=message
        )