#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import re
import json
import sys
import getopt
import shutil
import time
import datetime
import random
from collections import defaultdict
import yaml
tree = lambda: defaultdict(tree)

# VARS
source_file_extension = 'json'
counterQuestionsTotal    = 0 # counter for questions

# VARS

# language strings
langStrings = dict() # NOT using 'collections import defaultdict' and 'lambda: defaultdict(tree)' above
langStrings['de']                   = dict()
langStrings['de']['answers']        = "Antworten"
langStrings['de']['plsCheckTotal']  = "Bitte ankreuzen"
langStrings['de']['solution']       = "Lösung"
langStrings['de']['source']         = "Quelle"

langStrings['en']                   = dict()
langStrings['en']['answers']        = "Answers"
langStrings['en']['plsCheckTotal']  = "Answers to check"
langStrings['en']['solution']       = "Solution"
langStrings['en']['source']         = "Source"
# / language strings

#metadata
date_current            = time.strftime("%Y-%m-%d %H:%M:%S")
meta = dict()
meta['date_updated']    = date_current

answers_random          = dict() # to make sure the order with the answers is the same as the questions

file_path_csv = 'quicz-counting-' + source_file_extension + '.csv'
os.remove(file_path_csv)

file_names = glob.glob('*.' + source_file_extension)

for file_name_in in file_names:
    file_id_stump = os.path.basename(file_name_in)[1:12]
    
    qAllArr             = tree() # using 'collections import defaultdict' and 'lambda: defaultdict(tree)' above
    counterQuestions    = 0 # counter for questions
    qAnswerCount        = 0 # counter for answers
    qItemSection        = 0 # to mark if metaYaml, question or answers
    tempYaml            = 0 # if metaYaml found not zero

    print('- Reading ' + source_file_extension + ' file: "' + file_name_in + '"')

    # Opening JSON file
    with open(file_name_in) as json_file:
        test_questions = json.load(json_file)
    
    if 'items' in test_questions:
        countQuestions = len(test_questions['items'])
    else:
        countQuestions = 0
        
    print('--- Number of questions found in set: ' + str(countQuestions))

    # write to csv file
    with open(file_path_csv, 'a') as quiczcounting:
        quiczcounting.write('"' + file_name_in + '", "' + str(countQuestions) + '"\n')

    counterQuestionsTotal = counterQuestionsTotal + int(countQuestions)

print('Count of total questions found: ' + str(counterQuestionsTotal))
print('Searched through ' + str(len(file_names)) + ' ' + source_file_extension + ' files.')
