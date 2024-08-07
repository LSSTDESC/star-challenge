# This scripts takes the publicly available HSC-Y3
# catalog and transforms it into a formast that TXPipe
# understands. It is based on scripts written by Tianqing/Xiangchong 
#
# The precimputed version can be found in  
# Perlmutter:/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3

import os, sys, git, h5py
import numpy as np
import healpy as hp
import pandas as pd
from astropy.io import fits

def rd2tp(ra,dec):
    """Convert ra,dec -> tht,phi"""
    tht = (-dec+90.0)/180.0*np.pi
    phi = ra/180.0*np.pi
    return tht,phi

def tp2rd(tht,phi):
    """Convert tht,phi -> ra,dec"""
    ra  = phi/np.pi*180.0
    dec = -1*(tht/np.pi*180.0-90.0)
    return ra,dec

def spherical_pointpick(mask,dens_target):
    """ Populate until we hit deseired density """
    nside        = hp.npix2nside(mask.shape[0])
    area_arcmin2 = np.sum(mask)/mask.shape[0]*(180/np.pi)**2*4*np.pi*60**2
    dens   = 0
    totra  = []
    totdec = []
    while dens<dens_target:
        u   = np.random.uniform(low=0,high=1,size=5000000)
        v   = np.random.uniform(low=0,high=1,size=5000000)
        phi = 2*np.pi*u
        tht = np.arccos(2*v-1)
        pix = hp.ang2pix(nside,tht,phi)
        idx = np.where(mask[pix]>0)[0]
        ra,dec = tp2rd(tht[idx],phi[idx]) 
        totra  += np.ndarray.tolist(ra)
        totdec += np.ndarray.tolist(dec)
        dens    = len(totra)/area_arcmin2
        print("current density: %.3f pts/arcmin2"%(dens))
    return totra,totdec

# Extract git hash, which will be saved in the header
repo  = git.Repo('./',search_parent_directories=True)
sha   = repo.head.object.hexsha

# These are the star catalogs use in Xiangchong's paper
file_star         = '/pscratch/sd/x/xiangchl/data/catalog/hsc_year3_shape/catalog_others/{field}_star.fits'

# These are the star catalogs used in Tianqing's paper
file_star_used    = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/hscy3_star_moments_psf.csv'
file_star_resv    = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/hscy3_star_moments_nonpsf.csv'

# Main shear catalog
file_shear        = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/shear/{field}_calibrated.fits' 

# Output catalogs in TXPipe format
file_out_shear         = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/shear/txpipe_allfield_shear.h5'
file_out_random        = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/shear/random_cats.hdf5'
file_out_star          = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/txpipe_allfield_star.h5'
file_out_star_nosnrcut = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/txpipe_allfield_star_nosnrcut.h5'
file_out_star_nosnrcut_withareacut = '/global/cfs/cdirs/lsst/groups/WL/projects/txpipe-sys-tests/hsc-y3/star/catalog/txpipe_allfield_star_nosnrcut_withareacut.h5'

#----------------- Uncalibrated shear catalog --------------------
print("-------------------------------------------------------")
print("Creating shear catalog (Xiangchong's catalog)")

# Name of sub-fields
field_list = ['GAMA09H', 'GAMA15H', 'HECTOMAP', 'WIDE12H', 'VVDS', 'XMM']

# Precomputed mulitiplicative and additive biases 
asel_list  = np.array([-99, 0.005757300075048228, 0.007966889498601236, 0.008428564522033983,  0.008382723879301538])
msel_list  = np.array([-99, 0.01711262019090257 , 0.018377595498915943, 0.011807321550085953, -0.0006360553708744804])

table_list = []

# Initialize arrays
tot_objid     = []
tot_ra        = []
tot_dec       = []
tot_sigma_e   = []
tot_m         = []
tot_c1        = []
tot_c2        = []
tot_e1        = []
tot_e2        = []
tot_g1        = []
tot_g2        = []
tot_aselepsf1 = []
tot_aselepsf2 = []
tot_msel      = []
tot_weight    = []
tot_T         = []
tot_objID     = []
tot_psf_e1    = []
tot_psf_e2    = []
tot_psf_T     = []
tot_mag_i     = []
tot_magerr_i  = []
tot_flag      = []
tot_mean_z    = []
tot_sn        = []

