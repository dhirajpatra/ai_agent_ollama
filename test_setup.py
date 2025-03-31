import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# initialize the OpenAI API key
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0,
)

# Test the OpenAI API key
def test_openai_api_key():
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"
    assert llm is not None, "Failed to initialize ChatOpenAI with the API key"
    print("OpenAI API key is set and ChatOpenAI initialized successfully.")

# Test the model
response = llm("What is the capital of France?")
print("Response from OpenAI API:", response)

