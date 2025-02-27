"""Entrypoint for CLI"""

import argparse
import datetime
import os
import pickle
import sys
from collections import Counter
import warnings

import numpy as np
import pandas as pd
import shap
from dimorphite_dl.dimorphite_dl import DimorphiteDL
from loguru import logger
from mordred import Calculator, descriptors
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, MolStandardize
from rdkit.Chem.MolStandardize import Standardizer, rdMolStandardize

from dilipred.constants import (
    ABSTRACT,
    ASSAY_TYPE,
    BANNER,
    CITE,
    DESCS,
    LIV_DATA,
    SOURCE,
)


warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

logger.remove()
logger.add(sys.stderr, level="CRITICAL")


def standardized_smiles(smiles):
    standardizer = Standardizer()

    # Read SMILES and convert it to RDKit mol object
    mol = Chem.MolFromSmiles(smiles)

    try:
        smiles_clean_counter = Counter()
        mol_dict = {}
        is_finalize = False

        for _ in range(5):

            # This solved phosphate oxidation in most cases but introduces a problem for some compounds: eg. geldanamycin where the stable strcutre is returned
            inchi_standardised = Chem.MolToInchi(mol)
            mol = Chem.MolFromInchi(inchi_standardised)

            # removeHs, disconnect metal atoms, normalize the molecule, reionize the molecule
            mol = rdMolStandardize.Cleanup(mol)
            # if many fragments, get the "parent" (the actual mol we are interested in)
            mol = rdMolStandardize.FragmentParent(mol)
            # try to neutralize molecule
            uncharger = (
                rdMolStandardize.Uncharger()
            )  # annoying, but necessary as no convenience method exists

            mol = uncharger.uncharge(mol)  # standardize molecules using MolVS and RDKit
            mol = standardizer.charge_parent(mol)
            mol = standardizer.isotope_parent(mol)
            mol = standardizer.stereo_parent(mol)

            # Normalize tautomers
            # Method 1
            normalizer = MolStandardize.tautomer.TautomerCanonicalizer()
            mol = normalizer.canonicalize(mol)

            # Method 2
            te = rdMolStandardize.TautomerEnumerator()  # idem
            mol = te.Canonicalize(mol)

            # Method 3
            mol = standardizer.tautomer_parent(mol)

            # Final Rules
            mol = standardizer.standardize(mol)
            mol_standardized = mol

            # convert mol object back to SMILES
            smiles_standardized = Chem.MolToSmiles(mol_standardized)

            if smiles == smiles_standardized:
                is_finalize = True
                break

            smiles_clean_counter[smiles_standardized] += 1
            if smiles_standardized not in mol_dict:
                mol_dict[smiles_standardized] = mol_standardized

            smiles = smiles_standardized
            mol = Chem.MolFromSmiles(smiles)

        if not is_finalize:
            # If the standardization process is not finalized, we choose the most common SMILES from the counter
            smiles_standardized = smiles_clean_counter.most_common()[0][0]
            # ... and the corresponding mol object
            # mol_standardized = mol_dict[smiles_standardized]

        return smiles_standardized

    except:

        return "Cannot_do"


def protonate_smiles(smiles):

    dimorphite = DimorphiteDL(min_ph=7.0, max_ph=7.0, pka_precision=0)
    protonated_smiles = dimorphite.protonate(smiles)

    # print("protonated_smiles")

    if len(protonated_smiles) > 0:
        protonated_smiles = protonated_smiles[0]

    return protonated_smiles


def smiles_to_inchikey(smiles):

    try:

        # Convert SMILES to a molecule object
        mol = Chem.MolFromSmiles(smiles)
        # Convert the molecule object to an InChI string
        inchi_string = Chem.MolToInchi(mol)
        # Convert the InChI string to an InChIKey
        inchi_key = Chem.inchi.InchiToInchiKey(inchi_string)

        return inchi_key

    except:

        return "Cannot_do"


def MorganFingerprint(s):
    x = Chem.MolFromSmiles(s)
    return AllChem.GetMorganFingerprintAsBitVect(x, 2, 2048)


def MACCSKeysFingerprint(s):
    x = Chem.MolFromSmiles(s)
    return AllChem.GetMACCSKeysFingerprint(x)


def get_num_charged_atoms_neg(mol):
    mol_h = Chem.AddHs(mol)
    Chem.rdPartialCharges.ComputeGasteigerCharges(mol_h)

    positive = 0
    negative = 0

    for atom in mol_h.GetAtoms():
        if float(atom.GetProp("_GasteigerCharge")) <= 0:
            negative += 1

    return negative


