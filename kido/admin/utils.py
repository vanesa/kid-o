# -*- coding: utf-8 -*-
""" Flask-Admin utilities."""


from flask import abort, redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.base import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from functools import wraps

from kido import app
from kido.constants import PERMISSION_ADMIN


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("views.general.login", next=request.url))
        users_permissions = current_user.permissions
        if PERMISSION_ADMIN not in users_permissions:
            app.logger.debug("Not an admin")
            abort(404)
        return f(*args, **kwargs)

    return decorated


def permission_required(permissions):
    if not isinstance(permissions, (list, set, tuple)):
        permissions = [permissions]
    permissions = [x.upper() for x in permissions]

    def decorator(method):
        @wraps(method)
        def f(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("views.general.login", next=request.url))
            users_permissions = current_user.permissions
            if PERMISSION_ADMIN not in users_permissions:
                for permission in permissions:
                    if permission not in users_permissions:
                        app.logger.debug("Missing permission: {0}".format(permission))
                        abort(404)
            return method(*args, **kwargs)

        return f

    return decorator


class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


class CustomAdminIndexView(AdminIndexView):
    extra_css = None
    extra_js = None

    @expose("/")
    @admin_required
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("views.general.login", next=request.url))
        return super(CustomAdminIndexView, self).index()

    @expose("/login/")
    def login_view(self):
        return redirect(url_for("views.general.login", next=request.url))

    @expose("/logout/")
    def logout_view(self):
        return redirect("/logout")


class CustomModelView(ModelView):
    page_size = 50
    extra_css = None
    extra_js = None

    action_template = "admin/action.html"
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"
    list_template = "admin/model/custom_list.html"

    _include = None

    class_attributes = [
        "page_size",
        "can_create",
        "can_edit",
        "can_delete",
        "column_searchable_list",
        "column_filters",
        "column_exclude_list",
        "column_default_sort",
    ]

    def __init__(self, *args, **kwargs):
        if "exclude" in kwargs:
            self.form_excluded_columns = kwargs["exclude"]
            del kwargs["exclude"]
        if "include" in kwargs:
            self._include = kwargs["include"]
            del kwargs["include"]

        for item in self.class_attributes:
            if item in kwargs:
                setattr(self, item, kwargs[item])
                del kwargs[item]

        super(CustomModelView, self).__init__(*args, **kwargs)

    def get_list_columns(self):
        if self._include:
            return self.get_column_names(
                only_columns=self.scaffold_list_columns() + self._include,
                excluded_columns=self.column_exclude_list,
            )
        return super(CustomModelView, self).get_list_columns()

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        users_permissions = current_user.permissions
        return PERMISSION_ADMIN in users_permissions

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)
