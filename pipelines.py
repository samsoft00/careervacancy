# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from peewee import *
import datetime
import uuid

import models

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CareerPipeline(object):

	def __init__(self):
		models.DATABASE.connect()
		models.DATABASE.create_tables([models.Job, models.Category, models.JobsCategory], safe=True)


	def process_item(self, item, spider):
		valid = True

		for data in item:
			if not data :
				valid = False
				raise DropItem("Missing {0}".format(data))

		if valid :
			try:
				with models.DATABASE.transaction():
					jobber = models.Job.create(
							url=item['url'], 
							title=str(item['title']).strip(), 
							description=str(item["description"]).strip(),
							location=str(item["location"]).strip(),
							uuid=str(uuid.uuid4()),
							sponsor=item["sponsor"]
							)
				# jobber.categories.add(models.Category.create(str(category=item['category']).strip()))

			except IntegrityError:
				existing_job = models.Job.get(url=item['url'])
				existing_job.title = str(item['title']).strip()
				existing_job.description = str(item['description']).strip()
				existing_job.location = str(item['location']).strip()
				existing_job.sponsor = item['sponsor']
				existing_job.save()


			cat_lists = str(item['category']).strip().split(',')
			for cat in cat_lists :
				try :
					# with models.DATABASE.transaction():
					cat = models.Category.create(category=cat.strip())
					cat.jobs.add(jobber)

				except IntegrityError:
					# models.Category.get(str(category=item['category']).strip())
					pass

		return item