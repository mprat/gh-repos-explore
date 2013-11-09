from flask import Flask 
from flask import render_template, url_for, session, redirect, request, g

from flask.ext.github import GitHub

import json

app = Flask(__name__)
app.config.from_object(__name__)

app.config['GITHUB_CLIENT_ID'] = 'b6603acaf2227fa9c3b5'
app.config['GITHUB_CLIENT_SECRET'] = '8c58928560451849455566f5bf1489d93fab3182'
app.config['GITHUB_CALLBACK_URL'] = 'http://localhost:5000/github-callback'

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

github = GitHub(app)

# class User():
#     def __init__(self, github_token):
#         self.github_access_token = github_token

@app.before_request
def before_request():
    g.token = None
    if 'github_token' in session:
        g.token = session['github_token']

@app.route('/')
def index():
    token = "not logged in"
    if g.token:
        token = g.token
    return render_template("main.html", name=g.token)

@app.route('/login')
def login():
    return github.authorize()

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))

@app.route('/review')
def review_commits():
    y1 = []
    y2 = ["ameena12", "hind12"]
    def meetify(inp):
        return inp + "-meet"
    list_to_rev = map(meetify, y2)
    repo_name = "MEET-YL2"
    c = []
    for username in list_to_rev:
        all_commits = github.get('repos/' + username + '/' + repo_name + '/commits')
        url_msgs = []
        for commit in all_commits:
            url_msg = {'url': commit['html_url'], 'msg': commit['commit']['message']}
            url_msgs.append(url_msg)
        c.append({'username': username, 'url_msgs': url_msgs})
    return render_template("review_commits.html", commit_list=c)

@github.access_token_getter
def token_getter():
    token = g.token
    if token is not None:
        return token

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        return redirect(next_url)

    # user = User(oauth_token)
    session["github_token"] = oauth_token

    return redirect(url_for('review_commits'))

if __name__ == "__main__":
    app.run(debug=True)