#!/usr/bin/python

import sys, os
from os import sys, path
import logging
logging.basicConfig(stream=sys.stderr)
#sys.path.insert(0,"/var/www/FlaskApp/")
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

#from app import app as application
from FlaskApp.app import app as application
application.secret_key = 'qwertyuikol3456789sdfghjzxzcvbn'
