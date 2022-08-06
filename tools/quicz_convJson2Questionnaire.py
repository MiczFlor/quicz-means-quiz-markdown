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
output_formats_avail = ['docx', 'html', 'odt', 'pdf', 'rtf']
lang_avail = ['de', 'en']
lang_default = 'en'
filename_suffix = "questionnaire"

def main(argv):
    global inputfile
    inputfile = ''
    global outputfile
    outputfile = ''
    global lang_used
    lang_used = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(os.path.basename(__file__) + ' -i <source> -o <target> -l <language>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(os.path.basename(__file__) + ' -i <source> -o <target> -l <language>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-l", "--lang"):
            lang_used = arg

if __name__ == "__main__":
    main(sys.argv[1:])

if inputfile.strip() != "":
    file_name_in = inputfile
    print ('Converting file: "' + inputfile + '"')
else:
    print ('No source file specified. Use:\n$ ' + os.path.basename(__file__) + ' -i <source> -o <target>')
    sys.exit()

if outputfile.strip() != "":
    file_name_out = os.path.splitext(outputfile)[0] + '.' + filename_suffix + os.path.splitext(outputfile)[1]
    # check if file extension is in available formats
    target_file_extension = os.path.splitext(file_name_out)[1][1:]
    if target_file_extension in output_formats_avail:
        print ('Result will be saved to: "' + file_name_out + '"')
    else:
        print ('"' + target_file_extension + '" target format is not available. Use one of these:')        
        print(output_formats_avail)
        sys.exit()
else:
    print('No target file specified. Use:\n$ ' + os.path.basename(__file__) + ' -i <source> -o <target>')
    print('Output format is set by the <target> file extension. Available options are:')
    print(output_formats_avail)
    sys.exit()

if lang_used.strip() != "":
    # check if lang available
    if lang_used in lang_avail:
        print ('Language used: "' + lang_used + '"')
    else:
        print ('Language "' + lang_used + '" is not available. Use one of these:')      
        print(output_formats_avail)
        lang_used = lang_default
        print('Using default language: "' + lang_used + '"')
else:
    lang_used = lang_default
    print('No language specified, using default: "' + lang_used + '"')

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
meta['filename_source'] = os.path.basename(file_name_in)
meta['path_source']     = os.path.abspath(file_name_in)
meta['filename_target'] = os.path.basename(file_name_out)
meta['path_target']     = os.path.abspath(file_name_out)
meta['date_updated']    = date_current


answers_random          = dict() # to make sure the order with the answers is the same as the questions

# setting for A4 questionnaire printout
PDF_answers_shuffle = True
PDF_print_filename = False
PDF_print_solutions_inline = False
PDF_print_answers_end = True
PDF_format = "A4" # A4 or A6
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
if 'date' in test_questions['meta']:
    # if the 'date' key was set in the metadata, keep it, bc that should overrule system info date_created
    meta_pdf['date_title'] = test_questions['meta']['date']
elif 'date_created' in test_questions['meta']:
    meta_pdf['date_title'] = test_questions['meta']['date_created']
else:
    meta_pdf['date_title'] = date_current
if 'abstract' in test_questions['meta']:
    meta_pdf['abstract'] = test_questions['meta']['abstract']
else:
    meta_pdf['abstract'] = ""
# write MD format
file_name_md = ((os.path.splitext(file_name_in)[0]) + '-' + str(hash(os.path.splitext(file_name_in)[0])) + '.md')
with open(file_name_md, 'w') as f:
    print("- Converting to temporary MD:" + file_name_md)
    if PDF_format == "A6":
        f.write("---\ngeometry: 'top=0.5cm, bottom=0cm, left=1cm, right=1cm'\npapersize: a6\ndocumentclass: article\nabstract: " + meta_pdf['abstract'] + "\ndate: " + meta_pdf['date_title'] + "\ntitle: " + meta_pdf['title'] + "\nsubtitle: " + meta_pdf['subtitle'] + "\n...\n")
        f.write('\n\n' + (os.path.basename(file_name_in)) + ' \pagebreak\n')
    elif PDF_format == "A4":
        f.write("---\ngeometry: 'top=2cm, bottom=2cm, left=2cm, right=2cm'\npapersize: a4\ndocumentclass: book\ndate: " + meta_pdf['date_title'] + "\ntitle: " + meta_pdf['title'] + "\nsubtitle: " + meta_pdf['subtitle'] + "\n...\n")
        # commented out: ugly fix for PDF to have filename in header. But does not work for other formats  (docx, etc.)
        #f.write('\n# ' + os.path.splitext(file_name_in)[0] + '\n')
        #f.write('\n## ' + os.path.splitext(file_name_in)[0] + '\n')
    
    if PDF_print_answers_end:
        answers_end = "\n# " + langStrings[lang_used]['answers'] + "\n\n"

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
            answers_end = answers_end + "  **" + str(q_num) + "**: "
            # create comma separated list for numbers of correct answer elements
            answerNumList = list()

        if 'multipleChoice' in test_questions['items'][q_num]['type']:
            answer_ids = list(test_questions['items'][q_num]['answers'].keys())
            # if set above to true, the answers will be shuffled before printing
            if PDF_answers_shuffle: 
                random.shuffle(answer_ids)
            answers_random[q_num] = answer_ids
            # correct answers counter to zero
            answers_correct = 0
            answers_counter = 0
            for answer_id in answers_random[q_num]:
                answers_counter = answers_counter + 1
                if test_questions['items'][q_num]['answers'][answer_id]['bolean']:
                    answers_correct = answers_correct + 1
                    if PDF_print_answers_end:
                        answerNumList.append(str(answers_counter))
#                        answers_end = answers_end + str(answers_counter) + ", "
            f.write(' \n\n(' + langStrings[lang_used]['plsCheckTotal'] +': ' + str(answers_correct) + ')\n\n')
            for answer_id in answer_ids:
                f.write('1. ' + test_questions['items'][q_num]['answers'][answer_id]['text'] + '\n')
            if PDF_print_answers_end:
                answers_end = answers_end + '[ ' + ', '.join(answerNumList) + ' ]'            
        elif "freeText" in test_questions['items'][q_num]['type']:
            if PDF_print_answers_end:
                freeTextList = list()
                # create comma separated list
                for aText_num in test_questions['items'][q_num]['answers']:
                    freeTextList.append(test_questions['items'][q_num]['answers'][aText_num]['text'])
                answers_end = answers_end + '"' + '; '.join(freeTextList) + '"'            
        ##############
        if PDF_print_solutions_inline:
            f.write('\pagebreak\n\n')
            # with answers
            f.write(text_topline + test_questions['items'][q_num]['question'])
            f.write(' \n\n' + langStrings[lang_used]['solution'] + ':\n\n')
            if "multipleChoice" in test_questions['items'][q_num]['type']:
                # correct answers counter to zero
                answers_correct = 0
                for answer_id in answers_random[q_num]:
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
                for info_id in test_questions['items'][q_num]['info']:
                    f.write('\n| *' + test_questions['items'][q_num]['info'][info_id]['key'].capitalize() + '*: ')
                    if 'value' in test_questions['items'][q_num]['info'][info_id]:
                        f.write(test_questions['items'][q_num]['info'][info_id]['value'])
                    if 'url' in test_questions['items'][q_num]['info'][info_id]:
                        f.write('<' + test_questions['items'][q_num]['info'][info_id]['url'] + '>')

            f.write('\pagebreak\n\n')
    # print the answers on the last page?
    if PDF_print_answers_end:
        f.write(answers_end)

# write PDF
#file_name_out = ((os.path.splitext(file_name_in)[0]) + '.' + filename_suffix + '.' + target_file_extension)
exec_string = "pandoc -s -i '" + file_name_md + "' -o '" + file_name_out + "'"
os.system(exec_string)
print('- Writing ' + target_file_extension + ' to: ' + file_name_out)
os.remove(file_name_md)

    