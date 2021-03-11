import requests
import json
import os
import random

from dotenv import load_dotenv

load_dotenv()

AUTH = os.environ.get("HARPER_AUTH_TOKEN")
url = "https://quote-api-vyvyvi.harperdbcloud.com"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {AUTH}'
}


def nosql_search(table, search_attr, search_val, get_attrs="*"):
    payload = "{\n\t\"operation\":\"search_by_value\",\n\t\"schema\":\"dev\",\n\t\"table\":\"%s\",\n\t\"search_attribute\":\"%s\",\n\t\"search_value\":\"%s\",\n\t\"get_attributes\":[\"%s\"]\n}" % (
        table, search_attr, search_val, get_attrs)
    res = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(res.text.encode('utf8'))


def sql_query(query):
    payload = "{\n\t\"operation\":\"sql\",\n\t\"sql\":\"%s\"\n}" % (query)
    res = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(res.text.encode('utf8'))


def fetch_by_id(id):
    return sql_query(query=f"SELECT * FROM dev.quotes where id = {id}")


def fetch_by_author(author):
    return sql_query(
        query=f"SELECT * FROM dev.quotes where Author = '{author}'")


def fetch_by_author_id(id):
    author = nosql_search('author', 'id', id, 'Author')[0]['Author']
    return fetch_by_author(author)


def fetch_author(Author):
    res = nosql_search('author', 'Author', Author)
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


def fetch_random_quotes(num = 1):
    QUOTES = []
    quotes_num = quote_amount()
    if num > quotes_num:
        data = sql_query(query="SELECT * FROM dev.quotes")
        return [[i] for i in data]

    else:
        nums = random.sample(range(0, quotes_num), num)
        for i in nums:
            QUOTES.append(sql_query(query="SELECT * FROM dev.quotes WHERE id = %s" % i))
        return QUOTES

def quote_amount():
    payload = "{\n\t\"operation\":\"describe_table\",\n\t\"table\":\"quotes\",\n\t\"schema\":\"dev\"\n}"
    res = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(res.text.encode('utf8'))['record_count']
