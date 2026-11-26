from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.llm_service import get_answer

app = FastAPI(title="LLM Failover API", version="1.0.0")

class ChatRequest(BaseModel):
    prompt: str
    
# class ChatResponse(BaseModel)
    
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(req: ChatRequest):
    
    result = await get_answer(req.prompt)   # pass the prompt here
    if result["answer"] is None:
        raise HTTPException(status_code=503, detail=result["errors"])
    return result