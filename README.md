STAR Challenge Notes
=====================

This repo is work in progress and will record how we made and where we put files for the STAR challenge.

Each subdirectory will contain a certain sample and we will record steps for its generation as well as intermediate data products that are derived from the sample. We currently have the following samples:

- `gaussian-sim-srd-sample` - Gaussian simulations with SRD-like sample
- `cosmodc2-srd-sample` - SRD-like sample from CosmoDC2
- `cosmodc2-redmagic-sample` - CosmoDC2 sample that uses redmagic as lenses
- `dc2-lss-sample` - DC2 sample used for LSS project #91

Under each sample, we record in subdirectories:

- `generation` - basic information and generation of the samples
- `photo-z` - information about training set and n(z)
- `data-vector` - information about running TXPipe to obtain data vectors and covariances
- `modeling` - information about running Firecrown to obtain cosmological inference
