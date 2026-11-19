# cg_sims

Coarse-grained (CG) simulation scripts, preparation notebooks, and analysis workflows for protein folding and entanglement.

## Data provenance

The per-protein input structures (`<UniProt>_clean.pdb`, one all-atom file
in the `template/setup/` folder of each of the 24 `sc_ent/` and 24
`nsc_nent/` protein folders) come from <AUTHORS: source — e.g.
AlphaFold DB release and retrieval date, or the experimental/PDB entries
used — and list or reference the UniProt accession set>. They were prepared
by <AUTHORS: cleaning/preparation steps — what was removed or
renamed (e.g. hydrogens, missing residues), whether pLDDT scores are kept
in the B-factor column, and which script performed the preparation>. The CG
model files (`*_clean_ca.psf/.cor/.top`,
`*_clean_nscal1_fnn1_go_bt.prm/.xml`) are derived from these structures by
the CG model builder recorded in each `create_model/go_model.log`.



## Primary entry points


| Workflow                                                                      | Location            | Contents                                                                  |
| ----------------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------- |
| CG folding of age-associated structural-change and entangled proteins         | `sc_ent/`           | Setup for proteins in this category                                       |
| CG folding of non-age-associated structural-change and non-entangled proteins | `nsc_nent/`         | Setup for proteins in this category                                       |
| Template scripts                                                              | `scripts/`          | Reusable simulation and analysis job templates                            |
| Template analysis notebooks                                                   | `scripts/analysis/` | MSM analysis, free-energy plots, visualization, representative structures |


## Step-by-step: run CG simulations

### Step 1: `1_copy_sim_set.sh` (prepare trajectory folders)

Copies the `template` directory into 50 trajectory folders (`0` to `49`) and replaces `SETINDEX` in `job.sh`, `control.cntrl`, `job_cg_ext.sh`, and `control_ext.cntrl`.

```bash
./1_copy_sim_set.sh
```

### Step 2: `2_submit_set_of_jobs.sh` (submit MD production jobs)

Submits initial CG MD production jobs (`job.sh`) for all 50 trajectories. Each job runs `single_run.py` with `control.cntrl`.

```bash
./2_submit_set_of_jobs.sh
```

### Step 3: `3_copy_GQ.sh` (prepare GQ entanglement scripts)

Copies GQ job scripts (`job_GQ.sh`, `job_GQ_mgc.sh`, `job_GQ_open.sh`) from `template` into each trajectory folder and replaces `SETINDEX`.

```bash
./3_copy_GQ.sh
```

### Step 4: `4_submit_GQ.sh` (submit entanglement analysis)

Submits GQ analysis jobs to compute entanglement metrics (G, Q) from production trajectories.

Available submission scripts:

- `4_submit_GQ.sh`: standard GQ (`job_GQ.sh`)
- `4_b_submit_GQ_mgc.sh`: MGC variant (`job_GQ_mgc.sh`)
- `4_c_submit_GQ_open.sh`: open variant (`job_GQ_open.sh`)

```bash
./4_submit_GQ.sh
```

### Step 5: `5_check_md_finish.sh` (check MD completion)

Verifies that production trajectories finished correctly by checking for `{i}_prod.dcd` and `fQ.dat`, and by confirming the last value in `fQ.dat` is `100000000`.

```bash
./5_check_md_finish.sh
```

### Step 6: `6_check_GQ.sh` (check GQ output)

Checks that G and Q files exist (`{i}/GQ/G/{i}.G`, `{i}/GQ/Q/{i}.Q`) and have the expected number of lines (default: `20000`).

```bash
./6_check_GQ.sh
```

### Step 7: `7_check_fQ.sh` (inspect `fQ.dat`)

Prints the first two lines and last line of `fQ.dat` for each trajectory for quick inspection of native-contact fraction time series.

```bash
./7_check_fQ.sh
```

### Optional step 8: `8_copy_sim_set_ext.sh` (prepare extended simulation scripts)

Copies extended-simulation files (`job_cg_ext.sh`, `control_ext.cntrl`) into each trajectory folder and replaces `SETINDEX`.

Use this step only if simulations need to run longer than 1.5 microseconds (as defined in `control.cntrl`).

```bash
./8_copy_sim_set_ext.sh
```

### Optional step 9: `9_submit_set_of_jobs_ext.sh` (submit extended MD jobs)

Run this step only if Step 8 is required.

