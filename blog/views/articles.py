from flask import Blueprint, render_template, request, current_app, redirect, url_for
from sqlalchemy.orm import joinedload
# from blog.views.users import USERS
from werkzeug.exceptions import NotFound
# from blog.models import User
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from blog.models.database import db
from blog.models import Article, Author, User, Tag
from blog.forms.article import  CreateArticleForm
import requests


articles_app = Blueprint("articles_app", __name__)


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles)


@articles_app.route("/api/", endpoint="list_api")
def api_articles_list():
    """
    Function for get articles list from api
    :return:
    """
    response = requests.get(
        "http://127.0.0.1:5000/api/articles/?include=author%2Ctags&page%5Bnumber%5D=1&page%5Bsize%5D=10"
    )
    articles = response.json()
    return render_template("articles/apilist.html", articles=articles)


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id: int):
    article = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()
    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), body=form.body.data)

        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)

        db.session.add(article)
        if current_user.author:
            # use existing author if present
            article.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author = current_user.author

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article.")
            error = "Could not create article"
        else:
            return redirect(url_for("articles_app.details", article_id=article.id))

    return render_template("articles/create.html", form=form, error=error)
