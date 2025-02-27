# -*- coding: utf-8 -*-
# file: clean_files.py
# time: 13:51 04/06/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
import os

import findfile

for f in findfile.find_files("../", or_key=['model_state_dict.pt']):
    print(f)
    os.remove(f)
