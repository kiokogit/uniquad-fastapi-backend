# indexing, and searching specific indexies
from .client import client as es

# create documents


# def index_documents(index: str, documents: list[dict]): # to be more specified
#     create_index_if_does_not_exist(index)
    
#     for rec in documents:
#         es.index(index=index, document=rec)
    


# def create_index_if_does_not_exist(index):
#     if not es.indices.exists(index=index):
#         es.indices.create(index=index)


