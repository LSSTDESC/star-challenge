# https://github.com/LSSTDESC/star-challenge.git
# Based on script written by Tianqing 
# Main directory 
# /global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/
import os, sys, git, h5py
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.table import Table, vstack

# Extract git hash, which will be saved in the header
repo  = git.Repo('./',search_parent_directories=True)
sha   = repo.head.object.hexsha

dir_shape_catalog = '/hildafs/projects/phy200017p/share/HSC_shape_catalog_Y3/catalog_obs_reGaus_no_m/'
dir_bin_id        = '/hildafs/projects/phy200017p/xiangchl/work/S19ACatalogs/photoz_2pt/'
dir_star          = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/'

file_star_used    = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/hscy3_star_moments_psf.csv'
file_star_resv    = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/hscy3_star_moments_nonpsf.csv'
file_shear        = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/shear/{field}_calibrated.fits' 

file_out_shear    = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/shear/txpipe_allfield_shear.h5'
file_out_star     = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/txpipe_allfield_star.h5'

#----------------- Uncalibrated shear catalog --------------------
field_list = ['GAMA09H', 'GAMA15H', 'HECTOMAP', 'WIDE12H', 'VVDS', 'XMM']

asel_list  = np.array([-99, 0.005757300075048228, 0.007966889498601236, 0.008428564522033983,  0.008382723879301538])
msel_list  = np.array([-99, 0.01711262019090257 , 0.018377595498915943, 0.011807321550085953, -0.0006360553708744804])

table_list = []

# Initialize arrays
tot_objid   = []
tot_ra      = []
tot_dec     = []
tot_sigma_e = []
tot_m       = []
tot_c1      = []
tot_c2      = []
tot_e1      = []
tot_e2      = []
tot_g1      = []
tot_g2      = []
tot_weight  = []
tot_T       = []
tot_objID   = []
tot_psf_e1  = []
tot_psf_e2  = []
tot_psf_T   = []
tot_mag_i   = []
tot_magerr_i= []
tot_flag    = []
tot_mean_z  = []


for field in field_list:

    print("Processing field:", field)
    #this_shape_cat  = Table.read(dir_shape_catalog + "{}_no_m.fits".format(field))
    #this_bin_id_cat = Table.read(dir_bin_id + "source_sel_{}.fits".format(field))
    #this_shape_cat['dnnz_bin'] = this_bin_id_cat['dnnz_bin']
    d = fits.open(file_shear.format(field=field))[1].data

    zbin     = d['hsc_y3_zbin']
    
    #d = this_shape_cat[this_bin_id_cat['dnnz_bin'] == bin_id]

    # Basic columns needed by TXPipe
    objid    = d['object_id']
    ra       = d['i_ra']
    dec      = d['i_dec']
    sigma_e  = d['i_hsmshaperegauss_derived_rms_e']
    weight   = d['i_hsmshaperegauss_derived_weight']
    m        = msel_list[zbin]
    c1       = d['i_hsmshaperegauss_derived_shear_bias_c1']
    c2       = d['i_hsmshaperegauss_derived_shear_bias_c2']
    e1       = d['i_hsmshaperegauss_e1']
    e2       = d['i_hsmshaperegauss_e2']
    T        = d['i_sdssshape_psf_shape11']+d['i_sdssshape_psf_shape22']
    mag_i    = d['i_cmodel_flux']
    magerr_i = d['i_cmodel_fluxerr']
    mean_z   = zbin
    flag     = d['weak_lensing_flag']
    
    
    # Extra column: precalibrated g1/g2
    R        = 1 - sigma_e**2
    mean_R   = np.sum(weight*R)/np.sum(weight)

    asel     = asel_list[zbin]
    msel     = msel_list[zbin]
    tmp_e1   = (e1/(2*mean_R) - c1)
    tmp_e2   = (e2/(2*mean_R) - c2)

    psf_e1   = (d['i_sdssshape_psf_shape11']-d['i_sdssshape_psf_shape22'])/(d['i_sdssshape_psf_shape11']+d['i_sdssshape_psf_shape22'])
    psf_e2   = 2*d['i_sdssshape_psf_shape12']/(d['i_sdssshape_psf_shape11'] + d['i_sdssshape_psf_shape22'])
    psf_T    = (d['i_sdssshape_psf_shape11']+d['i_sdssshape_psf_shape22'])

    g1       = (tmp_e1 - asel*psf_e1)/(1+msel)
    g2       = (tmp_e2 - asel*psf_e2)/(1+msel)

    # remove the 20 sq deg in GAMA09H because of excessive B-mode in this region.
    if field=='GAMA09H':
        mask     = (ra>=132.5) & (ra<=140.) & (dec>=1.6) & (dec<5.2) | (zbin<1)
        mask     = ~mask
    else:
        mask     = (zbin<1)
        mask     = ~mask     

    # Append to the total list
    tot_objid    += list(objid[mask])
    tot_ra       += list(ra[mask])
    tot_dec      += list(dec[mask])
    tot_sigma_e  += list(sigma_e[mask])
    tot_m        += list(m[mask])
    tot_c1       += list(c1[mask])
    tot_c2       += list(c2[mask])
    tot_e1       += list(e1[mask])
    tot_e2       += list(e2[mask])
    tot_g1       += list(g1[mask])
    tot_g2       += list(g2[mask])
    tot_weight   += list(weight[mask])
    tot_T        += list(T[mask])
    tot_psf_e1   += list(psf_e1[mask])
    tot_psf_e2   += list(psf_e2[mask])
    tot_psf_T    += list(psf_T[mask])
    tot_mag_i    += list(mag_i[mask])
    tot_magerr_i += list(magerr_i[mask])
    tot_mean_z   += list(mean_z[mask])
    tot_flag     += list(flag[mask])        

