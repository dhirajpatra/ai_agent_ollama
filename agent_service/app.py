import os
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain_community.llms import Ollama

from fastapi.middleware.cors import CORSMiddleware


# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Ollama Llama 3 model
llm = Ollama(
    model="deepseek-r1:1.5b",
    base_url="http://ollama_server:11434",  # Ensure correct endpoint
    temperature=0,
)

# Define request/response schema
class InputText(BaseModel):
    text: str

class OutputData(BaseModel):
    classification: str
    entities: List[str]
    summary: str

# Define state structure
class State(Dict):
    text: str
    classification: str = ""
    entities: List[str] = []
    summary: str = ""

# Function to classify text
def classification_node(state: State):
    """Classify text into categories."""
    # Define the classification prompt
    classification_prompt = """Classify the following text into one of these categories: 
    - News
    - Blog
    - Research
    - Other

    Text: "{text}"

    Respond with only the category name."""


    prompt = PromptTemplate(
        input_variables=["text"],
        # template="Classify the following text into one of the categories: News, Blog, Research, or Other.\n\nText: {text}\n\nCategory:"
        template=classification_prompt
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    classification = llm.invoke(message.content).strip()
    return {"classification": classification}

# Function to extract named entities
def entity_extraction_node(state: State):
    """Extract named entities from text."""
    # Define the entity extraction prompt
    entity_extraction_prompt = entity_extraction_prompt = """Extract key entities (people, organizations, locations) from the text:

    Text: "{text}"

    Respond with a JSON list of entities only."""


    prompt = PromptTemplate(
        input_variables=["text"],
        # template="Extract all entities (Person, Organization, Location) from the following text. Provide them as a comma-separated list.\n\nText: {text}\n\nEntities:"
        template=entity_extraction_prompt
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    entities = llm.invoke(message.content).strip().split(", ")
    return {"entities": entities}

# Function to summarize text
def summarize_node(state: State):
    """Summarize text in one sentence."""
    # Define the summarization prompt
    summary_prompt = summary_prompt = """Summarize the following text in one concise sentence:

    Text: "{text}"

    Respond with only the summary sentence."""

    # template = "Summarize the following text in one sentence.\n\nText: {text}\n\nSummary:"
    template = summary_prompt
    prompt = PromptTemplate.from_template(
        template=template,
    )
    chain = prompt | llm
    response = chain.invoke({"text": state["text"]})
    return {"summary": response.strip()}


# Define LangGraph workflow
graph = StateGraph(State)
graph.add_node("classification_node", classification_node)
graph.add_node("entity_extraction", entity_extraction_node)
graph.add_node("summarization", summarize_node)

graph.set_entry_point("classification_node")
graph.add_edge("classification_node", "entity_extraction")
graph.add_edge("entity_extraction", "summarization")
graph.add_edge("summarization", END)

# Compile the graph
workflow = graph.compile()

@app.post("/analyze", response_model=OutputData)
def analyze_text(input_data: InputText):
    """API endpoint to analyze text"""
    try:
        state_input = {"text": input_data.text}
        result = workflow.invoke(state_input)
        return {
            "classification": result["classification"],
            "entities": result["entities"],
            "summary": result["summary"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "running"}

# Run FastAPI server (For local debugging)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
