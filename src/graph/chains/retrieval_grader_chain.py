from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

load_dotenv(dotenv_path='../../.env')

llm = ChatOpenAI(temperature=0)

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents"""

    # Important for the LLM to decide whether doc is important or not. Enforcement of the schema
    binary_score:str    = Field(
        description="Documents are relevant to the question, 'yes' or 'no'",
    )

# LLM is going to use function calling. For every doc: PydanticOutput
structured_llm_grader   = llm.with_structured_output(GradeDocuments)

system  = """You are a grader assessing relevance of a retrieved document to a user question. \n
             If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.
             Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. 
"""

grade_prompt    = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}")
    ]
)

retrieval_grader    = grade_prompt | structured_llm_grader