from flask import *
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegisterForm, BlogForm, PortfolioForm, ContactForm
from werkzeug.datastructures import MultiDict
from app.utils import UserLogin
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user,
)
from app.models import Post, Message, Product, Comment, Users
# from .forms import *
from app import login_manager, db, index_, schema
from tantivy import SnippetGenerator
import re


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


@current_app.route("/")
def index():
    products = Product.query.order_by(Product.likes.desc()).all()
    return render_template("index.html", products=products, address="/")


@current_app.route("/user_avatar")
def current_user_avatar():
    img = current_user.get_avatar(current_app)
    
    if not img:
        return ""

    h = make_response(img)
    h.headers["Content-Type"] = "image/png"
    return h


@current_app.route("/user_avatar/<int:id>")
def user_avatar(id):
    img = load_user(id).get_avatar(current_app)
    
    if not img:
        return ""

    h = make_response(img)
    h.headers["Content-Type"] = "image/png"
    return h


@current_app.route('/load_port_image/<int:id>/<int:num>')
def load_port_image(id, num):
    product = Product.query.get(id)
    h = make_response(product.images[num])
    h.headers["Content-Type"] = "image/png"
    return h


@current_app.route('/load_post_image/<int:id>/<name>')
def load_post_image(id, name):
    post = Post.query.get(id)
    h = make_response(post.images[name])
    h.headers["Content-Type"] = "image/png"
    return h


@current_app.route('/load_post_heading/<int:id>')
def load_post_heading(id):
    post = Post.query.get(id)
    h = make_response(post.heading_image)
    h.headers["Content-Type"] = "image/png"
    return h


@current_app.route("/profile")
@login_required
def profile():
    posts = Post.query.filter_by(user_id=current_user.get_id()).all()
    products = Product.query.filter_by(user_id=current_user.get_id()).all()
    return render_template("profile.html", posts=posts, products=products)


@current_app.route("/portfolio")
def portfolio():
    products = Product.query.order_by(Product.likes.desc()).all()
    tags = {}

    for el in products:
        tags[el.id] = " ".join(list(map(lambda x: "offers__filter--" + x, el.tags.split())))
    
    
    return render_template("portfolio.html", products=products, tags=tags)


def get_related(l: list, tags: str):
    tags = tags.split()
    r = []

    for el in l:
        els = el.tags.split()
        for tag in tags:
            if tag in els:
                r.append(el)
                break

    return r
        

@current_app.route("/portfolio_details/<int:id>")
def port_details(id):
    product = Product.query.get(id)
    plist = Product.query
    related = get_related(plist.all(), product.tags)
    return render_template("portfolio_details.html", product=product, pnext=plist[abs(id % len(plist.all()))].id, previous=plist[abs((id - 2) % len(plist.all()))].id, 
                           plist=plist, userDB=UserLogin().fromDB, related=related)


@current_app.route("/logout")
@login_required
def logout():
    logout_user()
    res = make_response(redirect(url_for(".login")))
    res.set_cookie("logged_user", "", max_age=0)
    flash("You ve logged out", "correct")
    return res


@current_app.errorhandler(404)
def NotFoundError(error):
    return render_template("error404.html")



@current_app.route("/blog")
def get_blog_data():
    posts = Post.query.order_by(Post.likes.desc()).all()
    recent = Post.query.order_by(Post.date.desc()).all()

    return render_template("blog.html", posts=posts, recent=recent, userDB=UserLogin().fromDB)


@current_app.route("/blog/<int:id>")
def go_to_post(id):
    post = Post.query.get(id)
    comments = Comment.query.filter_by(post_id=id)
    return render_template("single_post.html", post=post, comments=comments, userDB=UserLogin().fromDB)


@current_app.route("/blog/<int:id>/save_comment", methods=["GET", "POST"])
@login_required
def save_comment(id):
    if request.method == "POST":
        text = request.form['message']
        comment = Comment(text=text, post_id=id, user_id=current_user.get_id())
        
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception:
            return "Exception has occured updating the post"

    return redirect('/blog/' + str(id))


@current_app.route("/blog/<int:id>/delete")
def delete_post(id):
    post = Post.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect("/blog")
    except Exception:
        return "Exception has occured deleting the post"

@current_app.route('/product/<int:id>/delete')
def delete_product(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/profile')
    except Exception:
        return "Exception has occured deleting the product"
    

@current_app.route("/<page>")
def load_page(page):
    """id = request.cookies.get("logged_user")

    if id:
        user_login = UserLogin().create(Users.query.get(int(id)))
        login_user(user_login)"""

    try:
        return render_template(f"{page}.html")
    except TemplateNotFound:
        return abort(404)


@current_app.route("/<section>/<path:file>")
def load_file(section, file):
    return send_from_directory(section, file)


@current_app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password, form.password.data):
            res = make_response(redirect(request.args.get("next") or "/"))
            user_login = UserLogin().create(user)
            login_user(user_login)
            flash("You have been logged in successfully", "correct")
            return res
        else:
            flash("Incorrect password or email", "error")

    return render_template("login.html", form=form)


@current_app.route("/register", methods=["GET", "POST"])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        pas1 = form.password.data
        pas2 = form.password2.data

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
            res = make_response(redirect(url_for(".index")))
            res.set_cookie("logged_user", str(user.id))
            return res
        else:
            flash("Incorect input", "error")
    return render_template("register.html", form=form)


@current_app.route("/create_portfolio", methods=["GET", "POST"])
def create_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        caption = form.caption.data
        ptype = form.type.data
        text = form.text.data
        tags = form.tags.data
        roles =  form.roles.data
        images = form.images.data
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

    return render_template("create_portfolio.html", form=form)


