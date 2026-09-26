import json
from pathlib import Path
from datetime import datetime


class AgentMemory:

    def __init__(self, storage_path=None):

        if storage_path is None:
            root_dir = (
                Path(__file__)
                .resolve()
                .parent
                .parent
                .parent
            )

            storage_path = (
                root_dir
                / "data"
                / "execution_history.json"
            )

        self.storage_path = Path(storage_path)

        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.data = self._load()

    # =====================================================
    # LOAD
    # =====================================================

    def _load(self):

        if not self.storage_path.exists():

            return {
                "executions": [],
                "workflows": [],
                "learned_actions": []
            }

        try:

            with open(
                self.storage_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, dict):

                data.setdefault(
                    "executions",
                    []
                )

                data.setdefault(
                    "workflows",
                    []
                )

                data.setdefault(
                    "learned_actions",
                    []
                )

                return data

        except Exception as error:

            print(
                f"⚠️ Could not load memory: {error}"
            )

        return {
            "executions": [],
            "workflows": [],
            "learned_actions": []
        }

    # =====================================================
    # SAVE
    # =====================================================

    def _save(self):

        with open(
            self.storage_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.data,
                file,
                indent=2
            )

    # =====================================================
    # SAVE WORKFLOW
    # =====================================================

    def save_workflow(self, workflow):

        workflow_record = {
            "workflow_name": workflow.get(
                "workflow_name",
                "Unnamed Workflow"
            ),

            "intent": workflow.get(
                "intent",
                ""
            ),

            "actions": workflow.get(
                "actions",
                []
            ),

            "confidence": workflow.get(
                "confidence",
                0
            ),

            "saved_at": datetime.now().isoformat()
        }

        existing = [
            item
            for item in self.data["workflows"]
            if item.get("workflow_name")
            == workflow_record["workflow_name"]
        ]

        if not existing:

            self.data["workflows"].append(
                workflow_record
            )

            self._save()

            print(
                "\n🧠 Workflow learned and stored in memory."
            )

        return workflow_record

    # =====================================================
    # SAVE EXECUTION
    # =====================================================

    def save_execution(
        self,
        result,
        workflow_name=None
    ):

        execution = {

            "execution_id": (
                f"execution-"
                f"{len(self.data['executions']) + 1}"
            ),

            "timestamp": (
                datetime.now().isoformat()
            ),

            "workflow_name": (
                workflow_name
                or result.get(
                    "workflow_name",
                    "Unnamed Workflow"
                )
            ),

            "status": result.get(
                "status",
                "unknown"
            ),

            "success": result.get(
                "success",
                False
            ),

            "execution_history": result.get(
                "execution_history",
                []
            )
        }

        self.data["executions"].append(
            execution
        )

        self._save()

        print(
            "\n💾 Execution saved to memory."
        )

        return execution

    # =====================================================
    # LEARN ACTION
    # =====================================================

    def learn_action(
        self,
        tool,
        result
    ):

        learned = {

            "tool": tool,

            "result_type": (
                type(result).__name__
            ),

            "learned_at": (
                datetime.now().isoformat()
            )
        }

        self.data[
            "learned_actions"
        ].append(
            learned
        )

        self._save()

        return learned

    # =====================================================
    # AGENT CONTEXT
    # =====================================================

    def get_agent_context(self):

        return {

            "known_workflows": self.data[
                "workflows"
            ],

            "previous_executions": self.data[
                "executions"
            ][-10:],

            "learned_actions": self.data[
                "learned_actions"
            ][-20:]
        }

    # =====================================================
    # FIND WORKFLOW
    # =====================================================

    def find_workflow(
        self,
        workflow_name
    ):

        for workflow in self.data["workflows"]:

            if workflow.get(
                "workflow_name"
            ) == workflow_name:

                return workflow

        return None

    # =====================================================
    # EXECUTION HISTORY
    # =====================================================

    def get_execution_history(self):

        return self.data[
            "executions"
        ]

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.data = {
            "executions": [],
            "workflows": [],
            "learned_actions": []
        }

        self._save()

        print(
            "\n🗑️ Agent memory cleared."
        )