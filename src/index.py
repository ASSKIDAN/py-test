#! learning py
from flask import Flask, render_template, url_for
from flask_cors import CORS
import requests
import json

with open('config.json') as json_df: config = json.load(json_df)
app = Flask(__name__)
CORS(app)
headers = {
    'user-agent': 'codex-test-python',
    'Accept': 'application/vnd.github.v3+json',
}
auth = (config['github']['user'], config['github']['password'])
count = 50


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/repos', methods=['GET'])
def get_repos():
    url = config['github']['hostapi'] + 'orgs/facebook/repos?page='
    data = list()

    def recursive_load_repos(page):
        res = requests.get(url + str(page) + '&per_page=' + str(count), auth=auth)
        data.extend(res.json())
        if len(res.json()) == count:
            recursive_load_repos(page + 1)

    recursive_load_repos(0)
    return json.dumps(data)


@app.route('/repos/<owner>/<repo>/commits', methods=['GET'])
def get_commits(owner, repo):
    url = config['github']['hostapi'] + 'repos/' + owner + '/' + repo + '/commits?per_page=' + str(count)
    res = requests.get(url, auth=auth, headers=headers)
    return json.dumps(res.json())


if __name__ == '__main__':
    app.run(port=8080, debug=True)
