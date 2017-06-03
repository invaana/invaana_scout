import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SCOUT_PATH = os.path.join(CURRENT_PATH, '..')
sys.path.append(SCOUT_PATH)
from flask import Flask, render_template, request, jsonify
from flask_mongoengine import MongoEngine
from browsers.bing import BrowseBing
from scout import ScoutThis

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'invaana_scout',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine(app)


@app.route("/")
def hello():
    return render_template('index.html',)


@app.route("/test")
def test():
    return "Test done, working greate!"


@app.route("/apis/browse/")
def browse():
    """
    To search in a browser
    Usage:
        http://localhost:5000/apis/browse/?q=innovation%20centres
        
    :return:
    """
    kw = request.args.get('q', None)
    if kw:
        scout_instance = ScoutThis(kw=kw, generate_kws=False)
        scout_instance.run()
        return jsonify(scout_instance.data)
    return {}

if __name__ == "__main__":
    app.run(debug=True)