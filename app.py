#!/usr/bin/env python

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor
from arachne import Arachne

from flask import (Flask, g, request, render_template, flash, redirect, url_for)
from flask.ext.paginate import Pagination
#from flask import Blueprint

from flask_restful import Resource, Api

import models
#from scrapy.conf import settings

app = Arachne(__name__, settings='/var/www/FlaskApp/settings.py')
api = Api(app)
#mod = Blueprint('jobs', __name__)

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
#reactor.listenTCP(, site)


@app.before_request
def before_request() :
	"""Connect to Database before each request"""
	g.db = models.DATABASE
	g.db.connect()


@app.after_request
def after_request(response) :
	"""Close Database after each request"""
	g.db.close()
	return response


@app.route('/', methods=('GET', 'POST'))
def index():
	"""Index page """
	id = request.args.get('details', '')
	uuid = request.args.get('uuid', '')


	if id != '' and uuid != '':
		try:
			job = models.Job.select().where( models.Job.uuid == uuid.strip() and models.Job.id == id.strip() ).first()
			return render_template('view_job.html', jobs=job)

		except models.DoesNotExist:
			pass

	if request.method == 'POST':
		return redirect(url_for('search_result'))
		
	return render_template('index.html')



@app.route('/jobs-in-nigeria',  methods=('GET', 'POST'))
def search_result():
	""" Search Result page """
	keywords = request.args.get('k', '')
	location = request.args.get('l', '')

	page, per_page, offset = get_page_items()
	# return searchword
	if keywords != '' or location != '':
		jobs = models.Job.select().where(
			(models.Job.title.contains(keywords.strip().title())) & (models.Job.location.contains(location.strip().title())) )#get(models.Job.title == "Reader (Behavioral Studies)")
	else:
		jobs = models.Job.select()

	all_jobs = jobs.paginate(page, per_page)

	pagination = Pagination(page=page, per_page=per_page, total=jobs.count(), search=False, record_name='jobs', css_framework='bootstrap3')
	#for cat in jobs.categories
	query_fields = {'k':keywords, 'l':location}
	return render_template('search.html', jobs=all_jobs, pagination=pagination, **query_fields)

#	return job_cat
#view?o=473&uuid=88383-3333-22222-3333
@app.route('/view')
def displayJobs() :
	o = request.args.get('o', '')
	uuid = request.args.get('uuid', '')

	if o == '' and uuid == '':
		return redirect(url_for('index'))
	#Query
	job = models.Job.select().where( (models.Job.uuid == uuid.strip()) & (models.Job.id == o.strip()) ).first()
	return job.title
	return render_template('view_job.html', jobs=job)


def get_page_items():
	page = int(request.args.get('page', 1))
	per_page = request.args.get('per_page')
	if not per_page:
		per_page = 10#current_app.config.get('PER_PAGE', 10)
	else:
		per_page = int(per_page)

	offset = (page - 1) * per_page
	return page, per_page, offset


###################################################################
# API RESOURCES
###################################################################

# @api.route('/api/v1.0/jobs/<int:job_id>', methods=('GET'))
# def get_job(job_id):

# api.add_resource(models.Job, '/api/v1.0/jobs/<int:job_id>')


if __name__ == '__main__':
	models.initialize()

	reactor.run()
#	app.run()
