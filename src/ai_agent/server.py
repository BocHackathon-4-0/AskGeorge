from flask import Flask
from flask import request
from util import initialize_indices, get_balance_index, get_spending_index

from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI


from llama_index.tools import QueryEngineTool, ToolMetadata

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

@app.route("/query", methods=["GET"])
def query_index():
    balance_index = get_balance_index()
    spending_index = get_spending_index()
    print(balance_index)
    print(spending_index)
    input()
    
    query_text = request.args.get("text", None)
    if query_text is None:
        return "No text found, please include a ?text=blah parameter in the URL", 400

    # build query engine
    balance_engine = balance_index.as_query_engine(similarity_top_k=3)
    spending_engine = spending_index.as_query_engine(similarity_top_k=3)
    
    query_engine_tools = [
        QueryEngineTool(
            query_engine=balance_engine,
            metadata=ToolMetadata(
                name="balance",
                description="Provides information about my account balance (either current and savings), daily, weekly, breakdown with absolute changes from time period to time period."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
        QueryEngineTool(
            query_engine=spending_engine,
            metadata=ToolMetadata(
                name="spending",
                description="Provides information about my spending, it's categories and specifically how much of my money I'm spending where"
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ]

    # build agent

    llm = OpenAI(model="gpt-4")
    agent = ReActAgent.from_tools(query_engine_tools, llm=llm, verbose=True)
    response = agent.chat(query_text)
    return str(response), 200


if __name__ == "__main__":
    initialize_indices()
    app.run(host="0.0.0.0", port=5601)