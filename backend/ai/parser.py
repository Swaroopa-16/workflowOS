"""
WorkFlowOS AI Response Parser
Handles extraction and validation of structured JSON responses from LLM outputs.
"""

import json
import re
from typing import Any, Dict


def parse_ai_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Safely cleans and parses JSON from an AI response string.
    Handles markdown fences, extraneous text, and trailing formatting.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty response received from AI model.")

    cleaned = raw_text.strip()

    # Remove markdown code blocks if present (```json ... ``` or ``` ...)
    if "```" in cleaned:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
        if match:
            cleaned = match.group(1).strip()
        else:
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    # Attempt direct JSON load
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # Extract first JSON object from substring if mixed with text
    json_match = re.search(r"\{[\s\S]*\}", cleaned)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError as err:
            raise ValueError(f"Failed to parse extracted JSON object: {err}\nRaw text: {raw_text}")

    raise ValueError(f"Could not parse valid JSON from AI response:\n{raw_text}")
