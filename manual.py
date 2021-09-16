import requests
import json
import os
from ratelimit import limits
from dotenv import load_dotenv
from urllib.parse import urlencode


load_dotenv()


class Author:
    pass


class ScopusClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_author(self, author_id):
        data = self.request(
            URL=f'https://api.elsevier.com/content/author/author_id/{author_id}',
            parameters={
                'field': ','.join(['document-count', 'cited-by-count', 'h-index', 'citation-count', 'given-name', 'surname']),
            }
        )

        return data


    def get_documents(self, author_id):
        data = self.request(
            URL=f'https://api.elsevier.com/content/author/author_id/{author_id}',
            parameters={
                'view': 'documents',
            }
        )

        return data


    @limits(calls=1, period=1)
    def request(self, URL, parameters):

        headers = {
            "X-ELS-APIKey"  : self.api_key,
            "Accept"        : 'application/json'
        }

        r = requests.get(URL, params=parameters, headers=headers)

        self._status_code=r.status_code

        if r.status_code == 200:
            self._status_msg='data retrieved'
            return json.loads(r.text)
        else:
            self._status_msg="HTTP " + str(r.status_code) + " Error from " + URL + " and using headers " + str(headers) + ": " + r.text
            raise requests.HTTPError("HTTP " + str(r.status_code) + " Error from " + URL + "\nand using headers " + str(headers) + ":\n" + r.text)


sc = ScopusClient(api_key=os.environ["API_KEY"])

print(sc.get_documents('7005783434'))
