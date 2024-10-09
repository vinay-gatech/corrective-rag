from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain import hub
from sympy.physics.units import temperature
load_dotenv()

llm         = ChatOpenAI(temperature=0)
rag_prompt  = hub.pull("rlm/rag-prompt")

generation_chain    = rag_prompt | llm | StrOutputParser()
