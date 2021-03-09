import random
from flask import Flask, request, jsonify
from query import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

QUOTES = {
        "author1": ['quote1', 'quote2', 'quote34'],
        "author2": ['quote3'],
        "anonymous": ['quote5', 'quote7']
        }

@app.route('/')
def render_index():
    return 'beep boop'

#/?author=name&num=x
@app.route('/quote/', methods=['GET'])
def query_quote():
    status = [200, "OK", ""]
    author = request.args.get('author')
    num = request.args.get('num')
    random_author = random.choice(list(QUOTES.keys()))
    DATA = {"quotes": [{random.choice(QUOTES[random_author]): random_author}]}
    if author and (author in QUOTES):
        DATA = {"quotes": [{random.choice(QUOTES[author]): author}]}
        if num:
            while len(DATA["quotes"]) < int(num):
                rand_q = {random.choice(QUOTES[author]): author}
                DATA["quotes"] += [rand_q] if rand_q not in DATA["quotes"] else []
                if int(num) > len(QUOTES[author]) and len(DATA["quotes"]) == len(QUOTES[author]):
                    status = [400, "Bad Request", " - ERROR: num value given by user too large"]
                    break
    else:
        if num:
            NUM_QUOTES = sum([len(QUOTES[i]) for i in QUOTES])
            while len(DATA["quotes"]) < int(num):
                rand_qa = random.choice(list(QUOTES.items()))
                rand_q = {random.choice(rand_qa[1]): rand_qa[0]}
                DATA["quotes"] += [rand_q] if rand_q not in DATA["quotes"] else []
                if int(num) > NUM_QUOTES and len(DATA["quotes"]) == NUM_QUOTES:
                    status = [400, "Bad Request", f" - ERROR: num value given by user too large"]
                    break
        if author and author not in QUOTES:
            if status == 400:
                status[2] += f" and No entries found for queried author- {author}..."
            else:
                status = [400, "Bad Request", f" - ERROR: No entries found for queried author- {author}"]
    DATA = {**{"status": status[0], "status_message": f'{status[1]}{status[2]}'}, **DATA}
    return jsonify(DATA), status[0]

#/?num=x
@app.route('/quote/random')
def random_quote():
    status = [200, "OK", ""]
    random_author = random.choice(list(QUOTES.keys()))
    num = request.args.get('num')
    if num:
        while len(DATA["quotes"]) < int(num):
            rand_qa = random.choice(list(QUOTES.items()))
            rand_q = {random.choice(rand_qa[1]): rand_qa[0]}
            DATA["quotes"] += [rand_q] if rand_q not in DATA["quotes"] else []
            if int(num) > NUM_QUOTES and len(DATA["quotes"]) == NUM_QUOTES:
                status = [400, "Bad Request", " - ERROR: num value given by user too large"]
                break
    DATA = {**{"status": status[0], "status_message": f'{status[1]}{status[2]}'}, **DATA}
    return jsonify(DATA), status[0]

# GET /quote/<id>
@app.route('/quote/<int:id>')
def query_by_id(id: int):
    status = [200, "OK", ""]
    res = fetch_by_id(id)
    if len(res) != 0:
        res = res[0]
        DATA = {"status": status[0],
                "status_message": f"{status[1]}{status[2]}",
                "id": res['id'],
                "quote": res['Quote'],
                "categories": res['Category'],
                "author": fetch_author(res['Author']),
                "last_eddited_at": res['__updatedtime__']}
    else:
        status = [404, "Not Found", f" - Resource with id = {id} NOT found"]
        DATA = {"status": status[0], "status_message": f'{status[1]}{status[2]}'}
    return jsonify(DATA), status[0]

# GET /quote/author/<name/author-id>
@app.route('/quote/author/<index>')
def query_by_name(index: str):
    status = [200, "OK", ""]
    DATA = {}

    if index.isdigit():
        res = fetch_by_author_id(index)
    else:
        res = fetch_by_author(index)
    if len(res) != 0:
        DATA = {'status': status[0],
                'status_message': f"{status[1]}{status[2]}",
                'author': fetch_author(res[0]['Author']),
                'quotes': []}
        for q in res:
            quote = {
                "quote": q['Quote'],
                "id": q['id'],
                "last_eddited_at": q['__updatedtime__'],
                "categories": q['Category'],
                "author": q["Author"].title().replace("_", " ")
            }
            DATA["quotes"].append(quote)
    else:
        status = [404, "Not Found", f" - Author with name = {name} NOT found"]
        DATA = {"status": status[0], 'status_message': f'{status[1]}{status[2]}'}
    return jsonify(DATA), status[0]

if __name__=='__main__':
    app.run()
