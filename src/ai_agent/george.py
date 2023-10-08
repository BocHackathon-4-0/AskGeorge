from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI


from llama_index.tools import QueryEngineTool, ToolMetadata
'''
try:
    storage_context = StorageContext.from_defaults(persist_dir="./storage/balance")
    balance_index = load_index_from_storage(storage_context)

    storage_context = StorageContext.from_defaults(persist_dir="./storage/spending")
    spending_index = load_index_from_storage(storage_context)

    index_loaded = True
except:
    index_loaded = False

if not index_loaded:
    # load data
    balance_docs = SimpleDirectoryReader(
        input_dir="data/balance/"
    ).load_data()
    spending_docs = SimpleDirectoryReader(
        input_dir="data/spending/"
    ).load_data()

    # build index
    balance_index = VectorStoreIndex.from_documents(balance_docs)
    spending_index = VectorStoreIndex.from_documents(spending_docs)

    # persist index
    balance_index.storage_context.persist(persist_dir="./storage/balance")
    spending_index.storage_context.persist(persist_dir="./storage/spending")
'''

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

llm = OpenAI(model="gpt-4")
agent = ReActAgent.from_tools(query_engine_tools, llm=llm, verbose=True)

'''
llm_instruct = OpenAI(model="gpt-3.5-turbo-instruct")
agent_instruct = ReActAgent.from_tools(
    query_engine_tools, llm=llm_instruct, verbose=True
)
'''
response = agent.chat("What is my current account balance?")
print(str(response))
response = agent.chat("Oh wow, ok. How much is in my savings? And how much is my current + savings?")
print(str(response))