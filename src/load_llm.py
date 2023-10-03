# Import necessary libraries and modules
from langchain.llms import CTransformers
from typing import AsyncIterator

def Load_LLM(callback_handler:AsyncIterator):
    """
    Function to load the Language Model (LLM).
    :param callback_handler: An asynchronous iterator for handling callbacks.
    :return: A CTransformers instance with the specified model and parameters.
    """
    # Create a CTransformers instance with the specified model and parameters
    llm = CTransformers(
        model = "../models/llama-2-13b-chat.Q4_K_M.gguf",  # Path to the model
        model_type="llama2",  # Type of the model
        temperature = 0.9,  # Temperature parameter for the model
        streaming=True,  # Enable streaming
        callbacks=[callback_handler],  # Callback handler
        n_gpu_layers = -1,  # Number of GPU layers
        n_batch = 2048,  # Batch size
        n_ctx=2048  # Context size
    )
    return llm