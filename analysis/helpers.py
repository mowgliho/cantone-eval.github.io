import os

# row fns
def clean_pcpt_row(pid, row):
  syl = os.path.splitext(os.path.basename(row['file']))[0]
  seg = syl[:-1]
  tone = syl[-1]
  return [{ 'id': pid, 'round': row['round'], 'syl': syl, 'seg': seg, 'tone': tone, 'guess': row['guessed_tone']}]

def clean_list_test_round_row(pid, row):
  ret = {'id':pid}
  ret.update(row)
  ret['duration'] = int(ret['end']) - int(ret['start'])
  del ret['end']
  return [ret]

def pass_through(pid, row):
  ret = {'id':pid}
  ret.update(row)
  return [ret]

def clean_list_train_pass(pid,row):
  ret = {'id':pid}
  ret.update({k if k != 'id' else 'round':v for k,v in row.items()})
  ret['tone'] = ret['syl'][-1]
  return [ret]

def clean_list_train_trial(pid,row):
  ret = {'id':pid}
  ret.update({k if k != 'id' else 'round':v for k,v in row.items()})
  for x in ['correct','end']:
    ret[x] = int(ret[x]) - int(ret['start'])
  return [ret]

def clean_prod_test_contour(pid, row):
  return [{'id': pid, 'round': row['round'], 'attempt': row['attempt'], 'st': st, 'idx': i} for i, st in enumerate(row['contour'].strip().split(','))]
