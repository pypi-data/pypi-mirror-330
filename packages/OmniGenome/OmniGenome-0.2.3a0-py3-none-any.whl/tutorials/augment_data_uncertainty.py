# -*- coding: utf-8 -*-
# file: pk_augment.py
# time: 13:29 22/08/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
import autocuda
import torch
import omnigenome
from omnigenome import OmniGenomeDatasetForTokenClassification
import random
from tqdm import tqdm
from transformers import AutoConfig, AutoTokenizer, AutoModelForMaskedLM
import numpy as np

aug_num = 10

def mask_basked_on_probability(sequence, probability_matrix, mask_prob=0.3, largest=False):
    """
    sequence: Tensor of tokenized input sequences.
    model_outputs: Model's output logits (before softmax).
    mask_prob: Percentage of most uncertain nucleotides to mask.
    """
    probability_matrix = torch.Tensor(probability_matrix)
    # entropy = -torch.sum(probability_matrix * torch.log(probability_matrix + 1e-10), dim=-1)
    num_to_mask = int(mask_prob * len(sequence))
    most_uncertain_indices = torch.topk(probability_matrix, num_to_mask, largest=largest).indices

    masked_indices = torch.zeros_like(probability_matrix, dtype=torch.bool)
    masked_indices[most_uncertain_indices] = True

    # Reshape the masked indices back to the original sequence shape
    masked_indices = masked_indices.view(len(sequence))

    return masked_indices

def softmax_to_entropy(softmax_vals):
    # print(softmax_vals)
    # softmax_vals = softmax_vals.cpu().detach().numpy()
    entropy = -torch.sum(softmax_vals * torch.log(softmax_vals + 1e-9))  # small epsilon to avoid log(0)
    return entropy

def uncertainty_quantification_masking(model, tokenizer, sequence, method="logits",
                                      temperature=1):
    device = autocuda.auto_cuda()
    model.to(device)
    inputs = tokenizer(
                sequence,
                padding="do_not_pad",
                truncation=False,
                return_tensors="pt",
            )
    inputs = inputs.to(device)
    sequence = np.array(list(sequence), dtype=np.str_)
    # Inject ways of measuring uncertainty here
    if method == "logits":
        logits = model(**inputs)[0]
        # print(f"Logits Shape: {logits.shape}")
        probabilities = torch.softmax(logits / temperature, dim=-1)
        # print(f"Probabilities Shape {probabilities.shape}")
        entropy = torch.empty(probabilities.shape[:-1], dtype=probabilities.dtype, device=probabilities.device)
        for i, x in enumerate(probabilities):
            entropy[i] = softmax_to_entropy(x)
        uncertainty_matrix = entropy
    elif method == "temp_scaling":
        temperature = 1.923 # Obtained from running temperature_scaling on validation set 
        logits = model(**inputs)[0]
        # print(f"Logits Shape: {logits.shape}")
        probabilities = torch.softmax(logits / temperature, dim=-1)
        # print(f"Probabilities Shape {probabilities.shape}")
        entropy = torch.empty(probabilities.shape[:-1], dtype=probabilities.dtype, device=probabilities.device)
        for i, x in enumerate(probabilities):
            entropy[i] = softmax_to_entropy(x)
        uncertainty_matrix = entropy
    elif method == "new_method":
        pass
    # Create a probability matrix based on the uncertainty
    probability_matrix = np.zeros(len(sequence))
    token_idx = 0
    for char_idx, char in enumerate(sequence):
        if token_idx < uncertainty_matrix.shape[1]:
            probability_matrix[char_idx] = uncertainty_matrix[0, token_idx]
        if token_idx + 1 < uncertainty_matrix.shape[1] and tokenizer.decode(inputs['input_ids'][0, token_idx+1]) == '':
            token_idx += 1
        token_idx += 1

    # Mask based on the probability matrix
    masked_indices = mask_basked_on_probability(sequence, probability_matrix)
    return masked_indices, probability_matrix