def get_num_charged_atoms_pos(mol):
    mol_h = Chem.AddHs(mol)
    Chem.rdPartialCharges.ComputeGasteigerCharges(mol_h)

    positive = 0
    # negative = 0

    for atom in mol_h.GetAtoms():
        if float(atom.GetProp("_GasteigerCharge")) >= 0:
            positive += 1
    return positive


def get_assembled_ring(mol):
    ring_info = mol.GetRingInfo()
    num_ring = ring_info.NumRings()
    ring_atoms = ring_info.AtomRings()
    num_assembled = 0

    for i in range(num_ring):
        for j in range(i + 1, num_ring):
            x = set(ring_atoms[i])
            y = set(ring_atoms[j])
            if not x.intersection(y):  # 2つの環が縮環でない場合に
                for x_id in x:
                    x_atom = mol.GetAtomWithIdx(x_id)
                    neighbors = [k.GetIdx() for k in x_atom.GetNeighbors()]
                    for x_n in neighbors:
                        if x_n in y:  # 環同士を繋ぐ結合があるか否か
                            num_assembled += 1

    return num_assembled


def get_num_stereocenters(mol):
    return AllChem.CalcNumAtomStereoCenters(
        mol
    ) + AllChem.CalcNumUnspecifiedAtomStereoCenters(mol)


def calc_descriptors(dataframe):
    mols = dataframe.smiles_r.apply(Chem.MolFromSmiles)
    # mols_fps=[AllChem.GetMorganFingerprintAsBitVect(x,2) for x in mols]
    descr = []
    for m in mols:
        descr.append(
            [
                Descriptors.TPSA(m),
                Descriptors.NumRotatableBonds(m),
                AllChem.CalcNumRings(m),
                Descriptors.NumAromaticRings(m),
                Descriptors.NumHAcceptors(m),
                Descriptors.NumHDonors(m),
                Descriptors.FractionCSP3(m),
                Descriptors.MolLogP(m),
                Descriptors.NHOHCount(m),
                Descriptors.NOCount(m),
                Descriptors.NumHeteroatoms(m),
                get_num_charged_atoms_pos(m),
                get_num_charged_atoms_neg(m),
                get_assembled_ring(m),
                get_num_stereocenters(m),
            ]
        )
    descr = np.asarray(descr)
    return descr


descs = DESCS


def calc_all_fp_desc(data):

    calc = Calculator(descriptors, ignore_3D=True)
    logger.debug(f"Calculated {len(calc.descriptors)} Descriptors")
    Ser_Mol = data["smiles_r"].apply(Chem.MolFromSmiles)
    # as pandas
    Mordred_table = calc.pandas(Ser_Mol)
    Mordred_table = Mordred_table.astype("float")
    # Mordred_table['smiles_r'] = model_tox_data['smiles_r']

    MACCSfingerprint_array = np.stack(data["smiles_r"].apply(MACCSKeysFingerprint))
    MACCS_collection = []
    for x in np.arange(MACCSfingerprint_array.shape[1]):
        x = "MACCS" + str(x)
        MACCS_collection.append(x)
    MACCSfingerprint_table = pd.DataFrame(
        MACCSfingerprint_array, columns=MACCS_collection
    )

    MorganFingerprint_array = np.stack(data["smiles_r"].apply(MorganFingerprint))
    Morgan_fingerprint_collection = []
    for x in np.arange(MorganFingerprint_array.shape[1]):
        x = "Mfp" + str(x)
        Morgan_fingerprint_collection.append(x)
    Morgan_fingerprint_table = pd.DataFrame(
        MorganFingerprint_array, columns=Morgan_fingerprint_collection
    )

    a = calc_descriptors(data)
    descdf = pd.DataFrame(a, columns=descs)
    descdf_approved = descdf.reset_index(drop=True)

    tox_model_data = pd.concat(
        [
            data,
            Morgan_fingerprint_table,
            MACCSfingerprint_table,
            descdf_approved,
            Mordred_table,
        ],
        axis=1,
    )

    return tox_model_data


liv_data = LIV_DATA


def predict_individual_liv_data(data_dummy, features, endpoint):  # predict animal data
    with open(
        os.path.dirname(os.path.abspath(__file__))
        + f"/models/bestlivmodel_{endpoint}_model.sav",
        "rb",
    ) as f:
        loaded_rf = pickle.load(f)

    X = data_dummy[features]
    X = X.values
    y_proba = loaded_rf.predict_proba(X)[:, 1]

    return y_proba


def predict_individual_cmax_data(data_dummy, features, endpoint):  # predict animal data
    with open(
        os.path.dirname(os.path.abspath(__file__))
        + f"/models/bestlivmodel_{endpoint}_model.sav",
        "rb",
    ) as f:
        regressor = pickle.load(f)

    X = data_dummy[features]
    X = X.values
    # Add predictions to held out test set dili
    y_pred = regressor.predict(X)

    return y_pred


