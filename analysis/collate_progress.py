#!/usr/bin/python3
# python collate_progress.py results/info.tsv data/ results/progress.tsv

import sys
import os
import csv
from filenames import filenames

intra_task_pts = {
  'listen_train': {
    '11': 'level',
    '23': 'contour',
    '29': 'all'
  }
}

def mins(time):
  return ('%.2f' % (time/60000)) if time else ''

def analyze_progress(pid, lines):
  last_task_end = None
  start = None
  last_subtask_end = None
  data = []
  for line in lines:
    tokens = line.strip().split('\t')
    timestamp = int(tokens[2])
    if start is None:
      start = timestamp
    if tokens[1] == 'completed':
      if last_task_end == None:
        time = None
      else:
        time = timestamp - last_task_end
      last_task_end = timestamp
      last_subtask_end = timestamp
      data.append({'id': pid, 'task': tokens[0], 'subtask': '', 'time': time,'min': mins(time)})
    elif tokens[0] in intra_task_pts and tokens[1] in intra_task_pts[tokens[0]]:
      time = (timestamp - last_subtask_end) if last_subtask_end else None
      last_subtask_end = timestamp
      data.append({'id': pid, 'task': tokens[0], 'subtask': intra_task_pts[tokens[0]][tokens[1]], 'time': time,'min': mins(time)})
  total_time = last_task_end - start
  data.append({'id': pid, 'task': 'total', 'subtask': '', 'time': total_time,'min': mins(total_time)})
  return data

info_fn = sys.argv[1]
data_dir = sys.argv[2]
out_fn = sys.argv[3]

missing = {}

with open(info_fn,'r') as f:
  reader = csv.DictReader(f, dialect = csv.excel_tab)
  pids = [row['id'] for row in reader]

data = []

for pid in pids:
  fn = os.path.join(data_dir, pid, 'progress.txt')
  with open(fn, 'r') as f:
    data += analyze_progress(pid, [line for line in f])

if len(data) != 0:
  with open(out_fn,'w') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys(), dialect=csv.excel_tab)
    writer.writeheader()
    for row in data:
      writer.writerow(row)
