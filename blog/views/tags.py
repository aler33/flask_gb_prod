from flask import Blueprint, render_template, request, current_app, redirect, url_for
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from blog.models.database import db
from blog.models import Article, Author, User, Tag
from blog.forms.article import  CreateArticleForm

tags_app = Blueprint("tags_app", __name__)


@tags_app.route("/", endpoint="list")
def tags_list():
    tags = Tag.query.all()
    return render_template("tags/list.html", tags=tags)


@tags_app.route("/<int:tag_id>/", endpoint="details")
def tag_details(tag_id: int):
    tag = Tag.query.filter_by(id=tag_id).options(joinedload(Tag.articles)).one_or_none()
    if tag is None:
        raise NotFound
    return render_template("tags/details.html", tag=tag)
