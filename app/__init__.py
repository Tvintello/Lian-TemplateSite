from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import tempfile
import pathlib
import tantivy
import os, config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = "Please, login to open the page"
login_manager.login_message_category = "neutral"

schema_builder = tantivy.SchemaBuilder()
schema_builder.add_integer_field("doc_id", stored=True)
schema_builder.add_text_field("caption", stored=True)
schema_builder.add_text_field("text", stored=True)
schema = schema_builder.build()
index_ = tantivy.Index(schema)

index_path = pathlib.Path(r"D:\lesson sites\Lian\app\indexes")
index_path.mkdir(exist_ok=True)
persistent_index = tantivy.Index(schema, path=str(index_path))


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    app.app_context().push()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app