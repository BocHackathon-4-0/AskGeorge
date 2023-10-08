from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
from llama_index import ServiceContext
import nest_asyncio

nest_asyncio.apply()

# Using the LlamaDebugHandler to print the trace of the sub questions
# captured by the SUB_QUESTION callback event type
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])
service_context = ServiceContext.from_defaults(callback_manager=callback_manager)

balance_docs = SimpleDirectoryReader(
    input_dir="data/balance/"
).load_data()
spending_docs = SimpleDirectoryReader(
    input_dir="data/spending/"
).load_data()

# build index and query engine
vector_query_engine = VectorStoreIndex.from_documents(
    spending_docs, use_async=True, service_context=service_context
).as_query_engine()

query_engine_tools = [
    QueryEngineTool(
        query_engine=vector_query_engine,
        metadata=ToolMetadata(
            name="spending_docs", description="JSON files containing data on categories and amount of spending"
        ),
    ),
]

query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools,
    service_context=service_context,
    use_async=True,
)

response = query_engine.query(
    "How was my spending changed in the last 3 months?"
)