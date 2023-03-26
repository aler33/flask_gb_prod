from flask import Blueprint, render_template
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from blog.models import Author, Article

authors_app = Blueprint("authors_app", __name__)


@authors_app.route("/", endpoint="list")
def authors_list():
    authors = Author.query.all()
    return render_template("authors/list.html", authors=authors)


@authors_app.route("/<int:author_id>/", endpoint="details")
def author_details(author_id: int):
    author = Author.query.filter_by(id=author_id).one_or_none()
    articles = Article.query.filter_by(author_id=author_id)
    if author is None:
        raise NotFound
    return render_template("authors/details.html", author=author, articles=articles)
