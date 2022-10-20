STAR Challenge
=====================

This repo is work in progress and will record how we made and where we put files for the STAR challenge.

Each subdirectory will contain a certain sample and we will record steps for its generation as well as intermediate data products that are derived from the sample. We currently have the following samples:

- `gaussian-sim-srd-sample` - Gaussian simulations with SRD-like sample
- `cosmodc2-srd-sample` - SRD-like sample from CosmoDC2
- `cosmodc2-redmagic-sample` - CosmoDC2 sample that uses redmagic as lenses
- `dc2-lss-sample` - DC2 sample used for LSS project #91

Under each sample, we record detailed instructions on how to generate the samples as well as carry out a catalog-to-cosmology analysis using that sample. The firecrown parameters are separately stored in the `firecrown-parameter-inference` directory.

To run anything in these directories it is likely that you will need to install [TXPipe](https://github.com/LSSTDESC/TXPipe) and [Firecrown](https://github.com/LSSTDESC/firecrown). We provide simple instructions here to install both, though please read the respective documentation of the two packages for the most up-to-date instructions.


## TXPipe

Follow one of the options for [here](https://txpipe.readthedocs.io/en/latest/installation.html). Since many of the catalogs will be on NERSC, doing the NERSC shifter option is likely the fastest. Note that you would still need to clone TXPipe since the config files are in that repo. 

## Firecrown

You can read up on the installation options [here](https://firecrown.readthedocs.io/en/latest/install_quick.html). You probably want to choose the developer installation. 

### Install dependencies
        conda create --name firecrown_dev_env -c conda-forge sacc pyccl fitsio fuzzywuzzy urllib3 PyYAML portalocker idna dill charset-normalizer requests matplotlib flake8 pylint black pytest coverage pandas zeus-mcmc emcee
        conda activate firecrown_dev_env
        CC=clang CXX=clang++ pip install cosmosis cobaya
        git clone github.com:joezuntz/cosmosis-standard-library
        export CSL_DIR=your_path_to_the_cosmosis_standard_library

### Install firecrown
        git clone github.com:LSSTDESC/firecrown
        cd firecrown
        pip install -e . 
        export FIRECROWN_DIR=${PWD}/firecrown
