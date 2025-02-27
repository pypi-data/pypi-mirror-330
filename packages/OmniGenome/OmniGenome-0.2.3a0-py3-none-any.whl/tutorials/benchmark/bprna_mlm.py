import json
import random

import RNA
import autocuda
import torch
import tqdm
from transformers import AutoModelForMaskedLM, AutoTokenizer

from omnigenome import ClassificationMetric, OmniGenomeTokenizer
from omnigenome import (
    OmniGenomeDatasetForTokenClassification,
)


# compute_metrics = ClassificationMetric(ignore_y=-100, average="macro").f1_score
compute_metrics = ClassificationMetric(ignore_y=-100).accuracy_score

# train_file = "rgb/RNA-SSP-bpRNA/train.json"
# valid_file = "rgb/RNA-SSP-bpRNA/valid.json"

# test_file = "rgb/RNA-SSP-Archive2/test.json"
# test_file = "rgb/RNA-SSP-bpRNA/test.json"
# test_file = "rgb/RNA-SSP-rnastralign/test.json"
test_file = "../../examples/benchmark/rgb/RNA-SSP-Rfam/test.json"
# test_file = "rgb/RNA-mRNA/test.json"

device = autocuda.auto_cuda()

model_name_or_path = "anonymous8/OmniGenome-52M"
# model_name_or_path = "anonymous8/OmniGenome-186M"
# model_name_or_path = "../benchmark/genomic_foundation_models/SpliceBERT-510nt"

model = AutoModelForMaskedLM.from_pretrained(
    model_name_or_path, trust_remote_code=True
).to(device)
# tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
tokenizer = OmniGenomeTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

test_set = []
labels = []
with open(test_file) as f:
    for line in f.readlines()[:1000]:
        line = json.loads(line)
        seq = line["seq"] if "seq" in line else line["sequence"]
        test_set.append(seq+"<eos>"+RNA.fold(seq)[0])
        # test_set.append(seq)

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
        :, random.randint(0, len(tokenized_inputs["input_ids"][0]) // 2)
        # :, random.randint(0, len(tokenized_inputs["input_ids"][0]) - 1)
    ] = tokenizer.mask_token_id
    label_ids = tokenizer(
        seq,
        padding="do_not_pad",
        truncation=True,
        max_length=1024,
        return_tensors="pt",
    )["input_ids"]
    label_ids[
        tokenized_inputs["input_ids"] != tokenizer.mask_token_id
    ] = -100
    with torch.no_grad():
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