def mlm_mutate(population, structure, mutation_ratio, model, tokenizer):
    def mutate(sequence, mutation_rate):

        masked_indices, probability_matrix = \
        uncertainty_quantification_masking(model, tokenizer, sequence)
        sequence = np.array(list(sequence), dtype=np.str_)
        sequence[masked_indices] = "$"
        mut_seq = "".join(sequence.tolist()).replace("$", tokenizer.mask_token)
        return mut_seq

    mlm_inputs = []
    masked_sequences = []

    for seq, struct in zip(population[:1], structure[:1]):
        for _ in range(aug_num):
            masked_sequence = mutate(seq, mutation_ratio)
            masked_sequences.append(masked_sequence)
            mlm_inputs.append(
                f"{masked_sequence}{tokenizer.eos_token}{''.join(struct)}"
            )
    print(f"mlm_inputs {mlm_inputs}")
    outputs = mlm_predict(mlm_inputs, structure, model, tokenizer)

    mut_population = []

    for i in range(len(outputs)):
        # print(f"Outputs {outputs[i]}")
        old_sequence = mlm_inputs[i].replace("<mask>","$")
        sequence = tokenizer.convert_ids_to_tokens(outputs[i].tolist())
        print(f"len new sequence {len(sequence)}")
        print(sequence)
        new_sequence, counter = "", 0
        for x in old_sequence:
            if x == "$": 
                x = sequence[counter]
                counter += 1
            new_sequence += x
        # print(f"Sequence {sequence}")
        fixed_sequence = [
            x
            if x in "AGCT" and y == "$"
            else (y if y and y != "$" else random.choice(["A", "T", "G", "C"]))
            for x, y in zip(
                sequence,
                list(masked_sequences[i].replace(tokenizer.mask_token, "$")),
            )
        ]
        mut_population.append((new_sequence, structure[i//aug_num]))
    return mut_population


def mlm_predict(mlm_inputs, structures, model, tokenizer, accept_threshold=0.5, temperature=1):
    batch_size = 16
    all_outputs = []
    softmax_outputs = []
    from transformers import set_seed

    set_seed(random.randint(0, 99999999), deterministic=False)

    with torch.no_grad():
        for i in tqdm(range(0, len(mlm_inputs), batch_size)):
            batch_mlm_inputs = tokenizer(
                mlm_inputs[i: i + batch_size],
                padding="max_length",
                max_length=1024,
                truncation=True,
                return_tensors="pt",
            )
            for col in batch_mlm_inputs:
                if batch_mlm_inputs[col].dtype == torch.int64:
                    batch_mlm_inputs[col] = batch_mlm_inputs[col].to(torch.int64)
            batch_mlm_inputs = batch_mlm_inputs.to(model.device)
            with torch.cuda.amp.autocast():
                outputs = model(**batch_mlm_inputs)[0]
                # Temp = 1 if not temperature scaling
                probabilities = torch.softmax(outputs / temperature, dim=-1)
                predictions = probabilities.cpu().detach().argmax(dim=-1)
                # print(f"probabilities: {probabilities.shape}")
                accepted_mask_inputs = []
                # Iterate through each nucleotide position
                probability_idx = i % 16
                for prob_idx in range(len(probabilities[probability_idx])):
                    # print(f"outputs {len(outputs)}")
                    # print(f"probabilities len {len(probabilities)}")
                    temp = []
                    masked_seq = mlm_inputs[i].replace("<mask>","$")
                    # Collect acceptable candidates for the current nucleotide position
                    for candidate_idx in range(len(probabilities[probability_idx][prob_idx])):
                        # print(f"uncertainty: {probabilities[0][prob_idx]}")
                        if probabilities[probability_idx][prob_idx][candidate_idx] <= accept_threshold:
                            temp.append(candidate_idx)
                        else: # inefficient but temporary
                            pass
                            # temp.append(0)
                    temp_tensor = torch.Tensor(temp)
                    accepted_mask_inputs.append(temp_tensor)
                
                # Convert accepted_mask_inputs to a PyTorch tensor
                accepted_mask_inputs_tensor = torch.nn.utils.rnn.pad_sequence(accepted_mask_inputs,
                                                                              batch_first=True)

            # softmax_outputs.append(outputs)
            # if not temperature_scaling:
            #     outputs = outputs.argmax(dim=-1)
            # print(f"Accepted Inputs {accepted_mask_inputs_tensor}")
            all_outputs.append(accepted_mask_inputs_tensor)
            del batch_mlm_inputs
            del outputs
    outputs = torch.cat(all_outputs, dim=0)
    return outputs #[outputs[i, 1: 1 + len(structures[i//aug_num])] for i, _ in enumerate(mlm_inputs)], softmax_outputs



print(omnigenome.__version__)

# Predefined dataset label mapping
label2id = {"(": 0, ")": 1, ".": 2}

# The is FM is exclusively powered by the OmniGenome package
# model_name_or_path = "../AMR_Model/OmniGenome-186M/"
model_name_or_path = "anonymous8/OmniGenome-186M"
# Generally, we use the tokenizers from transformers library, such as AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

# However, OmniGenome provides specialized tokenizers for genomic data, such as single nucleotide tokenizer and k-mers tokenizer
# we can force the tokenizer to be used in the model
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

# Define the modelz
config = AutoConfig.from_pretrained(
    model_name_or_path, num_labels=len(label2id), trust_remote_code=True
)

ssp_model = AutoModelForMaskedLM.from_pretrained(model_name_or_path, trust_remote_code=True)
ssp_model.to(torch.float32)

# valid_file="data/valid/valid.json"
valid_file=r"C:\Users\chuan\OneDrive - University of Exeter\AIProjects\OmniGenomeBench\examples\jack.ffi\valid_pkinc.json"
valid_set = OmniGenomeDatasetForTokenClassification(
    data_source=valid_file,
    tokenizer=tokenizer,
    label2id=label2id,
    max_length=512,
    shuffle=True,
)
valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=16)

# Add Temperature Scaling to Model
# from temperature_scaling.temperature_scaling_transformers import ModelWithTemperature
# scaled_model = ModelWithTemperature(ssp_model)
# Re-calibrate model using temperature scaling
# scaled_model.set_temperature(valid_loader)
temperature_scaling = False

# ssp_model = scaled_model

# We have implemented a diverse set of genomic models in OmniGenome, please refer to the documentation for more details

# Add masking to the current training data

import json
origin_data = []
new_data = []
# with open("data/rna_only/RNAStrAlign/rnastralign_pk_train_data_with_T.json", "r") as json_file:
with open(valid_file, "r") as json_file:
    lines = json_file.readlines()
    lines = sorted(lines, key=lambda x: len(json.loads(x)["label"]))
    for line in lines:
        line2 = json.loads(line)
        if len(line2["label"].strip()) > 500:
            continue
        line = json.loads(line.strip())
        origin_data.append(line.copy())
        line["label"]=line["label"].replace('[', '.')
        line["label"]=line["label"].replace(']', '.')
        line["label"]=line["label"].replace('{', '.')
        line["label"]=line["label"].replace('}', '.')
        line["label"]=line["label"].replace('<', '.')
        line["label"]=line["label"].replace('>', '.')
        new_data.append(line)

device = autocuda.auto_cuda()
ssp_model.to(device)
augmentations = mlm_mutate([x["seq"] for x in new_data], [x["label"] for x in new_data], 0.3, ssp_model, tokenizer)

print(f"Augmentation: {augmentations[0]}")
synthetic_training_data = [{"label": origin_data[i//aug_num]["label"], "seq": seq} for i, (seq, label) in enumerate(augmentations)]
# train_data = []
# with open("../train_pkfree.json", "r") as json_file:
#     for line in json_file:
#         train_data.append(json.loads(line.strip()))
# synthetic_training_data += train_data

# with open('data/rna_only/RNAStrAlign/uncertainty_synthetic_train_data_largest.json', 'w') as json_file:
with open('data/valid/valid_augmented.json', 'w') as json_file:
    for item in synthetic_training_data:
        json.dump(item, json_file)
        json_file.write('\n')
