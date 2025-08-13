from fastapi import FastAPI

import llm_model 

app = FastAPI()

@app.get("/")
def root_controller():
    return {"status": "healthy"}

@app.get("/chat")
def ask_hamming(msg: str) -> str:
    return llm_model.ask_hamming(msg)
