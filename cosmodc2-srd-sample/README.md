This readme explains how to obtain the two-point measurements for the cosmoDC2 sample used in Prat, Zuntz, et al. The instructions below are for cori at nersc.

1. Check the pipeline and config files (and edit them if you like):
    examples/star-challenge/sample-for-pz_full.yml
    examples/star-challenge/config_full.yml
    
2. Edit the output directory 'output_dir' to the folder of your choice (use SCRATCH since the output files are big). 
   You can have TXPipe installed in your home directory or SCRATCH but the output folder should always be SCRATCH. 

3. Get interactive nodes:
   salloc -N 6 -q interactive -C haswell -t 04:00:00 -A m1727
  
4. Run the following command:
   source /global/cfs/cdirs/lsst/groups/WL/users/zuntz/setup-txpipe

5. Check what we will run:
   tx ceci --dry-run examples/star-challenge/sample-for-pz_full.yml
   
   The output of the above is also useful if you want to run stages individually (just copy and paste each stage).
    
6. Actually run the whole pipeline:
   tx ceci examples/star-challenge/sample-for-pz_full.yml  
   
7. Check the ouptuts in the 'output_dir'. 



