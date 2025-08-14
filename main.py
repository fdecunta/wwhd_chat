from fastapi import FastAPI
from llm_model import ask_hamming

app = FastAPI()

@app.get("/")
def root_controller():
    return {"status": "healthy"}

@app.get("/chat")
def ask_hamming(msg: str) -> str:
    return ask_hamming(msg)
