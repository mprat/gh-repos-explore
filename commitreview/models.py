from commitreview import app 
from flask.ext.sqlalchemy import SQLAlchemy
import dateutil.parser

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
    repo = db.Column(db.String(10))

    def __init__(self, name, repo):
        self.username = name
        self.repo = repo

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20), unique=True)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Tag %r>' % self.text