from flask import *
from datetime import date
from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(50), nullable="False")
    email = db.Column(db.String(60), nullable="False")
    password = db.Column(db.String(60), nullable="False")
    avatar = db.Column(db.LargeBinary)
    anchor = db.Column(db.String(8), default="center")
    scale = db.Column(db.Integer, default=100)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    caption = db.Column(db.String(50), nullable="False")
    ptype = db.Column(db.String(50), nullable="False")
    text = db.Column(db.Text(9999), nullable="False")
    tags = db.Column(db.String(50), nullable="False")
    roles = db.Column(db.String(50), nullable="False")
    user_id = db.Column(db.Integer)
    likes = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=date.today())
    images = db.Column(db.PickleType)
    favorite_for = db.Column(db.PickleType, default=[])



class Message(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(50), nullable="False")
    email = db.Column(db.String(60), nullable="False")
    message = db.Column(db.Text(1000), nullable="False")

    def __repr__():
        return f"<Message {id}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    user_id = db.Column(db.Integer)
    likes = db.Column(db.Integer, default=0)
    favorite_for = db.Column(db.PickleType, default=[])
    text = db.Column(db.Text(9999), nullable="False")
    date = db.Column(db.DateTime, default=date.today())
    post_id = db.Column(db.Integer)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    tag = db.Column(db.String(50), nullable="False")
    caption = db.Column(db.String(150), nullable="False")
    text = db.Column(db.Text(9999), nullable="False")
    date = db.Column(db.DateTime, default=date.today())
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer)
    favorite_for = db.Column(db.PickleType, default=[])
    images = db.Column(db.PickleType, default={})
    heading_image = db.Column(db.LargeBinary)

    def __repr__(post):
        return f"<Post {post.id if post else id}>"
    