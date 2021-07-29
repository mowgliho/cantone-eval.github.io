#!/usr/bin/python
import os
import json
import cgi
import cgitb
import csv

DIR = 'evaluations'

print("Content-type: text/plain\n")
try:
  cgitb.enable()
  form = cgi.FieldStorage()

  eid = form['id'].value

  sample_fn = os.path.join(DIR, eid + '_samples.tsv')
  answer_fn = os.path.join(DIR, eid + '_answers.tsv')

  with open(sample_fn, 'r') as f:
    reader = csv.DictReader(f, dialect = csv.excel_tab)
    rows = [row for row in reader]

  if os.path.exists(answer_fn):
    with open(answer_fn,'r') as f:
      existing = [row for row in csv.DictReader(f, dialect = csv.excel_tab)]
  else:
    existing = []
  
  ratings = {}
  for row in existing:
    if row['speaker'] not in ratings:
      ratings[row['speaker']] = set()
    ratings[row['speaker']].add(row['fn'])

  rows = [row for row in rows if (row['speaker'] not in ratings) or (row['fn'] not in ratings[row['speaker']])]
  # return output
  print(json.dumps({'data': rows}))
except Exception as e:
  print(json.dumps({'data': None, 'err': str(e)}))
