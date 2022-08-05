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
source_file_extension = "qcz"
target_file_extension = "json"

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
    
qAllArr             = tree() # using 'collections import defaultdict' and 'lambda: defaultdict(tree)' above
counterQuestions    = 0 # counter for questions
qAnswerCount        = 0 # counter for answers
qItemSection        = 0 # to mark if metaYaml, question or answers
tempYaml            = 0 # if metaYaml found not zero
quiczSpecChar = ["+", "-", "*", ">", "["]

# SPECIAL CHARACTERS
#    >   the first line of the question.
#       following lines belong to question until empty line
#   -   beginning of a wrong answer
#       following lines belong to question until empty line OR other bullet
#   +   beginning of a correct answer
#       following lines belong to question until empty line OR other bullet
#   *   beginning of a possible answer for a free text (written) question type
#       following lines belong to question until empty line OR other bullet
#   [   non markdown compatible use:
#       key, url, value
#       [string is var name](string is var value)
#       [string is var name](https://mi.cz rest string is var value)
#       MUST be one line
#       MUST be preceded and followed by an empty line

date_current = time.strftime("%Y-%m-%d %H:%M:%S")
qAllArr['meta']['filename_source'] = os.path.basename(file_name_in)
qAllArr['meta']['path_source'] = os.path.abspath(file_name_in)
qAllArr['meta']['filename_target'] = os.path.basename(file_name_out)
qAllArr['meta']['path_target'] = os.path.abspath(file_name_out)
qAllArr['meta']['date_updated'] = date_current

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

print('- Number of questions found: ' + str(counterQuestions))

#foreach($qAllArr['items'] as $key => $arr) {
#    if(
#        !(is_array($arr))
#        || !(isset($arr['answers']))         // answers undefined
#        || !(is_array($arr['answers']))      // answers not array
#        || (count($arr['answers']) < 1)      // zero answer options
#        || !(isset($arr['question']))        // question undefined
#        || !(is_string($arr['question']))    // question not a string
#        || count($arr['type']) != 1          // mix of question types (e.g. multipleChoice && freeText)     
#        ) {
#        unset($qAllArr['items'][$key]);
#    }
#}

# write JSON
with open(file_name_out, 'w') as fp:
    json.dump(qAllDict, fp, indent=2)
    print('- Writing ' + target_file_extension + ' to: ' + file_name_out)

