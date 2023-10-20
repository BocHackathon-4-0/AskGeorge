import os
from llama_index import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

index = None
balance_index = None
spending_index = None
full_index = None

filename_fn = lambda filename: {'file_name': filename}


def get_balance_index():
    return balance_index

def get_spending_index():
    return spending_index

def get_full_index():
    return full_index

def initialize_indices():
    global balance_index
    global spending_index
    global full_index

    try:
        storage_context = StorageContext.from_defaults(persist_dir="./storage/balance")
        balance_index = load_index_from_storage(storage_context)
            
        storage_context = StorageContext.from_defaults(persist_dir="./storage/spending")
        spending_index = load_index_from_storage(storage_context)

        storage_context = StorageContext.from_defaults(persist_dir="./storage/full")
        full_index = load_index_from_storage(storage_context)

        print("balance index, spending index, full index loaded")
        index_loaded = True
    except:
        index_loaded = False

    if not index_loaded:
        # load data
        balance_docs = SimpleDirectoryReader(
            input_dir="data/balance/",
            filename_as_id=True,
            file_metadata=filename_fn
        ).load_data()
        spending_docs = SimpleDirectoryReader(
            input_dir="data/spending/",
            filename_as_id=True,
            file_metadata=filename_fn
        ).load_data()
        all_docs = SimpleDirectoryReader(
            input_dir="data/", recursive=True,
            filename_as_id=True,
            file_metadata=filename_fn
        ).load_data()

        # build index
        balance_index = VectorStoreIndex.from_documents(balance_docs)
        spending_index = VectorStoreIndex.from_documents(spending_docs)
        full_index = VectorStoreIndex.from_documents(all_docs)

        # persist index
        balance_index.storage_context.persist(persist_dir="./storage/balance")
        spending_index.storage_context.persist(persist_dir="./storage/spending")
        full_index.storage_context.persist(persist_dir="./storage/full")
