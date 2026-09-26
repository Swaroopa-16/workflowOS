from backend.workflow import workflow_validator
from backend.agent.memory import AgentMemory
from backend.ai.grok import GrokClient

from backend.agent.approval import ApprovalManager
from backend.agent.agent import WorkFlowAgent

from backend.workflow.repetition_detector import RepetitionDetector
from backend.workflow.workflow_generator import WorkflowGenerator

from backend.agent.observer import ActivityObserver

from backend.tools.gmail_tool import GmailTool
from backend.tools.crm_tool import CRMTool
from backend.tools.slack_tool import SlackTool


class WorkFlowOS:

    def __init__(self):

        print("\n" + "=" * 70)
        print("🚀 INITIALIZING WORKFLOWOS")
        print("=" * 70)

        # AI
        self.grok = GrokClient()

        # Activity observer
        self.observer = ActivityObserver()

        # Repetition detector
        self.detector = RepetitionDetector()

        # Workflow generator
        self.generator = WorkflowGenerator(
            self.grok
        )

        # Approval manager
        self.approval = ApprovalManager()
        self.memory = AgentMemory()

        # Mock applications
        self.gmail = GmailTool()
        self.crm = CRMTool()
        self.slack = SlackTool()

        # Register tools
        tools = {
            "gmail_read_email":
                self.gmail.read_email,

            "gmail_download_attachment":
                self.gmail.download_attachment,

            "crm_search_customer":
                self.crm.search_customer,

            "crm_update_customer":
                self.crm.update_customer,

            "slack_send_message":
                self.slack.send_message
        }

        # Main agent
        self.agent = WorkFlowAgent(
    tools=tools,
    grok_client=self.grok,
    memory=self.memory
)

        print("\n✅ WorkFlowOS initialized successfully.")

    def detect_workflow(self, sessions):

        print("\n" + "=" * 70)
        print("🔍 ANALYZING USER ACTIVITY")
        print("=" * 70)

        return self.detector.detect(
            sessions
        )

    def generate_workflow(self, detected_workflow):
        print("\n" + "=" * 70)
        print("🧠 UNDERSTANDING REPEATED WORKFLOW")
        print("=" * 70)

        workflow = self.generator.generate(
            detected_workflow
        )

        # Remember the workflow
        self.memory.save_workflow(
            workflow
        )

        return workflow
    def request_approval(self, workflow):

        return self.approval.request_approval(
            workflow
        )

    def execute_workflow(self, workflow):

        print("\n" + "=" * 70)
        print("🤖 STARTING AI AGENT")
        print("=" * 70)

        return self.agent.run(
            workflow
        )

    def run(self, sessions):

        # 1. Detect repetition
        detection = self.detect_workflow(
            sessions
        )

        print("\nDetection Result:")
        print(detection)

        if not detection:

            print(
                "\nℹ️ No repeated workflow detected."
            )

            return {
                "status":
                    "no_repeated_workflow"
            }

        # 2. Generate workflow
        workflow = self.generate_workflow(
            detection
        )

        # 3. Ask for approval
        approved = self.request_approval(
            workflow
        )

        if not approved:

            print(
                "\n⏸️ Workflow postponed by user."
            )

            return {
                "status":
                    "workflow_postponed"
            }

        # 4. Execute approved workflow
        return self.execute_workflow(
            workflow
        )


if __name__ == "__main__":

    print(
        "\nWorkFlowOS backend is ready."
    )