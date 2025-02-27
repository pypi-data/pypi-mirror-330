# -*- coding: utf-8 -*-
# file: shap_test.py
# time: 10:27 25/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

import os

import matplotlib as mpl
import numpy as np
from transformers import AutoTokenizer

from omnigenome import ModelHub

# set working path
os.chdir("")
mpl.rcParams["figure.dpi"] = 1000

model = ModelHub.load("OmniGenome-185M")

examples = [
    {
        "gene": "LOC_Os09g24440.1",
        "rna": [
            "CACACAGATTTTGGCCCAACATAACGGCCCATAAAATCTAACTTTTCGGTGGGCCACAAGCCCAAAGCCACGGAAAAGGGAGCGTCCCTGCCGCGGGATCCGGCGTGCACCCAGTCCATATCCATAGACCACCACGGCACGAGCGCCTCGAGGCGTCCGGTCCCCACCGCGTCCCCGTGAACCGGGTCCACGCGTAGCACCCCCCCTCTCTCCCCCCACCGCGGCGGAGAAAGATCTGAGCCACGTCTTCGCTCGCTCGCCGGCGAGAGGTCGACCACTTCCTCTCCTCCTCCTCCCCGCCTATAAATACGACCCACCCCCCCCCCCCCCCCCCCCCCGCGGCTTCTCCCCTCGCTTTCCCCACACGGCCGCGCGATGACGTGGCGCGCCTCGACACCACCACCTCACCTCTGAAGCCCCCCACCTCACTTCCGACCGCCTTTGGTCCCCTTCTAGAAGCTTCCAAACCCTAGAGGAGGAGGAGGAGGAGGGGTTTCGGT",
            "1",
        ],
        "label": "1",
    },
    {
        "gene": "LOC_Os08g40620.2",
        "rna": [
            "CTAACTAAAACCACACCTCCCCTCACCACTATAGAACAAAATCCCCAGCCTCTCTCTCTAGATTCTCTCTCCTAATAAAAGAGAGAAAAAAAACCCAAGAAAAATAAGAGAGAGAAACTCTCTCTCTCTCATCACCCACCCAACCAAGCCACCCCCTCTCTCTCTTCCTTGCAAGCATCCATCTCATCAAAGGCCAAACCCTCCTCCTCTCCCCAACAAGAACAACAAGGAGGCGCGATTCACGCGAACAATCACAGGAGGGGGAGAGAAGGGGAGAAATCATCCGCTCATCTCCCAAAATCCTCCAAAAAAATCCATCTTTATCCCGAAAAGATCCTCCTTTTCTTGGGGTTTCTGACAGGCGTGCACGGCTATCTTTAGGCGTTCTCGGCCTCATCTCTCGTGGAAAGGTTCTTCTTCTTCGGGGTTGTTTGCTGCTGCTTAATTTGAGGAGGAAAAGCCCAATTCTTGTGGGGAGTGAAGGGAGGGAGGAGGGGGGC",
            "0",
        ],
        "label": "0",
    },
    {
        "gene": "LOC_Os02g16550.1",
        "rna": [
            "AAGGAGAACAGCAGAACTGGAACTTCACCCCATCGATGACAAACGTGACAACAATGGAGGCCCATAAATTTCCGGCCCAAAACCCATCAATCACCCCATCGATGCTTCTCCACCGGAGAAGTCCAATTCGATTCGTATCCCCACGTGCTCTTTCTTCTTCCTCCTCTCCGCATCCAACGCTCGAAGCGAGGAAGAAAAAGAAAAAAGAAAAAAAAAACAGAGATCCCCCACAACTTCCGAATCCGATCGGCGGTCGCGGCGGCGGCGGCGGCGTCGGCGACGGCGACGGCGGGGAGCTTCTTCCCGATCCCCTCCTGATCGCCCGCAGGATCGATCGAGCTCTCCCCCCCTCTCACTCACCTCGGGGGGCGCGGCGGTGGGGGGCTAGGGATTTGAGCCGGATCGCGGCGAGCTTGAAGGGGCGCGGACTGAGGCGGCGAGAGGAGCGGGTTTCCGGTTCGGGGGAAGGAGGGGAGGAGTAGTAGGAGGAGGAGGAGGAG",
            "1",
        ],
        "label": "1",
    },
    {
        "gene": "LOC_Os02g33670.1",
        "rna": [
            "AGAGTTTGAAAGGAGGAGAAACATAATGCCTAACTTGCTCTAACATGCTCCCCTTGTTTCCTCCCCCTTGGACTTTGAGGTTTGAACAACTCCATCCCATCCTATACTAATATAATGCAATGCTAATACTAGCACTAGTAGTACTATATAACTAAGCTTAACAACCATCCCTTTTTTTAATTTCTATTGTCACACATATATCCTTTTATACTACTCCTCTGTCCCTCCTCTCCCTAACCCATATATCTCCACCCCTCTTCTCCCCTCACTCACCATTTGCTCTCTTCTCTCTTCTCTCTTCTCCACATCACCACAGCCACACCACACTAGCTAGTGTTCATCATCATCATCATCATCATCATCATCTTCTTCTTCTTCTTCTTCTTCTTCCTCGCTTCGTTTTGCTAGCTCGATCGTGTCTAGCTGGTCGTCGTCGTCGTCGTCGTCTTCGCCATGGCCGGCTGTTTGCAGACGAGAAGCAGGAGGAGGAGGAGGCGGCC",
            "1",
        ],
        "label": "1",
    },
    {
        "gene": "LOC_Os09g11270.1",
        "rna": [
            "CACGGGCATACTACTAGTGAAAAAAAAAACCTTTATACACTTGCTTAGGTACGCATGCGTACGGACACCAATACGCCCATACGGATACGTACACGTACGGCCTCGACTCATCGAGCTCGAGCCGCCGGCCTGGCCACCCTTCGTCGCCCGCGAACCCCCCTTTCTCCGTCGTTCCCTCCCTTTCAACCTCCTTTCAAACCCTAGAAACTCGATTCCCCACCTCCAAAACCCTAACCCTAGCTCGCCGCGGAGAGCCTCCTCTCTCCTCCCCCTTCACGCCGCCCCCCCGCGGCTCCTGCGGCCGCCGGAACCCAAGCCCCCGCCTGACGGGGCCCTCGCGGACCTAGGGTTTGCCCGCGCGCGCTCCCCCCTCCTTGGGCCCCGACCCTGCGGGGCGGTAGCGGTCGGCGCGTGTGGGGGTGGAGAGAGAGGGAGAGGAGGTGGGGGAGGTGGAGATGAGATGAGGCGGCGGGGTGGCGGTGGTGGTGGTGGTGGTGGTG",
            "0",
        ],
        "label": "0",
    },
    {
        "gene": "LOC_Os01g61860.1",
        "rna": [
            "ACGAGGAGAAACCCACGAGGGGTGGTCATTCCCGAGTCCCCATCTGGCCATCTCTCCAATCTCCATGACAAAAAAATAACCAACCGGTCGAAAGAAAAATTCAACGAGTTGTGAAGACTTGTCCTCCAATTTCCCAACTCCCCAATCTGTCACCTCGCAGCTTCACGCTTCCACGCACACAGATCAAATCTCGAAATCCTACGACTCGTAGGATGGAGGAGTCGGAGTAGTAGTAAACGGCGATCGGATCGAATCGAATCATCGGCGCTGCTGCCTCCCCGAGCCGTGACCCCCCCCCTCCAAACCGCCGATAAGCTAAATTCATTCACACTCCACTTCACTCGCTCACGCTTCGCCGTCCGCGTCGCGTCGCGTTGCGTCGGCGGCGCCGCTGCACTGCACGCCTCGCCACCGGCGAGCGAAGGGAAGGAAGAGGAGGAGGAGGAGTTGGTGGTGGTGGTGGTGGCGCGGAGTCAGTGGCGGCGGCGGCGCGGGTGGAG",
            "0",
        ],
        "label": "0",
    },
]

