#!/usr/bin/python3
#  python create_groups.py groups.tsv out groups
# expects
#   first argument is a tsv of [id, speaker]
#   second argument is directory to put output
#   third argument is directory to put info for each id.
#   ref: folder with reference audio (always used)
#   data: folder with speaker data. In particular, we look for data/[id]/prod_test_round.tsv
#   wav: folder with wav files: [id]_prod_test_[round].wav

import os
import csv
import sys
import json
import functools
import random
import pyloudnorm as pyln
import audio2numpy
import scipy.io.wavfile
import numpy as np

LOUDNESS = -19
DTYPE = np.int16
AMPLITUDE = np.iinfo(DTYPE).max

def copy_wav(output_dir, in_wav, out_wav):
  out_fn = os.path.join(output_dir, out_wav)
  if os.path.exists(out_fn):
    return
  print(in_wav, out_fn)
  x, sampleRate = audio2numpy.audio_from_file(in_wav)
  #stereo to mono
  if len(x.shape) == 1:
    pass
  elif len(x.shape) ==2 and x.shape[1] == 2:
    x = x.sum(axis=1)/2
  loudness = pyln.Meter(sampleRate).integrated_loudness(x)
  x = pyln.normalize.loudness(x, loudness, LOUDNESS)
  scipy.io.wavfile.write(out_fn, sampleRate, (x*AMPLITUDE).astype(DTYPE))

input_fn = sys.argv[1]
output_dir = sys.argv[2]
group_dir = sys.argv[3]

DATA = 'data'
REF = 'ref'
WAV = 'wav'
FN = 'prod_test_round.tsv'
LOUDNESS = -19#https://developers.google.com/assistant/tools/audio-loudness

#read which speakers go to which ids
with open(input_fn, 'r') as f:
  reader = csv.DictReader(f, dialect=csv.excel_tab)
  rows = [row for row in reader]

ids = {}
for row in rows:
  if row['id'] not in ids:
    ids[row['id']] = set(['ref'])
  ids[row['id']].add(row['speaker'])

all_speakers = set(functools.reduce(lambda a,b: a | b, ids.values()))
speakers = set(list(all_speakers))
speakers.remove('ref')

data = {x: [] for x in all_speakers}

# look at round data for each speaker
for speaker in speakers:
  with open(os.path.join(DATA, speaker, FN),'r') as f:
    rows = [row for row in csv.DictReader(f, dialect=csv.excel_tab)]
  for row in rows:
    seg = row['syl'][:-1]
    data[speaker].append({'seg': seg, 'syl': row['syl'], 'tone': row['tone'], 'round': row['round']})

# link with wav files
for x in os.listdir(WAV):
  basename, ext = os.path.splitext(x)
  if ext != '.wav':
    continue
  tokens = basename.split('_')
  rnd = tokens[-1]
  speaker = tokens[0]
  if speaker not in data:
    continue
  for row in data[speaker]:
    if row['round'] == rnd:
      row.update({'in_wav': os.path.join(WAV,x), 'out_wav': '%s_%s.wav' % (speaker, rnd)})

# add ref files
data['ref'] = []
for i, fn in enumerate(os.listdir(REF)):
  syl = os.path.splitext(fn)[0]
  data['ref'].append({'seg': syl[:-1], 'syl': syl, 'tone': syl[-1], 'round': str(i), 'in_wav': os.path.join(REF,fn), 'out_wav': '%s_%s.wav' % ('ref', str(i))})

# create assignments for each id
group_data = dict()
for x, speakers in ids.items():
  group_data[x] = []
  for speaker in speakers:
    segs = set([row['seg'] for row in data[speaker]])
    for seg in segs:
      rows = [row for row in data[speaker] if row['seg'] == seg]
      random.shuffle(rows)
      for row in rows:
        group_data[x].append({'seg': row['seg'], 'syl': row['syl'],'tone': row['tone'], 'fn': row['out_wav']})
        copy_wav(output_dir, row['in_wav'], row['out_wav'])

# write tsvs for each id
for x, rows in group_data.items():
  with open(os.path.join(group_dir,x + '.tsv'),'w') as f:
    writer = csv.DictWriter(f, dialect = csv.excel_tab, fieldnames = rows[0].keys())
    writer.writeheader()
    for row in rows:
      writer.writerow(row)
