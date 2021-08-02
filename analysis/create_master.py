import random
import sys
import os
import csv

random.seed(0)

shared = [
  'ref',
  '94e5ff60-0f93-4169-9c06-0de84a5220ab',
  'f9528342-e36b-47fb-ae0d-2655e0cc2721'
]

raters = ['samuel','nh','vchow','twc','wahpo','gemma','yuchen']

input_fn = sys.argv[1]
output_fn = sys.argv[2]

with open(input_fn,'r') as f:
  pids = [line.strip().split(' ')[0] for line in f]

pids = [x for x in pids if x not in shared]
pids.sort()

random.shuffle(pids)

rows = [{'id': r, 'speaker': pid} for r in raters for pid in shared]

for i, pid in enumerate(pids):
  rows.append({'id': raters[i % len(raters)], 'speaker':pid})

with open(output_fn, 'w') as f:
  writer = csv.DictWriter(f,fieldnames = rows[0].keys(), dialect = csv.excel_tab)
  writer.writeheader()
  for row in rows:
    writer.writerow(row)
