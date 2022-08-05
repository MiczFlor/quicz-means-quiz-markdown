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
from collections import defaultdict
import yaml
tree = lambda: defaultdict(tree)

# VARS
source_file_extension = "json"
target_file_extension = "gift"

def main(argv):
    global inputfile
    inputfile = ''
    global outputfile
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(os.path.basename(__file__) + ' -i <source> -o <target>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(os.path.basename(__file__) + ' -i <source> -o <target>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

if __name__ == "__main__":
    main(sys.argv[1:])

if inputfile.strip() != "":
    file_name_in = inputfile
    print ('Converting file: "' + inputfile + '"')
else:
    print ('No source file specified. Use:\n$ ' + os.path.basename(__file__) + ' -i <source>')
    sys.exit()

if outputfile.strip() != "":
    file_name_out = outputfile
    print ('Result will be saved to: "' + outputfile + '"')
else:
    print ('No target file specified. You can use:\n$ ' + os.path.basename(__file__) + ' -o <target>')
    file_name_out = os.path.basename(os.path.splitext(inputfile)[0]) + '.' + target_file_extension
    print ('Result will be saved to: "' + file_name_out + '"')
    
# VARS
counterQuestions    = 0 # counter for questions

#metadata
date_current            = time.strftime("%Y-%m-%d %H:%M:%S")
meta = dict()
meta['filename_source'] = os.path.basename(file_name_in)
meta['path_source']     = os.path.abspath(file_name_in)
meta['filename_target'] = os.path.basename(file_name_out)
meta['path_target']     = os.path.abspath(file_name_out)
meta['date_updated']    = date_current

# percentage of *correct* answer values spread evenly amongst possible answers
answer_correct_percentage = {}
answer_correct_percentage[1] = '%100%'
answer_correct_percentage[2] = '%50%'
answer_correct_percentage[3] = '%33.33333%'
answer_correct_percentage[4] = '%25%'
answer_correct_percentage[5] = '%20%'
answer_correct_percentage[6] = '%16.66667%'
answer_correct_percentage[7] = '%14.28571%'
answer_correct_percentage[8] = '%12.5%'
answer_correct_percentage[9] = '%11.11111%'
answer_correct_percentage[10] = '%10%'
answer_correct_percentage[20] = '%5%'

print('- Reading ' + source_file_extension + ' file: "' + file_name_in + '"')
# Opening JSON file
with open(file_name_in) as json_file:
    test_questions = json.load(json_file)

# write GIFT format
file_name_out = ((os.path.splitext(file_name_in)[0]) + '.gift')
with open(file_name_out, 'w') as f:
    print('- Writing ' + target_file_extension + ' to: ' + file_name_out)
    
    # metadata for entire set first
    
    # 1. if no meta section in json, create one
    if not 'meta' in test_questions:
        test_questions['meta'] = dict()
    # 2. update meta info we usually create for this conversion
    for meta_key in meta.keys():
        test_questions['meta'][meta_key] = meta[meta_key]
    # 3. add some meta information if missing
    if 'date_created' not in test_questions['meta']:
        # creation date
        test_questions['meta']['date_created'] = date_current
    if 'path_origin' not in test_questions['meta']:
        # path of the first file from which this started
        test_questions['meta']['path_origin'] = os.path.abspath(file_name_in)
    # 4. now write metadata
    for q_meta in test_questions['meta'].keys():
        f.write('//"' + q_meta + '" : "' + test_questions['meta'][q_meta] + '"\n')
    # write individual questions
    for q_num in test_questions['items']:
        counterQuestions = counterQuestions + 1
        f.write('::ID' + os.path.splitext(file_name_in)[0] + '-' + str(q_num) + '::[markdown]' + test_questions['items'][q_num]['question'] + '\n')
        f.write('{\n')

        if test_questions['items'][q_num]['type']['multipleChoice']:
            answer_ids = test_questions['items'][q_num]['answers'].keys()
            # correct answers counter to zero
            answers_correct = 0
            for answer_id in answer_ids:
                if test_questions['items'][q_num]['answers'][answer_id]['bolean']:
                    answers_correct = answers_correct + 1
            if answers_correct > 0: 
                answer_correct_percentage[answers_correct]
            for answer_id in answer_ids:
                if test_questions['items'][q_num]['answers'][answer_id]['bolean']:
                    answers_percentage = answer_correct_percentage[answers_correct]
                else:
                    answers_percentage = ""
                f.write('  ~' + answers_percentage + test_questions['items'][q_num]['answers'][answer_id]['text'] + '\n')
        elif test_questions['items'][q_num]['type'] == 'freeText':
            f.write('  =%100%' + test_questions['items'][q_num]['answers']['0']['text'] + '#\n')
        #print('}\n')
        f.write('}\n\n')
print('- Number of questions found: ' + str(counterQuestions))
    