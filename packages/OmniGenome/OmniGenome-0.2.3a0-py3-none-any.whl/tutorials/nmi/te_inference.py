# -*- coding: utf-8 -*-
# file: te_inference.py
# time: 10:39 21/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

from omnigenome import ModelHub

print(
    ModelHub.load("OmniGenome-185M").inference(
        "GGAAGCUGUGAGAGAGGAGACUUGGGAACGCGGGUUUUCAAGCCCCCCACAGAAAAG"
    )
)
