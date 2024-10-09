from pprint import pprint

from dotenv import load_dotenv
from graph.chains.retrieval_grader_chain import GradeDocuments, retrieval_grader
from ingestion import retrieve_documents

load_dotenv()


def test_retrieval_grader_answer_yes()->None:
    question    = "agent memory"
    docs        = retrieve_documents().invoke(question)
    doc_txt     = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score=="yes"

def test_retrieval_grader_answer_no()->None:
    question    = "agent memory"
    docs        = retrieve_documents().invoke(question)
    doc_txt     = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": "How to make pizza", "document": doc_txt}
    )

    assert res.binary_score=="no"
