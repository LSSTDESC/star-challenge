# Sample Generation

## Basic Information

This catalog is used for the DC2 LSS project. It is based on the DC2 dr6 catalog and contains about 56.7M galaxies in an area of roughly 300 deg^2.

### Selection:
* i-band magnitude: 17 < i < 25.3
* Redshift binning: 0.2 to 1.4 in 6 equally-spaced bins.  We use the peak of the pdf in the catalog to assign the galaxy to a particular bin, then stack the pdf's to get the n(z) distribution.

Selection cuts:
standard_cuts =[
  GCRQuery('detect_isPrimary'),
  GCRQuery('modelfit_CModel_flag_badCentroid==False'),
  GCRQuery('base_SdssCentroid_flag==False'),
  GCRQuery('base_PixelFlags_flag_edge==False'),
  GCRQuery('base_PixelFlags_flag_interpolatedCenter==False'),
  GCRQuery('base_PixelFlags_flag_saturatedCenter==False'),
  GCRQuery('base_PixelFlags_flag_bad==False'),
  GCRQuery('base_PixelFlags_flag_suspectCenter==False'),
  GCRQuery('deblend_skipped==False'),
  GCRQuery('cModelFlux_flag_i==False'),
  GCRQuery('base_PsfFlux_flag==False'),
  GCRQuery('base_SdssShape_flag_psf==False'),
  GCRQuery('modelfit_DoubleShapeletPsfApprox_flag==False'),
  GCRQuery('base_ClassificationExtendedness_flag==False'),
  GCRQuery('modelfit_CModel_flags_region_usedInitialEllipseMin==False'),
]
blend_cut = [
  GCRQuery('base_Blendedness_abs<=0.42169650342')
]
gal_cut=[
  GCRQuery('base_ClassificationExtendedness_value==1')
]
ugrizyflux_cut = i band snr>6 and at least two other bands’ snr>3
pzodds_cut=[
  GCRQuery('photoz_odds>0')
]


### Depth mask
i band 5sigma depth > 25.3; this cuts out 2% of objects.  

Available on cori/nersc in /global/cfs/cdirs/lsst/groups/LSS/DC2_R2.2i/dr6

### Bright object mask: 
using mag dependent radius (90% of max object density); this cuts out 13% of objects.  In GCRCatalog, we find all stars using extendedness==0 and separate them into mag_i_cModel bins: (0,17) (17,18) (18,20) (20,22) . For the stars in each bin we calculate the ratio f= #object density in discs/mean #object density of discs around each star as a function of the radius of the disc, we choose the radii @ f~0.9 as the radii of bright object masks of each bin.   

Available on cori/nersc in   /global/cfs/cdirs/lsst/groups/LSS/DC2_R2.2i/dr6


