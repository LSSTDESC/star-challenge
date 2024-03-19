# Link to public release
  https://des.ncsa.illinois.edu/releases/y3a2
  
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

A slightly modified version of this code, that saves a catalog that is in a format that TXPipe understands is provided in this repository.
   ```extract_catalogs_desy3_txpipe.py```

## Lens catalog

## Shear catalog

## PSF catalog
The PSF catalog can be obtained from here:<BR>
   http://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/psf/psf_y3a1-v29.fits

# Validated catalog location on Perlmutter
The git commit version of ```extract_catalogs_desy3_txpipe.py``` used to extract the catalog is stored in the header.

RedMaGiC: <BR>
Maglim  : <BR>
Metacal :  `/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/des-y3/shear_catalog_desy3_unmasked_withfakez_v2.h5` <BR>

Note: DES-Y3 uses SOM for redshift assignment. For convenience, each galaxy has been assigned a fake redshift (hence the tag `withfakez`) in the file according to which tomographic bin the galaxy should fall in.
  ```
  SOM bin1 -> 0.1
  SOM bin2 -> 0.3
  SOM bin3 -> 0.5
  SOM bin4 -> 0.7
  ```
Therefore, in the config.yml file, under `TXSourceSelectorMetacal` the `source_zbin_edges` must be set to `[0.0, 0.2, 0.4, 0.6, 0.8]` to place galaxies in the correct tomographic bins.