for field in field_list:

    print("Processing:", field)
    d = fits.open(file_shear.format(field=field))[1].data

    zbin     = d['hsc_y3_zbin']
    
    # Basic columns needed by TXPipe
    objid    = d['object_id']
    ra       = d['i_ra']
    dec      = d['i_dec']
    sigma_e  = d['i_hsmshaperegauss_derived_rms_e']
    weight   = d['i_hsmshaperegauss_derived_weight']
    m        = d['i_hsmshaperegauss_derived_shear_bias_m']
    c1       = d['i_hsmshaperegauss_derived_shear_bias_c1']
    c2       = d['i_hsmshaperegauss_derived_shear_bias_c2']
    e1       = d['i_hsmshaperegauss_e1']
    e2       = d['i_hsmshaperegauss_e2']
    T        = d['i_sdssshape_shape11']+d['i_sdssshape_shape22']
    mag_i    = d['i_cmodel_mag']
    magerr_i = d['i_cmodel_magerr']
    mean_z   = zbin
    flag     = 1-d['weak_lensing_flag'] # 1 ==valid 0==invalid
    sn       = d['i_cmodel_flux']/d['i_cmodel_fluxerr']
    
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
    #g1        = (tmp_e1 )/(1+msel)
    #g2        = (tmp_e2 )/(1+msel)

    # Extra column
    aselepsf1 = asel*psf_e1
    aselepsf2 = asel*psf_e2

    # mask
    mask     = ((ra>=132.5) & (ra<=140.) & (dec>=1.6) & (dec<5.2)) | (zbin<1)
    mask     = ~mask
    
    # Append to the total list
    tot_objid    += list(objid[mask])
    tot_ra       += list(ra[mask])
    tot_dec      += list(dec[mask])
    tot_sigma_e  += list(sigma_e[mask])
    tot_m        += list(m[mask])
    tot_c1       += list(c1[mask])
    tot_c2       += list(c2[mask])
    tot_e1       += list(e1[mask]) # This is feeding in pdf subtracted debiased e1/e2
    tot_e2       += list(e2[mask]) # This is feeding in pdf subtracted debiased e1/e2
    tot_g1       += list(g1[mask])    # This doesnt get used
    tot_g2       += list(g2[mask])    # This doesnt get used
    tot_aselepsf1+= list(aselepsf1[mask])  
    tot_aselepsf2+= list(aselepsf2[mask])  
    tot_msel     += list(msel[mask])  
    tot_weight   += list(weight[mask])
    tot_T        += list(T[mask])
    tot_psf_e1   += list(psf_e1[mask])
    tot_psf_e2   += list(psf_e2[mask])
    tot_psf_T    += list(psf_T[mask])
    tot_mag_i    += list(mag_i[mask])
    tot_magerr_i += list(magerr_i[mask])
    tot_mean_z   += list(mean_z[mask])
    tot_flag     += list(flag[mask])      
    tot_sn       += list(sn[mask])      
      

# Create a hdf5 file. This will contain both reserved and used stars.
with h5py.File(file_out_shear, 'w') as f:
    g = f.create_group("provenance")
    f.create_group("shear")
    f.attrs['githash']      = sha
    f['shear'].attrs['catalog_type'] = 'hsc'          # This gets read in data_types/types.py
    f['shear/objectId']     = np.asarray(tot_objid)
    f['shear/ra']           = np.asarray(tot_ra)
    f['shear/dec']          = np.asarray(tot_dec)
    f['shear/flags']        = np.asarray(tot_flag)
    f['shear/g1']           = np.asarray(tot_e1)      # Note here that we are saving e1/e2 not g1/g2
    f['shear/g2']           = np.asarray(tot_e2)
    f['shear/aselepsf1']    = np.asarray(tot_aselepsf1)      # Note here that we are saving e1/e2 not g1/g2
    f['shear/aselepsf2']    = np.asarray(tot_aselepsf2)
    f['shear/msel']         = np.asarray(tot_msel)
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
    f['shear/s2n']          = np.asarray(tot_sn)       # Just place a copy of s?n in i-band
    f['shear/snr_i']        = np.asarray(tot_sn) 
    f['shear/weight']       = np.asarray(tot_weight) 



