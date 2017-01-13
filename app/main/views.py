# -*- coding:utf-8 -*-

from flask import render_template, url_for, flash, redirect, request, g, current_app
from flask_login import login_required, current_user
from . import main
from .forms import AddAnchorForm, SearchForm, MessageForm
from ..getName import NameGetter
from ..LiveChecker import LiveChecker
from ..models import User, TV, Anchor, Message
from .. import db

@main.before_app_request
def before_request(): #定义全局变量
    g.search_form = SearchForm()

@main.route('/')
def index():
	if  not current_user.is_authenticated:
		return render_template('welcome.html')
	if Anchor.query.all() == []:
		anchors = None
	else:
		anchors = current_user.anchors.all()
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
		anchor.is_live = LiveChecker(anchor).is_live
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
	if current_user.is_limit():
		anchor = Anchor.query.filter_by(name=name).first()
		anchor.add_user(current_user)
		flash(u'关注成功')
	else:
		flash(u'您的关注的主播数量已达上限')
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
	page = request.args.get('page', 1, type=int)
	pagination = Anchor.query.order_by(Anchor.users_count).paginate(
		page, per_page=current_app.config['EASYSEE_PER_PAGE'], error_out=False)
	anchors = pagination.items[::-1] 
	return render_template('hot.html', anchors=anchors, pagination=pagination)

@main.route('/search', methods = ['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query = g.search_form.search.data))

@main.route('/search-results/<query>')
def search_results(query):
    anchors = Anchor.query.filter(Anchor.name.like('%'+query+'%')).all()
    return render_template('search_results.html', anchors=anchors)

@main.route('/leave-message', methods=['GET', 'POST'])
@login_required
def leave_message():
	form = MessageForm()
	if form.validate_on_submit():
		body = form.message.data
		user_name = current_user.username 
		user_email = current_user.email 
		message = Message(body=body, user_name=user_name, user_email=user_email)
		db.session.add(message)
		db.session.commit()
		flash(u'已经受到您的反馈，我们将在几个工作日内作出回复')
		return redirect(url_for('.index'))
	return render_template('leave_message.html', form=form)
