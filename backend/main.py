"""
WorkFlowOS - Main Application Server
Exposes REST endpoints for triggering agents, workflows, and monitoring executions.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from backend.agent.agent import WorkFlowAgent
from backend.ai.grok import default_grok_client

app = FastAPI(
    title="WorkFlowOS API",
    description="Autonomous workflow discovery and execution backend.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorkflowExecutionRequest(BaseModel):
    name: str
    trigger: str
    actions: List[str]
    condition: Optional[str] = None
    max_steps: Optional[int] = 15


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "WorkFlowOS Backend",
        "ai_provider": default_grok_client.provider,
        "ai_model": default_grok_client.model
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/agent/run")
def run_agent(request: WorkflowExecutionRequest):
    try:
        agent = WorkFlowAgent()
        workflow_data = request.model_dump()
        max_steps = workflow_data.pop("max_steps", 15)
        
        result = agent.run(workflow_data, max_steps=max_steps)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
