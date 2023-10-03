import asyncio
from functools import lru_cache
from typing import AsyncGenerator
from langchain.llms import CTransformers
from fastapi import Depends, FastAPI,Request
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import ConversationChain,LLMChain
import asyncio
from functools import lru_cache
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
from langchain.prompts import (
    PromptTemplate,
)
from pydantic import BaseModel
from pydantic_settings import BaseSettings



template = """You are Ria, an efficient personal assistant skilled in extracting key details from tasks. Your responses should be helpful, safe, and free from harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Ensure your responses are unbiased and positive.

You are adept at handling a variety of inquiries, from simple questions to complex explanations. Your skill lies in generating human-like text based on available information, enabling coherent conversations. Your primary role is to understand specific queries and requests for help, and respond in a contextually appropriate manner.

State the desired outcome in your responses and clarify any uncertainties. If a question is incoherent or doesn't make sense, explain why instead of providing incorrect answers. If you don't know the answer, admit it instead of sharing false information.

Introduce yourself once in a conversation, typically at the beginning. Avoid colloquial language and don't respond with "As a personal assistant!".

{chat_history}
Human: {human_input}
Chatbot:"""

CHAT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)


class StreamingConversationChain:
    """
    Class for handling streaming conversation chains.
    It creates and stores memory for each conversation,
    and generates responses using the ChatOpenAI model from LangChain.
    """

    def __init__(self,  temperature: float = 0.0):
        self.memories = {}
        self.temperature = temperature

    async def generate_response(
        self, conversation_id: str, message: str
    ) -> AsyncGenerator[str, None]:
        """
        Asynchronous function to generate a response for a conversation.
        It creates a new conversation chain for each message and uses a
        callback handler to stream responses as they're generated.
        :param conversation_id: The ID of the conversation.
        :param message: The message from the user.
        """
        callback_handler = AsyncIteratorCallbackHandler()
        llm = CTransformers(
            #model = "../models/llama-2-7b-chat.Q4_0.gguf",
            model = "../models/llama-2-13b-chat.Q4_K_M.gguf",
            #model = "../models/falcon-40b-Q3_K_M.gguf",
            model_type="llama2",
            temperature = 0.9,
            streaming=True,
            # callbacks=[],
            callbacks=[callback_handler],
            n_gpu_layers = -1, # Change this value based on your model and your GPU VRAM pool.
            n_batch = 2048, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
            n_ctx=2048
            )

        memory = self.memories.get(conversation_id)
        if memory is None:
            memory = ConversationBufferWindowMemory(return_messages=True,memory_key="chat_history")
            self.memories[conversation_id] = memory
      
        chain = LLMChain(
            memory=memory,
            prompt=CHAT_PROMPT_TEMPLATE,
            llm=llm,
        )

        run = asyncio.create_task(chain.apredict(human_input=message))

        async for token in callback_handler.aiter():
            yield token

        await run


class ChatRequest(BaseModel):
    """Request model for chat requests.
    Includes the conversation ID and the message from the user.
    """
    sentence: str

app = FastAPI()

streaming_conversation_chain = StreamingConversationChain(
)


@app.post("/api/v1/chat-clive", response_class=StreamingResponse)
async def generate_response(data: ChatRequest,request: Request) -> StreamingResponse:
    """Endpoint for chat requests.
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
    """Check the api is running"""
    return {"status": "🤙"}
    

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="localhost",
        port=7000,
        reload=True
    )
