# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱地址', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(Form):
    email = StringField(u'邮箱地址', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(4, 64)])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=u'两次密码必须相同')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被使用')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入密码不一致')])
    password2 = PasswordField(u'确认新密码', validators=[Required()])
    submit = SubmitField(u'更改密码')


class PasswordResetRequestForm(Form):
    email = StringField(u'请输入您的注册邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'更改密码')


class PasswordResetForm(Form):
    email = StringField(u'注册邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入密码不一致')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'修改密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'请输入正确的邮箱地址')


class ChangeEmailForm(Form):
    email = StringField(u'请输入新的邮箱地址', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'更改邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已被注册')
