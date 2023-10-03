# 🚀 FastAPI Streaming Chat API

This project is a FastAPI application that provides a streaming chat API.

## 📝 Description

The application uses a `StreamingConversationChain` to generate responses to chat requests. These responses are then sent as a streaming response.

## 🛠️ Installation

To install the necessary libraries, use the following command:

pip install fastapi uvicorn["standard"] langchain

## 🚀 Usage

To start the server, run the following command:

uvicorn src.main:app --reload

The application provides the following endpoints:

- `POST /api/v1/chat-ria`: 🗨️ This endpoint accepts chat requests and returns responses as a stream. The request data should be provided in the following format:

{
"sentence": "Your sentence here"
}


- `GET /health`: 💓 This endpoint can be used to check if the API is running. It returns a JSON object with the status of the API.

## 🤝 Contributing

Contributions are welcome. Please make sure to update tests as appropriate.

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)