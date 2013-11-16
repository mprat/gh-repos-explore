# from flask import Flask 
from flask import render_template, url_for, session, redirect, request, g, jsonify

from commitreview import app
from commitreview.models import db, User, Commit, Tag

from flask.ext.github import GitHub
# from flask.ext.sqlalchemy import SQLAlchemy

import json
import dateutil.parser

# app = Flask(__name__)
# app.config.from_object(__name__)

app.config['GITHUB_CLIENT_ID'] = 'b6603acaf2227fa9c3b5'
app.config['GITHUB_CLIENT_SECRET'] = '8c58928560451849455566f5bf1489d93fab3182'
app.config['GITHUB_CALLBACK_URL'] = 'http://localhost:5000/github-callback'

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

github = GitHub(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commits.db'


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

@app.route('/review_ajax', methods=['GET'])
def get_commits_to_review():
    filter_list = request.args.get('filter_list', 0, type=str)

    c = Commit.query.filter_by(reviewed=False)
    u = []
    t = Tag.query.all()

    if filter_list:
        filter_list = filter_list.split(",")
        for f in filter_list:
            temptag=Tag.query.filter_by(text=f.strip()).first()
            tempu = User.query.filter(User.tags.contains(temptag)).all()
            for temp_tempu in tempu:
                if temp_tempu not in u:
                    u.append(temp_tempu)
    else:
        u = User.query.order_by(User.username).all()

    return jsonify({'user_list': [i.serialize for i in u], 'commit_list': [i.serialize for i in c]})
    # return jsonify({'commit_list': c, 'user_list': u, 'tags_list': t})
    # return render_template("review_commits.html", commit_list=c, user_list=u, tags_list=t)

@app.route('/review')
def review_commits():
    t = Tag.query.all()
    return render_template("review_commits.html", tags_list=t)

@app.route('/query')
def get_all_commits():
    for user in User.query.all():
        username = user.username
        repo_name = user.repo
        all_commits = github.get('repos/' + username + '/' + repo_name + '/commits')
        url_msgs = []
        for commit in all_commits:
            sha = commit['sha']
            if Commit.query.filter_by(sha=sha).first() is None:
                url = commit['html_url']
                msg = commit['commit']['message']
                date = commit['commit']['author']['date']
                author = user.id
                new_commit = Commit(author, date, msg, sha, url)
                db.session.add(new_commit)
                db.session.commit()
    return redirect(url_for('review_commits'))

@app.route('/markreviewed', methods=['POST'])
def mark_reviewed():
    h = request.form['shahash']
    print h
    c = Commit.query.filter_by(sha=h).first()
    c.reviewed = True
    db.session.commit()
    return redirect(url_for('review_commits'))

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