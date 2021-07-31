#!/usr/bin/python3
# python collate_tsv.py results/info.tsv data/ results/

import sys
import os
import csv
from filenames import filenames

info_fn = sys.argv[1]
data_dir = sys.argv[2]
out_dir = sys.argv[3]

missing = {}

with open(info_fn,'r') as f:
  reader = csv.DictReader(f, dialect = csv.excel_tab)
  pids = [row['id'] for row in reader]

for key, info in filenames['tsv'].items():
  print(key)
  data = []
  for pid in pids:
    fn = os.path.join(data_dir, pid, info['filename'])
    if not os.path.exists(fn):
      if pid not in missing:
        missing[pid] = []
      missing[pid].append(info['filename'])
      continue
    with open(os.path.join(data_dir, pid, info['filename']),'r') as f:
      reader = csv.DictReader(f, dialect=csv.excel_tab)
      for row in reader:
        data += info['row_fn'](pid, row)

  if len(data) > 0:
    with open(os.path.join(out_dir, key + '.tsv'),'w') as f:
      writer = csv.DictWriter(f, fieldnames=data[0].keys(), dialect=csv.excel_tab)
      writer.writeheader()
      for row in data:
        writer.writerow(row)

print('\nMissing: ', missing)
