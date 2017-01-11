# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Anchor, User, TV

class AddAnchorForm(Form):
	tv = SelectField(u'直播平台',  coerce=int)
	room = StringField(u'房间号', validators=[Required(), Length(0, 64)])
	submit = SubmitField(u'添加')

	def __init__(self, *args, **kwargs):
		super(AddAnchorForm, self).__init__(*args, **kwargs)
		self.tv.choices = [(tv.id, tv.name) for tv in TV.query.order_by(TV.name).all()]