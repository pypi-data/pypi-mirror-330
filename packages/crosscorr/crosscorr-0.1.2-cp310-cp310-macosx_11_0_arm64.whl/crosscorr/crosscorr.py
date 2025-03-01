# from .CCF_1d import CCF_1d
# from .CCF_3d import CCF_3d
# import CCF_1d, CCF_3d
# from . import CCF_1d, CCF_3d
# We don't need to do relative import as these are extensions as part of setup.py
from . import _CCF_1d, _CCF_3d, _CCF_pix
import numpy as np
import matplotlib.pyplot as plt


def calculate_ccf(w, f, v, mask_l, mask_h, mask_w, berv=0.,
                  wavel_clip_edges=0., method='doppler_3d', verbose=True):
    """
    Calculate a weighted binary mask CCF.

    INPUT:
        w - array of wavelengths for one order
        f - array of fluxes for one order
        v - velocity grid to loop over in km/s (OR grid in pixels)
        mask_l - left edges of binary mask
        mask_h - right edges of binary mask
        mask_w - weight of binary mask
        berv - barycentric velocity in km/s
        wavel_clip_edges - do not use lines that are this close to the edge of the order
        method - 'doppler_1d' or 'doppler_3d' adopted from Gummi's code for performing CCF in redshift space, 'pixel' for CCF in pixel space
        verbose: print diagnostics

    OUTPUT:
        ccf - array of ccf evaluated at velocity grid v

    NOTES:
        - Uses the CCF fortran algorithm in CERES. Super fast.
        - Note that that algorithm uses the 1d Doppler EQ.
        - wavel_clip_edges # THE LAST ARGUMENT CHANGES GJ 905 FROM -75.8 to -77.8km/s
        - RCT updated June 21, 2019: modified to enable CCF in pixel space
    """
    N = len(v)
    ccf = np.zeros(N)
    mm = np.isfinite(f)
    w = w[mm]
    f = f[mm]
    # print(w.min(), w.max())
    II = np.where((mask_l > wavel_clip_edges + w.min()) & (mask_h < w.max() - wavel_clip_edges))
    # print(II)
    # print(len(II[0]))
    # This is an additional scaling parameter in the CERES CCF generation, we don't need that so set to 1
    sn = np.ones(len(f))
    # print(len(mask_l > wavel_clip_edges + w.min()))
    # print(sum(mask_l > wavel_clip_edges + w.min()))
    # print(sum(mask_h < w.max() - wavel_clip_edges))
    # print(mask_l)
    # print(wavel_clip_edges + w.min())
    if method == 'doppler_3d':
        try:
            for k in range(N):
                ccf[k] = _CCF_3d.ccf(mask_l[II],
                                     mask_h[II],
                                     w,
                                     f,
                                     mask_w[II],
                                     sn,  # Additional SNR scaling factor, just setting to 1
                                     v[k],
                                     berv,
                                     0.)  # Additional velocity that is not needed
            return ccf
        except Exception as e:
            if verbose: print(e)
            return np.zeros(len(v))
    elif method == 'doppler_1d':
        try:
            for k in range(N):
                ccf[k] = _CCF_1d.ccf(mask_l[II],
                                     mask_h[II],
                                     w,
                                     f,
                                     mask_w[II],
                                     sn,  # Additional SNR scaling factor, just setting to 1
                                     v[k] - berv,
                                     0.)  # Additional velocity that is not needed
            return ccf
        except Exception as e:
            if verbose: print(e)
            return np.zeros(len(v))
    elif method == 'pixel':
        try:
            for k in range(N):
                # print v[k]
                ccf[k] = _CCF_pix.ccf(mask_l[II],
                                      mask_h[II],
                                      w,
                                      f,
                                      mask_w[II],
                                      sn,
                                      v[k] - berv,
                                      0.,
                                      0.)
            return ccf
        except Exception as e:
            if verbose: print(e)
            return np.zeros(len(v))
    else:
        raise StandardError()


