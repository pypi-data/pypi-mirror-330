# DILIPRedictor

DILI Predictor is an open-source app framework built specifically for human drug-induced liver injury (DILI)

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

Select from the sidebar to predict DILI for a single molecule! For bulk jobs, or local use: use code from Github page: https://github.com/srijitseal/DILI_Predictor

## Installation

### Install using `PyPI`

```sh 
pip install dilipred
```

### Build from source using `python-poetry`

```sh
git clone https://github.com/Manas02/dili-pip.git
cd dili-pip/
poetry install 
```

## Usage

### Running `DILIPredictor` as CLI

#### Help
Simply run `dili` or `dili -h` or `dili --help` to get the helper.
![](https://github.com/Manas02/dili-pip/raw/main/dilipred_help.png?raw=True)

#### Inference given SMILES strings
Output is stored in a directory with the name in the format `DILIPRedictor_dd-mm-yyyy-hh-mm-ss.csv`
Use `-d` or `--debug` to get more info.

![](https://github.com/Manas02/dili-pip/raw/main/dilipred_run.png?raw=True)

### Running `DILIPRedictor` as Library

```py
from dilipred import DILIPRedictor


if __name__ == '__main__':
    dp = DILIPRedictor()
    smiles = "CCCCCCCO"
    result = dp.predict(smiles)
```

## Cite

If you use DILIPred in your work, please cite:
> Improved Detection of Drug-Induced Liver Injury by Integrating Predicted In Vivo and In Vitro Data
> Srijit Seal, Dominic Williams, Layla Hosseini-Gerami, Manas Mahale, Anne E. Carpenter, Ola Spjuth,
> and Andreas Bender
> doi: https://doi.org/10.1021/acs.chemrestox.4c00015
