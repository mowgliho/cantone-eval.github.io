#!/usr/bin/python3
#python collate_info.py data results/info.tsv

import csv
import sys
import os
from filenames import filenames

data_dir = sys.argv[1]
out_fn = sys.argv[2]

data = []
for pid in os.listdir(data_dir):
  # check if finished
  progress_fn = os.path.join(data_dir, pid, filenames['progress'])
  if not os.path.exists(progress_fn):
    continue
  finished = False
  with open(progress_fn, 'r') as f:
    for line in f:
      if line.strip().startswith('end\tcompleted'):
        finished = True
  if not finished:
    continue
  
  # load info
  pid_data = {}
  info_fn = os.path.join(data_dir, pid, filenames['info'])
  with open(info_fn, 'r') as f:
    for row in f:
      tokens = row.strip().split('\t')
      pid_data[tokens[0]] = tokens[1]
  data.append(pid_data)

if len(data) > 0:
  with open(out_fn, 'w') as f:
    writer = csv.DictWriter(f, fieldnames = data[0].keys(), dialect=csv.excel_tab)
    writer.writeheader()
    for row in data:
      writer.writerow(row)
