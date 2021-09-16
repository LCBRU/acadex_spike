import os
import csv
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor
from dotenv import load_dotenv


class BrcElsAuthor(ElsAuthor):
    def __init__(self, scopus_id):
        self.scopus_id = scopus_id
        super().__init__(uri=f'https://api.elsevier.com/content/author/author_id/{self.scopus_id}')

    @property
    def citation_count(self):
        return self.data[u'coredata'][u'citation-count']

    @property
    def cited_by_count(self):
        return self.data[u'coredata'][u'cited-by-count']

    @property
    def document_count(self):
        return self.data[u'coredata'][u'document-count']

    @property
    def h_index(self):
        return self.data[u'h-index']

COL_SCOPUS_ID = 'scopus_id'
COL_FULL_NAME = 'full_name'
COL_DOCUMENT_COUNT = 'document_count'
COL_CITATION_COUNT = 'citation_count'
COL_H_INDEX = 'h_index'

load_dotenv()

ids = []

with open('author_ids.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    ids = [a[COL_SCOPUS_ID] for a in reader]

client = ElsClient(os.environ["API_KEY"])

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        COL_SCOPUS_ID,
        COL_FULL_NAME,
        COL_DOCUMENT_COUNT,
        COL_CITATION_COUNT,
        COL_H_INDEX,
    ])

    writer.writeheader()

    for id in filter(lambda id: id, ids):
        author = BrcElsAuthor(scopus_id=id)

        if not author.read(client):
            raise RuntimeError('Reading author details failed')

        if not author.read_metrics(client):
            raise RuntimeError('Reading metrics details failed')

        writer.writerow({
            COL_SCOPUS_ID: id,
            COL_FULL_NAME: author.full_name,
            COL_DOCUMENT_COUNT: author.document_count,
            COL_CITATION_COUNT: author.citation_count,
            COL_H_INDEX: author.h_index,
        })
