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
source_file_extension = 'qcz'
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

file_names = glob.glob('*.' + source_file_extension)

for file_name_in in file_names:
    file_id_stump = os.path.basename(file_name_in)[1:12]
    
    qAllArr             = tree() # using 'collections import defaultdict' and 'lambda: defaultdict(tree)' above
    counterQuestions    = 0 # counter for questions
    qAnswerCount        = 0 # counter for answers
    qItemSection        = 0 # to mark if metaYaml, question or answers
    tempYaml            = 0 # if metaYaml found not zero

    print('- Reading ' + source_file_extension + ' file: "' + file_name_in + '"')
    with open(file_name_in) as file:
        lines = file.readlines()
    
    for line in lines:
        if line.strip() != "":
            line = line.strip()
            firstChar = line[0]
            # beginning == metadata yaml, question, or answer inside answerblock?
            if line == "---":
                print ("  - YAML header found")
                qItemSection = "metaYaml" # check later where to add the line
                tempYaml = ""
            elif firstChar is ">":
                # increment counter
                counterQuestions = counterQuestions + 1
                # reset counter of answers bc of new question item
                qAnswerCount = 0 
                qItemSection = "question" # check later where to add the line
                # save first line of question
                qAllArr['items'][counterQuestions]['question'] = line[1:].strip()
                #qAllArr['items'][$counterQuestions]['question'] = trim(substr($line, 1));
            elif firstChar is "+":
                # Answer: type multiple choice and correct
                qAnswerCount = qAnswerCount + 1
                qItemSection = "answer" # check later where to add the line
                qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['text'] = line[1:].strip()
                qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['bolean'] = True
                qAllArr['items'][counterQuestions]['type']['multipleChoice'] = True
            elif firstChar is "-":
                # Answer: type multiple choice and incorrect
                qAnswerCount = qAnswerCount + 1
                qItemSection = "answer" # check later where to add the line
                qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['text'] = line[1:].strip()
                qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['bolean'] = False
                qAllArr['items'][counterQuestions]['type']['multipleChoice'] = True
            elif firstChar is "*":
                # Answer: type free text and one possible option
                qAnswerCount = qAnswerCount + 1
                qItemSection = "answer" # check later where to add the line
                qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['text'] = line[1:].strip()
                qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['bolean'] = True
                qAllArr['items'][counterQuestions]['type']['freeText'] = True
            elif firstChar is "[":
                qAnswerCount = qAnswerCount + 1
                item = dict()
                output = re.search('\[(.*?)\]\((.*?)\)', line, flags=re.IGNORECASE)
                item['key'] = re.search('\[(.*?)\]\((.*?)\)', line, flags=re.IGNORECASE).group(1).strip()
                value = re.search('\[(.*?)\]\((.*?)\)', line, flags=re.IGNORECASE).group(2).strip()
                if value is not None:
                    if (value[0:4].lower()) == "http":
                        item['url'] = value
                    else:
                        item['value'] = value
                    qAllArr['items'][counterQuestions]['info'][qAnswerCount] = item
            else:
                # additional line for current element
                if qItemSection == "metaYaml":
                    if line == "...":
                        qItemSection == 0
                    else:
                        tempYaml = tempYaml + line + "\n"
                elif qItemSection is "question":
                    qAllArr['items'][counterQuestions]['question'] = qAllArr['items'][counterQuestions]['question'] + " " + line.strip()
                elif qItemSection is "answer":
                    qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['text'] = qAllArr['items'][counterQuestions]['answers'][qAnswerCount]['text'] + " " + line.strip()
    
    # add metadata from YAML to meta section in JSON (if any)
    if tempYaml != 0:
        metaYamlDict = json.loads(json.dumps(yaml.safe_load(tempYaml)))
        # add some meta information if missing
        if 'date_created' not in metaYamlDict:
            # creation date
            metaYamlDict['date_created'] = date_current
        if 'path_origin' not in metaYamlDict:
            # path of the first file from which this started
            metaYamlDict['path_origin'] = os.path.abspath(file_name_in)
        for itemId in metaYamlDict:
            qAllArr['meta'][str(itemId)] = metaYamlDict[str(itemId)]
        
    # now drop all the *invalid* ones
    
    # to do so: handle the process in a dictionary
    qAllDict = json.loads(json.dumps(qAllArr))
    
    for itemId in qAllArr['items']:
        itemDict = json.loads(json.dumps(qAllArr['items'][itemId]))
        if 'question' not in itemDict:
            #print(qAllDict['items'].pop(itemId, None))
            del qAllDict['items'][str(itemId)]
    
    print('--- Number of questions found in set: ' + str(counterQuestions))
    counterQuestionsTotal = counterQuestionsTotal + counterQuestions
    #print('- qAllArr: ' + str(qAllArr))

print('Count of total questions found: ' + str(counterQuestionsTotal))
print('Searched through ' + str(len(file_names)) + ' ' + source_file_extension + ' files.')

