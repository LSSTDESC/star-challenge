# Sample Generation

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

## Training Samples

We have defined three training samples for CosmoDC2: optimistic, realistic and pessimistic, each described below. 

All training samples are subsets of the catalog at the following filepath: 

    /global/projecta/projectdirs/lsst/groups/WL/users/zuntz/data/cosmoDC2-1.1.4_oneyear/photometry_catalog.hdf5. 
    
Training sample files are hdf5 files with two keys: 'indices' and 'i-mag' 
indices is a list of indices in the photometry_catalog corresponding to the training sample, and i-mag are the corresponding i-band magnitudes so you can double check that you're counting indices the same way I did.
Before making training samples, galaxies with one or ore magnitudes set as 'inf' were removed.

Training samples live on NERSC at:

    /global/home/i/irenem/STAR_challenge/training_samples

### Optimistic Sample (Fully Representative)
This sample was made by making a list of indices for all the data. The indices were randomly shuffled, then the first 2.2M were selected.
The number of galaxies was chosen to be approximately the same size as the other two training samples.

File name:

    cosmodc2_representative_training_sample.hdf5

### Realistic Sample
This sample was generated using the GridSelection degrader in RAIL, with the default settings (implementing a color-based redshift cut).

File name:

    cosmodc2_realistic_training_sample.hdf5

### Pessimistic Sample
The pessimistic sample was generated using the GridSelection degrader, with the redshift_cut parameter set to 0.8.
This produces a similar sample to the realistic sample, but also excludes any galaxies with redshifts > 0.8.

File name:

    cosmodc2_pessimistic_training_sample.hdf5
