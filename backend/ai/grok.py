"""
WorkFlowOS - Grok / AI Integration Engine
Provides unified access to xAI Grok, GroqCloud, and OpenAI with fallback simulation.
"""

import sys
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Ensure root_dir is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.ai.parser import parse_ai_json_response

# Load environment variables from project root .env
load_dotenv(dotenv_path=root_dir / ".env")
load_dotenv()  # Fallback to current working directory


class GrokClient:
    """
    Unified AI Client supporting:
    1. xAI Grok API (via OpenAI client with base_url https://api.x.ai/v1)
    2. GroqCloud API (via groq SDK or OpenAI compatibility)
    3. OpenAI API (official endpoint)
    4. Mock Simulation (fallback when API keys are not yet configured)
    """

    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None):
        self.xai_key = api_key or os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        self.provider = provider
        self.client = None
        self.model = os.getenv("AI_MODEL", "grok-2-latest")
        self.is_mock = False

        self._initialize_client()

    def _initialize_client(self):
        # 1. xAI Grok
        if self.xai_key and (self.provider in (None, "xai", "grok")):
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=self.xai_key,
                    base_url="https://api.x.ai/v1"
                )
                self.provider = "xai"
                if not os.getenv("AI_MODEL"):
                    self.model = "grok-2-latest"
                return
            except Exception as e:
                print(f"⚠️ Failed to initialize xAI client: {e}")

        # 2. GroqCloud
        if self.groq_key and (self.provider in (None, "groq")):
            try:
                from groq import Groq
                self.client = Groq(api_key=self.groq_key)
                self.provider = "groq"
                if not os.getenv("AI_MODEL"):
                    self.model = "llama-3.3-70b-versatile"
                return
            except Exception as e:
                print(f"⚠️ Failed to initialize Groq client: {e}")

        # 3. OpenAI
        if self.openai_key and (self.provider in (None, "openai")):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_key)
                self.provider = "openai"
                if not os.getenv("AI_MODEL"):
                    self.model = "gpt-4o-mini"
                return
            except Exception as e:
                print(f"⚠️ Failed to initialize OpenAI client: {e}")

        # 4. Fallback Mock Simulation
        self.is_mock = True
        self.provider = "mock"
        self.model = "mock-grok-simulator"

    def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        """Sends a chat completion request and returns the raw response text."""
        if self.is_mock or self.client is None:
            return self._mock_reasoning(user_prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ AI API error ({self.provider}): {e}. Falling back to simulation.")
            return self._mock_reasoning(user_prompt)

    def chat_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> Dict[str, Any]:
        """Sends a chat request and parses the output as structured JSON."""
        raw_output = self.chat(system_prompt, user_prompt, temperature)
        return parse_ai_json_response(raw_output)

    def _mock_reasoning(self, user_prompt: str) -> str:
        """Deterministic mock reasoning engine for development and offline testing."""
        import json

        # Infer state from history in user_prompt
        if '"action": "slack_send_message"' in user_prompt:
            return json.dumps({
                "action": "complete",
                "parameters": {},
                "reason": "Customer request has been processed, CRM updated, and team notified in Slack."
            })
        elif '"action": "crm_update_customer"' in user_prompt:
            return json.dumps({
                "action": "slack_send_message",
                "parameters": {
                    "channel": "#customer-ops",
                    "message": "Processed quotation request for customer ABC Ltd."
                },
                "reason": "CRM update succeeded. Sending Slack confirmation to team."
            })
        elif '"action": "crm_search_customer"' in user_prompt:
            return json.dumps({
                "action": "crm_update_customer",
                "parameters": {
                    "customer_id": "CRM-001",
                    "request": "New quotation required",
                    "attachment": "quotation.pdf"
                },
                "reason": "Customer CRM-001 identified. Updating customer record with email request details."
            })
        elif '"action": "gmail_download_attachment"' in user_prompt:
            return json.dumps({
                "action": "crm_search_customer",
                "parameters": {
                    "customer": "ABC Ltd"
                },
                "reason": "Quotation attachment downloaded. Searching CRM for customer record."
            })
        elif '"action": "gmail_read_email"' in user_prompt:
            return json.dumps({
                "action": "gmail_download_attachment",
                "parameters": {
                    "filename": "quotation.pdf"
                },
                "reason": "Email read. Downloading quotation attachment."
            })
        else:
            return json.dumps({
                "action": "gmail_read_email",
                "parameters": {},
                "reason": "Initiating workflow by reading the latest customer email."
            })


# Global default client instance
default_grok_client = GrokClient()