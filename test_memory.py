from backend.agent.memory import AgentMemory


print("\n")
print("=" * 60)
print("🧠 MEMORY TEST")
print("=" * 60)


memory = AgentMemory()


workflow = {
    "workflow_name": "Process Customer Request",
    "intent": "Automatically process customer quotation requests.",
    "actions": [
        {
            "step": 1,
            "action": "gmail_read_email"
        },
        {
            "step": 2,
            "action": "gmail_download_attachment"
        },
        {
            "step": 3,
            "action": "crm_search_customer"
        },
        {
            "step": 4,
            "action": "crm_update_customer"
        },
        {
            "step": 5,
            "action": "slack_send_message"
        }
    ],
    "confidence": 0.98
}


# Save workflow
memory.save_workflow(
    workflow
)


# Save fake execution
memory.save_execution(
    {
        "success": True,
        "status": "completed",
        "execution_history": []
    },
    workflow_name="Process Customer Request"
)


# Read memory
context = memory.get_agent_context()


print("\n📚 STORED AGENT CONTEXT:")
print(context)


print("\n")
print("=" * 60)
print("✅ MEMORY TEST COMPLETE")
print("=" * 60)