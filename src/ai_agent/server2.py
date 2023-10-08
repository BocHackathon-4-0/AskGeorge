from flask import Flask
from flask import request
from flask_cors import CORS

from util import initialize_indices, get_balance_index, get_spending_index

from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI

from llama_index.tools import QueryEngineTool, ToolMetadata

from tools import add_tool, multiply_tool

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello World!"

@app.route("/query", methods=["GET"])
def query_index():
    balance_index = get_balance_index()
    spending_index = get_spending_index()

    
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
    agent = OpenAIAgent.from_tools(
            [multiply_tool, add_tool] + query_engine_tools, 
            llm=llm, 
            verbose=True,
            system_prompt="You are AskGeorge, an expert personal financial helper with context about my spending (i.e. which categories I spend in, what stores I spend in) as well as my earnings and account balances. You also will eventually learn some of my goals. The date today is 2023-10-08 (8th of October, 2023). This corresponds to Month 10 in the data sources that you will consult, so if I ask you about last month, I'm referring to month 9. If I ask you how much money I have all together, add the latest Month 10 money from my current account to my savings account. You are almost always talking about money or percentage changes, the currency is euros, so when you format numbers make sure to add the currency sign and if it's a decimal number make it 2 decimal points."
            )
    response = agent.chat(query_text)
    return str(response), 200


if __name__ == "__main__":
    initialize_indices()
    app.run(host="0.0.0.0", port=5601)