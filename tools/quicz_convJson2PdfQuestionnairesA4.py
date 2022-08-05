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
target_file_extension = "pdf"

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

#metadata
date_current            = time.strftime("%Y-%m-%d %H:%M:%S")
meta = dict()
meta['filename_source'] = os.path.basename(file_name_in)
meta['path_source']     = os.path.abspath(file_name_in)
meta['filename_target'] = os.path.basename(file_name_out)
meta['path_target']     = os.path.abspath(file_name_out)
meta['date_updated']    = date_current

# print file name on top of each question?

# setting for A6 decks to learn
PDF_print_filename = True
PDF_print_solutions_inline = True
PDF_print_answers_end = False
PDF_format = "A6" # A4 or A6
filename_suffix = "flashcard"
# print document ID (if exists) on top of each question?
PDF_print_question_id = True

# setting for A4 print out to dry run
PDF_print_filename = False
PDF_print_solutions_inline = False
PDF_print_answers_end = True
PDF_format = "A4" # A4 or A6
filename_suffix = "questionnaire"
# print document ID (if exists) on top of each question?
PDF_print_question_id = False

print('- Reading ' + source_file_extension + ' file: "' + file_name_in + '"')
# Opening JSON file
with open(file_name_in) as json_file:
    test_questions = json.load(json_file)
# read metadata for PDF output
meta_pdf = dict()
if 'title' in test_questions['meta']:
    meta_pdf['title'] = test_questions['meta']['title']
else:
    meta_pdf['title'] = meta['filename_source']
if 'subtitle' in test_questions['meta']:
    meta_pdf['subtitle'] = test_questions['meta']['subtitle']
else:
    meta_pdf['subtitle'] = meta['path_source']
if 'date_created' in test_questions['meta']:
    meta_pdf['date_created'] = test_questions['meta']['date_created']
else:
    meta_pdf['date_created'] = date_current
if 'abstract' in test_questions['meta']:
    meta_pdf['abstract'] = test_questions['meta']['abstract']
else:
    meta_pdf['abstract'] = ""
