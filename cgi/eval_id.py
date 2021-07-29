#!/usr/bin/python
import os
import json
import cgi
import cgitb
import csv

DIR = 'groups'

print("Content-type: text/plain\n")
try:
  cgitb.enable()
  form = cgi.FieldStorage()

  eid = form['id'].value

  fn = os.path.join(DIR, eid + '.tsv')

  with open(fn, 'r') as f:
    reader = csv.DictReader(f, dialect = csv.excel_tab)
    rows = [row for row in reader]

  # return output
  print(json.dumps({'data': rows}))
except Exception as e:
  print(json.dumps({'data': None, 'err': str(e)}))
