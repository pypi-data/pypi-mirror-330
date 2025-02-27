# -*- coding: utf-8 -*-
# file: ssp_viennarna.py
# time: 22:47 24/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
import json
import pickle
import random

import RNA
import sklearn.metrics as metrics
import torch
import tqdm

from transformers import AutoModelForTokenClassification, AutoTokenizer

# test_file = "__OMNIGENOME_DATA__/RGB/RNA-SSP-Rfam/valid.json"
# test_file = "__OMNIGENOME_DATA__/RGB/RNA-SSP-Rfam/test.json"
# test_file = "__OMNIGENOME_DATA__/RGB/RNA-SSP-Archive2/test.json"
# test_file = "__OMNIGENOME_DATA__/RGB/RNA-SSP-bpRNA/test.json"
# test_file = "__OMNIGENOME_DATA__/RGB/RNA-SSP-rnastralign/test.json"

# test_file = r"C:\Users\chuan\OneDrive - University of Exeter\AIProjects\OmniGenomeBench\examples\benchmark\__OMNIGENOME_DATA__\benchmarks\RGB\RNA-SSP-Archive2\test.json"
# test_file = r"C:\Users\chuan\OneDrive - University of Exeter\AIProjects\OmniGenomeBench\examples\benchmark\__OMNIGENOME_DATA__\benchmarks\RGB\RNA-SSP-rnastralign\test.json"
test_file = r"C:\Users\chuan\OneDrive - University of Exeter\AIProjects\OmniGenomeBench\examples\benchmark\__OMNIGENOME_DATA__\benchmarks\RGB\RNA-SSP-bpRNA\test.json"
# test_file = r"C:\Users\chuan\OneDrive - University of Exeter\AIProjects\OmniGenomeBench\examples\benchmark\__OMNIGENOME_DATA__\benchmarks\RGB\RNA-SSP-bpRNA\train.json"
# test_file = r"C:\Users\chuan\OneDrive - University of Exeter\AIProjects\OmniGenomeBench\examples\benchmark\__OMNIGENOME_DATA__\benchmarks\RGB\RNA-SSP-bpRNA-2000-90\test.json"
lines = []
with open(test_file) as f:
    for line in f.readlines():
        lines.append(json.loads(line))
# lines = random.sample(lines, 1000)
seqs = [line["seq"] for line in lines]
labels = [line["label"] for line in lines]
print(len(seqs))

preds = []
truths = []
for seq, label in zip(seqs, labels):
    truth = [{"(": "(", ")": ")", ".": "."}.get(x, '.') for x in list(label)]
    pred = list(RNA.fold(seq)[0])
    if len(truth) != len(pred):
        print(seq)
        print(truth)
        print(pred)
        continue
    truths += truth
    preds += pred

# preds = pickle.load(open("preds.pkl", "rb"))
# pickle.dump(preds, open("preds.pkl", "wb"))
f1_score = metrics.f1_score(truths, preds, average="macro")
mcc = metrics.matthews_corrcoef(truths, preds)
print("f1_score", f1_score)
print("mcc", mcc)


ssp_model = AutoModelForTokenClassification.from_pretrained(
    "anonymous8/OmniGenome-186M"
    # "anonymous8/OmniGenome-52M"
)
ssp_model.to("cuda")
tokenizer = AutoTokenizer.from_pretrained("anonymous8/OmniGenome-52M")
example = "GCCCGAAUAGCUCAGCGGUUAGAGCACUUGACUGUUAAUCAGGGGGUCGUUGGUUCGAGUCCAACUUCGGGCGCCA"

# seqs = [seq + "<eos>" + RNA.fold(seq)[0] for seq in seqs]
preds = []
truths = []
for i in tqdm.tqdm(range(0, len(seqs), 16)):
    seq = seqs[i : i + 16]
    label = labels[i : i + 16]
    inputs = tokenizer(
        seq, max_length=1024, padding=True, truncation=True, return_tensors="pt"
    ).to("cuda")
    with torch.no_grad():
        outputs = ssp_model(**inputs)
        logits = outputs.logits
        predicted_index = logits.argmax(-1).tolist()
        for pred, lab in zip(predicted_index, label):
            predicted_token = [ssp_model.config.id2label[i] for i in pred][
                1 : len(lab) + 1
            ]
            if len(predicted_token) != len(lab):
                print(seq)
                print(lab)
                print(predicted_token)
                continue
            preds += predicted_token
            truths += list(lab)


f1_score = metrics.f1_score(truths, preds, average="macro")
mcc = metrics.matthews_corrcoef(truths, preds)
print("f1_score", f1_score)
print("mcc", mcc)