def predict_liv_all(data):
    # Read columns needed for rat data

    with open(
        os.path.dirname(os.path.abspath(__file__))
        + f"/features/features_morgan_mordred_maccs_physc.txt",
        "r",
    ) as file:
        file_lines = file.read()
    features = file_lines.split("\n")
    features = features[:-1]

    data_dummy = data

    for endpoint in liv_data:
        # print(endpoint)
        y_proba = predict_individual_liv_data(data_dummy, features, endpoint)
        data[endpoint] = y_proba

    for endpoint in [
        "median pMolar unbound plasma concentration",
        "median pMolar total plasma concentration",
    ]:
        y_proba = predict_individual_cmax_data(data_dummy, features, endpoint)
        data[endpoint] = y_proba

    return data


def predict_DILI(data):  # log human_VDss_L_kg model

    # Read columns needed for rat data
    with open(
        os.path.dirname(os.path.abspath(__file__))
        + f"/features/features_morgan_mordred_maccs_physc.txt",
        "r",
    ) as file:
        file_lines = file.read()
    features = file_lines.split("\n")
    features = features[:-1]

    features = (
        list(features)
        + [
            "median pMolar unbound plasma concentration",
            "median pMolar total plasma concentration",
        ]
        + list(liv_data)
    )

    with open(
        os.path.dirname(os.path.abspath(__file__)) + "/models/final_dili_model.sav",
        "rb",
    ) as f:
        loaded_rf = pickle.load(f)

    # Note this mode was trained on all data before releasing (not just ncv data)
    X = data[features]
    y_proba = loaded_rf.predict_proba(X)[:, 1]
    best_thresh = 0.612911
    logger.debug("Best Threshold=%f" % (best_thresh))

    y_pred = [1 if y_proba > best_thresh else 0]

    explainer = shap.TreeExplainer(loaded_rf)
    shap_values = explainer.shap_values(X)

    # shap.force_plot(
    #     explainer.expected_value[1], shap_values[1], X.iloc[0], matplotlib=True
    # )

    flat_shaplist = [item for sublist in shap_values[1] for item in sublist]

    interpret = pd.DataFrame()
    interpret["name"] = features
    interpret["SHAP"] = flat_shaplist  # print(flat_shaplist)
    # plt.show()
    # Explaining the 4th instance

    return (interpret, y_proba, y_pred)


