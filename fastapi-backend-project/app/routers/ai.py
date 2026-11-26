import asyncio
from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["Async Demo"])

client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    
@router.post("/ask")
async def ask_llm(data: AskRequest):
    try:
        response = await client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a helpful assignment."
                "Answer clearly and concisely."
            ),
            input=data.question,
        )
        return {"answer": response.output_text}
    
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="The AI service is Temporarily unvailable",
        )