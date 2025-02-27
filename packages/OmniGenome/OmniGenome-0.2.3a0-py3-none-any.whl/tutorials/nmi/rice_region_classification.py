import autocuda
import torch
from metric_visualizer import MetricVisualizer
from transformers import AutoConfig, AutoTokenizer

from omnigenome import ClassificationMetric, OmniGenomeTokenizer
from omnigenome import (
    OmniGenomeDatasetForTokenClassification,
    OmniBPETokenizer,
)
from omnigenome import (
    OmniGenomeModelForTokenClassification,
)
from omnigenome import OmniSingleNucleotideTokenizer, OmniKmersTokenizer
from omnigenome import Trainer


class RegionClassificationDataset(OmniGenomeDatasetForTokenClassification):
    def __init__(self, data_source, tokenizer, max_length, **kwargs):
        super().__init__(data_source, tokenizer, max_length, **kwargs)

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
            tokenized_inputs["labels"] = torch.tensor(
                [-100] + labels[: self.max_length - 2] + [-100]
            )
        return tokenized_inputs


label2id = {"5utr": 0, "cds": 1, "3utr": 2}


epochs = 10
# epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 4
# seeds = [42]
seeds = [45, 46, 47, 48, 49]

compute_metrics = ClassificationMetric(ignore_y=-100, average="macro").f1_score

mv = MetricVisualizer("region")

for gfm in [
    # "multimolecule/rnamsm",
    # "multimolecule/rnafm",
    "multimolecule/rnabert",
    "yangheng/plantrna-fm",
    "../tutorials/pretrained_models/nucleotide-transformer-v2-50m-multi-species",
    "../tutorials/pretrained_models/esm2_t12_35M_UR50D",
    # "../tutorials/pretrained_models/esm2_rna_35M",
    # "../tutorials/pretrained_models/esm2_rna_35M_ss",
    # "../tutorials/pretrained_models/splicebert/SpliceBERT-510nt",
    # "../tutorials/pretrained_models/cdsBERT",
    # "../tutorials/pretrained_models/3utrbert",
    # "../tutorials/pretrained_models/hyenadna-large-1m-seqlen-hf",
    "../tutorials/pretrained_models/DNABERT-2-117M",
]:
    for seed in seeds:
        # train_file = "RNA-Region-Classification/Rice/train.json"
        # test_file = "RNA-Region-Classification/Rice/test.json"
        # valid_file = "RNA-Region-Classification/Rice/valid.json"
        train_file = "RNA_Region_Classification/Arabidobsis/train.json"
        test_file = "RNA_Region_Classification/Arabidobsis/test.json"
        valid_file = "RNA_Region_Classification/Arabidobsis/valid.json"
        if 'multimolecule' in gfm:
            from multimolecule import RnaTokenizer, AutoModelForTokenPrediction

            tokenizer = RnaTokenizer.from_pretrained(gfm)
            model = AutoModelForTokenPrediction.from_pretrained(gfm, trust_remote_code=True).base_model
        else:
            model = gfm
            tokenizer =AutoTokenizer.from_pretrained(gfm, trust_remote_code=True)

        train_set = RegionClassificationDataset(
            data_source=train_file,
            tokenizer=tokenizer,
            max_length=440,
            max_examples=8000,
        )
        test_set = RegionClassificationDataset(
            data_source=test_file,
            tokenizer=tokenizer,
            max_length=440,
            max_examples=1000,
        )
        valid_set = RegionClassificationDataset(
            data_source=valid_file,
            tokenizer=tokenizer,
            max_length=440,
            max_examples=1000,
        )
        train_loader = torch.utils.data.DataLoader(
            train_set, batch_size=batch_size, shuffle=True
        )
        valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

        ssp_model = OmniGenomeModelForTokenClassification(
            model,
            tokenizer=tokenizer,
            label2id=label2id,
            trust_remote_code=True,
        )

        ssp_model.to(autocuda.auto_cuda())

        optimizer = torch.optim.AdamW(
            ssp_model.parameters(), lr=learning_rate, weight_decay=weight_decay
        )
        trainer = Trainer(
            model=ssp_model,
            train_loader=train_loader,
            eval_loader=valid_loader,
            test_loader=test_loader,
            batch_size=batch_size,
            epochs=epochs,
            optimizer=optimizer,
            compute_metrics=compute_metrics,
            seeds=seeds,
        )

        metrics = trainer.train()
        mv.log(gfm.split("/")[-1]+"Arabidopsis", "F1", metrics["test"][-1]["f1_score"])
        # model.save("OmniGenome-185M", overwrite=True)
        print(metrics)
        mv.summary()
