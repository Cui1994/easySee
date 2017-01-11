# -*- coding:utf-8 -*-

from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from . import main
from .forms import AddAnchorForm
from ..getName import NameGetter
from ..models import User, TV, Anchor
from .. import db

@main.route('/')
def index():
	if current_user.is_authenticated:
		if Anchor.query.all() == []:
			anchors = None
		else:
			anchors = current_user.anchors.all()
	else:
		anchors = None
	return render_template('index.html', anchors=anchors)

@main.route('/add-anchor', methods=['GET', 'POST'])
@login_required
def add_anchor():
	form = AddAnchorForm()
	if form.validate_on_submit():
		name = NameGetter(TV.query.get(form.tv.data).name, form.room.data).name
		if not name:
			flash(u'查询不到该房间名对应的直播间，请输入正确的房间名')
			return redirect(url_for('.add_anchor'))
		if Anchor.query.filter_by(name=name).first():
			if current_user.is_following(Anchor.query.filter_by(name=name).first()):
				flash(u'您已经添加过该主播，请不要重复添加')
				return redirect(url_for('.add_anchor'))
			else:
				current_user.follow(Anchor.query.filter_by(name=name).first())
				flash(u'添加成功')
				return redirect(url_for('.index'))
		anchor = Anchor(name=name, room=form.room.data, 
			tv=TV.query.get(form.tv.data))
		current_user.follow(anchor)
		db.session.add(anchor)
		db.session.commit()
		flash(u'添加成功')
		return redirect(url_for('.index'))
	return render_template('add_anchor.html', form=form)

