# -*- coding:utf-8 -*-

from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from . import main
from .forms import AddAnchorForm
from ..getName import NameGetter
from ..LiveChecker import LiveChecker
from ..models import User, TV, Anchor
from .. import db

@main.route('/')
def index():
	if  not current_user.is_authenticated:
		return render_template('welcome.html')
	if Anchor.query.all() == []:
		anchors = None
	else:
		anchors = current_user.anchors.all()
		#for anchor in anchors:
		#	anchor.is_live = LiveChecker(anchor).is_live
		#	db.session.add(anchor)
		#	db.session.commit()
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
			if Anchor.query.filter_by(name=name).first().is_followed_by(current_user):
				flash(u'您已经添加过该主播，请不要重复添加')
				return redirect(url_for('.add_anchor'))
			else:
				anchor = Anchor.query.filter_by(name=name).first()
				anchor.add_user(current_user)
				anchor.is_live = LiveChecker(anchor).is_live
				db.session.add(anchor)
				db.session.commit()
				flash(u'添加成功')
				return redirect(url_for('.index'))
		anchor = Anchor(name=name, room=form.room.data, 
			tv=TV.query.get(form.tv.data))
		anchor.add_user(current_user)
		flash(u'添加成功')
		return redirect(url_for('.index'))
	return render_template('add_anchor.html', form=form)

@main.route('/unfollow/<name>')
@login_required
def unfollow(name):
	anchor = Anchor.query.filter_by(name=name).first()
	anchor.remove_user(current_user)
	flash(u'取消关注成功')
	return redirect(url_for('.index'))

@main.route('/follow/<name>')
@login_required
def follow(name):
	anchor = Anchor.query.filter_by(name=name).first()
	anchor.add_user(current_user)
	flash(u'关注成功')
	return redirect(url_for('.hot'))

@main.route('/set-remind')
@login_required
def set_remind():
	return render_template('set_remind.html', user=current_user)

@main.route('/change-remind')
@login_required
def change_remind():
	current_user.change_remind()
	if current_user.is_remind:
		flash(u'邮箱提醒开启成功')
	else:
		flash(u'邮箱提醒已关闭')
	return redirect(url_for('.index'))

@main.route('/hot')
@login_required
def hot():
	if Anchor.query.all() == []:
		anchors = None
	else:
		anchors = Anchor.query.order_by(Anchor.users_count)[:10]
	return render_template('hot.html', anchors=anchors)

