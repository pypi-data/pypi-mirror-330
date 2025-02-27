import autocuda
import torch
from metric_visualizer import MetricVisualizer
from transformers import AutoConfig, AutoTokenizer

from omnigenome import OmniGenomeDatasetForSequenceRegression
from omnigenome import OmniSingleNucleotideTokenizer, OmniKmersTokenizer
from omnigenome import (
    RegressionMetric,
    OmniGenomeModelForSequenceRegression,
)
from omnigenome import Trainer

label2id = {"0": 0, "1": 1}


class TERegressionDataset(OmniGenomeDatasetForSequenceRegression):
    def __init__(self, data_source, tokenizer, max_length):
        super().__init__(data_source, tokenizer, max_length)

    def prepare_input(self, instance, **kwargs):
        sequence, labels = instance["sequence"].split("$LABEL$")
        sequence = sequence.strip().replace("T", "U")
        tokenized_inputs = self.tokenizer(
            sequence,
            padding="do_not_pad",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
            **kwargs
        )
        for col in tokenized_inputs:
            tokenized_inputs[col] = tokenized_inputs[col].squeeze()

        if labels is not None:
            tokenized_inputs["labels"] = float(labels)
            tokenized_inputs["labels"] = torch.tensor(tokenized_inputs["labels"])
        return tokenized_inputs


epochs = 10
# epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 8
# seeds = [42]
seeds = [45, 46, 47, 48, 49]

compute_metrics = [
    RegressionMetric(ignore_y=-100).mean_squared_error,
]

mv = MetricVisualizer("Rice")

for gfm in [
    # "multimolecule/rnamsm",
    # "multimolecule/rnafm",
    "multimolecule/rnabert",
    # "yangheng/plantrna-fm",
    # "../tutorials/pretrained_models/nucleotide-transformer-v2-50m-multi-species",
    # "../tutorials/pretrained_models/esm2_t12_35M_UR50D",
    # "../tutorials/pretrained_models/esm2_rna_35M",
    # "../tutorials/pretrained_models/esm2_rna_35M_ss",
    # "../tutorials/pretrained_models/splicebert/SpliceBERT-510nt",
    # "../tutorials/pretrained_models/cdsBERT",
    # "../tutorials/pretrained_models/3utrbert",
    # "../tutorials/pretrained_models/hyenadna-large-1m-seqlen-hf",
    # "../tutorials/pretrained_models/DNABERT-2-117M",
]:
    for seed in seeds:
        # train_file = "RNA-TE-Prediction/Rice/train.txt"
        # test_file = "RNA-TE-Prediction/Rice/test.txt"
        # valid_file = "RNA-TE-Prediction/Rice/valid.txt"
        train_file = "TE_Classification/Arabidobsis/train.txt"
        test_file = "TE_Classification/Arabidobsis/test.txt"
        valid_file = "TE_Classification/Arabidobsis/valid.txt"
        if 'multimolecule' in gfm:
            from multimolecule import RnaTokenizer, AutoModelForTokenPrediction

            tokenizer = RnaTokenizer.from_pretrained(gfm)
            gfm = AutoModelForTokenPrediction.from_pretrained(gfm, trust_remote_code=True).base_model
        else:
            tokenizer =AutoTokenizer.from_pretrained(gfm, trust_remote_code=True)

        train_set = TERegressionDataset(
            data_source=train_file,
            tokenizer=tokenizer,
            max_length=440,
        )
        test_set = TERegressionDataset(
            data_source=test_file,
            tokenizer=tokenizer,
            max_length=440,
        )
        valid_set = TERegressionDataset(
            data_source=valid_file,
            tokenizer=tokenizer,
            max_length=440,
        )
        train_loader = torch.utils.data.DataLoader(
            train_set, batch_size=batch_size, shuffle=True
        )
        valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

        ssp_model = OmniGenomeModelForSequenceRegression(
            gfm,
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
            seeds=seed,
            device=autocuda.auto_cuda(),
        )

        metrics = trainer.train()
        mv.log(
            gfm.split("/")[-1],
            "mean_squared_error",
            metrics["test_metrics"]["mean_squared_error"],
        )
        # model.save("OmniGenome-185M", overwrite=True)
        print(metrics)
        mv.summary()
