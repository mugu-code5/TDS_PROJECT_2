import os
import httpx
import json
import logging
from dotenv import load_dotenv  

from app.utils.function_calls import function_call
from app.utils.function import *

load_dotenv()

# Load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# API Endpoints
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

# Headers for OpenAI
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}
import asyncio

import asyncio
async def maing(task: str):
    logging.debug(f"📤 Sending request to OpenAI with task: {task}")

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        try:
            response = await client.post(
                OPENAI_URL,
                headers=HEADERS,
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": task}],
                    "tools": function_call,
                    "tool_choice": "auto",
                },
            )
            logging.debug(f"🔍 OpenAI Response: {response.status_code} - {response.text}")

            # If successful, return response
            if response.status_code == 200:
                response_json = response.json()
                logging.info(f"✅ API Raw Response: {json.dumps(response_json, indent=2)}")
                return response_json

            # If rate limited (429), return an error immediately
            if response.status_code == 429:
                logging.error("❌ Rate limited! No retries allowed.")
                return {"error": "Rate limit exceeded. Please try again later."}

            # Log other errors
            logging.error(f"❌ API Error {response.status_code}: {response.text}")
            return {"error": response.text}

        except Exception as e:
            logging.error(f"❌ API request failed: {e}")
            return {"error": str(e)}

async def chatgpt(query, file_loc):
    result = await maing(query)

    # Check if API returned an error
    if "error" in result:
        logging.error(f"❌ OpenAI API Error: {result['error']}")
        return result

    try:
        message = result.get("choices", [{}])[0].get("message", {})
    except (KeyError, IndexError):
        logging.error(f"❌ Unexpected API response format: {result}")
        return {"error": "Unexpected API response format"}

    # Debugging: Log response message
    logging.debug(f"🔍 Processed message: {message}")

    # Handle function calls properly
    if "tool_calls" in message:
        function_name = message["tool_calls"][0]["function"]["name"]
        function_args = json.loads(message["tool_calls"][0]["function"]["arguments"])
        logging.debug(f"🔧 Function call detected: {function_name}, Args: {function_args}")

        if function_name == "vscode_code_s":
            return {"answer": vscode_code_s()}
        elif function_name == "format_and_hash":
            return {"answer": format_and_hash(file_loc)}
        elif function_name == "send_request":
            return {"answer": send_request(url=function_args["url"], email=function_args["email"])}
        elif function_name == "calculate_formula":
            return {"answer": calculate_formula(
                sheet_type=function_args["sheet_type"],
                formula=function_args["formula"],
                values=function_args["values"]
            )}
        elif function_name == "extract_hidden_value":
            return {"answer": extract_hidden_value(html=function_args["html"])}

    return {"error": "No valid function call detected."}