#----------------------- Random catalog -----------------------
# Generate mask using RA/DEC of source galaxies and pick point
# randomly that fall onto the mask. This is mainly to feed into
# TXPipe to generate jackknife patch centers.

dens    = 10 # pts/arcmin2
tht,phi = rd2tp( np.asarray(tot_ra), np.asarray(tot_dec) )
pix     = hp.ang2pix(1024,tht,phi)
mask    = np.bincount(pix,minlength=hp.nside2npix(1024))
mask[mask>0]=1

rand_ra,rand_dec = spherical_pointpick(mask,dens)

with h5py.File(file_out_random, 'w') as f:
    g = f.create_group("provenance")
    f.create_group("randoms")
    f['randoms/bin'] = np.random.randint(0,high=3,size=len(rand_ra))
    f['randoms/comoving_distance'] = np.asarray(np.ones_like(rand_ra)*900)
    f['randoms/ra']  = np.asarray(rand_ra)
    f['randoms/dec'] = np.asarray(rand_dec)
    f['randoms/z']   = np.asarray(np.ones_like(rand_ra)*0.3)

#----------------- Precalibrated shear catalog --------------------
print("-------------------------------------------------------")
print("Creating star catalog without snr cut")

# Initialize arrays
tot_objid   = []
tot_ra      = []
tot_dec     = []
tot_e1      = []
tot_e2      = []
tot_T       = []
tot_psf_e1  = []
tot_psf_e2  = []
tot_psf_T   = []
tot_flag_used  = []
tot_flag_resv  = []
tot_flag_resv2 = []

for field in field_list:

    print('Processing %s'%field)
    catalog   = fits.open(file_star.format(field=field))[1].data

    # objectid
    objid     = catalog['object_id'] 

    # extract ra, dec
    ra, dec   = catalog['i_ra'], catalog['i_dec']

    # set flag for psf vs nonpsf stars
    idx        = np.where(catalog['psf_star']==1)[0]
    flag_used  = np.zeros(len(ra)); flag_used[idx] = 1
    idx        = np.where(catalog['fgcm_non_psf_star']==1)[0] # fgcm matched non-psf star (used)
    flag_resv  = np.zeros(len(ra)); flag_resv[idx] = 1
    idx        = np.where(catalog['non_psf_star']==1)[0]      # plain non-psf star (not used) 
    flag_resv2 = np.zeros(len(ra)); flag_resv2[idx] = 1

    if np.sum(flag_used+flag_resv2) != len(ra):
        sys.exit("numbers of star does not add up")

    # mask -- here we are not masking anything
    mask     = np.full(len(ra), True)

    # extract star_e1, star_e2
    star_mxx = catalog['i_sdssshape_shape11']
    star_myy = catalog['i_sdssshape_shape22']
    star_mxy = catalog['i_sdssshape_shape12']
    star_e1  = 0.5*(star_mxx-star_myy)/(star_mxx+star_myy)
    star_e2  = 0.5*2*star_mxy/(star_mxx+star_myy)
    star_T   = (star_mxx+star_myy)

    # extract model_e1, model_e2
    psf_mxx  = catalog['i_sdssshape_psf_shape11']
    psf_myy  = catalog['i_sdssshape_psf_shape22']
    psf_mxy  = catalog['i_sdssshape_psf_shape12']
    psf_e1   = 0.5*(psf_mxx-psf_myy)/(psf_mxx+psf_myy)
    psf_e2   = 0.5*2*psf_mxy/(psf_mxx+psf_myy)
    psf_T    = (psf_mxx+psf_myy)

    # append to list
    tot_ra         += list(ra[mask] )
    tot_dec        += list(dec[mask])
    tot_e1         += list(star_e1[mask])
    tot_e2         += list(star_e2[mask])
    tot_T          += list(star_T[mask])
    tot_psf_e1     += list(psf_e1[mask])
    tot_psf_e2     += list(psf_e2[mask])
    tot_psf_T      += list(psf_T[mask])
    tot_flag_resv  += list(flag_resv[mask])
    tot_flag_used  += list(flag_used[mask])
    tot_flag_resv2 += list(flag_resv2[mask])


