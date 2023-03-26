from flask import Flask, g, render_template
from time import time
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.views.auth import login_manager, auth_app
from blog.views.authors import authors_app
from blog.views.tags import tags_app
from blog.models.database import db
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from blog.admin import admin
from blog.api import init_api


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/alexey/gb_lesson/Flask_g/Flask_gb/blog/blog.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "abcdefg123456"
cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
app.config.from_object(f"blog.configs.{cfg_name}")
db.init_app(app)
admin.init_app(app)


@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(auth_app, url_prefix="/auth")
app.register_blueprint(authors_app, url_prefix="/authors")
app.register_blueprint(tags_app, url_prefix="/tags")

login_manager.init_app(app)

flask_bcrypt.init_app(app)

migrate = Migrate(app, db, compare_type=True)

api = init_api(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time

    return response

# It's old function before create migration

# @app.cli.command("init-db")
# def init_db():
#     """
#     Run in terminal:
#     flask init-db
#     """
#     db.create_all()


# created command for create users
@app.cli.command("create-users")
def create_users():
    """
    Run in terminal:
    flask create-users
    """
    from blog.models import User
    admin = User(username='admin', is_staff=True, email='admin@localhost.ru')
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    james = User(username="James", email='james@localhost.ru')
    james.password = os.environ.get("JAMES_PASSWORD") or "1"
    brian = User(username="Brian", email='brian@localhost.ru')
    brian.password = os.environ.get("BRIAN_PASSWORD") or "1"
    peter = User(username="Peter", email='peter@localhost.ru')
    peter.password = os.environ.get("PETER_PASSWORD") or "1"

    db.session.add(admin)
    db.session.add(james)
    db.session.add(brian)
    db.session.add(peter)
    db.session.commit()

    print("done! created users:", admin, james)

# created command for create admin
@app.cli.command("create-admin")
def create_admin():
    """
    Run in terminal:
    flask create-admin
    """
    from blog.models import User
    admin = User(username='admin', is_staff=True, email='admin@localhost.ru')
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"

    db.session.add(admin)
    db.session.commit()

    print("done! created admin:", admin)


@app.cli.command("create-tags")
def create_tags():
    """
    Run in terminal:
    flask create-tags
    """
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
        "fastapi",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")
