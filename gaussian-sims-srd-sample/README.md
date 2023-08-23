# Gaussian simulations: DESC SRD Y1-like sample 

In Prat, Zuntz (2022), we use a simple Gaussian simulation to test whether TXPipe can deliver accurate and precise two-point function measurements to the LSST Y1 requirements. The simulations were designed to be like the LSST Y1 data, as specified by the LSST DESC SRD.

The generation of the sample is based on the method described in Giannantonio et al. (2008) and we describe the details [here]( https://github.com/LSSTDESC/star-challenge/tree/inference/gaussian-sims-srd-sample/generation).


### Catalogs on nersc

`/global/cfs/cdirs/lsst/groups/WL/users/jprat/gaussian_sims_srdnzs_fullsky/071222/`

## Instructions for running TXPipe

The instructions below are for cori at nersc. 

0. [Install TXPipe](https://github.com/LSSTDESC/star-challenge/tree/inference#txpipe) and also clone the TXPipe repo

1. In the TXPipe directory, check the pipeline and config files (and edit them if you like):

          https://github.com/LSSTDESC/TXPipe/blob/master/examples/gaussian_sims/pipeline_gaussian_sims.yml
          https://github.com/LSSTDESC/TXPipe/blob/master/examples/gaussian_sims/config.yml

2. Edit the output directory `output_dir` to the folder of your choice (use SCRATCH since the output files are big). 
   You can have TXPipe installed in your home directory or SCRATCH but the output folder should always be `$SCRATCH`. 

3. Get interactive nodes:

        salloc -N 6 -q interactive -C haswell -t 04:00:00 -A m1727
  
4. Run the following command:

        source /global/cfs/cdirs/lsst/groups/WL/users/zuntz/setup-txpipe

5. Check what we will run:

         tx ceci --dry-run examples/pipeline_gaussian_sims.yml

   The output of the above is also useful if you want to run stages individually (just copy and paste each stage).
    
6. Actually run the whole pipeline:

         tx ceci --dry-run examples/pipeline_gaussian_sims.yml

7. Check the ouptuts in the `output_dir`. 

A copy of all the output is stored in `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/TXPipe-full-output`. 

### Output sacc file on nersc

* Real space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/data_vectors/summary_statistics_real.sacc`
* Harmonic space `/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/data_vectors/summary_statistics_fourier.sacc`

## Instructions for running Firecrown

0. [Install firecrown](https://github.com/LSSTDESC/star-challenge/tree/inference#firecrown)

1. Activate firecrown environment
          
          conda activate firecrown

2. Set up paths

          export CSL_DIR=/where/cosmosis-standard-library/is/installed
          export FIRECROWN_DIR=/where/firecrown/is/installed
          export FIRECROWN_ROOT_DIR=/where/firecrown/is/installed

3. Run firecrown (in `firecrown-parameter-inference`) with the `test` sampler, ie. single evaluation of likelihood. 

          cosmosis cosmosis/gaussian_sims_3x2pt.ini

4. Run firecrown (in `firecrown-parameter-inference`) with the `emcee` sampler, ie. a chain. 

          sbatch submit

where `submit` will looks something like this on nersc

          #!/bin/bash                                                                   
          #SBATCH --qos=regular                                                              
          #SBATCH --time=10:00:00                                                             
          #SBATCH --nodes=10                                                               
          #SBATCH --constraint=haswell                                                          
          #SBATCH --account=m1727                                                             
          #SBATCH --job-name=gaussian_twopoint                                                      
          #SBATCH --output=%x.log                                                             
          #SBATCH --mail-type=END
          
          module load openmpi
          module load python
          source activate firecrown
          export CSL_DIR=/where/cosmosis-standard-library/is/installed
          export FIRECROWN_DIR=/where/firecrown/is/installed
          export FIRECROWN_ROOT_DIR=/where/firecrown/is/installed

          mpirun -n 210 cosmosis --mpi cosmosis/gaussian_sims_3x2pt.ini -p  runtime.sampler='emcee'


### Output chains on nersc 

`/global/cfs/cdirs/lsst/groups/WL/projects/star-challenge/gaussian/chains/`

