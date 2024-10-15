from dotenv import load_dotenv


from graph.graph import app

load_dotenv()

if __name__=='__main__':
    print("--Advanced RAG Flows--")
    res = app.invoke({"question": "What is agent memory and how is it useful in the larger world?"})
    print(res)