# Create a hdf5 file. This will contain both reserved and used stars.
with h5py.File(file_out_shear, 'w') as f:
    f.create_group("provenance")
    f.create_group("shear")
    f['provenance/githash'] = sha
    f['shear/objectId']     = np.asarray(tot_objid)
    f['shear/ra']           = np.asarray(tot_ra)
    f['shear/dec']          = np.asarray(tot_dec)
    f['shear/flags']        = np.asarray(tot_flag)
    f['shear/g1']           = np.asarray(tot_e1)
    f['shear/g2']           = np.asarray(tot_e1)
    f['shear/T']            = np.asarray(tot_T)
    f['shear/c1']           = np.asarray(tot_c1)
    f['shear/c2']           = np.asarray(tot_c2)
    f['shear/m']            = np.asarray(tot_m)
    f['shear/mag_i']        = np.asarray(tot_mag_i)
    f['shear/mag_err_i']    = np.asarray(tot_magerr_i)
    f['shear/mean_z']       = np.asarray(tot_mean_z)
    f['shear/psf_g1']       = np.asarray(tot_psf_e1) 
    f['shear/psf_g2']       = np.asarray(tot_psf_e2)
    f['shear/psf_T_mean']   = np.asarray(tot_psf_T)
    f['shear/sigma_e']      = np.asarray(tot_sigma_e) 
    f['shear/s2n']          = np.asarray(tot_magerr_i)    # Just place a copy of s?n in i-band
    f['shear/snr_i']        = np.asarray(tot_magerr_i) 
    f['shear/weight']       = np.asarray(tot_weight) 
    #f['stars/mag_r']       = 
    #f['stars/mag_err_r']   = 
    #f['stars/snr_r']       = 
    #f['stars/wl_fulldepth_fullcolor'] = np.concatenate([r_dec,u_dec])
    
    
#<KeysViewHDF5 ['T', 'c1', 'c2', 'dec', 'flags', 'g1', 'g2', 'lensfit_weight', 'm', 'mag_err_i', 'mag_err_r', 'mag_i', 'mag_r', 'mean_z', 'objectId', 'psf_T_mean', 'psf_g1', 'psf_g2', 'ra', 'redshift_true', 's2n', 'sigma_e', 'snr_i', 'snr_r', 'weight', 'wl_fulldepth_fullcolor']>


#table_origin = vstack(table_list)

# remove the 20 sq deg in GAMA09H because of excessive B-mode in this region. 
#mm=(table_origin['ra']>=132.5)&(table_origin['ra']<=140.)&(table_origin['dec']>=1.6)&(table_origin['dec']<5.2)
#mm=~mm
#table_origin=table_origin[mm]

#write_table(table_origin, 'data/egal.fits')

#----------------- Precalibrated shear catalog --------------------


