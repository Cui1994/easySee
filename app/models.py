# -*- coding:utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager

user_anchor = db.Table('user_anchor',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('anchor_id', db.Integer, db.ForeignKey('anchors.id'), primary_key=True)
    )

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_remind = db.Column(db.Boolean, default=False)

    anchors = db.relationship('Anchor', secondary=user_anchor, 
        backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def follow(self, anchor):
        if not self.is_following(anchor):
            self.anchors.append(anchor)
            db.session.add(self)
            db.session.commit()

    def is_following(self, anchor):
        return self.anchors.filter_by(id=anchor.id).first() is not None

    def unfollow(self, anchor):
        self.anchors.remove(anchor)
        db.session.add(self)
        db.session.commit()

    def change_remind(self):
        self.is_remind = not self.is_remind
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TV(db.Model):
    __tablename__ = 'tvs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    base_url = db.Column(db.String(128))

    anchors = db.relationship('Anchor', backref='tv')

    @staticmethod
    def insert_tvs():
        tvs = {
            u'斗鱼': 'https://www.douyu.com/',
            u'熊猫': 'http://www.panda.tv/',
            u'龙珠': 'http://star.longzhu.com/',
            u'全民': 'http://www.quanmin.tv/',
            u'虎牙': 'http://www.huya.com/',
            u'战旗': 'https://www.zhanqi.tv/'
        }
        for t in tvs:
            tv = TV.query.filter_by(name=t).first()
            if tv is None:
                tv = TV(name=t)
            tv.base_url = tvs[t]
            db.session.add(tv)
        db.session.commit()

class Anchor(db.Model):
    __tablename__ = 'anchors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    room = db.Column(db.String(64))
    is_live = db.Column(db.Boolean, default=False, index=True)
    users_count = db.Column(db.Integer, default=0)

    tv_id = db.Column(db.Integer, db.ForeignKey('tvs.id'))

    def add_user(self, user):
        if not self.is_followed_by(user):
            self.users.append(user)
            slef.users_count += 1
            db.session.add(self)
            db.session.commit()

    def is_followed_by(self, user):
        return self.users.filter_by(id=user.id).first() is not None

    def remove_user(self, user):
        self.users_count -= 1
        self.users.remove(user)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def insert_users_count():
        for anchor in Anchor.query.all():
            anchor.users_count = anchor.users.count()
            db.session.add(anchor)
            db.session.commit()


