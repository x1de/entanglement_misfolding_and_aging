# Data dictionary — `data/protein_abundances/`

Five pandas pickles used by `notebook/2_Association_structural_change_abundance_increase.ipynb`
("This analysis only consider protein detected in LiPMS on control sample and
RNA sequencing experiments"). Each gets an open-format CSV copy next to it,
written by `../export_open_copies.py` (run that script once and commit the
generated `.csv` files; re-run it whenever a `.pkl` changes).

## `Protein_Abundance_control_sample.pkl`

One row per protein quantified in the LiP-MS control sample.

| Field | Type | Units / values | Meaning |
| --- | --- | --- | --- |
| `Accession` | str | <AUTHORS: identifier namespace (e.g. UniProt, SGD, or the LiP-MS search's protein identifier)> | Protein accession; join key to `Normalization_factor.pkl` (notebook 2 merges on it). |
| `SGDID` | str | SGD ID | *Saccharomyces cerevisiae* Genome Database locus ID; join key to `SGD2Uniprot.pkl`. |
| `Description` | str | text | Protein description (notebook 2 drops this column before analysis). |
| `Replicate 1`, `Replicate 2`, `Replicate 3` | float | <AUTHORS: abundance unit (e.g. raw signal or log-intensity)> | Protein abundance in the three Old sample replicates (renamed `O1`, `O2`, `O3` in notebook 2; "first 3 numbers are Old. last 3 numbers are Young"). |
| `Replicate 1.1`, `Replicate 2.1`, `Replicate 3.1` | float | same unit | Protein abundance in the three Young sample replicates (renamed `Y1`, `Y2`, `Y3`). The `.1` suffix marks the second block of columns that carried the same names as the first block in the source table. |

Notebook 2 computes the abundance fold-change per protein as
`FC = mean(O1..O3) / mean(Y1..Y3)` and its p-value with a Welch t-test.

## `SGD2Uniprot.pkl`

Mapping table, one row per SGD locus: `SGDID` (SGD locus ID) and `Uniprot`
(matching UniProt accession). Notebook 2 joins it on `SGDID`; proteins
without a mapping get a missing `Uniprot`.

## `Normalization_factor.pkl`

Join table on `Accession`:

| Field | Type | Units / values | Meaning |
| --- | --- | --- | --- |
| `Accession` | str | accession | Join key to `Protein_Abundance_control_sample.pkl`. |
| `NormFactor` | float | fold-change <AUTHORS: state the direction (old/young or young/old)> | mRNA fold-change used to normalize the protein abundance fold-change (`FC_norm = FC / NormFactor`; notebook 2 comment "# mRNA fold-change"); computed from <AUTHORS: RNA-seq source/dataset and how the per-protein fold-change was derived>. |

## `Normalized_LiP_peptides_significant.pkl`

Peptide-level LiP-MS data for peptides that show a significant fold-change
between old and young samples (notebook 2 comment: "LiP-data, peptide exhibit
significant fold-change"). Notebook 2 derives the set of structural-change
proteins from it by joining on `SGDID` and collecting unique `Uniprot` values.

| Field | Type | Units / values | Meaning |
| --- | --- | --- | --- |
| `SGDID` | str | SGD ID | Join key to `SGD2Uniprot.pkl`. |
| `<AUTHORS: column name>` | <AUTHORS: type> | <AUTHORS: unit/values> | <AUTHORS: meaning> |

Significance rule: <AUTHORS: state the fold-change threshold and/or p-value cut-off applied when the file was built to select "significant" peptides>.

## `AF_Yeast_entanglement.pkl`

AlphaFold-model table used by notebook 2 for `Uniprot` and `length_AF`
("#to get protein length"); the remaining columns are dropped there.

| Field | Type | Units / values | Meaning |
| --- | --- | --- | --- |
| `Uniprot` | str | UniProt accession | UniProt accession of the protein. |
| `length_AF` | int | residues | Length of the AlphaFold model (used as the length confounder `length_z`). |
| `fragment` | <AUTHORS: type> | <AUTHORS: unit/values> | <AUTHORS: definition of the fragment identifier> |
| `uniprot_fragment` | <AUTHORS: type> | <AUTHORS: unit/values> | <AUTHORS: definition of the fragment-to-UniProt mapping/residue range> |
| `plddt` | float | 0–100 <AUTHORS: confirm whether per-residue values or a fragment-level value> | AlphaFold pLDDT predicted-confidence score. |
| `whGLN` | <AUTHORS: type> | <AUTHORS: unit/values> | <AUTHORS: definition of the entanglement measure computed for the fragment> |
| `entanglement_AF` | <AUTHORS: type> | <AUTHORS: unit/values> | <AUTHORS: definition of the entanglement classification/measure from the AlphaFold model> |
