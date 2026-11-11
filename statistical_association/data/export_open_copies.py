"""Write open-format CSV copies of the pickled datasets in data/.

The notebooks read the .pkl files with pd.read_pickle; the .csv copies
written here let others reuse the data outside Python. List-valued fields
(e.g. clustered_entangled_residues, Cutsite_residues, sasa_per_residue in
SC_Ent.pkl) are written as their list text, e.g. [12, 45].

Run once and commit the generated .csv files; re-run whenever a .pkl changes.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

PICKLES = [
    "SC_Ent.pkl",
    "protein_abundances/AF_Yeast_entanglement.pkl",
    "protein_abundances/Normalization_factor.pkl",
    "protein_abundances/Normalized_LiP_peptides_significant.pkl",
    "protein_abundances/Protein_Abundance_control_sample.pkl",
    "protein_abundances/SGD2Uniprot.pkl",
]

for rel in PICKLES:
    src = HERE / rel
    df = pd.read_pickle(src)
    # Keep the index in the CSV only when it carries information
    # (i.e. it is not a plain 0..n-1 range index).
    dst = src.with_suffix(".csv")
    df.to_csv(dst, index=not isinstance(df.index, pd.RangeIndex))
    print(f"wrote {dst}")
