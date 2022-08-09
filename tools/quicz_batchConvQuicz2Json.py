#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import sys

# VARS
source_file_extension = 'qcz'

# VARS

file_names = glob.glob('*.' + source_file_extension)

print(file_names)

for file_name_in in file_names:
    exec_string = 'quicz_convQuicz2Json -i "' + file_name_in + '"'
    print('- WRAPPER : ' + exec_string)
    os.system(exec_string)
