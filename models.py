from peewee import *
from playhouse.fields import ManyToManyField
import datetime


DATABASE = MySQLDatabase(
	'career', #Database name
	user='root', #Database username
	password='Adefioye&^%$#@!', #Database password
	host='127.0.0.1', # host
	)


class Job(Model):
	"""docstring for Jobs"""
	url = CharField(max_length=200, unique=True)
	title = TextField()
	description = TextField()
	sponsor = CharField(max_length=100)
	location = CharField(max_length=100)
	uuid = CharField(max_length=150)
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE
		order_by = ('-timestamp',)


class Category(Model):
	"""docstring for JobCategory"""
	category = CharField(max_length=100, unique=True)
	jobs = ManyToManyField(Job, related_name='categories')

	class Meta:
		database = DATABASE


JobsCategory = Category.jobs.get_through_model()


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Job, Category, JobsCategory], safe=True)