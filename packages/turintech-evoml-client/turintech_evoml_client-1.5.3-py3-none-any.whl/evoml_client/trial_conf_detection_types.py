from enum import Enum
from typing import Union


class NamedOption:
    name: str
    slug: str

    def __init__(self, name: str, slug: str = None):
        self.name = name
        self.slug = slug


class AutoEncoder(Enum):
    AUTO = NamedOption("auto", "auto")


class CategoricalEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    ONE_HOT_ENCODER = NamedOption("One Hot Encoder", "one-hot-encoder")
    LABEL_ENCODER = NamedOption("Label Encoder", "label-encoder")
    HASH_ENCODER = NamedOption("Hash Encoder", "hash-encoder")
    HELMERT_ENCODER = NamedOption("Helmert Encoder", "helmert-encoder")
    TARGET_ENCODER = NamedOption("Target Encoder", "target-encoder")
    CAT_BOOST_ENCODER = NamedOption("Cat Boost Encoder", "cat-boost-encoder")
    BACKWARD_DIFFERENCE_ENCODER = NamedOption("Backward Difference Encoder", "backward-difference-encoder")
    ORDINAL_ENCODER = NamedOption("Ordinal Encoder", "ordinal-encoder")


class BinaryEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    LABEL_ENCODER = NamedOption("Label Encoder", "label-encoder")


class BasicFloatEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    LOG_ENCODER = NamedOption("Log Encoder", "log-encoder")
    POWER_ENCODER = NamedOption("Power Encoder", "power-encoder")
    SQUARE_ENCODER = NamedOption("Square Encoder", "square-encoder")
    QUANTILE_TRANSFORM_ENCODER = NamedOption("Quantile Transform Encoder", "quantile-transform-encoder")
    RECIPROCAL_ENCODER = NamedOption("Reciprocal Encoder", "reciprocal-encoder")
    DIFFERENCE_TRANSFORM = NamedOption("Difference transform", "difference-transform")
    RATIO_TRANSFORM = NamedOption("Ratio transform", "ratio-transform")
    LOG_RATIO_TRANSFORM = NamedOption("Log-Ratio transform", "log-ratio-transform")


class BasicIntegerEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    LOG_ENCODER = NamedOption("Log Encoder", "log-encoder")
    POWER_ENCODER = NamedOption("Power Encoder", "power-encoder")
    DIFFERENCE_TRANSFORM = NamedOption("Difference transform", "difference-transform")
    RATIO_TRANSFORM = NamedOption("Ratio transform", "ratio-transform")
    LOG_RATIO_TRANSFORM = NamedOption("Log-Ratio transform", "log-ratio-transform")


class CurrencyEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    LOG_ENCODER = NamedOption("Log Encoder", "log-encoder")
    POWER_ENCODER = NamedOption("Power Encoder", "power-encoder")
    DIFFERENCE_TRANSFORM = NamedOption("Difference transform", "difference-transform")
    RATIO_TRANSFORM = NamedOption("Ratio transform", "ratio-transform")
    LOG_RATIO_TRANSFORM = NamedOption("Log-Ratio transform", "log-ratio-transform")


class FractionEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    LOG_ENCODER = NamedOption("Log Encoder", "log-encoder")
    POWER_ENCODER = NamedOption("Power Encoder", "power-encoder")
    DIFFERENCE_TRANSFORM = NamedOption("Difference transform", "difference-transform")
    RATIO_TRANSFORM = NamedOption("Ratio transform", "ratio-transform")
    LOG_RATIO_TRANSFORM = NamedOption("Log-Ratio transform", "log-ratio-transform")


class PercentageEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    LOG_ENCODE = NamedOption("Log Encoder", "log-encoder")
    POWER_ENCODER = NamedOption("Power Encoder", "power-encoder")
    DIFFERENCE_TRANSFORM = NamedOption("Difference transform", "difference-transform")
    RATIO_TRANSFORM = NamedOption("Ratio transform", "ratio-transform")
    LOG_RATIO_TRANSFORM = NamedOption("Log-Ratio transform", "log-ratio-transform")


class UnitNumberEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    LOG_ENCODER = NamedOption("Log Encoder", "log-encoder")
    POWER_ENCODER = NamedOption("Power Encoder", "power-encoder")
    DIFFERENCE_TRANSFORM = NamedOption("Difference transform", "difference-transform")
    RATIO_TRANSFORM = NamedOption("Ratio transform", "ratio-transform")
    LOG_RATIO_TRANSFORM = NamedOption("Log-Ratio transform", "log-ratio-transform")


class TextEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    TFIDF = NamedOption("tfidf", "tfidf")
    ALL_MPNET_BASE_V2 = NamedOption("sentence-transformers/all-mpnet-base-v2", "all-mpnet-base-v2")
    ALL_DISTILROBERTA_V1 = NamedOption("sentence-transformers/all-distilroberta-v1", "all-distilroberta-v1")
    ALL_MINILM_L6_V2 = NamedOption("sentence-transformers/all-MiniLM-L6-v2", "all-MiniLM-L6-v2")
    ALL_MINILM_L12_V2 = NamedOption("sentence-transformers/all-MiniLM-L12-v2", "all-MiniLM-L12-v2")
    BERT_BASE_UNCASED = NamedOption("bert-base-uncased", "bert-base-uncased")
    GPT2 = NamedOption("gpt2", "gpt2")
    DISTILBERT_BASE_UNCASED = NamedOption("distilbert-base-uncased", "distilbert-base-uncased")
    ROBERTA_BASE = NamedOption("roberta-base", "roberta-base")
    ALBERT_BASE_V2 = NamedOption("albert-base-v2", "albert-base-v2")
    XLNET_BASE_CASED = NamedOption("xlnet-base-cased", "xlnet-base-cased")
    ELECTRA_BASE_DISCRIMINATOR = NamedOption("google/electra-base-discriminator", "electra-base-discriminator")
    CODEBERT_BASE = NamedOption("microsoft/codebert-base", "codebert-base")


class ProteinSequenceEncoders(Enum):
    AUTO = NamedOption("auto", "auto")
    PROT_BERT = NamedOption("Rostlab/prot-bert", "prot-bert")
    PROT_BERT_BFD = NamedOption("Rostlab/prot-bert-bfd", "prot-bert-bfd")
    PROT_ELECTRA_DISCRIMINATOR_BFD = NamedOption(
        "Rostlab/prot-electra-discriminator-bfd", "prot-electra-discriminator-bfd"
    )


EncoderType = Union[
    CategoricalEncoders,
    BinaryEncoders,
    BasicFloatEncoders,
    BasicIntegerEncoders,
    CurrencyEncoders,
    FractionEncoders,
    PercentageEncoders,
    UnitNumberEncoders,
    TextEncoders,
    ProteinSequenceEncoders,
]


class Scaler(Enum):
    AUTO = NamedOption("auto", "auto")
    MIN_MAX_SCALER = NamedOption("Min Max Scaler", "min-max-scaler")
    STANDARD_SCALER = NamedOption("Standard Scaler", "standard-scaler")
    MAX_ABS_SCALER = NamedOption("Max Abs Scaler", "max-abs-scaler")
    ROBUST_SCALER = NamedOption("Robust Scaler", "robust-scaler")
    GAUSS_RANK_SCALER = NamedOption("Gauss Rank Scaler", "gauss-rank-scaler")
