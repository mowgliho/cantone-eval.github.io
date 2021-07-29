#!/usr/bin/python
import os
import json
import cgi
import cgitb
import csv

DIR = 'evaluations'

print("Content-type: text/plain\n")
try: 
  def key(row):
    return row['speaker'] + '_' + row['fn']

  cgitb.enable()
  form = cgi.FieldStorage()

  eid = form['id'].value
  if eid == 'demo':
    print(json.dumps({'message': 'Not saving answers for demo'}))
  else:
    answer_fn = os.path.join(DIR, eid + '_answers.tsv')

    inds = {}
    if os.path.exists(answer_fn):
      with open(answer_fn,'r') as f:
        rows = [row for row in csv.DictReader(f, dialect = csv.excel_tab)]
        for i,row in enumerate(rows):
          inds[key(row)] = i
    else:
      rows = []
    
    append = []
    amend = []
    for i,row in enumerate(json.loads(form['data'].value)):
      if key(row) in inds:
        amend.append((inds[key(row)], row))
      else:
        append.append(row)

    for i,row in amend:
      rows[i] = row
 
    rows += append

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
