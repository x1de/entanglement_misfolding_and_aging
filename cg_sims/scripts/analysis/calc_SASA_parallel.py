"""
Compute the per-residue solvent-accessible surface area (SASA) of the 50
all-atom backmapped trajectories.

For each trajectory folder <i> the script loads aa_<i>.dcd with topology
aa_<i>.psf, raises an error if either file is missing, checks that the
trajectory has the expected 20000 frames, and computes the per-residue SASA
of every 10th frame with mdtraj's Shrake-Rupley algorithm. Each result is
saved to SASA/sasa_<i>.npy; after all 50 trajectories are processed, the
results are stacked and saved as SASA/SASA.npy. Trajectories are processed
in parallel with a multiprocessing.Pool, and the residue count is read from
the template topology ../template/setup/top.psf.
"""

import os
import mdtraj as md
import numpy as np
import parmed as pmd
from multiprocessing import Pool

n_trajs = 50
n_frames = 20_000
p = pmd.load_file('../template/setup/top.psf')
n_residues = p.topology.getNumResidues()

os.makedirs('SASA', exist_ok=True)

def process_traj(i):
    print(f"Processing trajectory: {i}")
    dcd_file = f'../{i}/aa_{i}.dcd'
    psf_file = f'../{i}/aa_{i}.psf'

    if not (os.path.exists(dcd_file) and os.path.exists(psf_file)):
        raise FileNotFoundError(f"Missing files for traj {i}: {dcd_file} or {psf_file}")

    traj = md.load(dcd_file, top=psf_file)
    if traj.n_frames != n_frames:
        raise ValueError(
            f"Trajectory {i} has {traj.n_frames} frames, expected {n_frames}. "
            "Stopping execution."
        )
    sasa = md.shrake_rupley(traj[::10], mode='residue')
    np.save(f'SASA/sasa_{i}.npy', sasa)
    return sasa

if __name__ == '__main__':
    with Pool(processes=8) as pool:
        all_sasa = pool.map(process_traj, range(n_trajs))
    all_sasa = np.array(all_sasa, dtype=np.float32)
    np.save('SASA/SASA.npy', all_sasa)
    print("Finished. SASA.npy and individual SASA files saved.")
