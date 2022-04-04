# Sample Generation

## Basic Information

On this page we provide details of galaxy samples that are first used in the CosmoDC2-TXPipe project. This might later be replaced by the cosmodc2-srd-sample. The main difference with that sample is the use of redmagic as the lenses and more source bins. 

Area: 441.279 sq. deg.

Cosmology: https://github.com/LSSTDESC/TXPipe/blob/master/data/fiducial_cosmology.yml

NERSC Location: /global/projecta/projectdirs/lsst/groups/WL/users/jprat/cosmodc2_txpipe_outputs/


## Data Access

In the directory above we provide source and lens catalogs in tomographic bins, plus a 2D "all" bin, as well as truth n(z) data and plots. The n(z) files are also included in this repository directory. The files are:

    binned_shear_catalog.hdf5
    binned_lens_catalog.hdf5
    lens_photoz_stack.hdf5
    shear_photoz_stack.hdf5
    nz_lens.png
    nz_source.png  


### Reading the truth n(z)

    import h5py
    import numpy as np
    with h5py.File("lens_photoz_stack.hdf5") as f:
        group = f["n_of_z/lens"]

        # Read the z grid
        z = group["z"][:]

        # Read the number of tomo bins from the metadada
        nbin = group.attrs["nbin"]

        # Read the n(z)
        nz = np.zeros((nbin, z.size))
        for i in range(nbin):
            nz[i] = group[f"bin_{i}"][:]


## Process To Generate This Data Set

### Step 0: Getting TXPipe


The first few of these stages are happening in TXPipe, which you can get like this:

    git clone --recurse-submodules https://github.com/LSSTDESC/TXPipe
    cd TXPipe

### Step 1: Data Ingest and Noise Mocking

This initial ingestion phase is slow as it doesn't parallelize, and doesn't
have anything particularly configurable, so it's not worth running yourself. 
The subsequent steps configurations assume that instead of running this you are
using the files Joe produced earlier and centrally saved.

But for completeness, this will recreate the files on NERSC:

    source /global/cfs/cdirs/lsst/groups/WL/users/zuntz/setup-txpipe
    tx ceci examples/star-challenge/initial-ingest.yml


It would put files in `data/star-challenge/outputs`.  Joe's copies are in
`/global/projecta/projectdirs/lsst/groups/WL/users/zuntz/data/cosmoDC2-1.1.4_oneyear`.
They are too big to include here.

### Step 2: Generating the binning

This one is parallelizable.  From the TXPipe directory:

    salloc --nodes 1 --qos interactive --time 02:00:00 --constraint haswell
    source /global/cfs/cdirs/lsst/groups/WL/users/zuntz/setup-txpipe
    tx ceci examples/XXXX

It will make files in `data/XXX/outputs`.  Copies of the smaller output files (n(z) data and plots) are included in this repo directory.
