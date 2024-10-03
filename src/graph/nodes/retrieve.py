# Code for retrieval node
from typing import Any, Dict
from graph.state import GraphState
from ingestion import retrieve_documents

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")

    # Extract question from the current state
    question        = state['question']
    retriever_obj   = retrieve_documents()

    # Perform the semantic search and retrieve documents from the vectorDB
    documents       = retriever_obj.invoke(question)

    return {"documents": documents, "question": question}