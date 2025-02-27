# -*- coding: utf-8 -*-
# file: rna_design.py
# time: 13:07 17/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
import json
import os
import random
import time
from concurrent.futures import as_completed, ProcessPoolExecutor

import RNA
import autocuda
import numpy as np
import requests
import torch.nn
import tqdm
from transformers import AutoConfig, AutoTokenizer, AutoModelForMaskedLM, AutoModelForSeq2SeqLM

from omnigenome import OmniGenomeModelForMLM, OmniGenomeTokenizer
from omnigenome.src.misc.utils import seed_everything


# 修改temperature
def get_mlm_model(model_name_or_path, device="cuda"):
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    # tokenizer = OmniGenomeTokenizer.from_pretrained(model_name_or_path)
    base_model = AutoModelForMaskedLM.from_pretrained(
        model_name_or_path
    )
    mlm_model = OmniGenomeModelForMLM(
        base_model, tokenizer=tokenizer
    )
    return mlm_model.to(device)


def batch_predict(seqs, mlm_model):
    predictions = {"sequences": [], "logits": []}
    seed_everything(random.randint(0, 99999999))
    # seqs = [seq.partition("<eos>")[0] for seq in seqs]
    batch_seqs = [seqs[:4] for i in range(0, len(seqs), 4)]
    for i_seqs in batch_seqs:
        results = mlm_model.inference(i_seqs, padding=True)
        predictions["sequences"] += [
            "".join(predictions) for predictions in results["predictions"]
        ]
        del results
        torch.cuda.empty_cache()
    return predictions


# def batch_query_sequence(sequences, structures=""):
#     """查询序列"""
#     url = "http://localhost:5000/batch_predict"
#     # 构造POST请求的数据，这里的键需要与服务端接收的键匹配
#     if not isinstance(structures, list):
#         structures = [structures] * len(sequences)
#     payload = [
#         f"{seq}<eos>{struct}" if struct else seq
#         for seq, struct in zip(sequences, structures)
#     ]
#     data = json.dumps({"seq": payload})
#     # 发送POST请求
#     try:
#         response = requests.post(url, json=data)
#         # 检查响应状态码
#         if response.status_code == 200:
#             outputs = response.json()
#             probs = [probs for probs in outputs["probs"]]
#             seqs = [seq.replace("T", "U") for seq in outputs["sequence"]]
#             outputs = {"sequences": seqs, "probs": probs}
#             return outputs
#
#         else:
#             return {
#                 "sequences": ["G" * len(struct) for struct in structures],
#                 "probs": 0,
#             }
#     except Exception as e:
#         print(e)
#         time.sleep(0.1)
#         return batch_query_sequence(sequences, structures)


def batch_query_structure(sequences):
    """查询结构"""
    url = "http://localhost:5000/ss_predict"
    # 构造POST请求的数据，这里的键需要与服务端接收的键匹配
    data = json.dumps({"seq": sequences})
    # 发送POST请求
    try:
        response = requests.post(url, json=data)
        # 检查响应状态码
        if response.status_code == 200:
            outputs = response.json()
            outputs = {"sequences": outputs["sequence"]}
            return outputs
        else:
            return {"sequences": ["." * len(seq) for seq in sequences]}
    except Exception as e:
        print(e)
        time.sleep(0.1)
        return batch_query_structure(sequences)


def predict_structure(sequence):
    """使用RNA库预测RNA结构"""
    ss, mfe = RNA.fold(sequence)
    return ss


# def parallel_predict_structures(sequences, num_processes=24):
#     """并行计算多个序列的RNA结构"""
#     sequences1 = sequences[len(sequences) // 10:]
#     with Pool(num_processes) as pool:
#         results = pool.map(predict_structure, sequences1)
#     sequences2 = sequences[: len(sequences) // 10]
#     results += batch_query_structure(sequences2)['sequences']
#     return results


def parallel_predict_structures(sequences):
    """并行计算多个序列的RNA结构"""
    results = []
    for sequence in sequences:
        results.append(predict_structure(sequence))
    return results


