import sys
import os

# Fix Windows console UTF-8 output encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from backend.ai.grok import GrokClient, GrokAI
from backend.workflow.workflow_generator import WorkflowGenerator


detected_workflow = {
    "sequence": [
        "gmail_read_email",
        "gmail_download_attachment",
        "crm_search_customer",
        "crm_update_customer",
        "slack_send_message"
    ],
    "occurrences": 3,
    "average_similarity": 1.0
}


print("Starting WorkFlowOS...")

grok = GrokClient()

print(f"AI Provider: {grok.provider}")
print(f"AI Model: {grok.model}")

generator = WorkflowGenerator(grok)

print("\nGenerating workflow with Grok...")

workflow = generator.generate(detected_workflow)

generator.display_workflow(workflow)