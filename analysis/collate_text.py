#!/usr/bin/python3

import sys
import os
import csv
from filenames import filenames

info_fn = sys.argv[1]
data_dir = sys.argv[2]
out_dir = sys.argv[3]

with open(info_fn,'r') as f:
  reader = csv.DictReader(f, dialect = csv.excel_tab)
  pids = [row['id'] for row in reader]

for typ, info in filenames['text'].items():
  print(typ)
  data = []
  for pid in pids:
    fn = os.path.join(data_dir, pid, info['filename'])
    if os.path.exists(fn):
      with open(fn,'r') as f:
        question = None
        answer = ''
        for line in f:
          if line.strip() in info['questions']:
            if question and answer:
              data.append({'id': pid, 'question': question, 'answer': answer[:-1]})
            question = line.strip()
            answer = ''
          else:
            if line.strip():
              answer += line.strip() + ' '
        if question and answer:
          data.append({'id': pid, 'question': question, 'answer': answer[:-1]})
  if len(data) > 0:
    with open(os.path.join(out_dir, typ + '.tsv'),'w') as f:
      writer = csv.DictWriter(f, fieldnames = data[0].keys(), dialect = csv.excel_tab)
      writer.writeheader()
      for row in data:
        writer.writerow(row)
