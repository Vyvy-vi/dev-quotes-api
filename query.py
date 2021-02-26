import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

AUTH = os.environ.get("HARPER_AUTH_TOKEN")
url = "https://quote-api-vyvyvi.harperdbcloud.com"

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Basic {AUTH}'
}

def nosql_search(table, search_attr, search_val, get_attrs="*"):
    payload = "{\n\t\"operation\":\"search_by_value\",\n\t\"schema\":\"dev\",\n\t\"table\":\"%s\",\n\t\"search_attribute\":\"%s\",\n\t\"search_value\":\"%s\",\n\t\"get_attributes\":[\"%s\"]\n}" % (table, search_attr, search_val, get_attrs)
    res = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(res.text.encode('utf8'))


def sql_query(query):
    payload = "{\n\t\"operation\":\"sql\",\n\t\"sql\":\"%s\"\n}" % (query)
    res = requests.request("POST", url, headers=headers, data = payload)
    return json.loads(res.text.encode('utf8'))

def fetch_by_id(id):
    return sql_query(query=f"SELECT * FROM dev.quotes where id = {id}")

def fetch_by_author(author):
    return sql_query(query=f"SELECT * FROM dev.quotes where Author = '{author}'")

def fetch_author(Author):
    res = nosql_search('author', 'Author', Author, '*')
    if len(res) == 0:
        res = "anonymous"
    else:
        res = res[0]
        res['Author'] = res['Author'].title().replace('_', ' ')
        res = {
                'name': res['Author'],
                'author-id': res['id'],
                'socials': {
                    'Discord': res['Discord'],
                    'Twitter': res['Twitter'],
                    'Github': res['Github']
                    }
                }
    return res

print(fetch_by_id(1))
