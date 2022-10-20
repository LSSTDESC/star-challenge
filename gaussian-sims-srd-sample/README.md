# Gaussian simulations: DESC SRD Y1-like sample 

In Prat, Zuntz (2022), we use a simple Gaussian simulation to test whether TXPipe can deliver accurate and precise two-point function measurements to the LSST Y1 requirements. The simulations were designed to be like the LSST Y1 data, as specified by the LSST DESC SRD.

The generation of the sample is based on the method described in Giannantonio et al. (2008) and we describe the details [here]( https://github.com/LSSTDESC/star-challenge/tree/inference/gaussian-sims-srd-sample/generation).


### Catalogs on nersc

`/global/cfs/cdirs/lsst/groups/WL/users/jprat/gaussian_sims_srdnzs_fullsky/071222/`

## Instructions for running TXPipe

The instructions below are for cori at nersc. 

0. [Install TXPipe](https://github.com/LSSTDESC/star-challenge/tree/inference#txpipe)

1. Check the pipeline and config files (and edit them if you like):

          https://github.com/LSSTDESC/TXPipe/blob/master/examples/xxx
          https://github.com/LSSTDESC/TXPipe/blob/master/examples/xxx

2. Edit the output directory `output_dir` to the folder of your choice (use SCRATCH since the output files are big). 
   You can have TXPipe installed in your home directory or SCRATCH but the output folder should always be $SCRATCH. 

3. Get interactive nodes:

        salloc -N 6 -q interactive -C haswell -t 04:00:00 -A m1727
  
4. Run the following command:

        source /global/cfs/cdirs/lsst/groups/WL/users/zuntz/setup-txpipe

5. Check what we will run:

         tx ceci --dry-run examples/xxx

   The output of the above is also useful if you want to run stages individually (just copy and paste each stage).
    
6. Actually run the whole pipeline:

         tx ceci --dry-run examples/xxx

7. Check the ouptuts in the `output_dir`. 

A copy of all the output is stored in `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/xxx/`. 

### Output sacc file on nersc

* Real space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/data_vectors/summary_statistics_real.sacc`
* Harmonic space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/data_vectors/summary_statistics_fourier.sacc`

## Instructions for running Firecrown

### Output chains on nersc (fiducial wCDM)

* Real space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/chains/gaussian_sims_3x2pt_real_w0-wa.txt`
* Harmonic space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/chains/gaussian_sims_3x2pt_fourier_w0-wa.txt`