def calculate_ccf_for_hpf_orders(w, f, v, M, berv, orders=[3, 4, 5, 6, 14, 15, 16, 17, 18], plot=False, ax=None,
                                 color=None, subslice=None):
    """
    Loop through and Calculate CCFs for all HPF orders
    
    INPUT:
        w - wavelength matrix (of 28 orders)
        f - flux matrix for that wavelength array (of 28 orders)
        M - mask object
        berv - barycentric correction
        orders = orders to calculate. If only using a subset of 28 orders then the CCF for other orders will be 0s
    
    OUTPUT:
        An array the size of (len(v),28) with CCF
        
    EXAMPLE:
        M = mask.Mask(filename="0_MASKS/20190124_gj699/tellmask/all.mas",disp=2.,constant_v=True)
        v = np.linspace(-15,15,161)
        orders = [5]#[3,4,5,6],14,15,16,17
        c = calculate_ccf_for_hpf_orders(w,f,v,M,berv,orders=orders,plot=True)
    """
    num_hpf_orders = 28
    N = len(orders)
    if ax is None and plot is True:
        fig, ax = plt.subplots()
    ccf_array = np.zeros((num_hpf_orders + 1, len(v)))
    for o in orders:
        ccf_array[o] = calculate_ccf(w[o], f[o], v, M.wi, M.wf, M.weight, berv)
        if plot:
            if color is None:
                ax.plot(v, ccf_array[o] / np.nanmax(ccf_array[o]), label="o={}".format(o))
            else:
                ax.plot(v, ccf_array[o] / np.nanmax(ccf_array[o]), label="o={}".format(o), color=color)
    ccf_array[num_hpf_orders] = np.nansum(ccf_array[orders], axis=0)
    if plot:
        ax.legend(loc="lower right", fontsize=10)
        ax.set_xlabel('v [km/s]')
        ax.set_ylabel('Normalized flux')
        ax.set_title('CCF')
    return ccf_array


def calculate_ccf_for_neid_orders(w, f, v, M, berv, orders=[55, 56], plot=False, ax=None, color=None, subslice=None,
                                  num_neid_orders=94):
    """
    Loop through and Calculate CCFs for all HPF orders
    
    INPUT:
        w - wavelength matrix (of 28 orders)
        f - flux matrix for that wavelength array (of 28 orders)
        M - mask object
        berv - barycentric correction
        orders = orders to calculate. If only using a subset of 28 orders then the CCF for other orders will be 0s
    
    OUTPUT:
        An array the size of (len(v),28) with CCF
        
    EXAMPLE:
        M = mask.Mask(filename="0_MASKS/20190124_gj699/tellmask/all.mas",disp=2.,constant_v=True)
        v = np.linspace(-15,15,161)
        orders = [5]#[3,4,5,6],14,15,16,17
        c = calculate_ccf_for_hpf_orders(w,f,v,M,berv,orders=orders,plot=True)
    """

    N = len(orders)
    if ax is None and plot is True:
        fig, ax = plt.subplots()
    ccf_array = np.zeros((num_neid_orders + 1, len(v)))
    for o in (np.array(orders) - 10):
        ccf_array[o] = calculate_ccf(w[o], f[o], v, M.wi, M.wf, M.weight, berv)
        if plot:
            if color is None:
                ax.plot(v, ccf_array[o] / np.nanmax(ccf_array[o]), label="o={}".format(o + 10))
            else:
                ax.plot(v, ccf_array[o] / np.nanmax(ccf_array[o]), label="o={}".format(o + 10), color=color)
    ccf_array[num_neid_orders] = np.nansum(ccf_array[(np.array(orders) - 10)], axis=0)
    if plot:
        ax.legend(loc="lower right", fontsize=10)
        ax.set_xlabel('v [km/s]')
        ax.set_ylabel('Normalized flux')
        ax.set_title('CCF')
    return ccf_array
