import unittest
from app import create_app, db
from app.models import User, Anchor, TV


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_remove_user(self):
    	u = User(email='john@example.com', password='cat')
    	db.session.add(u)
    	db.session.commit()
    	a = Anchor(name='test')
    	db.session.add(a)
    	db.session.commit()
    	self.assertFalse(a.is_followed_by(u))
    	a.add_user(u)
    	self.assertTrue(a.is_followed_by(u))
    	a.remove_user(u)
    	self.assertFalse(a.is_followed_by(u))