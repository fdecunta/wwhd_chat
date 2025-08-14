from dotenv import load_dotenv
import os
import litellm

load_dotenv()

TALK_PATH = "./YouAndYourResearch.txt"
with open(TALK_PATH, 'r') as f:
    full_talk = f.read()

prompt_template = """
You are an assistant that talks like if you were Richard Hamming. 

Answer questions based ONLY on Hamming's famous talk, You And Your Research.

Follow this guidelines:

- Give short answers
- Ignore non science or tech questions
- Don't go out of character.
- Be provocative 

Here is the full talk: \\n
"""

system_msg = prompt_template + full_talk

def ask_hamming(msg):
    messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": msg},
    ]
    
    response = litellm.completion(
        model="gradient_ai/llama3.3-70b-instruct",
        api_key=os.environ["DIGITALOCEAN_INFERENCE_KEY"],
        messages=messages,
    ) 
    
    return response.choices[0].message.content
