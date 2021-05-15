import random
from flask import Flask, request, jsonify

from flask import render_template
from query import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def render_index():
    return render_template("index.html")

# GET /quote/?author=name&num=x
@app.route('/quote/', methods=['GET'])
def query_quote():
    status = [200, "OK", ""]
    author = request.args.get('author')
    num = request.args.get('num')
    num = 1 if not num else int(num)
    if num > quote_amount():
        status = [400, "Bad Reqest - ", "ERROR: num value given by user too large"]
    if author:
        res = fetch_by_author(author)
        if len(res) == 0:
            status = [400, "Bad Request - ", status[-1] + f" ERROR: Author {author} not found"]
            res = fetch_random_quotes(num)
        else:
            try:
                res = random.sample(res, num)
            except:
                status = [400, "Bad Request -", status[-1] + f"ERROR- Indexed author doesn't have that many quotes'"]
                res = random.sample(res, 1)
    else:
        res = fetch_random_quotes(num)
    DATA = {"status": status[0],
            "status_message": f"{status[1]}{status[2]}",
            "quotes": []}
    for q in res:
        try:
            q = q[0]
        except KeyError:
            q = q
        DATA["quotes"].append({
             "id": q['id'],
             "quote": q['Quote'].replace('\u2019', "'"),
             "categories": q['Category'],
             "author": fetch_author(q['Author']),
             "last_edited_at": q['__updatedtime__']
                })
    return jsonify(DATA), status[0]


# GET /quote/random/?num=x
@app.route('/quote/random/')
def random_quote():
    status = [200, "OK", ""]
    num = request.args.get('num')
    if num:
        num = int(num)
        if num > quote_amount():
            status = [400, "Bad Request", f" - ERROR: Value of num too high"]
        res = fetch_random_quotes(num)
    else:
        res = fetch_random_quotes()
    DATA = {"status": status[0],
            "status_message": f"{status[1]}{status[2]}",
            "quotes": []}
    for q in res:
        DATA['quotes'].append({
            "id": q[0]['id'],
            "quote": q[0]['Quote'].replace('\u2019', "'"),
            "categories": q[0]['Category'],
            "author": fetch_author(q[0]['Author']),
            "last_edited_at": q[0]['__updatedtime__']
            })
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
                "quote": res['Quote'].replace('\u2019', "'"),
                "categories": res['Category'],
                "author": fetch_author(res['Author']),
                "last_edited_at": res['__updatedtime__']}
    else:
        status = [404, "Not Found", f" - Resource with id = {id} NOT found"]
        DATA = {"status": status[0], "status_message": f'{status[1]}{status[2]}'}
    return jsonify(DATA), status[0]

# GET /quote/author/<name/author-id>
@app.route('/quote/author/<index>')
def query_by_name(index: str):
    status = [200, "OK", ""]
    DATA = {}

    res = fetch_by_author_id(index) if index.isdigit() else fetch_by_author(index)

    if len(res) != 0:
        DATA = {'status': status[0],
                'status_message': f"{status[1]}{status[2]}",
                'author': fetch_author(res[0]['Author']),
                'quotes': []}
        for q in res:
            quote = {
                "quote": q['Quote'].replace('\u2019', "'"),
                "id": q['id'],
                "last_edited_at": q['__updatedtime__'],
                "categories": q['Category'],
                "author": q["Author"].title().replace("_", " ")
            }
            DATA["quotes"].append(quote)
    else:
        status = [404, "Not Found", f" - Author with name or id = {index} NOT found"]
        DATA = {"status": status[0], 'status_message': f'{status[1]}{status[2]}'}

    return jsonify(DATA), status[0]


if __name__=='__main__':
    app.run(threaded=True, port=5000)
