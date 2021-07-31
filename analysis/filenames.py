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


filenames = {
  'info': 'info.txt',
  'progress': 'progress.txt',
  'text': {
    'questionnaire': {
      'filename': 'questionnaire.txt',
      'questions': [
        'What is/are your native language(s)?',
        'If you speak any other languages, what are they? Please indicate your proficiency.',
        'Do you have playing musical instruments, singing, or the like? Again, please indicate your proficiency.',
        'If you have found this study via Prolific, what is your Prolific ID?',
        'How old are you?'
        ]
      },
    'feedback': {
      'filename': 'feedback.txt',
      'questions': [
        'Q: How was your experience learning Cantonese tones?',
        'Q: Did you find some tones easier to learn than others?',
        'Q: Did you find some tones easier to learn than others? If so, which ones and why?',
        'Q: Which was easier, perception or production? Why?',
        'Q: How did you find the matching game for learning tones?',
        'Q: How helpful were the provided tone charts?',
        'Q: How helpful were the tuning bars in learning pronunciation?',
        'Q: How helpful was the visual feedback on the contours that you made while training?',
        'Q: How did you find the audio snippets that were adjusted to your vocal range?',
        'Q: Did you have issues with the system recognizing the contours that you produced?',
        'Q: Do you feel that you had enough time to learn Cantonese tones?',
        'Q: What other comments/feedback do you have?',
        'Q: Did you come across any bugs/errors?'
      ]
    }
  },
  'tsv': {
    'pcpt_canto': {
      'filename': 'pcpt_canto.tsv',
      'row_fn': clean_pcpt_row
    },
    'listen_test_click': {
      'filename': 'listen_test_click.tsv',
      'row_fn': pass_through
    },
    'listen_test_round': {
      'filename': 'listen_test_round.tsv',
      'row_fn': clean_list_test_round_row
    }
  }
}