with h5py.File(file_out_star_nosnrcut, 'w') as f:
    f.create_group("provenance")
    f.create_group("stars")
    f['provenance/githash']          = sha
    f['stars'].attrs['catalog_type'] = 'hsc' # This gets read in data_types/types.py
    f['stars/ra']                    =  np.asarray(tot_ra)
    f['stars/dec']                   =  np.asarray(tot_dec)
    f['stars/calib_psf_reserved']    =  np.asarray(tot_flag_resv)
    f['stars/calib_psf_reserved2']   =  np.asarray(tot_flag_resv2)
    f['stars/calib_psf_used']        =  np.asarray(tot_flag_used)
    f['stars/measured_e1']           =  np.asarray(tot_e1)
    f['stars/measured_e2']           = -np.asarray(tot_e2) 
    f['stars/measured_T']            =  np.asarray(tot_T)
    f['stars/model_e1']              =  np.asarray(tot_psf_e1)
    f['stars/model_e2']              = -np.asarray(tot_psf_e2)
    f['stars/model_T']               =  np.asarray(tot_psf_T)

print('Total number of psf stars         : %d'%(np.sum(np.asarray(tot_flag_used))) )
print('Total number of non-psf stars     : %d'%(np.sum(np.asarray(tot_flag_resv2))) )
print('Total number of fgcm non-psf stars: %d'%(np.sum(np.asarray(tot_flag_resv))) )
print('Saved: %s'%file_out_star_nosnrcut)


print("-------------------------------------------------------")
print("Creating star catalog without snr cut (but with area cut and blacklisted stars)")

# blacklist
blacklist=np.array([40990759851148197, 40994891609691304, 43137148282486296,
                    44165191654463776, 41197343483105687, 42261666443828153,
                    42270466831839566, 42275131166318353, 42283798410330727,
                    69608324512881297, 70347874931599131, 70360231552509046,
                    70387165292402692, 70399964294971996, 41055918799982127,
                    42133989951034055, 42151715281063569, 42155417542873456,
                    42186903948122558, 42213000169412238, 42213004464380385,
                    43251368642743678, 43255508991233602, 43259322922177595,
                    44306770956414980, 41619706272026521, 41650466827820573,
                    44782034857515908])

# Initialize arrays
tot_objid   = []
tot_ra      = []
tot_dec     = []
tot_e1      = []
tot_e2      = []
tot_T       = []
tot_psf_e1  = []
tot_psf_e2  = []
tot_psf_T   = []
tot_flag_used  = []
tot_flag_resv  = []
tot_flag_resv2 = []


