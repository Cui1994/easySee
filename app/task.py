# -*- coding:utf-8 -*-

import logging
from . import celery, db 
from .models import Anchor
from .LiveChecker import LiveChecker
from manage import app
from .email import send_email

@celery.task(name='circle_task')
def circletask():
	with app.app_context():
		anchors = Anchor.query.all()
		for anchor in anchors:
			if anchor.users.all() == []:
				db.session.delete(anchor)
				db.session.commit()
			else:
				is_live = LiveChecker(anchor).is_live
				if is_live == True and is_live != anchor.is_live:
					for user in anchor.users.all():
						if user.is_remind:
							send_email(user.email, u'主播上线通知', 'email/remind', user=user, name=anchor.name)
							logging.info('send a email')
				anchor.is_live = is_live
				db.session.add(anchor)
				db.session.commit()