Submits extended CG MD jobs (`job_cg_ext.sh`), where each job runs `single_run.py` with `control_ext.cntrl`.

```bash
./9_submit_set_of_jobs_ext.sh
```

## Summary workflow


| Step         | Script                        | Purpose                                 |
| ------------ | ----------------------------- | --------------------------------------- |
| 1            | `1_copy_sim_set.sh`           | Create trajectory folders from template |
| 2            | `2_submit_set_of_jobs.sh`     | Submit CG MD production jobs            |
| 3            | `3_copy_GQ.sh`                | Copy GQ scripts                         |
| 4            | `4_submit_GQ.sh`              | Submit entanglement (GQ) analysis       |
| 5            | `5_check_md_finish.sh`        | Verify MD completion                    |
| 6            | `6_check_GQ.sh`               | Verify GQ output                        |
| 7            | `7_check_fQ.sh`               | Inspect `fQ.dat`                        |
| 8 (optional) | `8_copy_sim_set_ext.sh`       | Copy extended-simulation scripts        |
| 9 (optional) | `9_submit_set_of_jobs_ext.sh` | Submit extended MD jobs                 |


## Setup data dictionary (`*/template/setup/`)

Every protein folder (24 in `sc_ent/`, 24 in `nsc_nent/`) holds the same set
of setup files in `template/setup/`. `control.cntrl` (read by `single_run.py`)
points at them by name (`psffile`, `prmfile`, `secondary_structure_def`,
`native_cor`, `corfile`), and `job_GQ.sh` passes the psf, cor, secondary
structure ranges and all-atom PDB to `GQ.py` (`-psf`, `-cor`, `-sec`, `--aa`).

| File | Format | Contents |
| --- | --- | --- |
| `<UniProt>_clean.pdb` | PDB (text) | All-atom cleaned input structure (single chain A) from which the CG model is built; the B-factor column carries per-residue pLDDT-like scores. Build record: `create_model/go_model.log`. |
| `<UniProt>_clean_ca.psf` | XPLOR PSF (text) | Coarse-grained Cα model topology produced by the CG model builder (one particle per residue). |
| `<UniProt>_clean_ca.cor` | CHARMM CRD (text) | Cα model coordinates (the native structure used as `native_cor`/reference). |
| `<UniProt>_clean_ca.top` | CHARMM topology (text) | Topology of the CG model. |
| `<UniProt>_clean_nscal1_fnn1_go_bt.prm` | CHARMM parameters (text) | CG force-field parameters (native contacts); the filename records the build settings `nscal=1`, `fnn=1`, `bt` potential. |
| `<UniProt>_clean_nscal1_fnn1_go_bt.xml` | OpenMM XML | OpenMM `ForceField` definition (particles, bonds, angles, Go contact terms); `single_run.py` loads it as `prmfile` (`ForceField(prmfile)`) and creates the simulation `System` from it. |
| `secondary_struc_defs.txt` | whitespace-delimited text, one row per element | Secondary-structure element ranges. Column 1: sequential element number (not used by the parsers). Column 2: first residue of the element (1-based). Column 3: last residue (inclusive). Both `single_run.py` (builds `sec_strc_def` from `words[1]`, `words[2]`) and `GQ.load_secondary_structure_ranges` (takes `parts[1]`, `parts[2]`) read columns 2–3; residues inside these ranges select which native contacts count (toward Q in `single_run.py`, and toward the native contact set of the entanglement analysis in `GQ.py`). |
| `create_model/go_model.cntrl` | text | Control file for the CG model builder: `pdbfile` (input all-atom structure), `casm`, `potential_name` (`bt`), `domain_file` (`domain_def.dat`). |
| `create_model/domain_def.dat` | text | Model-builder domain definitions: `domain = <first>-<last>` gives the residue range of each domain (in the example folder `sc_ent/0_P05744`, residues 1–107, the whole protein); `scale factor = <x>` is a per-domain scaling parameter <AUTHORS: confirmed exact use of the per-domain scale factor in the model builder>. |
| `create_model/go_model.log` | text | Record of the model build: configuration echoed, domains parsed, native-contact counts, STRIDE hydrogen bonds, and the files written (psf, cor, top, prm). |

The `create_model/` folder also holds same-named copies of the built model
files (`<UniProt>_clean_ca.psf`, `<UniProt>_clean_ca.cor`,
`<UniProt>_clean_ca.top`, `<UniProt>_clean_nscal1_fnn1_go_bt.prm`) written
by the model builder alongside its control file and log.


