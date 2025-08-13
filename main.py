import os
from langchain_gradient import ChatGradient
from dotenv import load_dotenv

from langchain_core.documents.base import Blob
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from fastapi import FastAPI

load_dotenv()
PDF_PATH = "./YouAndYourResearch.pdf"

def load_talk(PDF_PATH):
    """Load Hamming's talk"""
    blob = Blob.from_path(PDF_PATH)
    parser = PyPDFParser(mode = "single")
    
    docs = []
    docs_lazy = parser.lazy_parse(blob)
    for doc in docs_lazy:
        docs.append(doc)
    
    return(docs[0].page_content)

prompt_template = """
You are an assistant that talks like if you were Richard Hamming. 

Answer questions based ONLY on Hamming's famous talk, You And Your Research.

Follow this guidelines:

- Give short answers
- Ignore non science or tech questions
- Don't go out of character.
- Be provocative 

Full talk: {talk}

Question: {question}
"""


def init_chatbot(prompt_template):
    prompt = PromptTemplate.from_template(prompt_template)
    llm = ChatGradient(
            model="llama3.3-70b-instruct",
            api_key=os.getenv('DIGITALOCEAN_INFERENCE_KEY'),
             max_tokens=6000
    )
    parser = StrOutputParser()
    chain = prompt | llm | parser

    return chain


full_talk = load_talk(PDF_PATH)
chain = init_chatbot(prompt_template)

app = FastAPI()


@app.get("/")
def root_controller():
    return {"status": "healthy"}

@app.get("/chat")
def ask_hamming(msg: str) -> str:
    prompt_input = {
        "talk": full_talk,
        "question": msg
    }

    response = chain.invoke(prompt_input)
    return response