texts = [example["rna"][0] for example in examples]
labels = [example["label"] for example in examples]


import shap
import scipy as sp


# this defines an explicit python function that takes a list of strings and outputs scores for each class
def func(x):
    ex = [" ".join(list(y.replace("...", "<unk>"))) for y in x]
    try:
        # outputs = classifier.predict(ex, print_result=False, ignore_error=False)
        outputs = model.inference(ex, padding=True, truncation=True, max_length=512)[
            "logits"
        ]
        scores = (np.exp(outputs).T / np.exp(outputs).sum(-1)).T
        val = sp.special.logit(scores)
    except Exception as e:
        raise e
        val = np.array([np.zeros((len(label_names))) for _ in range(len(ex))])
    return val


def create_explainer(method, tokenizer):
    # build an explainer by passing a transformers tokenizer
    if method == "transformers tokenizer":
        explainer = shap.Explainer(func, tokenizer, output_names=label_names)

    # build an explainer by explicitly creating a masker
    elif method == "default masker":
        masker = shap.maskers.Text(
            r"\W"
        )  # this will create a basic whitespace tokenizer
        explainer = shap.Explainer(func, masker, output_names=label_names)

    # build a fully custom tokenizer
    elif method == "custom tokenizer":
        import re

        def custom_tokenizer(s, return_offsets_mapping=True):
            """Custom tokenizers conform to a subset of the transformers API."""
            pos = 0
            offset_ranges = []
            input_ids = []
            # for m in re.finditer(r"[^\w\t]", s):
            for m in re.finditer(r"[a-zA-Z]", s):
                # for m in re.finditer(r" ", s):
                start, end = m.span(0)
                offset_ranges.append((pos, start))
                input_ids.append(s[pos:start])
                pos = end
            if pos != len(s):
                offset_ranges.append((pos, len(s)))
                input_ids.append(s[pos:])
            out = {}
            out["input_ids"] = input_ids
            if return_offsets_mapping:
                out["offset_mapping"] = offset_ranges
            return out

        # masker = shap.maskers.Text(custom_tokenizer, mask_token=tokenizer.mask_token)
        masker = shap.maskers.Text(custom_tokenizer, mask_token=" ")
        explainer = shap.Explainer(func, masker, output_names=label_names)
    return explainer


# load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "../tutorials/pretrained_models/mprna_base_new", use_fast=True
)
model.tokenizer = tokenizer

label_names = ["0", "1"]

clean_explainer = create_explainer("custom tokenizer", tokenizer)
shap_values = clean_explainer(texts[0:1])

shap.plots.text(shap_values)
