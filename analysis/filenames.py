import os
import helpers


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
    'pcpt_canto': helpers.clean_pcpt_row,
    'listen_test_click': helpers.pass_through,
    'listen_test_round':  helpers.clean_list_test_round_row,
    'listen_train_line': helpers.clean_list_train_pass,
    'listen_train_play': helpers.clean_list_train_pass,
    'listen_train_trial': helpers.clean_list_train_trial,
    'mic_test_contour': helpers.pass_through,
    'mic_test_ref': helpers.pass_through,
    'prod_test_click': helpers.pass_through,
    'prod_test_contour': helpers.clean_prod_test_contour,
    'prod_test_round': helpers.pass_through,
    'prod_train_click': helpers.pass_through,
    'prod_train_contour': helpers.clean_prod_train_contour,
    'prod_train_round': helpers.pass_through
  }
}
