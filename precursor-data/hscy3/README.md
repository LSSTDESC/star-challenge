# Link to public release
  https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/ <BR>
  <BR>
  Thanks to Rachel Mandelbaum, Xiangchong Li and Tianqing Zhang for providing access to catalogs and processing scipts 
# 

# Obtaining reproducible catalogs

The original script to extract source galaxies used for cosmic shear and galaxy weak lensing is:<BR>
[compute_catalogs.py](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/) <BR>
and the code to measure psf disagnostics is:<BR>
[psfmod.py](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/) <BR>

A slightly modified version of the first code, that saves a catalog in a format that can be ingested by TXPipe is provided in this repository.
   ```extract_catalogs_hscy3_txpipe.py```

## Lens catalog
N/A<BR>

## Shear catalog
The original shear catalogs can be downloaded from [https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/)<BR>
and the files required are those with names:<BR>

```{field}_calibrated.fits```<BR>

where field = ['GAMA09H', 'GAMA15H', 'HECTOMAP', 'WIDE12H', 'VVDS', 'XMM']. <BR>

## PSF/star catalog
Two versions of the PSF/star catalog exist, depending on whether the goal is
to reproduce the systematic tests results in [2107.00136](https://arxiv.org/abs/2107.00136) or [2212.0325](https://arxiv.org/abs/2212.0325).

### 2107.00136
To produce the results presented in [2107.00136](https://arxiv.org/abs/2107.00136) we need to use the raw catalogs without any spatial cut as well as a SNR>180 cut:

  ```/pscratch/sd/x/xiangchl/data/catalog/hsc_year3_shape/catalog_others/{field}_star.fits```

where again field = ['GAMA09H', 'GAMA15H', 'HECTOMAP', 'WIDE12H', 'VVDS', 'XMM']. The key point about these catalogs is that they include FGCM matched stars. Note that there is a small difference in the number of stars when compared to the quoted numbers in the published paper.

### 2212.0325
To produce the results presented in [2212.0325](https://arxiv.org/abs/2212.0325), the two catalogs used are:

   [hscy3_star_moments_nonpsf.csv](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/)<BR>
   [hscy3_star_moments_psf.csv](https://hsc-release.mtk.nao.ac.jp/doc/index.php/wly3/)<BR>
   
In contrary to [2107.00136](https://arxiv.org/abs/2107.00136), FGCM matched stars are *not* used as reserved stars but the more general non-psf star sample is used. Also note that in [2107.00136](https://arxiv.org/abs/2107.00136), shear is used instead of ellipticity (i.e., $g_{\rm PSF}=e_{\rm PSF}/2$) in the measurements, whereas in [2212.0325](https://arxiv.org/abs/2212.0325) $e_{\rm PSF}$ is used, and this factor is already taken into account in the TXPipe catalog conversion script.

# Validated catalog location on Perlmutter
The git commit version of ```extract_catalogs_hscy3_txpipe.py``` used to extract the catalog is stored in the header and the latest version is:
```033b28d268a60665f269701acb3964bf0a848000```

Shear catalog:<BR>
`/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/shear/txpipe_allfield_shear.h5`<BR>
<BR>
Star catalog for 2107.00136:<BR>
`/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/txpipe_allfield_star_nosnrcut.h5` <BR>
<BR>
Star catalog for 2212.0325:<BR>
`/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/txpipe_allfield_star.h5` <BR>

