# ---------------------------------------------------------------------------
# Run provenance: appends the command line, start/stop clock times,
# interpreter and package versions, and sha256 checksums of every file named
# on the command line and of every file this run wrote, to
# calculation_SASA_provenance.log in the folder the run starts from.
# Records never stop the step; end-of-run records run via atexit.
# ---------------------------------------------------------------------------
import sys
import os
import time
import hashlib
import atexit

_PROV_T0 = time.time()
_PROV_LOG = "calculation_SASA_provenance.log"


def _prov_write(line):
    try:
        with open(_PROV_LOG, "a") as _fh:
            _fh.write(time.strftime("%Y-%m-%dT%H:%M:%S ") + line + "\n")
    except Exception:
        pass


def _prov_sha256(path):
    _h = hashlib.sha256()
    with open(path, "rb") as _fh:
        for _chunk in iter(lambda: _fh.read(1 << 20), b""):
            _h.update(_chunk)
    return _h.hexdigest()


def _prov_finish():
    _prov_write(
        f"stop: {time.strftime('%Y-%m-%dT%H:%M:%S')} wall_s={time.time() - _PROV_T0:.1f}"
    )
    _prov_write("python: " + sys.version.replace("\n", " "))
    try:
        from importlib.metadata import distributions

        _pkgs = sorted(
            f"{_d.metadata['Name']}=={_d.version}"
            for _d in distributions()
            if _d.metadata and _d.metadata.get("Name")
        )
        _prov_write("packages: " + "; ".join(_pkgs))
    except Exception:
        pass
    for _a in sys.argv:
        try:
            if os.path.isfile(_a):
                _prov_write(f"sha256 input {_a}: {_prov_sha256(_a)}")
        except Exception:
            pass
    try:
        for _n in sorted(os.listdir(".")):
            if _n == _PROV_LOG:
                continue
            _p = os.path.join(".", _n)
            if os.path.isfile(_p) and os.path.getmtime(_p) >= _PROV_T0:
                _prov_write(f"sha256 output {_n}: {_prov_sha256(_p)}")
    except Exception:
        pass


atexit.register(_prov_finish)
_prov_write(f"start: {time.strftime('%Y-%m-%dT%H:%M:%S')}")
_prov_write("command: " + " ".join(sys.argv))
# ---------------------------------------------------------------------------
# End of run-provenance block; the original script continues below.
# ---------------------------------------------------------------------------
import os
import mdtraj as md
import numpy as np
import parmed as pmd

n_trajs = 50
n_frames = 20_000
p = pmd.load_file('../template/setup/top.psf')
n_residues = p.topology.getNumResidues()

# allocate with NaNs so missing trajectories stay obvious
all_sasa = np.full((n_trajs, n_frames, n_residues), np.nan, dtype=np.float32)


for i in range(n_trajs):
    print(f"Calculating SASA for trajectory {i}")

    dcd_file = f'../{i}/aa_{i}.dcd'
    psf_file = f'../{i}/aa_{i}.psf'

    if not (os.path.exists(dcd_file) and os.path.exists(psf_file)):
        raise FileNotFoundError(f"Missing files for traj {i}: {dcd_file} or {psf_file}")

    # load trajectory
    traj = md.load(dcd_file, top=psf_file)

    # enforce frame count check
    if traj.n_frames != n_frames:
        raise ValueError(
            f"Trajectory {i} has {traj.n_frames} frames, expected {n_frames}. "
            "Stopping execution."
        )
    
    # calculate SASA per residue (frames × residues)
    sasa = md.shrake_rupley(traj, mode='residue')

    # write to array
    all_sasa[i] = sasa

# save to disk
np.save('SASA.npy', all_sasa)
print("Finished. SASA.npy saved.")