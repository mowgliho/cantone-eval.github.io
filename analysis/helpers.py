import os

def clean_pcpt_row(pid, row):
  syl = os.path.splitext(os.path.basename(row['file']))[0]
  seg = syl[:-1]
  tone = syl[-1]
  return { 'id': pid, 'round': row['round'], 'syl': syl, 'seg': seg, 'tone': tone, 'guess': row['guessed_tone']}

def clean_list_test_round_row(pid, row):
  ret = {'id':pid}
  ret.update(row)
  ret['duration'] = int(ret['end']) - int(ret['start'])
  del ret['end']
  return ret

def pass_through(pid, row):
  ret = {'id':pid}
  ret.update(row)
  return ret


