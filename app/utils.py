from flask import *
from flask_login import UserMixin
from app.models import Users, Product, Post
from app import index_
import tantivy


class UserLogin(UserMixin):
    def __init__(self):
        self.__user = None

    @staticmethod
    def fromDB(user_id):
        return UserLogin().create(Users.query.get(user_id))

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True if self.__user else False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False if self.__user else True

    def get_name(self):
        return str(self.__user.name)

    def get_id(self):
        return str(self.__user.id)

    def get_avatar(self, app1):
        img = None
        if not self.__user.avatar:
            try:
                with app1.open_resource(
                    app1.root_path
                    + url_for("static", filename="images/default_avatars/default.png"),
                    "rb",
                ) as f:
                    img = f.read()
            except FileNotFoundError as e:
                return "Default avatar have not been found" + str(e)
        else:
            img = self.__user.avatar

        return img

    def get_anchor(self):
        return str(self.__user.anchor)

    def get_scale(self):
        return str(self.__user.scale)
    
    def is_post_favorite(self, id):
        print(self.__user.id, Post.query.get(id).favorite_for)
        return self.__user.id in Post.query.get(id).favorite_for
    
    def is_product_favorite(self, id):
        return self.__user.id in Product.query.get(id).favorite_for

    def verifyExt(self, filename):
        ext = filename.rsplit(".", 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False
    

def write_indexes():
    writer = index_.writer()
    posts = Post.query.all()
    
    for post in posts:
        writer.add_document(tantivy.Document(
            doc_id=post.id,
            caption=[post.caption],
            text=[f"""{post.text}"""],
        ))

    writer.commit()
    writer.wait_merging_threads()
    index_.reload()