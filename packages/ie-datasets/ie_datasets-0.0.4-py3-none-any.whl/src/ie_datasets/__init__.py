from ie_datasets.datasets import (
    biored as BioRED,
    chemprot as ChemProt,
    crossre as CrossRE,
    cuad as CUAD,
    docred as DocRED,
    hyperred as HyperRED,
    knowledgenet as KnowledgeNet,
    re_docred as ReDocRED,
    scierc as SciERC,
    somesci as SoMeSci,
    wikievents as WikiEvents,
)
from ie_datasets.datasets.tplinker import (
    nyt as TPLinkerNYT,
    webnlg as TPLinkerWebNLG,
)


__all__ = [
    "BioRED",
    "ChemProt",
    "CrossRE",
    "CUAD",
    "DocRED",
    "HyperRED",
    "KnowledgeNet",
    "ReDocRED",
    "SciERC",
    "SoMeSci",
    "TPLinkerNYT",
    "TPLinkerWebNLG",
    "WikiEvents",
]
