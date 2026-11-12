# Native entanglement misfolding contributes to age-associated structural changes across the *Saccharomyces cerevisiae* proteome

This repository evaluates the association between native non-covalent lasso entanglements (NCLEs) and age-associated structural changes in the yeast proteome. It includes:

- Statistical association workflows (protein-level, residue-level, and association with abundance increase)
- Coarse-grained (CG) folding and misfolding simulation workflows
- Figure-generation notebooks
- A reproducible software environment (`bioenv.yml`)

## Design choices

This project does not use a formal workflow manager (for example, Snakemake or Nextflow) because:

- The analysis flow is linear.
- Major analysis steps are deterministic and notebook-based.
- The dataset is fixed and relatively small.
- Transparency and interactivity are priorities.

Given this scope, notebook-based orchestration was chosen for readability and accessibility.

## Primary entry points


| Workflow                | Location                   | Purpose                                                                                                                                      |
| ----------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Statistical association | `statistical_association/` | Main notebooks for NCLE vs. structural-change association (odds ratios and residue-level analyses). See `statistical_association/README.md`. |
| CG simulations          | `cg_sims/`                 | Temperature-quenching workflows at 300 K, MSM analyses, and visualization. See `cg_sims/README.md`.                                          |


## Project layout

- `statistical_association/`: Association analyses, datasets, and notebooks
- `cg_sims/`: CG simulation inputs, scripts, and analysis workflows
- `bioenv.yml`: Conda environment specification

## Data overview

This project uses two primary input datasets for the association analyses.

### Input data


