from commitreview.models import db, User, Commit, Tag 
import sys, csv

def addtags(listoftags, user):
    for tag in listoftags:
        tag = tag.strip()
        t = Tag.query.filter_by(text=tag).first()
        if t is None:
            t = Tag(tag)
            db.session.add(t)
            db.session.commit()
        if t not in user.tags:
            user.tags.append(t)
            db.session.commit()

if __name__=="__main__":
    filename = sys.argv[1]
    f = open(filename, 'rb')
    reader = csv.reader(f)
    for row in reader:
        uname = row[0].strip()
        reponame = row[1].strip()
        if (User.query.filter_by(username=uname).first() is None):
            u = User(uname, reponame)
            addtags(row[1:], u)
            db.session.add(u)
            db.session.commit()
        else: 
            addtags(row[1:], User.query.filter_by(username=uname).first())
            db.session.commit()
    f.close()