@current_app.route("/edit_avatar", methods=["GET", "POST"])
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


@current_app.route("/edit_name", methods=["GET", "POST"])
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


@current_app.route("/contact", methods=["GET", "POST"])
def contact_form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        text = request.form["message"]
        # msg = fmail.Message("Subject", sender=email, recipients=["burkow2007@gmail.com"])
        # msg.body = f"{name}\n{text}"
        # mail.send(msg)
        return redirect('/')

    return render_template("contact.html")


@current_app.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        tag = request.form["tag"]
        caption = request.form["caption"]
        text = request.form["text"]
        heading = request.files['heading']
        images = request.files.getlist('images')
        files = {}
    
        for file in images:
            files[file.filename] = file.read()

        post = Post(text=text, tag=tag, caption=caption, user_id=current_user.get_id(), images=files, heading_image=heading.read())

        try:
            db.session.add(post)
            db.session.commit()
            return redirect("/blog")
        except Exception:
            return "Exception has occured adding the post to the database"

    return render_template("create.html")


@current_app.route('/like_post', methods=["POST", "GET"])
@login_required
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
    

@current_app.route('/like_product', methods=["POST", "GET"])
@login_required
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


@current_app.route("/blog/<int:id>/edit", methods=["GET", "POST"])
def edit_post(id):
    form = BlogForm()
    post = Post.query.get(id)

    if form.validate_on_submit():
        post.tag = form.tag.data
        post.caption = form.caption.data
        post.text = form.text.data

        try:
            db.session.commit()
            return make_response(request.args.get("next") or redirect("/blog"))
        except Exception:
            return "Exception has occured updating the post"

    return render_template("edit_post.html", post=post, form=form)


@current_app.route('/blog/search', methods=["GET", "POST"])
def blog_search():
    searcher = index_.searcher()
    query = index_.parse_query(request.form['search'], ["caption", "text"])
    posts = []

    for best_score, best_doc_address in searcher.search(query, 3).hits:
        best_doc = searcher.doc(best_doc_address)
        posts.append(Post.query.get(best_doc['doc_id']))

    recent = sorted(posts, key=lambda x: x.date.timestamp())
    posts.sort(key=lambda x: x.likes)

    return render_template('blog.html', posts=posts, recent=recent, userDB=UserLogin().fromDB)

    


@current_app.route('/blog/search/json')
def blog_context_search():
    searcher = index_.searcher()
    client = request.args.get('q').replace("_", " ")
    query = index_.parse_query(client, ["caption", "text"])
    posts = []

    for best_score, best_doc_address in searcher.search(query, 3).hits:
        best_doc = searcher.doc(best_doc_address)

        hit_text = best_doc["text"][0]
        snippet_generator = SnippetGenerator.create(searcher, query, schema, "text")
        snippet = snippet_generator.snippet_from_doc(best_doc)
        highlights = snippet.highlighted()
        text = snippet.to_html() or hit_text
        text = text[0:160]

        posts.append({'text': " ".join(re.split('<[^b][^>]*[^b]>', text)), 'caption': best_doc['caption'], 'id': best_doc['doc_id'], 'score': best_score})

    predicted = []
    j = Post.query.all()
    cap = ''

    for i in j:
        if i.caption.startswith(client) and client != '':
            s = i.caption.split()
            c = client.split()[-1]

            if c in s and s.index(c) < len(s):
                cap = " ".join(s[0:s.index(c) + 2])


            predicted.append({'text': " ".join(re.split('<[^>]*>', i.text[0:160])), 'caption': cap, 'id': i.id})

    predicted.sort(key=lambda x: len(x['caption']), reverse=True)

    return jsonify([posts, predicted])


@current_app.route('/blog/load_more')
def load_more_posts():
    posts = Post.query.all()[int(request.args.get('l')):int(request.args.get('p'))]
    l = []

    for p in posts:
        user_name = UserLogin.fromDB(p.user_id).get_name()
        edit = ""
        liked = ""

        if not current_user.is_anonymous:
            if current_user.get_name() == user_name:
                edit = f"/blog/{p.id}/edit"

            if current_user.is_post_favorite(p.id):
                liked = "blog__list__item-btn--active"

        heading = ''
        if p.heading_image:
            heading = f'load_post_heading/{p.id}'

        l.append({'id': p.id, 'tag': p.tag, 'caption': p.caption, 'text': p.text, 'date': f"on {p.date:'%B %d, %Y'}", 'likes': p.likes, 
                  'user_name': f'by {user_name}', 'liked': liked, 'heading_image': heading, 'edit': edit})
        
    return jsonify(l)


@current_app.route("/portfolio/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    form = PortfolioForm()

    product = Product.query.get(id)

    if form.validate_on_submit():
        product.caption = form.caption.data
        product.ptype = form.type.data
        product.text = form.text.data
        images = form.images.data
        product.tags = form.tags.data
        product.roles = form.roles.data
        files = []
        for image in images:
            files.append(image.read())

        product.images = files

        try:
            db.session.commit()
            return make_response(request.args.get("next") or redirect("/portfolio"))
        except Exception:
            return "Exception has occured updating the post"

    return render_template("edit_product.html", product=product, form=form)


@current_app.errorhandler(413)
def file_too_large(e):
    flash(f"The file is too big! (the limit is {current_app.config['MAX_CONTENT_LENGTH']} bytes)", "error")
    return '<script>document.location.href = document.referrer</script>'
