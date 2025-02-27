import autocuda
import torch
from transformers import AutoConfig

from omnigenome.src.dataset.omnigenome_dataset import (
    OmniGenomeDatasetForTokenRegression,
)
from omnigenome.src.metric.regression_metric import RegressionMetric
from omnigenome.src.misc.utils import seed_everything
from omnigenome.src.model.regression.model import (
    OmniGenomeEncoderModelForTokenRegression,
)
from omnigenome.src.tokenizer.single_nucleotide_tokenizer import (
    OmniSingleNucleotideTokenizer,
)
from omnigenome.src.trainer.trainer import Trainer


class MRNADataset(OmniGenomeDatasetForTokenRegression):
    def __init__(self, data_source, tokenizer, max_length):
        super().__init__(data_source, tokenizer, max_length)

    def prepare_input(self, instance, **kwargs):
        seq, label = instance["text"].split("$LABEL$")
        tokenized_seq = self.tokenizer(
            seq,
            padding="max_length",
            max_length=self.max_length,
            truncation=True,
            return_tensors="pt",
        )
        tokenized_seq["input_ids"] = tokenized_seq["input_ids"].squeeze()
        tokenized_seq["attention_mask"] = tokenized_seq["attention_mask"].squeeze()
        tokenized_seq["labels"] = torch.tensor(float(label), dtype=torch.float32)
        return tokenized_seq


label2id = {"(": 0, ")": 1, ".": 2}

# model_name_or_path = "../tutorials/pretrained_models/MP-RNA-52M-v1"
model_name_or_path = "../tutorials/pretrained_models/mprna_small_new"
# model_name_or_path = "../tutorials/pretrained_models/mprna_base_new"
SN_tokenizer = OmniSingleNucleotideTokenizer.from_pretrained(model_name_or_path)

config = AutoConfig.from_pretrained(
    model_name_or_path, num_labels=1, trust_remote_code=True
)

model = OmniGenomeEncoderModelForTokenRegression(
    config, model_name_or_path, tokenizer=SN_tokenizer, trust_remote_code=True
)

# epochs = 10
epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 8
seeds = [42]
# seeds = [45, 46, 47]

# train_file = "rna_kaggle_mRNA_regression/dataset/train.json"
# test_file = "rna_kaggle_mRNA_regression/dataset/test.json"
# train_set = MRNADataset(data_source=train_file, tokenizer=SN_tokenizer, max_length=512, )
# test_set = MRNADataset(data_source=test_file, tokenizer=SN_tokenizer, max_length=512, )
# train_set, valid_set = train_test_split(train_set, test_size=0.1, random_state=42, shuffle=True)

train_file = "TE_Regression/train.txt"
test_file = "TE_Regression/test.txt"
valid_file = "TE_Regression/valid.txt"
train_set = MRNADataset(
    data_source=train_file,
    tokenizer=SN_tokenizer,
    max_length=512,
)
test_set = MRNADataset(
    data_source=test_file,
    tokenizer=SN_tokenizer,
    max_length=512,
)
valid_set = MRNADataset(
    data_source=valid_file,
    tokenizer=SN_tokenizer,
    max_length=512,
)

train_loader = torch.utils.data.DataLoader(
    train_set, batch_size=batch_size, shuffle=True
)
valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

# compute_metrics = ClassificationMetric(ignore_y=-100, average="macro").f1_score
compute_metrics = RegressionMetric(ignore_y=-100).mean_squared_error

for seed in seeds:
    seed_everything(seed)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=learning_rate, weight_decay=weight_decay
    )
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        eval_loader=valid_loader,
        test_loader=test_loader,
        batch_size=batch_size,
        epochs=epochs,
        optimizer=optimizer,
        compute_metrics=compute_metrics,
        device=autocuda.auto_cuda(),
    )

    metrics = trainer.train()
    metrics.summary()
