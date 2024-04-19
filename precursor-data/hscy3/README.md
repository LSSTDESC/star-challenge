# Link to public release
  https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/
  
# 

# Obtaining reproducible catalogs

The original script to extract source galaxies used in cosmic shear and galaxy weak lensing can be found in:<BR>
[link to compute_catalogs.py and psfmod.py](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/) <BR>

A slightly modified version of this code, that saves a catalog that is in a format that TXPipe understands is provided in this repository.
   ```extract_catalogs_hscy3_txpipe.py```

## Lens catalog
TBD<BR>

## Shear catalog
TBD<BR>

## PSF/star catalog
Two versions of the PSF/star catalog exist, depending on whether the goal is
to reproduce the systematic tests results in [2107.00136](https://arxiv.org/abs/2107.00136) or [2212.0325](https://arxiv.org/abs/2212.0325).

### 2107.00136
To produce the results presented in [2107.00136](https://arxiv.org/abs/2107.00136) we need to use the raw catalogs without any spatial cut as well as a SNR>180 cut:

  /pscratch/sd/x/xiangchl/data/catalog/hsc_year3_shape/catalog_others/{field}_star.fits

where field is one of VVDS,GAMA09H,WIDE12H,GAMA15H,HECTOMAP,XMM. The kety point about these catalogs is that they include FGCM matched stars. 

### 2212.0325
To produce the results presented in 2212.03257, the two catalogs used are:

   [hscy3_star_moments_nonpsf.csv](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/)<BR>
   [hscy3_star_moments_psf.csv](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/)<BR>
   
In contrary to 2107.00136, FGCM matched stars are *not* used as reserved stars but the more general non-psf star sample is used. Also note that in 2107.00136, shear is used instead of ellipticity (i.e., $g_{\rm PSF}=e_{\rm PSF}/2$) in the measurements, whereas in 2212.0325 $e_{\rm PSF}$ is used, and this factor is alraedy taken into account in the TXPipe catalog conversion script.

# Validated catalog location on Perlmutter
The git commit version of ```extract_catalogs_hscy3_txpipe.py``` used to extract the catalog is stored in the header.

Star catalog for 2107.00136:  `/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/des-y3/shear_catalog_desy3_unmasked_withfakez_v2.h5` <BR>
Star catalog for 2212.0325:  `/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/des-y3/shear_catalog_desy3_unmasked_withfakez_v2.h5` <BR>

