# -*- coding:utf-8 -*-

import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))  # 获得文件目录的绝对路径


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you can know this?'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	EASYSEE_MAIL_SUBJECT_PREFIX = '[EasySee]'
	EASYSEE_MAIL_SENDER = 'easySee <cuijt1994@163.com>'
	EASYSEE_ADMIN = os.environ.get('EASYSEE_ADMIN') or '<269584357@qq.com>'

	#celery config
	CELERY_BROKER_URL = 'redis://localhost:6379/0'
	CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
	CELERY_IMPORTS = ['app.task']
	CELERYBEAT_SCHEDULE = {
        'every-5-minute': {
            'task': 'circle_task',
            #'schedule': crontab(minute='*/1'),
            # 'args': (1,2),
            'schedule': timedelta(seconds=30)
        	},
    	}

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:632100@127.0.0.1:3306/easysee_dev'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://root:632100@127.0.0.1:3306/easysee_test'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:632100@127.0.0.1:3306/easysee'


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}