# write MD format
file_name_out = ((os.path.splitext(file_name_in)[0]) + '.md')
with open(file_name_out, 'w') as f:
    print("Converting to MD:\nTARGET: " + file_name_out)
    if PDF_format == "A6":
        f.write("---\ngeometry: 'top=0.5cm, bottom=0cm, left=1cm, right=1cm'\npapersize: a6\ndocumentclass: article\nabstract: " + meta_pdf['abstract'] + "\ndate: " + meta_pdf['date_created'] + "\ntitle: " + meta_pdf['title'] + "\nsubtitle: " + meta_pdf['subtitle'] + "\n...\n")
        f.write('\n\n' + (os.path.basename(file_name_in)) + ' \pagebreak\n')
    elif PDF_format == "A4":
        f.write("---\ngeometry: 'top=2cm, bottom=2cm, left=2cm, right=2cm'\npapersize: a4\ndocumentclass: book\ndate: " + meta_pdf['date_created'] + "\ntitle: " + meta_pdf['title'] + "\nsubtitle: " + meta_pdf['subtitle'] + "\n...\n")
        f.write('\n# ' + os.path.basename(file_name_in) + '\n')
        f.write('\n## ' + os.path.basename(file_name_in) + '\n')
    
    if PDF_print_answers_end:
        answers_end = "\n# Answers\n\n"

    for q_num in test_questions['items']:
        text_topline = '\n\n**' + q_num + '**'
        if PDF_print_filename:
            text_topline =  text_topline + ' \linebreak\n *' + (os.path.basename(file_name_in)) + '*'
        if 'id' in test_questions['items'][q_num].keys():
            if PDF_print_question_id:
                text_topline = text_topline + ' \linebreak\n *' + test_questions['items'][q_num]['id'] + '*'
        text_topline =  text_topline + '\n\n'
        #################
        # without answers
        f.write(text_topline + test_questions['items'][q_num]['question'])
        if PDF_print_answers_end:
            answers_end = answers_end + "  **" + str(q_num) + ".** : "
        if "multipleChoice" in test_questions['items'][q_num]['type']:
            answer_ids = test_questions['items'][q_num]['answers'].keys()
            # correct answers counter to zero
            answers_correct = 0
            answers_counter = 0
            for answer_id in answer_ids:
                answers_counter = answers_counter + 1
                if test_questions['items'][q_num]['answers'][answer_id]['bolean']:
                    answers_correct = answers_correct + 1
                    if PDF_print_answers_end:
                        answers_end = answers_end + str(answers_counter) + ". "
            f.write(' \n\n(Bitte ankreuzen: ' + str(answers_correct) + ')\n\n')
            for answer_id in answer_ids:
                f.write('1. ' + test_questions['items'][q_num]['answers'][answer_id]['text'] + '\n')
        elif "freeText" in test_questions['items'][q_num]['type']:
            if PDF_print_answers_end:
                freeTextList = list()
                # create comma separated list
                for aText_num in test_questions['items'][q_num]['answers']:
                    freeTextList.append(test_questions['items'][q_num]['answers'][aText_num]['text'])
                answers_end = answers_end + '; '.join(freeTextList)            
        ##############
        if PDF_print_solutions_inline:
            f.write('\pagebreak\n\n')
            # with answers
            f.write(text_topline + test_questions['items'][q_num]['question'])
            f.write(' \n\nLÖSUNG:\n\n')
            if "multipleChoice" in test_questions['items'][q_num]['type']:
                answer_ids = test_questions['items'][q_num]['answers'].keys()
                # correct answers counter to zero
                answers_correct = 0
                for answer_id in answer_ids:
                    answers_counter = answers_counter
                    if test_questions['items'][q_num]['answers'][answer_id]['bolean']:
                        answers_correct = answers_correct + 1
                for answer_id in answer_ids:
                    if test_questions['items'][q_num]['answers'][answer_id]['bolean']:
                        checkbox = '[x]'
                    else:
                        checkbox = '[ ]'
                    f.write('* ' + checkbox + ' ' + test_questions['items'][q_num]['answers'][answer_id]['text'] + '\n')
            elif "freeText" in test_questions['items'][q_num]['type']:
                #f.write('\n\n' + test_questions['items'][q_num]['answers']['0']['text'])
                freeTextList = list()
                # create comma separated list
                for aText_num in test_questions['items'][q_num]['answers']:
                    freeTextList.append(test_questions['items'][q_num]['answers'][aText_num]['text'])
                f.write('\n\n' + ('; '.join(freeTextList)))
            # write additional information (resources)
            if 'info' in test_questions['items'][q_num]:
                f.write('\n\n')
                print(test_questions['items'][q_num]['info'])
                for info_id in test_questions['items'][q_num]['info']:
                    print(info_id)
                    f.write(test_questions['items'][q_num]['info'][info_id]['key'].capitalize() + ': ')
                    if 'value' in test_questions['items'][q_num]['info'][info_id]:
                        f.write(test_questions['items'][q_num]['info'][info_id]['value'])
                    if 'url' in test_questions['items'][q_num]['info'][info_id]:
                        f.write('<' + test_questions['items'][q_num]['info'][info_id]['url'] + '>')

            f.write('\pagebreak\n\n')
    # print the answers on the last page?
    if PDF_print_answers_end:
        f.write(answers_end)

# write PDF
file_name_in = ((os.path.splitext(file_name_in)[0]) + '.md')
file_name_out = ((os.path.splitext(file_name_in)[0]) + '.' + filename_suffix + '.pdf')
print('- Writing ' + target_file_extension + ' to: ' + file_name_out)
exec_string = "pandoc -i '" + file_name_in + "' -o '" + file_name_out + "'"
os.system(exec_string)
#os.remove((os.path.splitext(file_name_in)[0]) + '.md')

    