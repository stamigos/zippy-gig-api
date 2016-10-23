from flask import url_for
from flask_admin.contrib.peewee import ModelView
from flask_admin import BaseView, expose
from zippy_gig.models import Account, db

#
# class MyView(BaseView):
#     @expose('/')
#     def index(self):
#         url = url_for('.accounts')
#         return self.render('admin/index.html', url=url)
#
#     @expose('/accounts/')
#     def accounts(self):
#         return self.render('admin/accounts.html', id=id)


class AccountAdmin(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_exclude_list = ['password']
    column_editable_list = ['is_active']


