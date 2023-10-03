# Import necessary libraries and modules
import asyncio
from typing import AsyncGenerator
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import  LLMChain
from src.utils.prompt_persona import CHAT_PROMPT_TEMPLATE
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from src.load_llm import Load_LLM


class StreamingConversationChain:
    """
    Class for handling streaming conversation chains.
    It creates and stores memory for each conversation,
    and generates responses using the ChatOpenAI model from LangChain.
    """

    def __init__(self,  temperature: float = 0.0):
        """
        Initialize the StreamingConversationChain instance.
        :param temperature: The temperature parameter for the model, controlling the randomness of the output.
        """
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
        # Create a callback handler for streaming responses
        callback_handler = AsyncIteratorCallbackHandler()

        # Load the Language Model (LLM) using the callback handler
        llm = Load_LLM(callback_handler)

        # Retrieve the memory for the conversation, or create a new one if it doesn't exist
        memory = self.memories.get(conversation_id)
        if memory is None:
            memory = ConversationBufferWindowMemory(return_messages=True, memory_key="chat_history")
            self.memories[conversation_id] = memory

        # Create a LLMChain instance with the memory, prompt template, and model
        chain = LLMChain(
            memory=memory,
            prompt=CHAT_PROMPT_TEMPLATE,
            llm=llm,
        )

        # Create a task to generate a response and yield tokens as they're generated
        run = asyncio.create_task(chain.apredict(human_input=message))
        async for token in callback_handler.aiter():
            yield token

        await run

