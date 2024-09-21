from flask import *
from flask_sqlalchemy import SQLAlchemy
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    login_required,
    logout_user,
)
import flask_mail as fmail


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
app.config["SECRET_KEY"] = "asdkfjasgnbmpobhjkw[dffmljdfjgfg]"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
app.app_context().push()
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please, login to open the page"
login_manager.login_message_category = "neutral"
mail = fmail.Mail(app)

post_image_dict = {}


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


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


class UserLogin:
    def __init__(self):
        self.__user = None

    def fromDB(self, user_id):
        self.__user = Users.query.get(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

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


class Message(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(50), nullable="False")
    email = db.Column(db.String(60), nullable="False")
    message = db.Column(db.Text(1000), nullable="False")

    def __repr__():
        return f"<Message {id}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(50), nullable="False")
    user_id = db.Column(db.Integer)


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

    def __repr__():
        return f"<Post {id}>"


@app.route("/")
def index():
    products = Product.query.order_by(Product.likes.desc()).all()
    return render_template("index.html", products=products, address="/")


@app.route("/user_avatar")
def user_avatar():
    img = current_user.get_avatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers["Content-Type"] = "image/png"
    return h

@app.route('/load_port_image/<int:id>/<int:num>')
def load_port_image(id, num):
    product = Product.query.get(id)
    h = make_response(product.images[num])
    h.headers["Content-Type"] = "image/png"
    return h


@app.route('/post/save_image', methods=["POST", "GET"])
def post_save_image():
    global post_image_dict
    if request.method == "POST":
        images = request.files.getlist('images')
        for image in images:
            post_image_dict[image.filename] = image.read()

        try:
            db.session.commit()
        except Exception:
            return "Data base error"
    
    return jsonify()


@app.route('/post/delete_image', methods=["POST", "GET"])
def post_delete_image():
    global post_image_dict
    if request.method == "POST":
        name = request.form['image']
        del post_image_dict[name]

        try:
            db.session.commit()
        except Exception:
            return "Data base error"
    
    return jsonify()


@app.route('/load_post_image/<int:id>/<name>')
def load_post_image(id, name):
    post = Post.query.get(id)
    h = make_response(post.images[name])
    h.headers["Content-Type"] = "image/png"
    return h


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(email=request.form["email"].lower()).first()
        if user and check_password_hash(user.password, request.form["password"]):
            res = make_response(request.args.get("next") or redirect("/"))
            res.set_cookie("logged_user", str(user.id))
            user_login = UserLogin().create(user)
            login_user(user_login)
            flash("You have been logged in successfully", "correct")
            return res
        else:
            flash("Incorrect password or email", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register_form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"].lower()
        pas1 = request.form["password1"]
        pas2 = request.form["password2"]

        if Users.query.filter_by(email=email).all():
            flash("This email already exists", "error")
            return render_template("register.html")

        if pas1 == pas2 and len(name) >= 4 and len(email) > 4 and len(pas1) > 4:
            pas2 = generate_password_hash(pas2)
            user = Users(name=name, email=email, password=pas2)
            db.session.add(user)
            db.session.commit()
            flash("You have been registered successfuly", "correct")
            user_login = UserLogin().create(user)
            login_user(user_login)
            res = make_response(redirect(url_for("index")))
            res.set_cookie("logged_user", str(user.id))
            return res
        else:
            flash("Incorect input", "error")
    return render_template("register.html")


@app.route("/profile")
@login_required
def profile():
    posts = Post.query.filter_by(user_id=current_user.get_id()).all()
    products = Product.query.filter_by(user_id=current_user.get_id()).all()
    return render_template("profile.html", posts=posts, products=products)

@app.route("/create_portfolio", methods=["GET", "POST"])
def create_portfolio():
    if request.method == "POST":
        caption = request.form['caption']
        ptype = request.form['ptype']
        text = request.form['text']
        tags = request.form['tag']
        roles = request.form['role']
        images = request.files.getlist('images')
        files = []
        for image in images:
            files.append(image.read())

        product = Product(text=text, tags=tags, caption=caption, ptype=ptype, roles=roles, user_id=current_user.get_id(), images=files)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect("/portfolio")
        except Exception as e:
            return "Exception has occured adding the product to the database" + str(e)

    return render_template("create_portfolio.html")

@app.route("/portfolio")
def portfolio():
    products = Product.query.order_by(Product.likes.desc()).all()
    return render_template("portfolio.html", products=products)


@app.route("/portfolio_details/<int:id>")
def port_details(id):
    product = Product.query.get(id)
    plist = Product.query
    return render_template("portfolio_details.html", product=product, pnext=plist[abs(id % len(plist.all()))].id, previous=plist[abs((id - 2) % len(plist.all()))].id, plist=plist)


@app.route("/edit_avatar", methods=["GET", "POST"])
@login_required
def edit_avatar():
    user = Users.query.get(current_user.get_id())
    posts = Post.query.filter_by(user_id=current_user.get_id()).all()
    if request.method == "POST":
        file = request.files["avatar"]
        user.scale = request.form["scale"]
        user.anchor = request.form.get("binding")

        if file:
            if current_user.verifyExt(file.filename):
                try:
                    user.avatar = file.read()
                except FileNotFoundError as e:
                    flash("Reading file error", "error")
            else:
                flash("Unsupporatable file resolution", "error")

        try:
            db.session.commit()
        except Exception:
            flash("Avatar updating error", "error")

    return render_template("profile.html", posts=posts)


@app.route("/edit_name", methods=["GET", "POST"])
@login_required
def edit_name():
    posts = Post.query.filter_by(user_id=current_user.get_id()).all()
    user = Users.query.get(current_user.get_id())
    if request.method == "POST":
        user.name = request.form["name"]
        try:
            db.session.commit()
        except Exception:
            return "Exception has occured updating the post"

    return render_template("profile.html", posts=posts)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    res = make_response(redirect(url_for("login")))
    res.set_cookie("logged_user", "", max_age=0)
    flash("You ve logged out", "correct")
    return res


@app.route("/contact", methods=["GET", "POST"])
def contact_form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        text = request.form["message"]
        msg = fmail.Message("Subject", sender=email, recipients=["burkow2007@gmail.com"])
        msg.body = f"{name}\n{text}"
        mail.send(msg)
        return redirect('/')

    return render_template("contact.html")

@app.errorhandler(404)
def NotFoundError(error):
    return render_template("error404.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        tag = request.form["tag"]
        caption = request.form["caption"]
        text = request.form["text"]
        post = Post(text=text, tag=tag, caption=caption, user_id=current_user.get_id(), images=post_image_dict)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect("/blog")
        except Exception:
            return "Exception has occured adding the post to the database"

    return render_template("create.html")


@app.route('/like_post', methods=["POST", "GET"])
def like_post():
    if request.method == "POST":
        post = Post.query.get(request.form['id'])
        action = request.form['action']
        post.likes += int(action)
        fav = list(post.favorite_for)
        
        if action == "1":
            fav.append(int(current_user.get_id()))
        elif action == "-1":
            fav.remove(int(current_user.get_id()))
        post.favorite_for = fav

        try:
            db.session.commit()
        except Exception:
            return "Data base error"
    
    return jsonify()
    
@app.route('/like_product', methods=["POST", "GET"])
def like_product():
    if request.method == "POST":
        product = Product.query.get(request.form['id'])
        action = request.form['action']
        product.likes += int(action)
        fav = list(product.favorite_for)
        
        if action == "1":
            fav.append(int(current_user.get_id()))
        elif action == "-1":
            fav.remove(int(current_user.get_id()))
        product.favorite_for = fav

        try:
            db.session.commit()
        except Exception:
            return "Data base error"
    
    return jsonify()

@app.route("/blog")
def get_blog_data():
    posts = Post.query.order_by(Post.likes.desc()).all()
    recent = Post.query.order_by(Post.date.desc()).all()

    return render_template("blog.html", posts=posts, recent=recent)


@app.route("/blog/<int:id>")
def go_to_post(id):
    post = Post.query.get(id)
    messages = Message.query.all()
    return render_template("single_post.html", post=post, messages=messages)


@app.route("/blog/<int:id>/edit", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get(id)

    if request.method == "POST":
        post.tag = request.form["tag"]
        post.caption = request.form["caption"]
        post.text = request.form["text"]

        try:
            db.session.commit()
            return make_response(request.args.get("next") or redirect("/blog"))
        except Exception:
            return "Exception has occured updating the post"

    return render_template("edit_post.html", post=post)

@app.route("/portfolio/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get(id)

    if request.method == "POST":
        product.caption = request.form['caption']
        product.ptype = request.form['ptype']
        product.text = request.form['text']
        images = request.files.getlist('images')
        product.tags = request.form['tag']
        product.roles = request.form['role']
        files = []
        for image in images:
            files.append(image.read())

        product.images = files

        try:
            db.session.commit()
            return make_response(request.args.get("next") or redirect("/portfolio"))
        except Exception:
            return "Exception has occured updating the post"

    return render_template("edit_product.html", product=product)

@app.route("/blog/<int:id>/delete")
def delete_post(id):
    post = Post.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return make_response(request.args.get("next") or redirect("/blog"))
    except Exception:
        return "Exception has occured deleting the post"

@app.route('/product/<int:id>/delete')
def delete_product(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return make_response(request.args.get("next") or redirect("/portfolio"))
    except Exception:
        return "Exception has occured deleting the product"
    

@app.route("/<page>")
def load_page(page):
    """id = request.cookies.get("logged_user")

    if id:
        user_login = UserLogin().create(Users.query.get(int(id)))
        login_user(user_login)"""

    try:
        return render_template(f"{page}.html")
    except TemplateNotFound:
        return abort(404)


@app.route("/<section>/<path:file>")
def load_file(section, file):
    return send_from_directory(section, file)


if __name__ == "__main__":
    app.run(debug=True)
