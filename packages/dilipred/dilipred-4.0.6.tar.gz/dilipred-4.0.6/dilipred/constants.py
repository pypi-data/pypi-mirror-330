BANNER = """
██████████   █████ █████       █████ ███████████                         █████
░░███░░░░███ ░░███ ░░███       ░░███ ░░███░░░░░███                       ░░███
 ░███   ░░███ ░███  ░███        ░███  ░███    ░███ ████████   ██████   ███████
 ░███    ░███ ░███  ░███        ░███  ░██████████ ░░███░░███ ███░░███ ███░░███
 ░███    ░███ ░███  ░███        ░███  ░███░░░░░░   ░███ ░░░ ░███████ ░███ ░███
 ░███    ███  ░███  ░███      █ ░███  ░███         ░███     ░███░░░  ░███ ░███
 ██████████   █████ ███████████ █████ █████        █████    ░░██████ ░░████████
░░░░░░░░░░   ░░░░░ ░░░░░░░░░░░ ░░░░░ ░░░░░        ░░░░░      ░░░░░░   ░░░░░░░░

"""

ABSTRACT = """
Drug-induced liver injury (DILI) has been a significant challenge in drug discovery, often leading
to clinical trial failures and necessitating drug withdrawals. The existing suite of in vitro
proxy-DILI assays is generally effective at identifying compounds with hepatotoxicity. However,
there is considerable interest in enhancing the in silico prediction of DILI because it allows for
evaluating large sets of compounds more quickly and cost-effectively, particularly in the early
stages of projects. In this study, we aim to study ML models for DILI prediction that first predict
nine proxy-DILI labels from in vitro (e.g., mitochondrial toxicity, bile salt export pump
inhibition) and in vivo (e.g., preclinical rat hepatotoxicity studies) datasets along with two
pharmacokinetic parameters, structural fingerprints, and physicochemical parameters as features to
predict DILI. The features include in vitro (e.g., mitochondrial toxicity, bile salt export pump
inhibition) data, in vivo (e.g., preclinical rat hepatotoxicity studies) data, pharmacokinetic
parameters of maximum concentration, structural fingerprints, and physicochemical parameters. We
trained DILI-prediction models on 888 compounds from the DILIst data set and tested them on a
held-out external test set of 223 compounds from the DILIst data set. The best model,
DILIPredictor, attained an AUC-PR of 0.79. This model enabled the detection of the top 25 toxic
compounds compared to models using only structural features (2.68 LR+ score). Using feature
interpretation from DILIPredictor, we identified the chemical substructures causing DILI and
differentiated cases of DILI caused by compounds in animals but not in humans. For example,
DILIPredictor correctly recognized 2-butoxyethanol as nontoxic in humans despite its hepatotoxicity
in mice models. Overall, the DILIPredictor model improves the detection of compounds causing DILI
with an improved differentiation between animal and human sensitivity and the potential for
mechanism evaluation.
"""

CITE = """If you use DILIPred in your work, please cite:
Improved Detection of Drug-Induced Liver Injury by Integrating Predicted In Vivo and In Vitro Data
Srijit Seal, Dominic Williams, Layla Hosseini-Gerami, Manas Mahale, Anne E. Carpenter, Ola Spjuth,
and Andreas Bender
doi: https://doi.org/10.1021/acs.chemrestox.4c00015\n"""


DESCS = [
    "PSA",
    "n_rot_bonds",
    "n_rings",
    "n_ar_rings",
    "n_HBA",
    "n_HBD",
    "Fsp3",
    "logP",
    "NHOHCount",
    "NOCount",
    "NumHeteroatoms",
    "n_positive",
    "_n_negative",
    "n_ring_asmbl",
    "n_stereo",
]


LIV_DATA = ["3", "5", "6", "7", "8", "11", "14", "15", "16"]

SOURCE = [
    "Human hepatotoxicity",
    "Animal hepatotoxicity A",
    "Animal hepatotoxicity B",
    "Preclinical hepatotoxicity",
    "Diverse DILI A",
    "Diverse DILI C",
    "BESP",
    "Mitotox",
    "Reactive Metabolite",
]


ASSAY_TYPE = [
    "Human hepatotoxicity",
    "Animal hepatotoxicity",
    "Animal hepatotoxicity",
    "Animal hepatotoxicity",
    "Heterogenous Data ",
    "Heterogenous Data ",
    "Mechanisms of Liver Toxicity",
    "Mechanisms of Liver Toxicity",
    "Mechanisms of Liver Toxicity",
]
