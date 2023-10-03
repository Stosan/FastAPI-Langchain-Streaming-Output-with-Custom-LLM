# Import necessary libraries and modules
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from src.core.stream_chain import StreamingConversationChain
from src.models.api_models import ChatRequest


# Create a FastAPI instance
app = FastAPI()

# Create a StreamingConversationChain instance
streaming_conversation_chain = StreamingConversationChain()

@app.post("/api/v1/chat-ria", response_class=StreamingResponse)
async def generate_response(data: ChatRequest, request: Request) -> StreamingResponse:
    """
    Endpoint for chat requests.
    It uses the StreamingConversationChain instance to generate responses,
    and then sends these responses as a streaming response.
    :param data: The request data.
    """
    return StreamingResponse(
        streaming_conversation_chain.generate_response(
            str(request.client.host), data.sentence
        ),
        media_type="text/event-stream",
    )

@app.get("/health")
async def health():
    """
    Endpoint to check if the API is running.
    """
    return {"status": "🤙"}

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(
        "app:app",
        host="localhost",
        port=7000,
        reload=True
    )