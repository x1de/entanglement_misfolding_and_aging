# statistical_association

Statistical association workflows for testing the relationship between native non-covalent lasso entanglements (NCLEs) and age-associated structural changes in the yeast proteome.

## Primary entry points

Main notebooks are located in `analysis/`.

| Notebook | Required input | Aim |
| --- | --- | --- |
| `1_0_SC_Ent_Protein_level.ipynb` | `statistical_association/data/SC_Ent.pkl` | Test the association between age-associated structural-change proteins and the presence of NCLEs. |
| `1_1_SC_Ent_Residue_level.ipynb` | `statistical_association/data/SC_Ent.pkl` | Test the association between age-associated structural-change residues and entangled regions (within entangled proteins). |
| `2_Association_structural_change_abundance_increase.ipynb` | `statistical_association/data/protein_abundances` | Test the association between age-related structural change and abundance increase with age. |

## Data folder

Primary datasets and preprocessing resources are in `data/`.

| Path | Description |
| --- | --- |
| `data/SC_Ent.pkl` | Integrated dataset used by protein-level and residue-level NCLE association notebooks. |
| `data/protein_abundances/` | Protein abundance data and preprocessing files used for abundance-vs-structural-change association analysis. |

### Provenance of `data/protein_abundances/`

The five pickles in `data/protein_abundances/` are preprocessing products of
the raw LiP-MS and RNA-seq input datasets (see the project README's Data
overview); their fields are documented field by field in
[`data/protein_abundances/README.md`](data/protein_abundances/README.md).
No notebook in this repository generates them, so their
generation is recorded here:

- `Protein_Abundance_control_sample.pkl`: <Authors: which LiP-MS
  search/quantification table it was extracted from, how peptide values were
  aggregated to protein level, and why only proteins detected in both the
  LiP-MS control sample and the RNA-seq experiment are included.>
- `SGD2Uniprot.pkl`: <Authors: source of the SGD-to-UniProt mapping
  (file/release or tool) and how it was built.>
- `Normalization_factor.pkl`: <Authors: how the per-protein mRNA
  fold-change normalization factor was computed from the RNA-seq data.>
- `Normalized_LiP_peptides_significant.pkl`: <Authors: how peptide
  intensities were normalized, how the old/young fold-change and its
  p-value were computed, and the significance rule that selected these
  peptides.>
- `AF_Yeast_entanglement.pkl`: <Authors: which AlphaFold release/model set
  it was built from and how `fragment`, `uniprot_fragment`, `plddt`,
  `whGLN` and `entanglement_AF` were computed.>

Alternatively, add the scripts that produced these files to the repository
and reference them in the list above.