#----------------- Star catalog (resv) --------------------
catalog  = pd.read_csv(file_star_resv, header = 0)

# extract ra, dec
r_ra, r_dec  = catalog['i_ra'], catalog['i_dec']

# extract star_e1, star_e2
r_star_mxx = catalog['i_sdssshape_shape11']
r_star_myy = catalog['i_sdssshape_shape22']
r_star_mxy = catalog['i_sdssshape_shape12']
r_star_e1  = (r_star_mxx-r_star_myy)/(r_star_mxx+r_star_myy)
r_star_e2  = 2*r_star_mxy/(r_star_mxx + r_star_myy)
r_star_T   = (r_star_mxx+r_star_myy)

# extract model_e1, model_e2
r_psf_mxx  = catalog['i_sdssshape_psf_shape11']
r_psf_myy  = catalog['i_sdssshape_psf_shape22']
r_psf_mxy  = catalog['i_sdssshape_psf_shape12']
r_psf_e1   = (r_psf_mxx-r_psf_myy)/(r_psf_mxx+r_psf_myy)
r_psf_e2   = 2*r_psf_mxy/(r_psf_mxx +r_psf_myy)
r_psf_T   = (r_star_mxx+r_star_myy)

# extract diff_e1, diff_e2
r_de1      = r_psf_e1 - r_star_e1
r_de2      = r_psf_e2 - r_star_e2

#----------------- Star catalog (used) --------------------
catalog  = pd.read_csv(file_star_used, header = 0)

# Apply cut that extracts sources with S/N > 180
catalog  = catalog[catalog['snr'] > 180]

# extract ra, dec
u_ra, u_dec  = catalog['i_ra'], catalog['i_dec']

# extract star_e1, star_e2
u_star_mxx = catalog['i_sdssshape_shape11']
u_star_myy = catalog['i_sdssshape_shape22']
u_star_mxy = catalog['i_sdssshape_shape12']
u_star_e1  =  (u_star_mxx-u_star_myy)/(u_star_mxx+u_star_myy)
u_star_e2  =  2*u_star_mxy/(u_star_mxx + u_star_myy)
u_star_T   =  (u_star_mxx+u_star_myy)

# extract model_e1, model_e2
u_psf_mxx  = catalog['i_sdssshape_psf_shape11']
u_psf_myy  = catalog['i_sdssshape_psf_shape22']
u_psf_mxy  = catalog['i_sdssshape_psf_shape12']
u_psf_e1   = (u_psf_mxx-u_psf_myy)/(u_psf_mxx+u_psf_myy)
u_psf_e2   = 2*u_psf_mxy/(u_psf_mxx +u_psf_myy)
u_psf_T    = (u_psf_mxx+u_psf_myy)

# extract diff_e1, diff_e2
u_de1      = u_psf_e1 - u_star_e1
u_de2      = u_psf_e2 - u_star_e2

# Compute the total number of stars and create a flag column
totstars   = len(u_ra)+len(r_ra) 
tmp        = np.concatenate([ np.ones(len(r_ra))*3, np.ones(len(u_ra))*4  ])
flag_resv  = np.zeros(totstars); flag_resv[tmp==3] = 1
flag_used  = np.zeros(totstars); flag_used[tmp==4] = 1

# Create a hdf5 file. This will contain both reserved and used stars.
with h5py.File(file_out_star, 'w') as f:
    f.create_group("provenance")
    f.create_group("stars")
    f['provenance/githash']       = sha
    f['stars/ra']                 = np.concatenate([r_ra ,u_ra ])
    f['stars/dec']                = np.concatenate([r_dec,u_dec])
    f['stars/calib_psf_reserved'] = flag_resv
    f['stars/calib_psf_used']     = flag_used
    f['stars/measured_e1']        = np.concatenate([r_star_e1, u_star_e1])
    f['stars/measured_e2']        = np.concatenate([r_star_e2, u_star_e2])
    f['stars/measured_T']         = np.concatenate([r_star_T , u_star_T])
    f['stars/model_e1']           = np.concatenate([r_psf_e1 , u_psf_e1])
    f['stars/model_e2']           = np.concatenate([r_psf_e2 , u_psf_e2])
    f['stars/model_T']            = np.concatenate([r_psf_T  , u_psf_T])
