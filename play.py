from flask import Flask 
from flask import render_template, url_for, session, redirect, request, g

from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy

import json
import dateutil.parser

app = Flask(__name__)
app.config.from_object(__name__)

app.config['GITHUB_CLIENT_ID'] = 'b6603acaf2227fa9c3b5'
app.config['GITHUB_CLIENT_SECRET'] = '8c58928560451849455566f5bf1489d93fab3182'
app.config['GITHUB_CALLBACK_URL'] = 'http://localhost:5000/github-callback'

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

github = GitHub(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commits.db'
db = SQLAlchemy(app)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sha = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime)
    commit_msg = db.Column(db.Text)
    url = db.Column(db.Text)
    reviewed = db.Column(db.Boolean, default=False)

    def __init__(self, author_id, time, commit_msg, sha, url):
        self.sha = sha
        self.time = dateutil.parser.parse(time)
        self.commit_msg = commit_msg
        self.url = url
        self.user_id = author_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    commits = db.relationship('Commit', backref='user')
    tags = db.relationship('Tag', secondary=tags,
        backref='user')

    def __init__(self, name):
        self.username = name

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20), unique=True)

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
    c = Commit.query.filter_by(reviewed=False)#.order_by(Commit.user)
    return render_template("review_commits.html", commit_list=c)

@app.route('/query')
def get_all_commits():
    y1 = []
    y2a = ["angelina12", "costas12", "ido12", "kais12", "kochava12", "nadeen12", "nadine12", "natalie12", "nina12", "omar12", "omer12", "omri12", "revital12", "ronl12", "sagi12", "waseem12", "yarden12", "yasmine12"]
    y2b = ["ameena12", "hind12"]
    def meetify(inp):
        return inp + "-meet"
    list_to_rev = map(meetify, y2a)
    repo_name = "MEET-YL2"
    for user in User.query.all():
        username = user.username
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