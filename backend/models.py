from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
from datetime import datetime

db=SQLAlchemy()

class Follow(db.Model):
 __tablename__ = 'follows'
 followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
 primary_key=True)
 follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
 primary_key=True)

class Likes(db.Model):
    __tablename__="likes"
    user_id=db.Column(db.String,db.ForeignKey('users.id'),primary_key=True)
    blog_id=db.Column(db.Integer,db.ForeignKey('blogs.id'),primary_key=True)

class Dislikes(db.Model):
    __tablename__="dislikes"
    user_id=db.Column(db.String,db.ForeignKey('users.id'),primary_key=True)
    blog_id=db.Column(db.Integer,db.ForeignKey('blogs.id'),primary_key=True)

class Comments(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id=db.Column(db.String,db.ForeignKey('users.id'))
    blog_id=db.Column(db.Integer,db.ForeignKey('blogs.id'))
    comment_time=db.Column(db.DateTime(timezone=True),default=datetime.now())
    comment=db.Column(db.String)

class Blogs(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    blog_title = db.Column(db.String, nullable=False)
    blog_img=db.Column(db.String,default="no-img.jpeg")
    blog_preview = db.Column(db.String)
    blog_content = db.Column(db.String)
    blog_time=db.Column(db.DateTime(timezone=True),default=datetime.now())
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    comments=db.relationship('Comments',foreign_keys=[Comments.blog_id],
                          backref=db.backref('comments', lazy='joined'))
    likes=db.relationship('Likes',foreign_keys=[Likes.blog_id],
                          backref=db.backref('likes', lazy='joined'))
    dislikes=db.relationship('Dislikes',foreign_keys=[Dislikes.blog_id],
                          backref=db.backref('dislikes', lazy='joined'))
    
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))) 

class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String , unique=True, nullable=False)
    password = db.Column(db.String , nullable=False)
    username = db.Column(db.String ,unique=True, nullable=True)
    profile_img=db.Column(db.String,default="no-profile-pic.jpeg")
    fullname = db.Column(db.String,default='')
    about = db.Column(db.String,default='')
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(), unique=True, nullable=False)
    # last_login_at = db.Column(db.Datetime(timezone=True))
    # current_login_at = db.Column(db.Datetime(timezone=True))
    # last_login_ip= db.Column(db.string())
    # current_login_ip= db.Column(db.string())
    # login_count= db.Column(db.integer())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    blogs=db.relationship('Blogs',foreign_keys=[Blogs.user_id],
                          backref=db.backref('user', lazy='joined'))
    comments=db.relationship('Comments',foreign_keys=[Comments.user_id],
                          backref=db.backref('user', lazy='joined'))
    likes=db.relationship('Likes',foreign_keys=[Likes.user_id],
                          backref=db.backref('user', lazy='joined'))
    dislikes=db.relationship('Dislikes',foreign_keys=[Dislikes.user_id],
                          backref=db.backref('user', lazy='joined'))
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],
    backref=db.backref('follower', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')
    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],
    backref=db.backref('followed', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())