class DILIPRedictor:
    def predict(self, smiles):

        desc = pd.read_csv(
            os.path.dirname(os.path.abspath(__file__))
            + "/features/all_features_desc.csv",
            encoding="windows-1252",
        )
        source = SOURCE
        assaytype = ASSAY_TYPE

        info = pd.DataFrame(
            {"name": liv_data, "source": source, "assaytype": assaytype}
        )
        SHAP = pd.DataFrame(
            columns=[
                "name",
                "source",
                "assaytype",
                "SHAP",
                "description",
                "value",
                "pred",
            ]
        )

        # predict
        y_pred = ""
        y_proba = ""
        smiles_r = ""

        smiles_r = standardized_smiles(smiles)
        test = {"smiles_r": [smiles_r]}
        test = pd.DataFrame(test)

        molecule = Chem.MolFromSmiles(smiles_r)

        test_mfp_Mordred = calc_all_fp_desc(test)
        test_mfp_Mordred_liv = predict_liv_all(test_mfp_Mordred)
        test_mfp_Mordred_liv_values = test_mfp_Mordred_liv.T.reset_index().rename(
            columns={"index": "name", 0: "value"}
        )

        interpret, y_proba, y_pred = predict_DILI(test_mfp_Mordred_liv)
        interpret = pd.merge(
            interpret, desc, right_on="name", left_on="name", how="outer"
        )
        interpret = pd.merge(
            interpret,
            test_mfp_Mordred_liv_values,
            right_on="name",
            left_on="name",
            how="inner",
        )

        if y_pred[0] == 1:
            logger.critical("The compound is predicted DILI-Positive")
        if y_pred[0] == 0:
            logger.critical("The compound is predicted DILI-Negative")

        top = interpret[interpret["SHAP"] > 0].sort_values(by=["SHAP"], ascending=False)
        proxy_DILI_SHAP_top = pd.merge(info, top[top["name"].isin(liv_data)])
        proxy_DILI_SHAP_top["pred"] = proxy_DILI_SHAP_top["value"] > 0.50
        proxy_DILI_SHAP_top["SHAP contribution to Toxicity"] = "Positive"
        proxy_DILI_SHAP_top["smiles"] = smiles_r

        top_positives = top[top["value"] == 1]
        top_MACCS = (
            top_positives[top_positives.name.isin(desc.name.to_list()[-166:])]
            .iloc[:1, :]["description"]
            .values[0]
        )
        top_MACCS_value = (
            top_positives[top_positives.name.isin(desc.name.to_list()[-166:])]
            .iloc[:1, :]["value"]
            .values[0]
        )
        top_MACCS_shap = (
            top_positives[top_positives.name.isin(desc.name.to_list()[-166:])]
            .iloc[:1, :]["SHAP"]
            .values[0]
        )
        top_MACCSsubstructure = Chem.MolFromSmarts(top_MACCS)

        bottom = interpret[interpret["SHAP"] < 0].sort_values(
            by=["SHAP"], ascending=True
        )
        proxy_DILI_SHAP_bottom = pd.merge(info, bottom[bottom["name"].isin(liv_data)])
        proxy_DILI_SHAP_bottom["pred"] = proxy_DILI_SHAP_bottom["value"] > 0.50
        proxy_DILI_SHAP_bottom["SHAP contribution to Toxicity"] = "Negative"
        proxy_DILI_SHAP_bottom["smiles"] = smiles_r

        bottom_positives = bottom[bottom["value"] == 1]
        bottom_MACCS = (
            bottom_positives[bottom_positives.name.isin(desc.name.to_list()[-166:])]
            .iloc[:1, :]["description"]
            .values[0]
        )
        bottom_MACCS_value = (
            bottom_positives[bottom_positives.name.isin(desc.name.to_list()[-166:])]
            .iloc[:1, :]["value"]
            .values[0]
        )
        bottom_MACCS_shap = (
            bottom_positives[bottom_positives.name.isin(desc.name.to_list()[-166:])]
            .iloc[:1, :]["SHAP"]
            .values[0]
        )
        bottom_MACCSsubstructure = Chem.MolFromSmarts(bottom_MACCS)

        logger.debug(
            "unbound Cmax: ",
            np.round(
                10
                ** -test_mfp_Mordred_liv["median pMolar unbound plasma concentration"][
                    0
                ]
                * 10**6,
                2,
            ),
            "uM",
        )
        logger.debug(
            "total Cmax: ",
            np.round(
                10
                ** -test_mfp_Mordred_liv["median pMolar total plasma concentration"][0]
                * 10**6,
                2,
            ),
            "uM",
        )

        SHAP = pd.DataFrame(
            columns=[
                "name",
                "source",
                "assaytype",
                "SHAP",
                "description",
                "value",
                "pred",
                "smiles",
            ]
        )
        SHAP = pd.concat([SHAP, proxy_DILI_SHAP_top])
        SHAP = pd.concat([SHAP, proxy_DILI_SHAP_bottom])
        SHAP["name"] = SHAP["name"].astype(str)
        SHAP = SHAP.sort_values(by=["name"], ascending=True)

        preds_DILI = pd.DataFrame(
            {
                "source": ["DILI"],
                "assaytype": ["DILIst_FDA"],
                "description": ["This is the predicted FDA DILIst label"],
                "value": [y_proba[0]],
                "pred": [y_pred[0]],
                "SHAP contribution to Toxicity": ["N/A"],
                "SHAP": ["N/A"],
            }
        )

        SHAP = SHAP[
            [
                "source",
                "assaytype",
                "description",
                "value",
                "pred",
                "SHAP contribution to Toxicity",
                "SHAP",
            ]
        ]
        SHAP = pd.concat([preds_DILI, SHAP]).reset_index(drop=True)
        SHAP["smiles"] = smiles
        SHAP["smiles_r"] = smiles_r
        return SHAP


def main():
    parser = argparse.ArgumentParser(
        description=BANNER + "\n\n" + ABSTRACT + "\n\n" + CITE,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--smiles",
        "-s",
        "-smi",
        "--smi",
        "-smiles",
        type=str,
        help="Input SMILES string to predict properties",
    )
    parser.add_argument(
        "--out",
        "--output",
        "-o",
        "-out",
        "-output",
        type=str,
        help="Save the output as this file name (format is csv)",
        required=True,
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.debug:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    dili_predictor = DILIPRedictor()
    print(BANNER)
    print(CITE)

    result = dili_predictor.predict(args.smiles)

    if args.out:
        filename = args.out if args.out.lower().endswith(".csv") else f"{args.out}.csv"
    else:
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        filename = f"DILIPRedictor_{timestamp}.csv"

    result.to_csv(filename, index=False)
    logger.info(f"Results saved in {filename}")


if __name__ == "__main__":
    main()
