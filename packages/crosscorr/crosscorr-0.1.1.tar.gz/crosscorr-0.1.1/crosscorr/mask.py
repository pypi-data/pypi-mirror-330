from __future__ import print_function
import numpy as np
import os
import astropy.io.fits
#try:
#    from . import airtovac
#except Exception:
#    import airtovac
from .airtovac import airtovac
import astropy.constants as aconst

HARPSMASKDIR = os.path.join(os.path.dirname(__file__),"data","harps","masks")
ESPRESSOMASKDIR = os.path.join(os.path.dirname(__file__),"data","espresso","masks")
HPFMASKDIR = os.path.join(os.path.dirname(__file__),"data","hpf","masks")
G2MASK = os.path.join(HARPSMASKDIR,"G2.mas")
K5MASK = os.path.join(HARPSMASKDIR,"K5.mas")
M2MASK = os.path.join(HARPSMASKDIR,"M2.mas")
ESPRESSO_M3MASK = os.path.join(ESPRESSOMASKDIR,"ESPRESSO_M3.fits")
G2_6300MASK = os.path.join(HARPSMASKDIR,"G2_6300.mas")
G2_5000_6300MASK = os.path.join(HARPSMASKDIR,"G2_5000_6300.mas")
HPFGJ699MASK = os.path.join(HPFMASKDIR,'gj699_combined_stellarframe.mas')
HPFSPECMATCHMASK = os.path.join(HPFMASKDIR,'specmatch_mask.mas')

class Mask:
    def __init__(self,filename=G2MASK,constant_v=True,disp=2.,use_airtovac=False,espresso=False,verbose=False):
        """
        A simple mask class.
        Reads in a .mas file that has the following columns:
         left    right     weights
        
    INPUT:
        filename - mask filename
            constant_v - use a constant velocity width (RECOMMENDED)
            dispersion - half-width of the constant velocity width in km/s
            use_airtovac: convert from airwavelength to vacuum. 
                          Only for HARPS, as the HPF masks are in vacuum 
                          wavelength already.

    OUTPUT:
        No output, main parameters of the object are:
            self.wi - left-edge wavelengths of mask
            self.wf - right-edge wavelegnths of mask
            self.weight - mask weights

    EXAMPLE:
            M = mask.Mask(filename="../data/hpf/masks/gj699.mas",
              disp=2.,constant_v=True)
        
        """
        if verbose:
            print("AIRTOVAC (TRUE for HARPS, FALSE TRUE HPF): ",use_airtovac)
        if espresso is False:
            self.wi, self.wf, self.weight = np.loadtxt(filename,unpack=True,dtype=np.float64)
        else:
            data = astropy.io.fits.getdata(filename)
            self.wmid = data['lambda']
            self.weight = data['contrast']
            self.wi = self.wmid # hack for now
            self.wf = self.wmid # hack for now
        if use_airtovac:
            self.wi = airtovac(self.wi)
            self.wf = airtovac(self.wf)
        self.wmid = 0.5*(self.wi+self.wf)
        width_in_km = self.wmid * disp / (aconst.c.value/1.e3)
        self.wi_v = self.wmid - width_in_km/2.
        self.wf_v = self.wmid + width_in_km/2.
        if constant_v:
            self.wi = self.wi_v
            self.wf = self.wf_v

#class Mask:
#    def __init__(self,filename=G2MASK,constant_v=True,disp=2.,use_airtovac=False,espresso=False):
#        """
#        A simple mask class.
#        Reads in a .mas file that has the following columns:
#         left    right     weights
#        
#    INPUT:
#        filename - mask filename
#            constant_v - use a constant velocity width (RECOMMENDED)
#            dispersion - half-width of the constant velocity width in km/s
#            use_airtovac: convert from airwavelength to vacuum. 
#                          Only for HARPS, as the HPF masks are in vacuum 
#                          wavelength already.
#
#    OUTPUT:
#        No output, main parameters of the object are:
#            self.wi - left-edge wavelengths of mask
#            self.wf - right-edge wavelegnths of mask
#            self.weight - mask weights
#
#    EXAMPLE:
#            M = mask.Mask(filename="../data/hpf/masks/gj699.mas",
#              disp=2.,constant_v=True)
#        
#        """
#        print("AIRTOVAC (TRUE for HARPS, FALSE TRUE HPF): ",use_airtovac)
#        self.wi, self.wf, self.weight = np.loadtxt(filename,unpack=True,dtype=np.float64)
#        if use_airtovac:
#            self.wi = airtovac(self.wi)
#            self.wf = airtovac(self.wf)
#        self.wmid = 0.5*(self.wi+self.wf)
#        width_in_km = self.wmid * disp / (aconst.c.value/1.e3)
#        self.wi_v = self.wmid - width_in_km/2.
#        self.wf_v = self.wmid + width_in_km/2.
#        if constant_v:
#            self.wi = self.wi_v
#            self.wf = self.wf_v
