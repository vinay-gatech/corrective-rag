from typing import List, TypedDict

# include all the states needed for graph execution
class GraphState(TypedDict):
    """
    Represents the

    Attributes:
        question:   Question
        generation: LLM generation
        web_seach:  Whether to search the web for additional info
        documents:  List of documents
    """

    question:   str
    generation: str
    web_seach:  bool
    documents:  List[str]
