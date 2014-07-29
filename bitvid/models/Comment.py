from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.restful import fields

from bitvid.shared import db, generate_token

class AuthorField(fields.Raw):
    def format(self,user):
        return user.email

class Comment(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.String(4096))
    token = db.Column(db.String(128))
    #parent_id = db.Column(db.Integer, ForeignKey("Comment.id"))
    #parent = relationship("Comment", backref=backref("children"))

    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref("comments"))

    marshal_fields = {
        "token": fields.String,
    }

    marshal_fields_get = {
        "token": fields.String,
        "title": fields.String,
        "content": fields.String,
        "author": AuthorField(attribute="user")
    }

    def __init__(self,title,content,user,video):
        self.title = title
        self.content = content
        self.user = user
        self.video = video
        self.token = generate_token()