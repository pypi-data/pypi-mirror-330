# -*- coding: utf-8 -*-
# file: tmp_test.py
# time: 23:45 03/10/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

import numpy as np
import json
import gradio as gr
import RNA

from omnigenome import ModelHub

path_to_save = "../OmniGenome-186M-SSP"

train_file = r"../../examples/benchmark/__OMNIGENOME_DATA__/benchmarks/RGB/RNA-SSP-rnastralign/train.json"

# Load the model checkpoint
ssp_model = ModelHub.load(path_to_save)
results = ssp_model.inference("CAGUGCCGAGGCCACGCGGAGAACGAUCGAGGGUACAGCACUA")
print(results["predictions"])
print("logits:", results["logits"])

def ss_validity_loss(rna_strct):
    dotCount = 0
    leftCount = 0
    rightCount = 0
    unmatched_positions = []  # 用于记录未匹配括号的位置
    uncoherentCount = 0
    prev_char = ""
    for i, char in enumerate(rna_strct):
        if prev_char != char:
            uncoherentCount += 1
        prev_char = char

        if char == "(":
            leftCount += 1
            unmatched_positions.append(i)  # 记录左括号位置
        elif char == ")":
            if leftCount > 0:
                leftCount -= 1
                unmatched_positions.pop()  # 移除最近的左括号位置
            else:
                rightCount += 1
                unmatched_positions.append(i)  # 记录右括号位置
        elif char == ".":
            dotCount += 1
        else:
            raise ValueError(f"Invalid character {char} in RNA structure")
    match_loss = (leftCount + rightCount) / (len(rna_strct) - dotCount + 1e-5)
    return match_loss


def find_invalid_ss_positions(rna_strct):
    left_brackets = []  # 存储左括号的位置
    right_brackets = []  # 存储未匹配的右括号的位置
    for i, char in enumerate(rna_strct):
        if char == "(":
            left_brackets.append(i)
        elif char == ")":
            if left_brackets:
                left_brackets.pop()  # 找到匹配的左括号，从列表中移除
            else:
                right_brackets.append(i)  # 没有匹配的左括号，记录右括号的位置
    return left_brackets + right_brackets


def fold(rna_sequence):
    ref_struct = RNA.fold(rna_sequence)[0]
    RNA.svg_rna_plot(rna_sequence, ref_struct, f"real_structure.svg")

    pred_structure = "".join(ssp_model.inference(rna_sequence)["predictions"])
    print(pred_structure)
    if ss_validity_loss(pred_structure) == 0:
        RNA.svg_rna_plot(rna_sequence, pred_structure, f"predicted_structure.svg")
        return (
            ref_struct,
            pred_structure,
            "real_structure.svg",
            "predicted_structure.svg",
        )
    else:
        # return blank image of predicted structure
        # generate a blank svg image
        with open("predicted_structure.svg", "w") as f:
            f.write(
                '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
            )
        return (
            ref_struct,
            pred_structure,
            "real_structure.svg",
            "predicted_structure.svg",
        )


def repair_rna_structure(rna_sequence, invalid_struct):
    try:
        invalid_ss_positions = find_invalid_ss_positions(invalid_struct)
        for pos_idx in invalid_ss_positions:
            if invalid_struct[pos_idx] == "(":
                invalid_struct = (
                    invalid_struct[:pos_idx] + "." + invalid_struct[pos_idx + 1 :]
                )
            else:
                invalid_struct = (
                    invalid_struct[:pos_idx] + "." + invalid_struct[pos_idx + 1 :]
                )

        best_pred_struct = invalid_struct
        RNA.svg_rna_plot(rna_sequence, best_pred_struct, f"best_pred_struct.svg")
        return best_pred_struct, "best_pred_struct.svg"
    except Exception as e:
        with open("best_pred_struct.svg", "w") as f:
            f.write(
                '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
            )
        return e, "best_pred_struct.svg"


def sample_rna_sequence():
    example = examples[np.random.randint(0, len(examples))]
    RNA.svg_rna_plot(example["seq"], example["label"], f"annotated_structure.svg")

    return example["seq"], example["label"], "annotated_structure.svg"


# 定义界面
with gr.Blocks() as demo:
    gr.Markdown("### RNA Secondary Structure Prediction")

    with gr.Row():
        with gr.Row():
            rna_input = gr.Textbox(
                label="RNA Sequence", placeholder="Enter RNA sequence here..."
            )
        with gr.Row():
            strcut_input = gr.Textbox(
                label="Annotated Secondary Structure",
                placeholder="Enter RNA secondary structure here...",
            )

    with gr.Row():
        #     examples = [
        #     ["GCGUCACACCGGUGAAGUCGCGCGUCACACCGGUGAAGUCGC"],
        #     ["GCUGGGAUGUUGGCUUAGAAGCAGCCAUCAUUUAAAGAGUGCGUAACAGCUCACCAGCGCUGGGAUGUUGGCUUAGAAGCAGCCAUCAUUUAAAGAGUGCGUAACAGCUCACCAGC"],
        #     ["GGCUGGUCCGAGUGCAGUGGUGUUUACAACUAAUUGAUCACAACCAGUUACAGAUUUCUUUGUUCCUUCUCCACUCCCACUGCUUCACUUGACUAGCCUU"],
        # ]
        #     gr.Examples(examples=examples, label="Examples", inputs=[rna_input])
        with open(train_file, "r") as f:
            examples = []
            for line in f:
                examples.append(json.loads(line))

        sample_button = gr.Button("Sample a RNA Sequence from RNAStrand2 testset")

    with gr.Row():
        submit_button = gr.Button("Run Prediction")

    with gr.Row():
        ref_structure_output = gr.Textbox(
            label="Secondary Structure by ViennaRNA", interactive=False
        )

    with gr.Row():
        pred_structure_output = gr.Textbox(
            label="Secondary Structure by Model", interactive=False
        )

    with gr.Row():
        anno_structure_output = gr.Image(
            label="Annotated Secondary Structure", show_share_button=True
        )
        real_image = gr.Image(
            label="Secondary Structure by ViennaRNA", show_share_button=True
        )
        predicted_image = gr.Image(
            label="Secondary Structure by Model", show_share_button=True
        )

    with gr.Row():
        repair_button = gr.Button("Run Prediction Repair")

    submit_button.click(
        fn=fold,
        inputs=rna_input,
        outputs=[
            ref_structure_output,
            pred_structure_output,
            real_image,
            predicted_image,
        ],
    )

    repair_button.click(
        fn=repair_rna_structure,
        inputs=[rna_input, pred_structure_output],
        outputs=[pred_structure_output, predicted_image],
    )

    sample_button.click(
        fn=sample_rna_sequence, outputs=[rna_input, strcut_input, anno_structure_output]
    )
demo.launch(share=True)