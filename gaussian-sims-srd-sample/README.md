# Gaussian simulations: DESC SRD Y1-like sample 

In Prat, Zuntz (2022), we use a simple Gaussian simulation to test whether TXPipe can deliver accurate and precise two-point function measurements to the LSST Y1 requirements. The simulations were designed to be like the LSST Y1 data, as specified by the LSST DESC SRD.

The generation of the sample is based on the method described in Giannantonio et al. (2008) and we describe the details here: https://github.com/LSSTDESC/star-challenge/tree/inference/gaussian-sims-srd-sample/generation.

### Catalogs on nersc:

## Instructions for running TXPipe


### Output sacc file on nersc:
* Real space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/data_vectors/summary_statistics_real.sacc`
* Harmonic space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/data_vectors/summary_statistics_fourier.sacc`

## Instructions for running Firecrown

### Output chains on nersc (fiducial wCDM):
* Real space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/chains/gaussian_sims_3x2pt_real_w0-wa.txt`
* Harmonic space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/chains/gaussian_sims_3x2pt_fourier_w0-wa.txt`
