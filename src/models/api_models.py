# Import necessary libraries and modules
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Request model for chat requests.
    Includes the conversation ID and the message from the user.
    """
    sentence: str