# Data dictionary — `statistical_association/data/`

Every dataset here is stored as a pandas pickle (`.pkl`, read with
`pd.read_pickle`) and gets an open-format CSV copy next to it, written by
`export_open_copies.py` (run that script once and commit the generated
`.csv` files; re-run it whenever a `.pkl` changes). The `.pkl` files are
what the notebooks read; the `.csv` copies are for reuse outside Python.

The `protein_abundances/` pickles are documented field by field in
[`protein_abundances/README.md`](protein_abundances/README.md).

## `SC_Ent.pkl`

One row per protein; `Uniprot` holds the protein's UniProt accession.
Read by `notebook/1_0_SC_Ent_Protein_level.ipynb` (protein-level analysis)
and `notebook/1_1_SC_Ent_Residue_level.ipynb` (residue-level analysis).

| Field | Type | Units / values | Meaning |
| --- | --- | --- | --- |
| `SC` | int | 0 or 1 | 1 = protein shows an age-associated structural change (significant LiP-MS peptide fold-change between old and young samples; notebook 2 derives its SC protein set the same way from `protein_abundances/Normalized_LiP_peptides_significant.pkl`), 0 = no structural change. <Authors: confirm the exact rule/threshold used when building the file.> |
| `entangled` | int | 0 or 1 | 1 = protein contains a native lasso entanglement (NCLE, from the entanglement dataset cited in the project README's Data overview), 0 = none. |
| `length_AF` | int | residues | Length of the protein's AlphaFold model; the notebooks use it as the length confounder (z-scored into `length_z`). |
| `Uniprot` | str | UniProt accession | UniProt accession of the protein; residue-level IDs are built as `{Uniprot}_{residue number}`. |
| `clustered_entangled_residues` | list of int | residue numbers | Residue numbers (1-based, within 1..`length_AF`) forming the protein's clustered entangled region(s). |
| `Cutsite_residues` | list of int | residue numbers | Residue numbers (1-based) identified as proteolytic cut sites; at residue level they define the structural-change indicator `is_cutsite`. |
| `sasa_per_residue` | list of float | Å² per residue <Authors: confirm unit> | Solvent-accessible surface area per residue, 0-indexed (`sasa_per_residue[i-1]` is residue `i`); currently unused by the notebooks (commented out in notebook 1_1). |

<Authors: confirm the definitions above against the preprocessing that built
the file, and state which tool/pipeline produced `clustered_entangled_residues`,
`Cutsite_residues` and `sasa_per_residue`.>
