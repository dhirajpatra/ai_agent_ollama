import os
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain_community.llms import Ollama

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

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
    classification: str
    entities: List[str]
    summary: str

# Function to classify text
def classification_node(state: State):
    """Classify the text into predefined categories."""
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Classify the following text into one of the categories: News, Blog, Research, or Other.\n\nText: {text}\n\nCategory:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    classification = llm.invoke([message]).strip()
    return {"classification": classification}

# Function to extract named entities
def entity_extraction_node(state: State):
    """Extract named entities from text."""
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Extract all entities (Person, Organization, Location) from the following text. Provide them as a comma-separated list.\n\nText: {text}\n\nEntities:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    entities = llm.invoke([message]).strip().split(", ")
    return {"entities": entities}

# Function to summarize text
def summarize_node(state: State):
    """Summarize text in one sentence."""
    prompt = PromptTemplate.from_template(
        "Summarize the following text in one sentence.\n\nText: {text}\n\nSummary:"
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
