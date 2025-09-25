from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agent
from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Multi-AI Agent API", version="0.1")

class RequestState(BaseModel):
    model_name: str
    system_prompt: str = "You are a helpful AI assistant."
    messages: List[str]
    allow_search: bool

@app.post("/chat", summary="Get response from AI agent")
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        # logger.warning(f"Model {request.model_name} is not allowed.")
        logger.error(f"Model {request.model_name} is not allowed.")
        raise HTTPException(status_code=400, detail="Invalid model name.")
    try:
        response = get_response_from_ai_agent(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        logger.info(f"Successfully got response from AI Agent: {request.model_name}")
        return {"response": response}
    
    except Exception as e:
        logger.error(f"Error occurred while processing request: {e}")
        raise HTTPException(status_code=500, 
                            detail=str(e) or "Internal Server Error")
