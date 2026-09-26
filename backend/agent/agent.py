from backend.ai.grok import GrokClient
from backend.agent.planner import WorkflowPlanner
from backend.agent.executor import WorkflowExecutor
from backend.agent.replanner import WorkflowReplanner


class WorkFlowAgent:

    def __init__(
        self,
        tools=None,
        grok_client=None,
        memory=None
    ):

        # AI reasoning engine
        self.grok = grok_client or GrokClient()

        # Planning engine
        self.planner = WorkflowPlanner(
            self.grok
        )

        # Execution engine
        self.executor = WorkflowExecutor(
            tools or {}
        )

        # Replanning engine
        self.replanner = WorkflowReplanner(
            self.grok
        )

        # Optional memory system
        self.memory = memory

        # Execution history for the current run
        self.execution_history = []

    # ==========================================================
    # MAIN AGENT LOOP
    # ==========================================================

    def run(self, workflow):

        print("\n")
        print("=" * 70)
        print("🤖 WORKFLOW AGENT STARTED")
        print("=" * 70)

        print(
            f"\nWorkflow: "
            f"{workflow.get('workflow_name', 'Unnamed Workflow')}"
        )

        # ------------------------------------------------------
        # 1. CREATE EXECUTION PLAN
        # ------------------------------------------------------

        print("\n🧠 Creating execution plan...")

        plan = self.planner.create_plan(
            workflow,
            self._get_memory()
        )

        self.planner.display_plan(plan)

        # ------------------------------------------------------
        # 2. EXECUTE PLAN STEP BY STEP
        # ------------------------------------------------------

        steps = plan.get(
            "steps",
            []
        )

        current_step_index = 0

        while current_step_index < len(steps):

            step = steps[current_step_index]

            print("\n")
            print(
                f"📍 Agent executing step "
                f"{current_step_index + 1}/"
                f"{len(steps)}"
            )

            # --------------------------------------------------
            # EXECUTE CURRENT STEP
            # --------------------------------------------------

            result = self.executor.execute_step(
                step
            )

            # Save execution history
            self.execution_history.append({
                "step": step,
                "result": result
            })

            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            if result.get("success"):

                print(
                    "\n✅ Agent observed successful result."
                )

                current_step_index += 1

                continue

            # --------------------------------------------------
            # FAILURE
            # --------------------------------------------------

            print(
                "\n⚠️ Agent observed a failed step."
            )

            print(
                "🧠 Asking Grok to replan..."
            )

            decision = self.replanner.replan(

                workflow=workflow,

                current_plan=plan,

                failed_step=step,

                tool_result=result,

                execution_history=
                    self.execution_history
            )

            decision_type = decision.get(
                "decision"
            )

            # --------------------------------------------------
            # RETRY
            # --------------------------------------------------

            if decision_type == "retry":

                print(
                    "\n🔄 Agent will retry the step."
                )

                continue

            # --------------------------------------------------
            # ALTERNATIVE
            # --------------------------------------------------

            if decision_type == "alternative":

                next_action = decision.get(
                    "next_action",
                    {}
                )

                if not next_action:

                    print(
                        "\n❌ No alternative action "
                        "was provided."
                    )

                    return self._ask_user(
                        decision
                    )

                alternative_step = {

                    "step":
                        step.get("step"),

                    "tool":
                        next_action.get("tool"),

                    "parameters":
                        next_action.get(
                            "parameters",
                            {}
                        ),

                    "depends_on":
                        step.get(
                            "depends_on",
                            []
                        ),

                    "description":
                        "Alternative action selected by agent."
                }

                print(
                    "\n🔀 Executing alternative action."
                )

                alternative_result = (
                    self.executor.execute_step(
                        alternative_step
                    )
                )

                self.execution_history.append({

                    "step":
                        alternative_step,

                    "result":
                        alternative_result
                })

                if alternative_result.get(
                    "success"
                ):

                    print(
                        "\n✅ Alternative action succeeded."
                    )

                    current_step_index += 1

                    continue

                print(
                    "\n❌ Alternative action failed."
                )

                return self._ask_user({
                    "message":
                        "The alternative action "
                        "also failed."
                })

            # --------------------------------------------------
            # CONTINUE
            # --------------------------------------------------

            if decision_type == "continue":

                print(
                    "\n➡️ Agent decided to continue."
                )

                current_step_index += 1

                continue

            # --------------------------------------------------
            # COMPLETE
            # --------------------------------------------------

            if decision_type == "complete":

                print(
                    "\n✅ Grok determined that "
                    "the workflow is complete."
                )

                return self._complete()

            # --------------------------------------------------
            # ASK USER
            # --------------------------------------------------

            if decision_type == "ask_user":

                return self._ask_user(
                    decision
                )

            # --------------------------------------------------
            # UNKNOWN DECISION
            # --------------------------------------------------

            print(
                "\n❌ Unknown agent decision:"
            )

            print(
                decision_type
            )

            return self._ask_user({

                "message":
                    "The agent could not "
                    "determine the next action."
            })

        # ------------------------------------------------------
        # ALL STEPS COMPLETED
        # ------------------------------------------------------

        return self._complete()

    # ==========================================================
    # WORKFLOW COMPLETED
    # ==========================================================

    def _complete(self):

        print("\n")
        print("=" * 70)
        print("🎉 WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 70)

        result = {

            "success": True,

            "status":
                "completed",

            "execution_history":
                self.execution_history
        }

        self._save_memory(
            result
        )

        return result

    # ==========================================================
    # HUMAN INTERVENTION
    # ==========================================================

    def _ask_user(self, decision):

        print("\n")
        print("=" * 70)
        print("👤 HUMAN INTERVENTION REQUIRED")
        print("=" * 70)

        message = decision.get(

            "message",

            "The agent requires your input."
        )

        print(
            f"\n🤖 Agent:\n{message}"
        )

        result = {

            "success": False,

            "status":
                "human_intervention_required",

            "message":
                message,

            "execution_history":
                self.execution_history
        }

        self._save_memory(
            result
        )

        return result

    # ==========================================================
    # MEMORY
    # ==========================================================

    def _get_memory(self):

        if self.memory is None:

            return {}

        try:

            return self.memory.get_agent_context()

        except Exception:

            return {}

    def _save_memory(self, result):

        if self.memory is None:

            return

        try:

            self.memory.save_execution(
                result
            )

        except Exception as error:

            print(
                f"⚠️ Could not save memory: "
                f"{error}"
            )