for field in field_list:

    print('Processing %s'%field)
    catalog   = fits.open(file_star.format(field=field))[1].data

    # objectid
    objid     = catalog['object_id'] 

    # extract ra, dec
    ra, dec   = catalog['i_ra'], catalog['i_dec']

    # set flag for psf vs nonpsf stars
    idx        = np.where(catalog['psf_star']==1)[0]
    flag_used  = np.zeros(len(ra)); flag_used[idx] = 1
    idx        = np.where(catalog['fgcm_non_psf_star']==1)[0] # fgcm matched non-psf star (used)
    flag_resv  = np.zeros(len(ra)); flag_resv[idx] = 1
    idx        = np.where(catalog['non_psf_star']==1)[0]      # plain non-psf star (not used) 
    flag_resv2 = np.zeros(len(ra)); flag_resv2[idx] = 1

    if np.sum(flag_used+flag_resv2) != len(ra):
        sys.exit("numbers of star does not add up")


    # mask -- masking bad region and any star in the blacklist
    mask     = (ra>=132.5) & (ra<=140.) & (dec>=1.6) & (dec<5.2) 
    mask     = ~mask

    maskb    = np.isin(objid,blacklist)
    maskb    = ~maskb

    mask     = mask*maskb 
    

    # extract star_e1, star_e2
    star_mxx = catalog['i_sdssshape_shape11']
    star_myy = catalog['i_sdssshape_shape22']
    star_mxy = catalog['i_sdssshape_shape12']
    star_e1  = 0.5*(star_mxx-star_myy)/(star_mxx+star_myy)
    star_e2  = 0.5*2*star_mxy/(star_mxx + star_myy)
    star_T   = (star_mxx+star_myy)

    # extract model_e1, model_e2
    psf_mxx  = catalog['i_sdssshape_psf_shape11']
    psf_myy  = catalog['i_sdssshape_psf_shape22']
    psf_mxy  = catalog['i_sdssshape_psf_shape12']
    psf_e1   = 0.5*(psf_mxx-psf_myy)/(psf_mxx+psf_myy)
    psf_e2   = 0.5*2*psf_mxy/(psf_mxx +psf_myy)
    psf_T    = (psf_mxx+psf_myy)

    tot_objid      += list(objid[mask] )
    tot_ra         += list(ra[mask] )
    tot_dec        += list(dec[mask])
    tot_e1         += list(star_e1[mask])
    tot_e2         += list(star_e2[mask])
    tot_T          += list(star_T[mask])
    tot_psf_e1     += list(psf_e1[mask])
    tot_psf_e2     += list(psf_e2[mask])
    tot_psf_T      += list(psf_T[mask])
    tot_flag_resv  += list(flag_resv[mask])
    tot_flag_used  += list(flag_used[mask])
    tot_flag_resv2 += list(flag_resv2[mask])


with h5py.File(file_out_star_nosnrcut_withareacut, 'w') as f:
    f.create_group("provenance")
    f.create_group("stars")
    f['provenance/githash']          = sha
    f['stars'].attrs['catalog_type'] = 'hsc' # This gets read in data_types/types.py
    f['stars/objid']                 =  np.asarray(tot_objid)
    f['stars/ra']                    =  np.asarray(tot_ra)
    f['stars/dec']                   =  np.asarray(tot_dec)
    f['stars/calib_psf_reserved']    =  np.asarray(tot_flag_resv)
    f['stars/calib_psf_reserved2']   =  np.asarray(tot_flag_resv2)
    f['stars/calib_psf_used']        =  np.asarray(tot_flag_used)
    f['stars/measured_e1']           =  np.asarray(tot_e1)
    f['stars/measured_e2']           = -np.asarray(tot_e2) 
    f['stars/measured_T']            =  np.asarray(tot_T)
    f['stars/model_e1']              =  np.asarray(tot_psf_e1)
    f['stars/model_e2']              = -np.asarray(tot_psf_e2)
    f['stars/model_T']               =  np.asarray(tot_psf_T)

print('Total number of psf stars         : %d'%(np.sum(np.asarray(tot_flag_used))) )
print('Total number of non-psf stars     : %d'%(np.sum(np.asarray(tot_flag_resv2))) )
print('Total number of fgcm non-psf stars: %d'%(np.sum(np.asarray(tot_flag_resv))) )
print('Saved: %s'%file_out_star_nosnrcut_withareacut)


#----------------- Star catalog (resv) --------------------
print("-------------------------------------------------------")
print("Creating star catalog with snr cut (Tianqing's catalog)")
# Note Tianqing's paper does e_psf x M4 which i.e. not g_psf
# So there there should be no factor of 1/2

catalog  = pd.read_csv(file_star_resv, header = 0)

# Apply cut that extracts sources with S/N > 180
# The raw catalog should already have this cut applied so this shouldn't do anything
catalog  = catalog[catalog['snr'] > 180] 

# objectid
r_objid     = catalog['object_id'] 

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
r_psf_T    = (r_psf_mxx+r_psf_myy)

# extract diff_e1, diff_e2
r_de1      = r_psf_e1 - r_star_e1
r_de2      = r_psf_e2 - r_star_e2

# Extract higher-order moments
r_psf_m40 = catalog['model_moment40'] 
r_psf_m04 = catalog['model_moment04']
r_psf_m13 = catalog['model_moment13']
r_psf_m31 = catalog['model_moment31']
r_psf_M4_e1 = (r_psf_m40-r_psf_m04)
r_psf_M4_e2 = (r_psf_m13+r_psf_m31)*2

