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
			is_live = LiveChecker(anchor).is_live
			if is_live == True and is_live != anchor.is_live:
				logging.info(anchor.name)
			anchor.is_live = is_live
			db.session.add(anchor)
			db.session.commit()
		logging.info("lalala")
