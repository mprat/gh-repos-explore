from commitreview import app 
from flask.ext.sqlalchemy import SQLAlchemy
import dateutil.parser

db = SQLAlchemy(app)

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'sha': self.sha,
            'user_id': self.user_id, 
            'time': dump_datetime(self.time),
            'commit_msg': self.commit_msg,
            'url': self.url,
            'reviewed': self.reviewed
        }
    

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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'commits':  self.serialize_commits,
            'tags': self.serialize_tags,
            'repo': self.repo
        }

    @property
    def serialize_commits(self):
        return [item.serialize for item in self.commits]

    @property
    def serialize_tags(self):
        return [item.serialize for item in self.tags]
    

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20), unique=True)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Tag %r>' % self.text

    @property
    def serialize(self):
        return {
            'id': self.id,
            'text': self.text
        }
    