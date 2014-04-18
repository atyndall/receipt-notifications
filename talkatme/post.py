#!/usr/bin/python

import sys, os
import cgi
import pickle
import time
import csv
from datetime import datetime
from string import *
from time import localtime, strftime

print "Content-type: text/html"

BASE_URL = "http://example.com/"

sys.stderr = sys.stdout

form = cgi.FieldStorage()
if "name" not in form or "msg" not in form:
	print "Location: " + BASE_URL + "/talkatme/error.html"
	print ""
	exit()

with open("log.txt", "a") as f:
        csvw = csv.writer(f, quoting=csv.QUOTE_ALL)

	name = form['name'].value
	if len(name) > 30:
		name = name[:30]

	msg = form['msg'].value
	if len(msg) > 140:
		msg = msg[:140]

        csvw.writerow([strftime("%a, %d %b %Y %X", localtime()), name, msg])

print "Location: " + BASE_URL + "/talkatme/sent.html"
print ""
