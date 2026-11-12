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
| `Accession` | str | accession | Protein accession; join key to `Normalization_factor.pkl` (notebook 2 merges on it). <Authors: state the identifier namespace.> |
| `SGDID` | str | SGD ID | *Saccharomyces cerevisiae* Genome Database locus ID; join key to `SGD2Uniprot.pkl`. |
| `Description` | str | text | Protein description (notebook 2 drops this column before analysis). |
| `Replicate 1`, `Replicate 2`, `Replicate 3` | float | <Authors: state the abundance unit (e.g. raw signal or log-intensity)> | Protein abundance in the three Old sample replicates (renamed `O1`, `O2`, `O3` in notebook 2; "first 3 numbers are Old. last 3 numbers are Young"). |
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
| `NormFactor` | float | fold-change | mRNA fold-change used to normalize the protein abundance fold-change (`FC_norm = FC / NormFactor`; notebook 2 comment "# mRNA fold-change"). <Authors: confirm the direction (old/young) and the RNA-seq source.> |

## `Normalized_LiP_peptides_significant.pkl`

Peptide-level LiP-MS data for peptides that show a significant fold-change
between old and young samples (notebook 2 comment: "LiP-data, peptide exhibit
significant fold-change"). Notebook 2 derives the set of structural-change
proteins from it by joining on `SGDID` and collecting unique `Uniprot` values.

| Field | Type | Units / values | Meaning |
| --- | --- | --- | --- |
| `SGDID` | str | SGD ID | Join key to `SGD2Uniprot.pkl`. |
| <other peptide-level fields> | | | <Authors: document the remaining columns of this file (e.g. peptide sequence, per-replicate values, fold-change, p-value) with units, and the significance rule used to select "significant" peptides.> |

## `AF_Yeast_entanglement.pkl`

AlphaFold-model table used by notebook 2 for `Uniprot` and `length_AF`
("#to get protein length"); the remaining columns are dropped there.

| Field | Type | Units / values | Meaning |
| --- | --- | --- | --- |
| `Uniprot` | str | UniProt accession | UniProt accession of the protein. |
| `length_AF` | int | residues | Length of the AlphaFold model (used as the length confounder `length_z`). |
| `fragment` | | | <Authors: define (fragment identifier).> |
| `uniprot_fragment` | | | <Authors: define (fragment-to-UniProT mapping/residue range).> |
| `plddt` | float | 0–100 | AlphaFold pLDDT predicted-confidence score. <Authors: confirm whether per-residue values or a fragment-level value.> |
| `whGLN` | | | <Authors: define (entanglement measure computed for the fragment).> |
| `entanglement_AF` | | | <Authors: define (entanglement classification/measure from the AlphaFold model).> |