def mutate_with_spans_mask(sequence, mutation_rate=0.2):
    """使用numpy一次性对多个span应用mask突变"""
    sequence = np.array(list(sequence), dtype=np.str_)
    n = len(sequence)
    # span_length = random.randint(1, max(int(len(sequence) // 10 * mutation_rate), 5))
    # num_spans = random.randint(1, int(5 + len(sequence) / 10 * mutation_rate))
    span_length = random.randint(1, len(sequence))
    num_spans = int(len(sequence)//span_length * mutation_rate)
    # 随机选择起始位置，确保不重叠
    start_indices = np.random.choice(n - span_length + 1, num_spans, replace=False)
    masks = [np.arange(span_length//span_length) + start_indices for start_indices in start_indices]
    for mask in masks:
        if random.random() < 0.999999:
            sequence[mask] = "$"
        else:
            sequence[mask] = np.random.choice(list('ACGU'), len(mask))

    return "".join(sequence).replace("$", "<mask>")


# def mutate_with_spans_mask(sequence, mutation_rate=0.2):
#     """使用numpy一次性对多个span应用mask突变"""
#     sequence = np.array(list(sequence), dtype=np.str_)
#     # n = len(sequence)
#     # # span_length = random.randint(1, min(max(10, int(len(sequence) // 10 * mutation_rate)), len(sequence)))
#     # # num_spans = random.randint(1,  min(max(10, int(len(sequence) // 10 * mutation_rate)), len(sequence)))
#     # span_length = random.randint(1, len(sequence))
#     # num_spans = int(len(sequence)//span_length * mutation_rate)
#     # # 随机选择起始位置，确保不重叠
#     # start_indices = np.random.choice(n - span_length + 1, num_spans)
#     # masks = [np.arange(span_length) + start_indices for start_indices in start_indices]
#
#     # 生成一个与sequence相同大小的随机概率矩阵
#     probability_matrix = np.full(sequence.shape, mutation_rate)
#     # 使用伯努利分布生成mask
#     masked_indices = np.random.rand(*sequence.shape) < probability_matrix
#
#     # 将mask应用到sequence上
#     sequence[masked_indices] = "$"
#     mut_seq = "".join(sequence.tolist()).replace("$", "<mask>")
#     return mut_seq


def batch_fm_mutate(sequences, structures, mutation_rate=0.1, mlm_model=None):
    inputs = []
    length = len(structures[0])
    for sequence, structure in zip(sequences, structures):
        sequence = mutate_with_spans_mask(sequence, mutation_rate=mutation_rate)
        inputs.append(f"{sequence}<eos>{structure}" if structure else sequence)
    # outputs = batch_query_sequence(inputs)
    outputs = batch_predict(inputs, mlm_model)
    for i in range(len(sequences)):
        sequence = [
            x if x in "AGCU" else random.choice(["G", "C"])
            for x, y in zip(
                outputs["sequences"][i], sequences[i].replace("<mask>", "M")
            )
        ][:length]
        sequences[i] = "".join(sequence)
    return sequences


def uniform_crossover(parent1, parent2, swap_prob=0.5):
    """均匀交叉：每个位置有swap_prob的概率交换，使用纯numpy操作"""
    # 将字符串转换为NumPy数组
    parent1 = np.array(list(parent1))
    parent2 = np.array(list(parent2))

    # 生成一个随机概率数组
    mask = np.random.rand(len(parent1)) < swap_prob

    # 使用mask来交换parent1和parent2的元素
    temp = np.copy(parent1[mask])
    parent1[mask] = parent2[mask]
    parent2[mask] = temp

    return "".join(parent1), "".join(parent2)


def batch_crossover(population, target_structure, mlm_model=None):
    """单点交叉"""
    crossover_generation = []
    batch_corssover_inputs = []
    population_size = len(population)
    parent1, parent2 = random.choices(population, k=2)  # 选择前50
    for i in range(population_size):
        parent1, parent2 = random.choices(population, k=2)  # 选择前50
        pos = random.randint(1, len(parent1) - 1)
        child1 = parent1[:pos] + "<mask>" * len(parent2[pos:])
        child2 = "<mask>" * len(parent1[:pos]) + parent2[pos:]
        if random.random() < 0.9999:
            batch_corssover_inputs.append(f"{child1}<eos>{target_structure}")
            batch_corssover_inputs.append(f"{child2}<eos>{target_structure}")
        else:
            child1, child2 = uniform_crossover(parent1, parent2)
            # crossover_generation.append(child1)
            # crossover_generation.append(child2)
            batch_corssover_inputs.append(f"{child1}<eos>{target_structure}")
            batch_corssover_inputs.append(f"{child2}<eos>{target_structure}")
    # outputs = batch_query_sequence(batch_corssover_inputs)
    outputs = batch_predict(batch_corssover_inputs, mlm_model)
    for i in range(0, len(outputs["sequences"])):
        sequence = [
            x if x in "AGCU" else random.choice(["G", "C"])
            for x in outputs["sequences"][i][: len(target_structure)]
        ]
        crossover_generation.append("".join(sequence))

    return crossover_generation


def batch_init_population(structure, population_size=100, mlm_model=None):
    """生成随机RNA序列"""
    population = []
    inputs = []
    for i in range(population_size):
        masked_sequence = "".join(
            [
                random.choice(["A", "G", "C", "U", "<mask>"])
                for _ in range(len(structure))
            ]
        )
        inputs.append(f"{masked_sequence}<eos>{''.join(structure)}")
    # outputs = batch_query_sequence(inputs)
    outputs = batch_predict(inputs, mlm_model)
    for i in range(population_size):
        sequence = [
            x if x in "AGCU" else random.choice(["G", "C"])
            for x in outputs["sequences"][i][: len(structure)]
        ]
        population.append("".join(sequence))
    return population


def batch_fitness(sequences, target_structure):
    """计算适应度，适应度是匹配的碱基对数量"""
    fitnesses = []
    results = parallel_predict_structures(sequences)
    for predicted_structure in results:
        # fitnesses.append(1 - sum(1 for a, b in zip(predicted_structure, target_structure) if a == b) / len(target_structure))
        scores = []
        for i in range(len(predicted_structure)):
            if predicted_structure[i] == target_structure[i]:
                scores.append(1)
            elif (
                predicted_structure[i] == ")"
                and target_structure[i] == "("
                or predicted_structure[i] == "("
                and target_structure[i] == ")"
            ):
                scores.append(-3)
            else:
                scores.append(0)
        score = 1 - sum(scores) / len(target_structure)
        fitnesses.append(score)
    return fitnesses


def batch_fitness_with_structures(sequences, target_structure):
    """计算适应度，适应度是匹配的碱基对数量"""
    fitnesses = []
    structures = [] * len(sequences)
    results = parallel_predict_structures(sequences)
    for predicted_structure in results:
        # fitnesses.append(1 - sum(1 for a, b in zip(predicted_structure, target_structure) if a == b) / len(target_structure))
        scores = []
        for i in range(len(predicted_structure)):
            if predicted_structure[i] == target_structure[i]:
                scores.append(1)
            elif (
                predicted_structure[i] == ")"
                and target_structure[i] == "("
                or predicted_structure[i] == "("
                and target_structure[i] == ")"
            ):
                scores.append(-3)
            else:
                scores.append(0)
        score = 1 - sum(scores) / len(target_structure)
        fitnesses.append(score)
        structures.append(predicted_structure)
    return fitnesses, structures


def mfe(sequence):
    """计算最小自由能"""
    return RNA.fold(sequence)[1]


def random_mutate(length):
    """随机突变"""
    return "".join(random.choices("AGCU", k=length))


def genetic_algorithm(
    target_structure, population_size=10000, generations=500, mlm_model=None
):
    if mlm_model is None:
        device = autocuda.auto_cuda()
        mlm_model = get_mlm_model(
            # "../benchmark/genomic_foundation_models/OmniGenome-52M", device
            "../pretrained_models/OmniGenome-52M/OmniGenome-52M", device
        )
        # mlm_model = get_mlm_model("../benchmark/genomic_foundation_models/OmniGenome-186M", device)
        # mlm_model = get_mlm_model(
        #     "../benchmark/genomic_foundation_models/SpliceBERT-510nt", device
        # )

    mutation_rate = 0.2
    min_fitness = 1
    patience = 0
    """遗传算法主函数"""
    # population = [generate_random_sequence(len(target_structure)) for _ in range(population_size)]
    population = batch_init_population(target_structure, population_size, mlm_model)
    population = batch_fm_mutate(
        population,
        [target_structure] * population_size,
        mutation_rate=0.2,
        # mutation_rate=0.9,
        mlm_model=mlm_model,
    )
    for generation in tqdm.tqdm(range(generations)):
        population_fitness = batch_fitness(population, target_structure)[
            :population_size
        ]
        # sorted by fitness
        population = sorted(zip(population, population_fitness), key=lambda x: x[1])[
            :population_size
        ]
        population = [x[0] for x in population]
        next_generation = population[:10]
        # next_generation = []

        next_generation += batch_crossover(population, target_structure, mlm_model)

        next_generation += batch_fm_mutate(
            list(next_generation),
            [target_structure] * len(next_generation),
            mutation_rate=mutation_rate,
            mlm_model=mlm_model,
        )

        fitnesses = batch_fitness(next_generation, target_structure)
        # fitnesses, structures = batch_fitness_with_structures(next_generation, target_structure)
        # sort fitness and population
        next_generation = sorted(zip(next_generation, fitnesses), key=lambda x: x[1])
        if next_generation[0][1] < min_fitness:
            patience = 0
        else:
            patience += 1

        best_sequence, min_fitness = next_generation[0][0], next_generation[0][1]
        print("\n" * 3)
        print(best_sequence)
        print("Best structure:", predict_structure(best_sequence))
        print("True structure:", target_structure)
        print(
            f"Generation {generation + 1}: Best fitness = {min_fitness}, Patience = {patience}"
        )
        if min_fitness == 0:
            print("Best sequence found:", best_sequence)
            del mlm_model
            torch.cuda.empty_cache()
            return best_sequence, target_structure

        population = [x[0] for x in next_generation[:population_size]]

        # if patience >= 10:
        #     population = population[patience:] + batch_init_population(
        #         target_structure, population_size - patience, mlm_model
        #     )

    print("Fail to design:", target_structure)
    del mlm_model
    torch.cuda.empty_cache()
    return "", target_structure


if __name__ == "__main__":
    torch.multiprocessing.set_start_method("spawn")  # good solution !!!!

    structures = []
    sequences = []
    best_sequences = []
    # mlm_model1 = get_mlm_model("../pretrained_models/mprna_small_new", 'cuda:0')
    # mlm_model2 = get_mlm_model("../pretrained_models/mprna_small_new1", 'cuda:1')

    with open("eterna100_vienna2.txt", encoding="utf8", mode="r") as f:
        for line in f.readlines()[1:]:
            parts = line.split("\t")
            structures.append(parts[4].strip())
            sequences.append(parts[5].strip())

    structures = structures[1:]
    outputs = []
    pred_count = 0
    acc_count = 0
    genetic_algorithm(structures[0], 100, 50, None)
    with ProcessPoolExecutor() as executor:
        # with ProcessPoolExecutor(12) as executor:
        for i, target_structure in enumerate(structures):
            time.sleep(1)
            outputs.append(
                executor.submit(
                    genetic_algorithm,
                    target_structure,
                    100,
                    50,
                    None,
                )
            )

        for result in as_completed(outputs):
            pred_count += 1
            best_sequence, target_structure = result.result()
            if best_sequence:
                acc_count += 1
                print("Best sequence found:", best_sequence)
            else:
                best_sequence = "Not Found"
                print("Not Found")
            print(f"Sum: {pred_count} Accuracy:", acc_count / pred_count)
            best_sequences.append(best_sequence)

            with open("eterna100_vienna2.txt.result", encoding="utf8", mode="w") as fw:
                for i, (target_structure, best_sequence) in enumerate(
                    zip(structures, best_sequences)
                ):
                    fw.write(f"{best_sequence}\t{target_structure}\n")

    # params_list = [(structures[i], 1000, 100, model_paths[i % 2]) for i in range(len(structures))]
    #
    # results = []
    # with Pool(cpu_count()) as pool:
    #     for params in params_list:
    #         # 异步提交任务
    #         result = pool.apply_async(genetic_algorithm, (params,))
    #         results.append(result)
    #
    #     # 异步获取结果
    #     best_sequences = []
    #     for result in results:
    #         best_sequence, target_structure = result.get()  # 使用 get() 阻塞等待结果
    #         best_sequences.append(best_sequence)
    #         print("Received:", best_sequence)
    #
    # # 文件写入操作
    # with open("eterna100_vienna2.txt.result", encoding="utf8", mode="w") as fw:
    #     for target_structure, best_sequence in zip(structures, best_sequences):
    #         fw.write(f"{best_sequence}\t{target_structure}\n")

    # while True:
    #     target_structure = input("Please input the target structure: ")
    #     if target_structure == "exit":
    #         break
    #     best_sequence = genetic_algorithm(target_structure)
    #     print("Best sequence found:", best_sequence)
    #     print("Predicted structure:", predict_structure(best_sequence))
