import json
from llama_index.indices.service_context import ServiceContext
from llama_index.indices.struct_store import JSONQueryEngine
from llama_index.llms import OpenAI

def jsonQuery(queryAsk, jsonData, jsonSchema):
    with open(jsonData) as f:
        json_value = json.load(f)

    with open(jsonSchema) as f:
        json_schema = json.load(f)

    llm = OpenAI(model="gpt-4")
    service_context = ServiceContext.from_defaults(llm=llm)
    query_engine = JSONQueryEngine(json_value=json_value, json_schema=json_schema, service_context=service_context)
    response = query_engine.query(queryAsk)

    return response