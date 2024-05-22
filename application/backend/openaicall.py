import os
from datetime import datetime
from openai import OpenAI

API_KEY = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY

from tenacity import retry, wait_random_exponential, stop_after_attempt
import logging

client = OpenAI()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, function_call=None, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            functions=tools,
            function_call=function_call
        )
        log.info(f"API response: {response}")
        return response
    except Exception as e:
        log.error("Unable to generate ChatCompletion response")
        log.error(f"Exception: {e}")
        return e
