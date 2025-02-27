# -*- coding: utf-8 -*-
# file: run_rgb_auto_bench.py
# time: 22:52 27/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

import argparse
import random

from omnigenome import AutoBench

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--root", type=str, default="omnigenome_rgb")
    parser.add_argument("--root", type=str, default="rgb")
    parser.add_argument(
        # "--gfm", type=str, default="genomic_foundation_models/OmniGenome-52M"
        # "--gfm", type=str, default="../pretrained_models/OmniGenome-52M/OmniGenome-52M"
        "--gfm", type=str, default="../pretrained_models/OmniGenome-186M/OmniGenome-186M"
        # "--gfm", type=str, default="genomic_foundation_models/OmniGenome-186M"
        # default="genomic_foundation_models/agro-nucleotide-transformer-1b"
        # "--gfm", type=str, default="genomic_foundation_models/SpliceBERT-510nt"
        # "--gfm", type=str, default="genomic_foundation_models/DNABERT-2-117M"
        # "--gfm", type=str, default="genomic_foundation_models/3utrbert"
        # "--gfm", type=str, default="genomic_foundation_models/cdsBERT"
    )
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--overwrite", type=bool, default=True)

    args = parser.parse_args()
    benchmark = args.root

    bench = AutoBench(
        benchmark=benchmark, model_name_or_path=args.gfm, overwrite=args.overwrite
    )
    # bench.run(autocast=False, batch_size=4)
    # bench.run(autocast=False, batch_size=8)
    bench.run(autocast=False, batch_size=args.batch_size, seeds=[0, 1, 2])
    # bench.run(autocast=False, batch_size=args.batch_size)
