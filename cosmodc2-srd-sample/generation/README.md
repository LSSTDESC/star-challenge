# SRD Sample Generation

## Basic Information

On this page we provide details of galaxy samples that are defined via SRD. This catalog is based on CosmoDC2 and is fairly idealistic in order to test TXPipe at a high precision. 

The samples use emulated noise on both the shears and magnitudes. The source sample is `T/Tpsf>0.5` and `SNR>10` and the lens sample is selected using `mag_i < 24`.  Both use a random forest selection for the tomography (5 source bins, 5 lens bins),

Sam has noted that this yields a sample with deeper u-band than expected.


Area: 441.279 sq. deg.

Cosmology: https://github.com/LSSTDESC/TXPipe/blob/master/data/fiducial_cosmology.yml

NERSC Location: /global/projecta/projectdirs/lsst/groups/WL/users/zuntz/star-challenge



## Data Access

In the directory above we provide source and lens catalogs in tomographic bins, plus a 2D "all" bin, as well as truth n(z) data and plots. The n(z) files are also included in this repository directory. The files are:

    binned_shear_catalog.hdf5
    binned_lens_catalog.hdf5
    lens_photoz_stack.hdf5
    shear_photoz_stack.hdf5
    nz_lens.png
    nz_source.png  


### Reading the shape catalog

    import h5py
    dirname = '/global/projecta/projectdirs/lsst/groups/WL/users/zuntz/star-challenge/'
    f = h5py.File(dirname + 'binned_shear_catalog.hdf5', 'r')

    for i in range(5):
        group = shearcat[f"shear/bin_{i}"]
        ra = group['ra'][:]
        dec = group['dec'][:]
        mag_r = group['mag_r'][:]
        mag_r_err = group['mag_r_err'][:]
        z_true = group['redshift_true'][:]
        weight = group['weight'][:]

etc. You can get a column list using the command `h5ls -r` on either file

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
    tx ceci examples/star-challenge/sample-for-pz.yml

It will make files in `data/star-challenge/outputs`.  Copies of the smaller output files (n(z) data and plots) are included in this repo directory.
