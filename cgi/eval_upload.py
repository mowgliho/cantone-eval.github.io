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
  if eid == 'demo':
    print(json.dumps({'message': 'Not saving answers for demo'}))
  else:
    answer_fn = os.path.join(DIR, eid + '_answers.tsv')

    if os.path.exists(answer_fn):
      with open(answer_fn,'r') as f:
        rows = [row for row in csv.DictReader(f, dialect = csv.excel_tab)]
    else:
      rows = []
    
    rows += json.loads(form['data'].value)

    if len(rows) > 0:
      with open(answer_fn,'w') as f:
        writer = csv.DictWriter(f, dialect = csv.excel_tab, fieldnames = rows[0].keys())
        writer.writeheader()
        for row in rows:
          writer.writerow(row)

    # return output
    print(json.dumps({'message': 'Saved Answers'}))
except Exception as e:
  print(json.dumps({'message': str(e)}))