| Data              | Original source                                                                                   |
| ------------------|------------------------------------------------------------------------------------------------- |
| LiP-MS data       | [Molecular Cell dataset](https://linkinghub.elsevier.com/retrieve/pii/S1097276523006512)          |
| Entanglement data |  [JMB dataset](https://www.sciencedirect.com/science/article/abs/pii/S0022283624000251?via%3Dihub) |


### Processed data (used in notebooks)

The above inputs are integrated into single pickle file datasets: `statistical_association/data/SC_Ent.pkl`

`SC_Ent.pkl` is a derived dataset: it was generated from the two raw input
datasets above by <Authors: describe the integration — which raw tables/files
from the LiP-MS and entanglement sources were used; what filtering,
normalization and significance thresholds were applied; how the two sources
were matched (join key); how `SC`, `entangled`, `length_AF`,
`clustered_entangled_residues`, `Cutsite_residues` and `sasa_per_residue`
were computed. If a script or notebook performed the integration, add it to
the repository and reference it here instead of the description.>

### Terms and constraints on upstream data and third-party components

The repository includes processed files derived from the upstream datasets (`statistical_association/data/SC_Ent.pkl` and `statistical_association/data/protein_abundances/`), and use and redistribution of these files, and of results derived from them, are subject to the terms of the upstream data each derives from:

- `statistical_association/data/SC_Ent.pkl` was generated from both the LiP-MS and the entanglement datasets, so <Authors: state the terms that apply to it — the combined terms of those two datasets as stated in the two bullets below, normally the more restrictive of the two; if both datasets state no restrictions beyond citing the original publications, write that>.
- `statistical_association/data/protein_abundances/` holds files derived from the LiP-MS dataset (`Protein_Abundance_control_sample.pkl`, `Normalized_LiP_peptides_significant.pkl`), the entanglement dataset (`AF_Yeast_entanglement.pkl`), RNA-seq data (`Normalization_factor.pkl`) and the SGD/UniProt reference mapping (`SGD2Uniprot.pkl`) — see `statistical_association/data/protein_abundances/README.md` for the file-by-file provenance — so <Authors: state the terms that apply to each of these files, following the two bullets below for the LiP-MS and entanglement data and stating the terms of the RNA-seq and SGD/UniProt sources for the other files; where a source states no restrictions beyond citing the original publication, write that>.

- **LiP-MS data** ([Molecular Cell dataset](https://linkinghub.elsevier.com/retrieve/pii/S1097276523006512)): <Authors: replace this placeholder with the terms of use as written in that publication's data availability statement and in the deposition record where the dataset is archived — the license the deposited data carry (e.g. a Creative Commons license, if that is what it states), or "no restrictions beyond citing the original publication", whichever the source actually states. State what is written, not an example; delete this instruction once filled.>
- **Entanglement data** ([JMB dataset](https://www.sciencedirect.com/science/article/abs/pii/S0022283624000251?via%3Dihub)): <Authors: replace this placeholder with the terms of use as written in that publication's data availability statement and in the deposition record where the dataset is archived — the license the deposited data carry (e.g. a Creative Commons license, if that is what it states), or "no restrictions beyond citing the original publication", whichever the source actually states. State what is written, not an example; delete this instruction once filled.>

Third-party software: all code in this repository was written for this project; no third-party code is vendored in. Dependencies are installed from `bioenv.yml` and are distributed under ordinary open-source licenses; none is academic-only, non-commercial, or registration-required, so no restrictions beyond their license terms apply to their use or redistribution.



## Installation

### Prerequisites

- [Conda/Miniconda](https://docs.conda.io/en/latest/miniconda.html)

All required packages are listed in `bioenv.yml`.

### Setup

1. Clone this repository and enter the project directory.
2. Create and activate the environment:

```bash
conda env create -f bioenv.yml
conda activate bioenv
```

## Reproducing results

### Statistical association

Notebook location: `statistical_association/notebook/`

Run the following notebooks:


| Notebook                                                   | Required input                                    |
| ---------------------------------------------------------- | ------------------------------------------------- |
| `1_0_SC_Ent_Protein_level.ipynb`                           | `statistical_association/data/SC_Ent.pkl`         |
| `1_1_SC_Ent_Residue_level.ipynb`                           | `statistical_association/data/SC_Ent.pkl`         |
| `2_Association_structural_change_abundance_increase.ipynb` | `statistical_association/data/protein_abundances` |


### CG simulations

Workflow location: `cg_sims/`

- Temperature quenching at 300 K: follow the workflow in `cg_sims/README.md`.

### Figures and tables

Main figures and Tables (results) are generated using following notebooks:

| Source                   | Notebook                                                                   | Output location                        |
| ------------------------ | -------------------------------------------------------------------------- | -------------------------------------- |
| Statistical association  | `1_0_Plot_Odd_at_protein_level.ipynb`, `1_1_Plot_Odd_at_residue_level.ipynb` | `statistical_association/notebook/`    |
| CG misfolding propensity | `Plot_misfolding_propensity_Nature_style.ipynb`                            | `cg_sims/plot_misfolding_probability/` |


## Computational requirements


| Component                                   | Storage                     | CPUs                                        | RAM   | GPUs     | Runtime                                                                                         |
| ------------------------------------------- | --------------------------- | ------------------------------------------- | ----- | -------- | ----------------------------------------------------------------------------------------------- |
| Statistical association (Jupyter notebooks) | Minimal                     | 1 core                                      | 8 GB  | None     | Negligible                                                                                      |
| CG simulations                              | Depends on trajectory count | 1 core (CPU-only) or 1 CPU + 1 GPU (faster) | 8 GB+ | Optional | ~3 h for short proteins (~100 residues, 1.5 us) to ~1 day for long proteins (~800 residues) |


Statistical association analyses run on modest hardware (for example, a laptop with 8 GB RAM and 1 CPU core). CG simulations can run on CPU only and benefit from optional GPU acceleration.

## Authors

Quyen V. Vu<sup>1</sup>, Ian Sitarik<sup>2,3</sup>, Daniel A. Nissley<sup>2,3</sup>, and Edward P. O'Brien<sup>1,2,3,4</sup>*

1. Department of Chemistry, Pennsylvania State University, University Park, PA, USA
2. National Science Foundation - National Synthesis Center for the Emergence in the Molecular and Cellular Sciences, Pennsylvania State University, University Park, PA, USA
3. Institute for Computational and Data Sciences, Pennsylvania State University, University Park, PA, USA
4. Bioinformatics and Genomics Graduate Program, The Huck Institutes of the Life Sciences, Pennsylvania State University, University Park, PA, USA

*Scientific correspondence: [epo2@psu.edu](mailto:epo2@psu.edu)*

*Maintainer (code/data): [qzv5006@psu.edu](mailto:qzv5006@psu.edu) or [vuqv.phys@gmail.com*](mailto:vuqv.phys@gmail.com)

## Troubleshooting and known issues

When re-running the notebooks you may see two non-routine warnings; here is what each means and how it affects the results:

- `statistical_association/notebook/1_1_SC_Ent_Residue_level.ipynb` stores a pandas `SettingWithCopyWarning` ("A value is trying to be set on a copy of a slice from a DataFrame") when cell 5 adds the `length_z` column to `df`, which cell 4 filtered from the full table with `df = df_all[df_all['entangled']==1]`. The warning means pandas cannot tell whether the assignment modified `df` or a temporary copy. In the stored run the column was created and used (the cells that follow read `length_z` without raising an error), so the stored results are unaffected. When re-running, you can remove the ambiguity and the warning by selecting an explicit copy in cell 4 (`df = df_all[df_all['entangled']==1].copy()`), then re-run and confirm the outputs are unchanged.
- `statistical_association/notebook/2_Association_structural_change_abundance_increase.ipynb` stores a numpy `RuntimeWarning: divide by zero encountered in log2` when cell 14 computes `df['log2FC'] = np.log2(df['FC_norm'])`: proteins whose normalized fold-change `FC_norm` is exactly 0 get `log2FC = -inf`. The association statistics are unaffected — `Abd_up` is classified from `FC_norm > 1` and `Pvalue < 0.01`, and the Fisher exact test and logistic regression in cell 16 use `Abd_up`, not `log2FC` — but the volcano plot in cell 18 plots `log2FC` on a fixed x-range, so those proteins are silently omitted from the figure. List them with `df[np.isinf(df['log2FC'])]` to check which proteins are affected.

Routine messages (deprecation notices, matplotlib font-cache notices, progress output) can be ignored. For problems not listed here, contact the code/data maintainer listed under "Authors" above.

## How to cite

If you use this repository's code or data in your work, please cite the repository using the ready-to-use metadata in [CITATION.cff](CITATION.cff), and cite the original publications of the two upstream datasets (the Molecular Cell LiP-MS dataset and the JMB entanglement dataset, linked under "Data overview" above). A journal reference for the manuscript describing this work will be added here once it is published.

This work was supported by the National Science Foundation (NSF) through the NSF National Synthesis Center for Emergence in the Molecular and Cellular Sciences (NCEMS) under Grant NSF MCB-2335029.

## License

This repository is licensed under the GNU General Public License v3.0 (GPL-3.0); see [LICENSE](LICENSE) for the full license text.

In addition, any reuse or redistribution of this repository or its contents must attribute NCEMS as described in [ATTRIBUTION.md](ATTRIBUTION.md).