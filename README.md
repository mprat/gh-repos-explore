gh-repos-explore
================

This is a small project that will make my teaching / grading / feedback for the MEET yearlong curriculum much easier. There are a total of about 120 students, and I want to be able to keep track of their code submission assignments and give them feedback.  

Since we are using Github as a primary means of submitting work, I can look at each student's commits and comment on them individually. This small Flask / SQLAlchemy / AJAX server does that for me, also allowing me to filter the users by a series of tags that I made. When you run it, it runs on localhost:5000 and that is currently what it is configured to run as. 

The time bottleneck is the set of queries to Github (using the Github API) to retrieve the commit histories of the 120ish students. This is why the local database exists in the first place. The idea is that this massive query for commit histories will only have to happen once a day or so (or you can choose to run it any time by clicking the button).

To run the server: 
`python runserver.py` 

(it even comes with a database - commits.db - that has all the student's progress so far). If you want to make your own database, you first need to set up the tables. To do that, do the following: 

1. Open a python shell
2. Do `from commitreview.models import db`
3. Run `db.create_all()`

Your tables should now be set up. You can either specify users in a file (look at all_users.csv for how to format the users / repo name / tags file) and then run `python importusers.py FILENAME.csv` and the users will be imported for you. 

The format of `all_users.py` is this:
`username, repo_name, tag1, tag2`, with each user entry on a separate line.

To access the main page it will first authenticate with Github so it can query it more than 50 times a minute. To do this, go to the `/login` URL. Once you are logged in (if you are not redirected), navigate to `/review` to see the students and all of their commits.  

BIGGEST PROBLEM / STUPID: I manually added DOM elements in the jQuery / AJAX calls. I should have figured out a smarter way to use template includes to make my life easier, but whatever. That's for the next iteration. And I still have the old template file I would use when this happens, so that is good news.
