#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_app import app

from models import db
from models import User, Movie, MoviePrice, ConsumeRecord, ChargeRecord, Comment


class UserView(ModelView):
    can_delete = True
    can_edit = False
    can_create = False
    can_view_details = True

    column_labels = dict(
        id='ID',
        username='用户名',
        password_hash='昵称',
        phone_number='电话',
        avatar='头像',
        balance='余额',
    )

    column_display_pk = True

    column_filters = (
        'username',
        'phone_number',
    )

    column_searchable_list = column_filters

    column_exclude_list = (
        'password_hash'
    )


class CommentView(ModelView):
    can_delete = True
    can_edit = False
    can_create = False
    can_view_details = True

    column_labels = dict(
        id='ID',
        from_user='用户',
        to_user='被评论用户',
        comment_time='评论时间',
        content='评论内容',
        point='评分',
    )

    column_filters = (
    )

    column_searchable_list = column_filters

    column_exclude_list = (
    )


class MoviePriceView(ModelView):
    can_create = False
    can_view_details = True

    column_labels = dict(
        movie='电影',
        price='价格',
    )

    column_filters = (
    )

    column_searchable_list = column_filters

    column_exclude_list = (
    )


class ConsumeRecordview(ModelView):
    can_create = False
    can_view_details = True

    column_labels = dict(
        consume_time='购买时间',
        movie='电影',
        money='金额',
        consumer='用户',
    )

    column_filters = (
    )

    column_searchable_list = column_filters

    column_exclude_list = (
    )

class ChargeRecordView(ModelView):
    can_create = False
    can_view_details = True

    column_labels = dict(
        charge_time='充值',
        money='金额',
        user='用户',
    )

    column_filters = (
    )

    column_searchable_list = column_filters

    column_exclude_list = (
    )

admin = Admin(app, name='电影船后台管理')

admin.add_view(UserView(User, db.session, name='用户'))
admin.add_view(CommentView(Comment, db.session, name='用户评论'))
admin.add_view(MoviePriceView(MoviePrice, db.session, name='价格'))
admin.add_view(ConsumeRecordview(ConsumeRecord, db.session, name='购买记录'))
admin.add_view(ChargeRecordView(ChargeRecord, db.session, name='充值记录'))
