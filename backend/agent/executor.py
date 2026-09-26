from typing import Any, Dict


class WorkflowExecutor:

    def __init__(self, tools=None):

        self.tools = tools or {}

    def execute_step(
        self,
        step: Dict[str, Any]
    ) -> Dict[str, Any]:

        tool_name = step.get("tool")

        if not tool_name:

            return {
                "success": False,
                "tool": None,
                "error": "Step does not contain a tool."
            }

        parameters = step.get(
            "parameters",
            {}
        )

        print("\n" + "-" * 60)
        print("⚙️ EXECUTING STEP")
        print("-" * 60)

        print(
            f"Step: {step.get('step')}"
        )

        print(
            f"Tool: {tool_name}"
        )

        print(
            f"Parameters: {parameters}"
        )

        if tool_name not in self.tools:

            print(
                f"❌ Tool not found: {tool_name}"
            )

            return {
                "success": False,
                "tool": tool_name,
                "step": step.get("step"),
                "error":
                    f"Tool '{tool_name}' is not registered."
            }

        tool_function = self.tools[tool_name]

        try:

            result = tool_function(
                **parameters
            )

            print("\n✅ STEP COMPLETED")

            print(
                f"Result: {result}"
            )

            return {
                "success": True,
                "tool": tool_name,
                "step": step.get("step"),
                "result": result
            }

        except Exception as error:

            print("\n❌ STEP FAILED")

            print(
                f"Error: {error}"
            )

            return {
                "success": False,
                "tool": tool_name,
                "step": step.get("step"),
                "error": str(error)
            }

    def execute_plan(self, plan):

        print("\n" + "=" * 60)
        print("🚀 EXECUTING WORKFLOW")
        print("=" * 60)

        results = []

        for step in plan.get("steps", []):

            result = self.execute_step(step)

            results.append(result)

            if not result["success"]:

                print("\n⏸️ WORKFLOW PAUSED")

                print(
                    "Reason: Previous step failed."
                )

                return {
                    "success": False,
                    "completed_steps": results,
                    "failed_step":
                        step.get("step"),
                    "results": results
                }

        print("\n" + "=" * 60)
        print("✅ WORKFLOW COMPLETED")
        print("=" * 60)

        return {
            "success": True,
            "completed_steps":
                len(results),
            "results": results
        }