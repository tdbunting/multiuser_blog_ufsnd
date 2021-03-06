import time
import re
from google.appengine.ext import db
from app.models.user import User

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.ReferenceProperty(User,
                                  collection_name='posts',
                                  required=True)
    def snippet(self):
        """ returns a 120 char snippet without any html styling """
        clean = re.compile('<.*?>')
        if len(self.content) < 120:
            return re.sub(clean, '', self.content)

        return re.sub(clean, '', self.content[0:120] + "...")

    def get_comments(self):
        comments = db.GqlQuery("SELECT * FROM Comment WHERE post = :1 ORDER BY created", self.key())
        if comments.count() > 0:
            return comments
        return False

    @classmethod
    def by_id(cls, pid):
        return Post.get_by_id(pid)


    @classmethod
    def recent_posts(cls, max_posts=10):
        return db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT %d" % max_posts)

    @classmethod
    def edit(cls, pid, subject, content, user):
        post = Post.by_id(pid)
        if post and user.username == post.author.username:
            post.subject = subject
            post.content = content
            post.put()
            return True

        return False

    @classmethod
    def delete(cls, pid, user):
        post = Post.by_id(int(pid))
        if post and user.username == post.author.username:
            db.delete(post)
            time.sleep(0.2)
            return True
        return False
