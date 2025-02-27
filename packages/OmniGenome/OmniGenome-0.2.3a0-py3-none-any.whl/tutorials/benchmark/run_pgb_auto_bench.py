# -*- coding: utf-8 -*-
# file: run_rgb_auto_bench.py
# time: 22:52 27/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

import argparse

from typing_extensions import Union

from omnigenome import AutoBench

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default="pgb")
    # parser.add_argument("--root", type=str, default="omnigenome_pgb")
    parser.add_argument(
        # "--gfm", type=str, default="genomic_foundation_models/SpliceBERT-510nt"
        # "--gfm", type=str, default="genomic_foundation_models/3utrbert"
        # "--gfm",        type=str,        default="genomic_foundation_models/cdsBERT"
        # "--gfm", type=str, default="genomic_foundation_models/hyenadna-large-1m-seqlen-hf/"
        # "--gfm", type=str, default="genomic_foundation_models/nucleotide-transformer-v2-100m-multi-species"
        "--gfm", type=str, default="genomic_foundation_models/OmniGenome-52M"
        # "--gfm", type=str, default="genomic_foundation_models/mprna_small_new"
    )
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--overwrite", type=bool, default=False)

    args = parser.parse_args()
    benchmark = args.root


    bench = AutoBench(benchmark=benchmark, model_name_or_path=args.gfm, overwrite = args.overwrite)
    # bench.run(autocast=False, batch_size=4)
    bench.run(
        autocast=False,
        batch_size=args.batch_size,
        # seeds=[2028],
    )
