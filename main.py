import random
from flask import Flask, request, jsonify

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

if __name__=='__main__':
    app.run()
