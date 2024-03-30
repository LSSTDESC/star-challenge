# https://github.com/LSSTDESC/star-challenge.git
# Based on script written by Tianqing 
# Main directory 
# /global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/
import os, sys, git, h5py
import numpy as np
import pandas as pd
from astropy.table import Table, vstack

# Extract git hash, which will be saved in the header
repo  = git.Repo(dict['base']['dir_healqest'],search_parent_directories=True)
sha   = repo.head.object.hexsha

dir_shape_catalog = '/hildafs/projects/phy200017p/share/HSC_shape_catalog_Y3/catalog_obs_reGaus_no_m/'
dir_bin_id        = '/hildafs/projects/phy200017p/xiangchl/work/S19ACatalogs/photoz_2pt/'
dir_star          = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/'

def 

#----------------- Uncalibrated shear catalog --------------------
field_list = ['GAMA09H', 'GAMA15H', 'HECTOMAP', 'WIDE12H', 'VVDS', 'XMM']

asel_list  = np.array([0.005757300075048228, 0.007966889498601236, 0.008428564522033983,  0.008382723879301538])
msel_list  = np.array([0.01711262019090257 , 0.018377595498915943, 0.011807321550085953, -0.0006360553708744804])

table_list = []

# Initialize arrays
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

for field in field_list:

    print("Processing field:", field)
    this_shape_cat  = Table.read(dir_shape_catalog + "{}_no_m.fits".format(field))
    this_bin_id_cat = Table.read(dir_bin_id + "source_sel_{}.fits".format(field))
    this_shape_cat['dnnz_bin'] = this_bin_id_cat['dnnz_bin']

    for bin_id in range(1,5):

        print(bin_id)

        d = this_shape_cat[this_bin_id_cat['dnnz_bin'] == bin_id]

        # Basic columns needed by TXPipe
        ra      = d['i_ra']
        dec     = d['i_dec']
        sigma_e = d['i_hsmshaperegauss_derived_rms_e']
        weight  = d['i_hsmshaperegauss_derived_weight']
        m       = msel_list[bin_id-1]
        c1      = d['i_hsmshaperegauss_derived_shear_bias_c1']
        c2      = d['i_hsmshaperegauss_derived_shear_bias_c2']
        e1      = d['i_hsmshaperegauss_e1']
        e2      = d['i_hsmshaperegauss_e2']
        T       = d['i_sdssshape_psf_shape11']+d['i_sdssshape_psf_shape22']

        # Extra column: precalibrated g1/g2
        R       = 1 - sigma_e**2
        mean_R  = np.sum(weight*R)/np.sum(weight)

        asel    = asel_list[bin_id-1]
        msel    = msel_list[bin_id-1]
        tmp_e1  = (e1/(2*mean_R) - c1)
        tmp_e2  = (e2/(2*mean_R) - c2)

        psf_e1  = (d['i_sdssshape_psf_shape11']-d['i_sdssshape_psf_shape22'])/(d['i_sdssshape_psf_shape11']+d['i_sdssshape_psf_shape22'])
        psf_e2  = 2*d['i_sdssshape_psf_shape12']/(d['i_sdssshape_psf_shape11'] + d['i_sdssshape_psf_shape22'])
        g1      = (tmp_e1 - asel*psf_e1)/(1+msel)
        g2      = (tmp_e2 - asel*psf_e2)/(1+msel)

        tot_ra      += list(ra)
        tot_dec     += list(dec)
        tot_sigma_e += list(sigma_e)
        tot_m       += list(m)
        tot_c1      += list(c1)
        tot_c2      += list(c2)
        tot_e1      += list(e1)
        tot_e2      += list(e2)
        tot_g1      += list(g1)
        tot_g2      += list(g2)
        tot_weight  += list(weight)
        tot_T       += list(T)
        

# Create a hdf5 file. This will contain both reserved and used stars.
with h5py.File('../inputs/photometry_catalog_desy1_RM.h5', 'w') as f:
    f.create_group("provenance")
    f.create_group("shear")
    f['provenance/githash'] = sha
    f['shear/objectId']     = np.concatenate([r_dec,u_dec])
    f['shear/ra']           = np.asarray(tot_ra)
    f['stars/dec']          = np.asarray(tot_dec)
    f['stars/flags']        = 
    f['stars/g1']           = np.asarray(tot_e1)
    f['stars/g2']           = np.asarray(tot_e1)
    f['stars/T']            = np.asarray(tot_T)
    f['stars/c1']           = np.asarray(tot_c1)
    f['stars/c2']           = np.asarray(tot_c2)
    f['stars/m']            = np.asarray(tot_m)
    f['stars/mag_i']        = 
    f['stars/mag_r']        = 
    f['stars/mag_err_i']    = 
    f['stars/mag_err_r']    = 
    f['stars/mean_z']       = 
    f['stars/psf_g1']       = np.concatenate([r_dec,u_dec])
    f['stars/psf_g2']       = np.concatenate([r_dec,u_dec])
    f['stars/psf_T_mean']   = 
    f['stars/redshift_true'] = np.concatenate([r_dec,u_dec])
    f['stars/s2n']           = 
    f['stars/sigma_e']       = np.asarray(tot_sigma_e) 
    f['stars/snr_i']         = 
    f['stars/snr_r']         = 
    f['stars/weight']        = np.asarray(tot_weight) 
    f['stars/wl_fulldepth_fullcolor'] = np.concatenate([r_dec,u_dec])
    
    
#<KeysViewHDF5 ['T', 'c1', 'c2', 'dec', 'flags', 'g1', 'g2', 'lensfit_weight', 'm', 'mag_err_i', 'mag_err_r', 'mag_i', 'mag_r', 'mean_z', 'objectId', 'psf_T_mean', 'psf_g1', 'psf_g2', 'ra', 'redshift_true', 's2n', 'sigma_e', 'snr_i', 'snr_r', 'weight', 'wl_fulldepth_fullcolor']>


table_origin = vstack(table_list)

# remove the 20 sq deg in GAMA09H because of excessive B-mode in this region. 
mm=(table_origin['ra']>=132.5)&(table_origin['ra']<=140.)&(table_origin['dec']>=1.6)&(table_origin['dec']<5.2)
mm=~mm
table_origin=table_origin[mm]

write_table(table_origin, 'data/egal.fits')

#----------------- Precalibrated shear catalog --------------------


#----------------- Star catalog (resv) --------------------
catalog  = pd.read_csv("../catalog/hscy3_star_moments_psf.csv", header = 0)

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
catalog  = pd.read_csv("../catalog/hscy3_star_moments_nonpsf.csv", header = 0)

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
tmp        = np.concatanete([ np.ones(len(r_ra))*3, np.ones(len(u_ra))*4  ])
flag_resv  = np.zeros(totstars); flag_resv[tmp==3] = 1
flag_used  = np.zeros(totstars); flag_used[tmp==4] = 1

# Create a hdf5 file. This will contain both reserved and used stars.
with h5py.File('../inputs/photometry_catalog_desy1_RM.h5', 'w') as f:
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
