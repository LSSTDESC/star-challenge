# Link to public release
  TBD
  
# 

# Obtaining reproducible catalogs
The lens catalog can be extracted from what is called the master catalog, which consists of the following files:<BR>
[DESY3_indexcat.h5](http://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_cats/DESY3_indexcat.h5) <BR>
[DESY3_GOLD_2_2.1.h5](http://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_cats/DESY3_GOLD_2_2.1.h5)<BR>
[DESY3_metacal_v03-004.h5](http://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_cats/DESY3_metacal_v03-004.h5)<BR>
[DESY3_maglim_redmagic_v0.5.1.h5](http://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_cats/DESY3_maglim_redmagic_v0.5.1.h5)<BR>
[DESY3_GOLD_2_2.1_DNF.h5](http://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_cats/DESY3_GOLD_2_2.1_DNF.h5)<BR>
[DESY3_sompz_v0.40.h5](http://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_cats/DESY3_sompz_v0.40.h5)<BR>

The original script to extract source galaxies from the master catalog can be found in:<BR>
https://github.com/des-science/DESY3Cats <BR>
compute_catalogs.py
psfmod.py

A slightly modified version of this code, that saves a catalog that is in a format that TXPipe understands is provided in this repository.
   ```extract_catalogs_hscy3_txpipe.py```

## Lens catalog
TBD<BR>

## Shear catalog
TBD<BR>

## PSF/star catalog
Two versions of the star catalog exist, depending on whether the goal is
to reproduce the systematic tests results in 2107.00136 or 2212.0325.

To produce the results presented in 2212.03257, the two catalogs used are 
[hscy3_star_moments_nonpsf.csv](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/)<BR>
[hscy3_star_moments_psf.csv](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/)<BR>
In contrary to 2107.00136, FGCM matched stars are *not* used as reserved stars but the more general non-psf star sample is used. Also note that in 2107.00136 $g_{\rm PSF}=e_{\rm PSF}/2$ is used for the measurements whereas in 2212.0325 $e_{\rm PSF}$ is used, and this factor is alraedy taken into account in the conversion script.

# Validated catalog location on Perlmutter
The git commit version of ```extract_catalogs_hscy3_txpipe.py``` used to extract the catalog is stored in the header.

Star catalog for 2107.00136:  `/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/des-y3/shear_catalog_desy3_unmasked_withfakez_v2.h5` <BR>
Star catalog for 2212.0325:  `/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/des-y3/shear_catalog_desy3_unmasked_withfakez_v2.h5` <BR>

