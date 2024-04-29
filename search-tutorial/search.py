import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class Search:
    def __init__(self):
        self.es = Elasticsearch('http://localhost:9200')  # <-- connection options need to be added here
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def reindex(self):
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        self.insert_documents(documents)

    def create_index(self):
        self.es.indices.delete(index='my_documents', ingore_unavailable=True)
        self.es.indices.create(index='my_documents')
        print('Index created!')

    def insert_document(self, document):
        insert_response = self.es.index(index='my_documents', body=document)
        print('Document inserted!')
        return insert_response

    def insert_documents(self, documents):
        operations = []
        for document in documents:
            operations.append(
                {
                    'index': {
                        '_index': 'my_documents'
                    }
                }
            )
            operations.append(document)
        bulk_response = self.es.bulk(operations=operations)
        print('Bulk inserted!')
        return bulk_response
