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

	def __init__(self, user, *args, **kwargs):
		super(AddAnchorForm, self).__init__(*args, **kwargs)
		self.tv.choices = [(tv.id, tv.name) for tv in TV.query.order_by(TV.name).all()]
		self.user = user

	#def validate_room(self, field):
	#	if Anchor.query.filter_by(tv=TV.query.get(tv.field), room=room.field, user=self.user).first():
	#		raise ValidationError(u'您已经关注过该直播间')
