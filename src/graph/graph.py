from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from graph.constants import RETRIEVE, GENERATE, GRADE_DOCUMENT, WEB_SEARCH
from graph.nodes import retrieve, generate, grade_documents, web_search
from graph.state import GraphState


load_dotenv()

def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")
    if state["web_search"]:
        print("""---DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO THE QUESTION, INCLUDE WEB SEARCH---""")
        return WEB_SEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE

graph_builder  = StateGraph(state_schema=GraphState)

graph_builder.add_node(RETRIEVE, retrieve)
graph_builder.add_node(GRADE_DOCUMENT, grade_documents)
graph_builder.add_node(WEB_SEARCH, web_search)
graph_builder.add_node(GENERATE, generate)

graph_builder.add_edge(RETRIEVE, GRADE_DOCUMENT)
graph_builder.add_conditional_edges(
    GRADE_DOCUMENT,
    decide_to_generate,
    path_map={
        WEB_SEARCH: WEB_SEARCH,
        GENERATE: GENERATE
    }
)
graph_builder.add_edge(WEB_SEARCH, GENERATE)
graph_builder.add_edge(GENERATE, END)

graph_builder.set_entry_point(RETRIEVE)

app = graph_builder.compile()
app.get_graph().draw_mermaid_png(output_file_path="c-rag-graph.png")