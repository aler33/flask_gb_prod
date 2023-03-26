from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from blog import models
from blog.models.database import db
from flask import redirect, url_for
from flask_login import current_user


class MyAdminIndexView(AdminIndexView):

    @expose("/")
    def index(self):
        if current_user.is_authenticated and not current_user.is_staff:
            return redirect(url_for("articles_app.list"))
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for("auth_app.login"))
        return super(MyAdminIndexView, self).index()


# Custom admin interface
class CustomView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth_app.login"))


class TagAdminView(CustomView):
    column_searchable_list = ("name",)
    column_filters = ("name",)
    can_export = True
    export_types = ["csv", "xlsx"]
    create_modal = True
    edit_modal = True


class AuthorAdminView(CustomView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_list = ("id", "user.username", "articles")


class ArticleAdminView(CustomView):
    column_list = ("author.user.username", "title", "body", "dt_created", "dt_updated")


class UserAdminView(CustomView):
    column_exclude_list = ("_password",)
    column_searchable_list = ("first_name", "last_name", "username", "is_staff", "email")
    column_filters = ("first_name", "last_name", "is_staff", "email")
    column_editable_list = ("first_name", "last_name", "is_staff")
    can_create = True
    can_edit = True
    can_delete = False


# Create admin with custom base template
admin = Admin(name="Blog Admin", index_view=MyAdminIndexView(), template_mode='bootstrap4')

# Add views
admin.add_view(TagAdminView(models.Tag, db.session, category="Models"))
admin.add_view(ArticleAdminView(models.Article, db.session, category="Models"))
admin.add_view(AuthorAdminView(models.Author, db.session, category='Models'))
admin.add_view(UserAdminView(models.User, db.session, category="Models"))
