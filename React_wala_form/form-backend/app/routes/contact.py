from fastapi import APIRouter

from app.schemas import ContactFormRequest, ContactFormResponse

router = APIRouter(prefix="/api/contact", tags=["Contact"])

@router.post("/", response_model=ContactFormResponse)
async def submit_contact(form: ContactFormRequest) -> ContactFormResponse:
    print(form.model_dump())
    
    return ContactFormResponse(
        success=True,
        message=f"Thanks, {form.name}. Your message has been received. We will get back to you at {form.email} soon!"
    )