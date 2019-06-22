# -*- coding: utf-8 -*-
""" Flask-Admin views """


from flask_admin import Admin, BaseView, expose

from kido import app
from kido.models import db, User
from .utils import (AuthenticatedMenuLink, CustomAdminIndexView,
                   CustomModelView, admin_required, permission_required)


admin = Admin(app, index_view=CustomAdminIndexView(), template_mode='bootstrap3')
admin.add_link(AuthenticatedMenuLink(name='Logout', endpoint='admin.logout_view'))


admin.add_view(CustomModelView(User, db.session, category='Users',
    column_default_sort=('created_at', True),
    exclude=['password'],
    column_exclude_list=[
        'password',
        'modified_at',
    ],
    column_filters=[
        'email', 'first_name', 'last_name', 'created_at', 'modified_at',
    ], column_searchable_list=[
        'email', 'first_name', 'last_name',
    ],
))
