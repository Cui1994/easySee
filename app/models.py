from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    anchors = db.relationship('User_Follow_Anchor', 
        backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

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
            f = User_Follow_Anchor(follower=self, anchor=anchor)
            db.session.add(f)
            db.session.commit()

    def is_following(self, anchor):
        return self.anchors.filter_by(anchor_id=anchor.id).first() is not None

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
            'douyu': 'https://www.douyu.com/',
            'xiongmao': 'http://www.panda.tv/',
            'longzhu': 'http://star.longzhu.com/',
            'quanmin': 'http://www.quanmin.tv/',
            'huya': 'http://www.huya.com/',
            'zhanqi': 'https://www.zhanqi.tv/'
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

    tv_id = db.Column(db.Integer, db.ForeignKey('tvs.id'))
    followers = db.relationship('User_Follow_Anchor', 
        backref=db.backref('anchor', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

class User_Follow_Anchor(db.Model):
    __tablename__ = 'user_follow_anchor'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    anchor_id = db.Column(db.Integer, db.ForeignKey('anchors.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