r_star_m40 = catalog['star_moment40'] 
r_star_m04 = catalog['star_moment04']
r_star_m13 = catalog['star_moment13']
r_star_m31 = catalog['star_moment31']
r_star_M4_e1 = (r_star_m40-r_star_m04)
r_star_M4_e2 = (r_star_m13+r_star_m31)*2

#----------------- Star catalog (used) --------------------
catalog  = pd.read_csv(file_star_used, header = 0)

# objectid
u_objid     = catalog['object_id'] 

# extract ra, dec
u_ra, u_dec  = catalog['i_ra'], catalog['i_dec']

# extract star_e1, star_e2
# Note: g1_psf/g2_psf = 0.5*e1_psf/e2_psf. See just below eq 5
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

# Extract higher-order moments
u_psf_m40 = catalog['model_moment40'] 
u_psf_m04 = catalog['model_moment04']
u_psf_m13 = catalog['model_moment13']
u_psf_m31 = catalog['model_moment31']
u_psf_M4_e1 = (u_psf_m40-u_psf_m04)
u_psf_M4_e2 = (u_psf_m13+u_psf_m31)*2

u_star_m40 = catalog['star_moment40'] 
u_star_m04 = catalog['star_moment04']
u_star_m13 = catalog['star_moment13']
u_star_m31 = catalog['star_moment31']
u_star_M4_e1 = (u_star_m40-u_star_m04)
u_star_M4_e2 = (u_star_m13+u_star_m31)*2

# Compute the total number of stars and create a flag column
totstars   = len(u_ra)+len(r_ra) 
tmp        = np.concatenate([ np.ones(len(r_ra))*3, np.ones(len(u_ra))*4  ])
flag_resv  = np.zeros(totstars); flag_resv[:len(r_ra)] = 1
flag_used  = np.zeros(totstars); flag_used[flag_resv==0] = 1

# Create a hdf5 file. This will contain both reserved and used stars.
with h5py.File(file_out_star, 'w') as f:
    f.create_group("provenance")
    f.create_group("stars")
    f['provenance/githash']          = sha
    f['stars'].attrs['catalog_type'] = 'hsc' # This gets read in data_types/types.py
    f['stars/objid']                 = np.concatenate([r_objid ,u_objid ])
    f['stars/ra']                    = np.concatenate([r_ra ,u_ra ])
    f['stars/dec']                   = np.concatenate([r_dec,u_dec])
    f['stars/calib_psf_reserved']    = flag_resv
    f['stars/calib_psf_used']        = flag_used
    f['stars/measured_e1']           = np.concatenate([r_star_e1   ,  u_star_e1])
    f['stars/measured_e2']           = np.concatenate([-r_star_e2  , -u_star_e2])
    f['stars/measured_T']            = np.concatenate([r_star_T    ,  u_star_T])
    f['stars/model_e1']              = np.concatenate([r_psf_e1    ,  u_psf_e1])
    f['stars/model_e2']              = np.concatenate([-r_psf_e2   , -u_psf_e2])
    f['stars/model_T']               = np.concatenate([r_psf_T     ,  u_psf_T])
    f['stars/model_moment4_e1']      = np.concatenate([r_psf_M4_e1 ,  u_psf_M4_e1])
    f['stars/model_moment4_e2']      = np.concatenate([r_psf_M4_e2 ,  u_psf_M4_e2])
    f['stars/measured_moment4_e1']   = np.concatenate([r_star_M4_e1,  u_star_M4_e1])
    f['stars/measured_moment4_e2']   = np.concatenate([r_star_M4_e2,  u_star_M4_e2])
    # This is follwoing the sign of M4 used in Tianqing's paper.

print('Total number of psf stars         : %d'%(np.sum(np.asarray(flag_used))) )
print('Total number of non-psf stars     : %d'%(np.sum(np.asarray(flag_resv))) )
print('Saved: %s'%file_out_star)

# NOTE1: de1,de2 are defined as 
# de1 = model_e1 - meas_e1
# de2 = model_e2 - meas_e2
# and what is saved is -de1, -de2


print('Done')
