#!/usr/bin/python

import sys, os
import cgi
import pickle
import time
import csv
from datetime import datetime
from string import *

print "Content-type: text/html"
print ""

with open("log.txt", "r") as f:
	txt = list(reversed([x for x in f.readlines() if x != ""]))
	if txt[0] == "CLEAR,,\n":
		print "UNNECESSARY"
		exit()

with open("log.txt", "a") as f:
	f.write("CLEAR,,\n")

print "DONE"
