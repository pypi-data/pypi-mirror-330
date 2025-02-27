import json
import pickle
import random

import ViennaRNA
import autocuda
import torch
import tqdm
from transformers import AutoModelForMaskedLM, AutoTokenizer

from omnigenome import ClassificationMetric
from omnigenome import (
    OmniGenomeDatasetForTokenClassification,
)

import json
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import autocuda
import numpy as np
import torch

from transformers import AutoModelForMaskedLM, AutoTokenizer, OmniGenomeModelForSeq2SeqLM
import requests


from concurrent.futures import ThreadPoolExecutor
import ViennaRNA


def predict_structure_single(sequence):
    """Predicts the RNA structure for a single sequence."""
    return ViennaRNA.fold(sequence.replace("T", "U"))[0]


def predict_structure(sequences):
    """Predicts structures for multiple sequences using multithreading."""
    if isinstance(sequences, list):
        with ThreadPoolExecutor() as executor:
            # Map the predict_structure_single function to each sequence
            structures = list(executor.map(predict_structure_single, sequences))
        return structures
    else:
        # Single sequence case
        return predict_structure_single(sequences)

class RegionClasssificationDataset(OmniGenomeDatasetForTokenClassification):
    def __init__(self, data_source, tokenizer, label2id, max_length):
        super().__init__(data_source, tokenizer, label2id, max_length)

    def prepare_input(self, instance, **kwargs):
        sequence = f'{instance["5utr"]}{instance["cds"]}{instance["3utr"]}'
        labels = (
            [0] * len(instance["5utr"])
            + [1] * len(instance["cds"])
            + [2] * len(instance["3utr"])
        )
        tokenized_inputs = self.tokenizer(
            sequence,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            # max_length=1024,
            return_tensors="pt",
            **kwargs,
        )
        for col in tokenized_inputs:
            tokenized_inputs[col] = tokenized_inputs[col].squeeze()

        if labels is not None:
            tokenized_inputs["labels"] = torch.tensor([-100] + labels + [-100])
        return tokenized_inputs


label2id = {"5utr": 0, "cds": 1, "3utr": 2}

compute_metrics = ClassificationMetric(ignore_y=-100, average="macro").f1_score

# train_file = "RNA-Region-Classification/Rice/train.json"
# test_file = "RNA-Region-Classification/Rice/test.json"
# valid_file = "RNA-Region-Classification/Rice/valid.json"
train_file = "RNA_Region_Classification/Arabidobsis/train.json"
test_file = "RNA_Region_Classification/Arabidobsis/test.json"
valid_file = "RNA_Region_Classification/Arabidobsis/valid.json"
#
device = autocuda.auto_cuda()

model_name_or_path = "yangheng/PlantRNA-FM"
# model_name_or_path = "../tutorials/pretrained_models/esm2_rna_35M_ss"
# model_name_or_path = "../../examples/benchmark/genomic_foundation_models/OmniGenome-186M"
# model_name_or_path = "../../examples/benchmark/genomic_foundation_models/OmniGenomeV5-186M"
# model_name_or_path = "../../examples/benchmark/genomic_foundation_models/SpliceBERT-510nt"

model = AutoModelForMaskedLM.from_pretrained(
    model_name_or_path, trust_remote_code=True
).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

test_set = []
labels = []
with open(test_file) as f:
    for line in f.readlines():
        line = json.loads(line)
        seq = line["5utr"] + line["cds"] + line["3utr"]
        test_set.append(seq)

if not os.path.exists("structures.pkl"):
    structures = predict_structure(test_set)
    with open("structures.pkl", "wb") as f:
        pickle.dump(structures, f)
else:
    with open("structures.pkl", "rb") as f:
        structures = pickle.load(f)
# test_set = [f"{seq}<eos>{struct}" for seq, struct in zip(test_set, structures)]

for i in range(len(test_set)):
    labels.append(list(test_set[i].replace('<eos>', '$')))

predictions = None
true_labels = None
for seq in tqdm.tqdm(test_set):
    tokenized_inputs = tokenizer(
        seq,
        padding="do_not_pad",
        truncation=True,
        max_length=1024,
        return_tensors="pt",
    )
    tokenized_inputs["input_ids"][
        :, random.randint(0, len(tokenized_inputs["input_ids"][0])//2)
    ] = tokenizer.mask_token_id
    label_ids = tokenizer(
        seq,
        padding="do_not_pad",
        truncation=True,
        max_length=1024,
        return_tensors="pt",
    )["input_ids"]
    label_ids[tokenized_inputs["input_ids"] != tokenizer.mask_token_id] = -100
    prediction = model(**tokenized_inputs.to(device))["logits"]
    prediction = prediction.argmax(dim=-1).view(-1).to("cpu")
    label_ids = label_ids.view(-1).to("cpu")
    predictions = (
        prediction if predictions is None else torch.cat([predictions, prediction])
    )
    true_labels = (
        label_ids if true_labels is None else torch.cat([true_labels, label_ids])
    )

f1 = compute_metrics(predictions[true_labels != -100], true_labels[true_labels != -100])
print(f1)
