import numpy as np
import astropy.units as u
import astropy.constants as const
import scipy.constants as spconst
#from astropy.cosmology import Planck15 as cosmo
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70.0, Om0=0.3, Tcmb0=2.725)
import M2_ProposalTools.numerical_integration as ni
from astropy.coordinates import Angle #
from scipy.ndimage import filters
import M2_ProposalTools.FilterImages as FI
import M2_ProposalTools.MakeRMSmap as MRM
from astropy.wcs import WCS
from astropy.io import fits                # To read/write fits
import sys,os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


from importlib import reload
MRM=reload(MRM)
defaultYM = 'A10'

def inst_params(instrument):
    """
    Returns a Compton y profile for an input pressure profile.
    
    Parameters
    ----------
    instrument : str
       Options are "MUSTANG", "MUSTANG2", "NIKA", "NIKA2", "BOLOCAM", and "ACT90"

    Returns
    -------
    output : tuple
       A tuple containing fwhm1,norm1,fwhm2,norm2,fwhm,smfw,freq,FoV
    """

    if instrument == "MUSTANG":
        fwhm1 = 8.7*u.arcsec  # arcseconds
        norm1 = 0.94          # normalization
        fwhm2 = 28.4*u.arcsec # arcseconds
        norm2 = 0.06          # normalization
        fwhm  = 9.0*u.arcsec
        smfw  = 10.0*u.arcsec
        freq  = 90.0*u.gigahertz # GHz
        FoV   = 42.0*u.arcsec #

    ### I don't use the double Guassian much. The only idea was to use it to
    ### get a better estimate of the beam volume, but we know that is variable.
    if instrument == "MUSTANG2":
        fwhm1 = 8.9*u.arcsec  # arcseconds
        norm1 = 0.97          # normalization
        fwhm2 = 25.0*u.arcsec # arcseconds
        norm2 = 0.03          # normalization
        fwhm  = 9.0*u.arcsec
        smfw  = 10.0*u.arcsec
        freq  = 90.0*u.gigahertz # GHz
        FoV   = 4.25*u.arcmin 
        
    if instrument == "NIKA":
        fwhm1 = 8.7*2.0*u.arcsec  # arcseconds
        norm1 = 0.94     # normalization
        fwhm2 = 28.4*2.0*u.arcsec # arcseconds
        norm2 = 0.06     # normalization
        fwhm  = 18.0*u.arcsec
        smfw  = 10.0*u.arcsec
        freq  = 150.0*u.gigahertz    # GHz
        FoV   = 2.15*u.arcmin 
        
    if instrument == "NIKA2":
        fwhm1 = 8.7*2.0*u.arcsec  # arcseconds
        norm1 = 0.94     # normalization
        fwhm2 = 28.4*2.0*u.arcsec # arcseconds
        norm2 = 0.06     # normalization
        fwhm  = 18.0*u.arcsec
        smfw  = 10.0*u.arcsec
        freq  = 150.0*u.gigahertz    # GHz
        FoV   = 6.5*u.arcmin 
        
    if instrument == "BOLOCAM":
        fwhm1 = 8.7*7.0*u.arcsec  # arcseconds
        norm1 = 0.94     # normalization
        fwhm2 = 28.4*7.0*u.arcsec # arcseconds
        norm2 = 0.06     # normalization
        fwhm  = 58.0*u.arcsec
        smfw  = 60.0*u.arcsec
        freq  = 140.0*u.gigahertz    # GHz
        FoV   = 8.0*u.arcmin * (u.arcmin).to("arcsec")
        
    if instrument == "ACT90":
        fwhm1 = 2.16*60.0*u.arcsec  # arcseconds
        norm1 = 1.0     # normalization
        fwhm2 = 1.0*u.arcsec # arcseconds
        norm2 = 0.00     # normalization
        fwhm  = 2.16*60.0*u.arcsec
        smfw  = 2.0*60.0*u.arcsec
        freq  = 97.0*u.gigahertz    # GHz
        FoV   = 60.0*u.arcmin #* (u.arcmin).to("arcsec")
        
    if instrument == "ACT150":
        fwhm1 = 1.3*60.0*u.arcsec  # arcseconds
        norm1 = 1.0     # normalization
        fwhm2 = 1.0*u.arcsec # arcseconds
        norm2 = 0.00     # normalization
        fwhm  = 1.3*60.0*u.arcsec
        smfw  = 1.2*60.0*u.arcsec
        freq  = 148.0*u.gigahertz    # GHz
        FoV   = 60.0*u.arcmin #* (u.arcmin).to("arcsec")
        
#    else:
#        fwhm1=9.0*u.arcsec ; norm1=1.0
#        fwhm2=30.0*u.arcsec ; norm2=0.0
#        fwhm = 9.0*u.arcsec ; smfw = 10.0*u.arcsec
#        freq = 90.0*u.gigahertz 
#        FoV   = 1.0*u.arcmin * (u.arcmin).to("arcsec")
#        
#    import pdb; pdb.set_trace()

    return fwhm1,norm1,fwhm2,norm2,fwhm,smfw,freq,FoV


def get_d_ang(z):
    """    
    Parameters
    ----------
    z : float
       The redshift.

    Returns
    -------
    d_ang : quantity
       The angular distance (with units of length)
    """

    d_ang = cosmo.comoving_distance(z) / (1.0 + z)

    return d_ang

def get_cosmo():
    """    
    Parameters
    ----------

    Returns
    -------
    cosmo : class
       Returns a cosmo object from astropy.cosmology
    """

    return cosmo

def Theta500_from_M500_z(m500,z):
    """    
    Parameters
    ----------
    m500 : Quantity
       A cluster's mass: M500
    z : float
       The cluster's redshift

    Returns
    -------
    theta500 : float
       R500 on the sky, in radians
    """
    
    d_ang = get_d_ang(z)
    r500,p500 = R500_P500_from_M500_z(m500,z)
    r500ang   = (r500/d_ang).decompose()
    #print(r500ang)
    
    return r500ang.value

def M500_from_R500_z(R500,z):
    """    
    Parameters
    ----------
    R500 : Quantity
       A cluster's R500, in physical length units (e.g. kpc)
    z : float
       The cluster's redshift

    Returns
    -------
    M500 : quantity
       M500, in solar masses.
    """

    dens_crit = cosmo.critical_density(z)
    E   = cosmo.H(z)/cosmo.H(0)
    h70 = (cosmo.H(0) / (70.0*u.km / u.s / u.Mpc))

    M500 = (4*np.pi/3)* dens_crit * R500**3 * 500
    M500 = M500.to("M_sun")

    return M500

def R500_P500_from_M500_z(M500,z):
    """    
    Parameters
    ----------
    m500 : Quantity
       A cluster's mass: M500
    z : float
       The cluster's redshift

    Returns
    -------
    R500 : quantity
       R500 in physical units (e.g. kpc)
    P500 : quantity
       P500 in units of pressure
    """

    dens_crit = cosmo.critical_density(z)
    E   = cosmo.H(z)/cosmo.H(0)
    h70 = (cosmo.H(0) / (70.0*u.km / u.s / u.Mpc))

    
    #P500 = (1.65 * 10**-3) * ((E)**(8./3)) * ((
    #    M500 * h70)/ ((3*10**14) * const.M_sun)
    #    )**(2./3) * h70**2 * u.keV / u.cm**3
    P500 = (1.65 * 10**-3) * ((E)**(8./3)) * ((
        M500 * h70)/ ((3*10**14 * h70**(-1)) * const.M_sun)
        )**(2./3+0.11) * h70**2 * u.keV / u.cm**3
    R500 = (3 * M500/(4*np.pi * 500 * dens_crit))**(1./3)

    return R500, P500

def y_delta_from_mdelta(m_delta,z,delta=500,ycyl=False,YMrel=defaultYM,h70=1.0):
    """
    Finds A,B (scaling law terms, in get_AAA_BBB()) and applies them.

    Parameters
    ----------
    m_delta : float
       A cluster's mass at some delta (e.g. M500 or M2500) in solar masses, as a value.
    z : float
       The cluster's redshift
    delta : float
       Specify the delta (500 or 2500)
    ycyl : bool
       Do you want y_cyl or y_Sph?
    YMrel : str
       Which Y-M relation to use. The default is "A10" other options include "M12", "P17".
    h70 : float
       Confirm the Hubble parameter at z=0, relative to 70 km/s/Mpc.

    Returns
    -------
    y_delta : float
       The corresponding integrated Y value
    """
    
    h       = cosmo.H(z)/cosmo.H(0)
    d_a     = get_d_ang(z).to('Mpc').value
    iv      = h**(-1./3)*d_a

    #print(YMrel)
    AAA,BBB = get_AAA_BBB(YMrel,delta,ycyl=ycyl,h70=h70)

    y_delta = m_delta**AAA * 10**BBB / (iv.value**2)

    return y_delta

def get_AAA_BBB(YMrel,delta,ycyl=False,h70=1.0):
    """
    Basically just a repository of Y-M relations.
    YMrel must be either:
       (1) 'A10' (Arnaud 2010)
       (2) 'A11' (Anderson 2011)
       (3) 'M12' (Marrone 2012)
       (4) 'P14' (Planck 2014), or
       (5) 'P17' (Planelles 2017)

    All are converted to Y = 10^BBB * M^AAA; mass (M) is in units of solar masses; Y is in Mpc^2 (i.e. with D_A^2 * E(z)^-2/3)

    Parameters
    ----------
    YMrel : str
       As indicated above
    delta : float
       The density contrast for which you want a scaling relation
    ycyl : bool
       Do you want a y_cyl relation or y_Sph?
    h70 : float
       Hubble parameter normalization.
    
    Returns
    -------
    AAA,BBB : tuple
       Scaling relation slope and normalization
   
    """

    if delta == 2500:
        if YMrel == 'A10':
            AAA    = 1.637;   BBB = -28.13  # From Comis+ 2011
        #if ycyl:
        #    AAA = 1.60;   BBB = -27.4   # From Comis+ 2011
        if YMrel == 'A11':
            AAA    = 1.637;   BBB = -28.13  # From Comis+ 2011
        #if ycyl:
        #    AAA = 1.60;   BBB = -27.4   # From Comis+ 2011
        elif YMrel == 'M12':
            #BBB = -29.66909090909 ???
            BBB = -30.669090909090908
            AAA = 1.0 / 0.55
        elif YMrel == 'M12-SS':
            BBB = -28.501666666666667
            AAA = 5.0/3.0
        elif YMrel == 'P14':
            AAA = 1.755          #### NOT PLANCK!!!
            BBB = -29.6833076    # -4.585
        elif YMrel == 'P17':     # Planelles 2017
            AAA = 1.755
            BBB = -29.6833076    # -4.585
        elif YMrel == 'H20':     #### NOT He et al. 2020!!!
            AAA = 1.755
            BBB = -29.6833076    # -4.585
        else:
            print('using Comis+ 2011 values')
            
    elif delta == 500:
        if YMrel == 'A10':
            AAA   = 1.78
            Jofx  = 0.7398 if ycyl else 0.6145  # Actually I(x) in A10, but, it plays the same role, so use this variable
            #print(Jofx,' ycyl: ',ycyl)
            Bofx  = 2.925e-5 * Jofx * h70**(-1) / (3e14/h70)**AAA
            #BBB = np.log10(Bofx.value)
            BBB = np.log10(Bofx)
        elif YMrel == 'A11':
            Btabulated = 14.06 # But this is some WEIRD Y_SZ (M_sun * keV) - M relation
            Bconversion = -18.855
            Aconversion = -24.176792495381836
            AAA    = 1.67;   BBB = Btabulated + Bconversion + Aconversion  # Anderson+ 2011, Table 6
        #if ycyl:
        #    AAA = 1.60;   BBB = -27.4   # From Comis+ 2011
        elif YMrel == 'M12':
            #BBB = -30.66909090909 # BBB = -16.567
            BBB = -37.65227272727
            AAA = 1.0 / 0.44
        elif YMrel == 'M12-SS':
            BBB = -28.735
            AAA = 5.0/3.0
        elif YMrel == 'P14':
            AAA = 1.79
            BBB = -30.6388907    # 
        elif YMrel == 'P17':
            AAA = 1.685
            BBB = -29.0727644    # -4.585
        elif YMrel == 'H20':
            AAA = 1.790
            BBB = -30.653047     # -4.739
        else:
            print('Woops')
            #print(YMrel,delta)
    else:
        import pdb;pdb.set_trace()

    return AAA,BBB

def get_xymap(map,pixsize,xcentre=[],ycentre=[],oned=True,cpix=0):
    """
    Returns a map of X and Y offsets (from the center) in arcseconds.

    INPUTS:
    -------
    map : a 2D array 
       for which you want to construct the xymap
    pixsize : a quantity 
       (with units of an angle)
    xcentre : float
       The number of the pixel that marks the X-centre of the map
    ycentre : float
       The number of the pixel that marks the Y-centre of the map
    oned : bool
       Specify 1D for most cases pertaining to fitting models.
    cpix : float
       Specify if pixel indexing has an offset (e.g. 0 or 1)

    """

    #cpix=0
    ny,nx=map.shape
    ypix = pixsize.to("arcsec").value # Generally pixel sizes are the same...
    xpix = pixsize.to("arcsec").value # ""
    if xcentre == []:
        xcentre = nx/2.0
    if ycentre == []:
        ycentre = ny/2.0

    #############################################################################
    ### Label w/ the transpose that Python imposes?
    #y = np.outer(np.zeros(ny)+1.0,np.arange(0,xpix*(nx), xpix)- xpix* xcentre)   
    #x = np.outer(np.arange(0,ypix*(ny),ypix)- ypix * ycentre, np.zeros(nx) + 1.0)
    #############################################################################
    ### Intuitive labelling:
    x = np.outer(np.zeros(ny)+1.0,np.arange(nx)*xpix- xpix* xcentre)   
    y = np.outer(np.arange(ny)*ypix- ypix * ycentre, np.zeros(nx) + 1.0)

    #import pdb;pdb.set_trace()
    if oned == True:
        x = x.reshape((nx*ny)) #How important is the tuple vs. integer?
        y = y.reshape((nx*ny)) #How important is the tuple vs. integer?

    
    return x,y

def make_rmap(xymap):
    """
    Return a map of radii

    Parameters
    ----------
    xymap : tuple(class:`numpy.ndarray`)
       A tuple of x- and y-coordinates

    Returns
    -------
    rmap : class:`numpy.ndarray`
       A map of radii
    """

    rmap = np.sqrt(xymap[0]**2 + xymap[1]**2)

    return rmap

def make_a10_map(M500,z,xymap,Theta500,nx,ny,nb_theta_range=150,Dist=False,c500=None,p=None,a=None,b=None,c=None):
    """
    Return a tuple of x- and y-coordinates.

    Parameters
    ----------
    M500 : quantity
       :math:`M\_{500}` with units of mass.
    z : float
       Redshift
    xymap : tuple(class:`numpy.ndarray`)
       A tuple of x- and y-coordinates
    Theta500 : float
       :math:`R\_{500}` in radians
    nx : int
       Number of pixels along axis 0
    ny : int
       Number of pixels along axis 1
    nb_theta_range : int
       Number of elements in an array of radii.
    Dist : bool
       Assume a disturbed A10 profile? Default is False
    c500 : float, none-type
      If None, adopts the radius scaling value for A10 (full or disturbed) sample
    p : float, none-type
      If None, adopts the normalization value for A10 (full or disturbed) sample
    a : float, none-type
      If None, adopts the alpha value for A10 (full or disturbed) sample
    b : float, none-type
      If None, adopts the beta value for A10 (full or disturbed) sample
    c : float, none-type
      If None, adopts the gamma value for A10 (full or disturbed) sample

    Returns
    -------
    ymap : class:`numpy.ndarray`
       An output Compton y map

    """

    minpixrad = (1.0*u.arcsec).to('rad')
    tnx       = [minpixrad.value,10.0*Theta500]  # In radians
    thetas    = np.logspace(np.log10(tnx[0]),np.log10(tnx[1]), nb_theta_range)
    d_ang     = get_d_ang(z)
    radkpc    = thetas*d_ang.to("kpc")
    PresProf  = a10_from_m500_z(M500, z,radkpc,Dist=Dist,c500=c500,p=p,a=a,b=b,c=c)
    to,yProf  = get_yProf(radkpc,PresProf,z)
    #x2p,y2p   = xymap
    #origshape = x2p.shape
    #xy2pass   = (x2p.flatten(),y2p.flatten())
    #print(xy2pass[0].shape,thetas.shape,yProf.shape,origshape)
    
    flatymap  = grid_profile(thetas,yProf,xymap)
    ymap      = flatymap.reshape((nx,ny))

    return ymap
    
def grid_profile(rads, profile, xymap, geoparams=[0,0,0,1,1,1,0,0],myscale=1.0,axis='z'):
    """
    Return a tuple of x- and y-coordinates.

    Parameters
    ----------
    rads : class:`numpy.ndarray`
       An array of radii (same units as xymap)
    profile : class:`numpy.ndarray`
       A radial profile of surface brightness.
    xymap : tuple(class:`numpy.ndarray`)
       A tuple of x- and y-coordinates
    geoparams : array-like
       [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    myscale : float
       Generally best to leave as unity.
    axis : str
       Which axis are you projecting along.

    Returns
    -------
    mymap : class:`numpy.ndarray`
       An output map

    """

    ### Get new grid:
    arc2rad =  4.84813681109536e-06 # arcseconds to radians
    (x,y) = xymap
    x,y = rot_trans_grid(x,y,geoparams[0],geoparams[1],geoparams[2]) # 0.008 sec per call
    x,y = get_ell_rads(x,y,geoparams[3],geoparams[4])                # 0.001 sec per call
    theta = np.sqrt(x**2 + y**2)*arc2rad
    theta_min = rads[0]*2.0 # Maybe risky, but this is defined so that it is sorted.
    bi=(theta < theta_min);   theta[bi]=theta_min
    mymap  = np.interp(theta,rads,profile)
    
    if axis == 'x':
        xell = (x/(geoparams[3]*myscale))*arc2rad # x is initially presented in arcseconds
        modmap = geoparams[5]*(xell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'y':
        yell = (y/(geoparams[4]*myscale))*arc2rad # x is initially presented in arcseconds
        modmap = geoparams[5]*(yell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'z':
        modmap = geoparams[5]

    if modmap != 1:
        mymap *= modmap   # Very important to be precise here.
    if geoparams[7] > 0:
        angmap = np.arctan2(y,x)
        bi = (abs(angmap) > geoparams[7]/2.0)
        mymap[bi] = 0.0

    return mymap

def rot_trans_grid(x,y,xs,ys,rot_rad):
    """   
    Shift and rotate coordinates

    :param x: coordinate along major axis (a) 
    :type x: class:`numpy.ndarray`
    :param y: coordinate along minor axis (b) 
    :type y: class:`numpy.ndarray`
    :param xs: translation along x-axis
    :type xs: float
    :param ys: translation along y-axis
    :type ys: float
    :param rot_rad: rotation angle, in radians
    :type rot_rad: float

    """

    xnew = (x - xs)*np.cos(rot_rad) + (y - ys)*np.sin(rot_rad)
    ynew = (y - ys)*np.cos(rot_rad) - (x - xs)*np.sin(rot_rad)

    return xnew,ynew

def get_ell_rads(x,y,ella,ellb):
    """   
    Get ellipsoidal radii from x,y standard

    :param x: coordinate along major axis (a) 
    :type x: class:`numpy.ndarray`
    :param y: coordinate along minor axis (b) 
    :type y: class:`numpy.ndarray`
    :param ella: scaling along major axis (should stay 1)
    :type ella: float
    :param ellb: scaling along minor axis
    :type ella: float

    """
 
    xnew = x/ella ; ynew = y/ellb

    return xnew, ynew

def a10_from_m500_z(m500, z,rads,Dist=True,c500=None,p=None,a=None,b=None,c=None):
    """
    Parameters
    ----------
    M500 : quantity
       :math:`M\_{500}` with units of mass.
    z : float
       Redshift
    xymap : tuple(class:`numpy.ndarray`)
       A tuple of x- and y-coordinates
    rads : quantity,array
       Array of radii (with units of length)
    Dist : bool
       Assume a disturbed A10 profile? Default is False
    c500 : float, none-type
      If None, adopts the radius scaling value for A10 (full or disturbed) sample
    p : float, none-type
      If None, adopts the normalization value for A10 (full or disturbed) sample
    a : float, none-type
      If None, adopts the alpha value for A10 (full or disturbed) sample
    b : float, none-type
      If None, adopts the beta value for A10 (full or disturbed) sample
    c : float, none-type
      If None, adopts the gamma value for A10 (full or disturbed) sample

    Returns
    -------
    gnfw_prof : quantity,array
       A radial profile with units of pressure

    """
    
    r500, p500 = R500_P500_from_M500_z(m500,z)
    if c500 is None:
        c500 = 1.083 if Dist else 1.177
    if p is None:
        p = 3.202 if Dist else 8.403
    if a is None:
        a = 1.4063 if Dist else 1.0510
    if b is None:
        b = 5.4905     # Fixed to simulations for all subsets.
    if c is None:
        c = 0.3798 if Dist else 0.3081 # Steeper for the disturbed sample! Oh Degeneracies.
    
    gnfw_prof  = gnfw(r500,p500,rads,c500=c500,p=p,a=a,b=b,c=c)
    
    return gnfw_prof

def get_yProf(radii,pprof,z):
    """
    Parameters
    ----------
    radii : quantity,array
       Array of radii (with units of length)
    pprof : quantity,array
       A radial profile with units of pressure
    z : float
       The redshift

    Returns
    -------
    thetas : array
       A radial profile in units of radians
    yProf_clust : array
       A radial profile of Compton y values

    """

    d_ang      = get_d_ang(z)
    thetas     = (radii/d_ang).decompose().value
    Pdl2y      = get_Pdl2y(z,d_ang)
    unitless_profile_clust = (pprof * Pdl2y).decompose().value
    yProf_clust = ni.int_profile(thetas, unitless_profile_clust,thetas)

    return thetas,yProf_clust

def gnfw(R500, P500, radii, c500= 1.177, p=8.403, a=1.0510, b=5.4905, c=0.3081):
    """
    .. math::

        P(r) = \\frac{P_{500} p}{(r* c_{500} / R_{500})^{\\gamma} \\left(1 + (r* c_{500} / R_{500})^{\\alpha} \\right)^{(\\beta - \\gamma)/\\alpha}}

    Parameters
    ----------
    R500 : quantity
       :math:`R\_{500}` with units of length.
    P500 : quantity
       :math:`P\_{500}` with units of pressure.
    radii : quantity,array
       An array of radii, with units of length
    c500 : float
       The concentration parameter
    p : float
       The pressure normalization parameter
    a : float
       The rollover parameter; the :math:`\\alpha` parameter
    b : float
       The slope at outer radii; the :math:`\\beta` parameter
    c : float
       The slope at inner radii; the :math:`\\gamma` parameter

    Returns
    -------
    result : quantity,array
       A radial profile with units of pressure

    """

    cosmo = get_cosmo()
    h70 = (cosmo.H(0) / (70.0*u.km / u.s / u.Mpc))

    P0 = P500 * p * h70**-1.5
    rP = R500 / c500 # C_500 = 1.177
    rf =  (radii/rP).decompose().value # rf must be dimensionless
    result = (P0 / (((rf)**c)*((1 + (rf)**a))**((b - c)/a)))

    return result

def get_Pdl2y(z,d_ang):
    """
    Parameters
    ----------
    z : float
       The redshift
    d_ang : quantity
       The angular distance; units of distance

    Returns
    -------
    Pdl2y : float
       A conversion factor from pressure to a unitless profile, optimal for analytic integration.
    """

    szcv,szcu = get_sz_values()
    Pdl2y     = (szcu['thom_cross']*d_ang/szcu['m_e_c2']).to("cm**3 keV**-1")

    return Pdl2y

def get_sz_values():
    """
    Returns
    -------
    szcv : dict
       A dictionary of constant values.
    szcu : dict
       A dictionary of constants with units.
    """
    ########################################################
    ### Astronomical value...
    tcmb = 2.72548*u.K # Kelvin (uncertainty = 0.00057)
    ### Reference:
    ### http://iopscience.iop.org/article/10.1088/0004-637X/707/2/916/meta
    
    ### Standard physical values.
    thom_cross = (spconst.value("Thomson cross section") *u.m**2).to("cm**2")
    m_e_c2 = (const.m_e *const.c**2).to("keV")
    kpctocm = 3.0856776 *10**21
    boltzmann = spconst.value("Boltzmann constant in eV/K")/1000.0 # keV/K  
    planck = const.h.to("eV s").value/1000.0 # keV s
    c = const.c
    keVtoJ = (u.keV).to("J") # I think I need this...) 
    Icmb = 2.0 * (boltzmann*tcmb.value)**3 / (planck*c.value)**2
    Icmb *= keVtoJ*u.W *u.m**-2*u.Hz**-1*u.sr**-1 # I_{CMB} in W m^-2 Hz^-1 sr^-1
    JyConv = (u.Jy).to("W * m**-2 Hz**-1")
    Jycmb = Icmb.to("Jy sr**-1")  # I_{CMB} in Jy sr^-1
    MJycmb= Jycmb.to("MJy sr**-1")

    ### The following constants (and conversions) are just the values (in Python):
    sz_cons_values={"thom_cross":thom_cross.value,"m_e_c2":m_e_c2.value,
                    "kpctocm":kpctocm,"boltzmann":boltzmann,
                    "planck":planck,"tcmb":tcmb.value,"c":c.value,}
    ### The following "constants" have units attached (in Python)!
    sz_cons_units={"Icmb":Icmb,"Jycmb":Jycmb,"thom_cross":thom_cross,
                   "m_e_c2":m_e_c2}

    return sz_cons_values, sz_cons_units

def make_A10Map(M500,z,pixsize=2,h70=1,nb_theta_range=150,Dist=True,nR500=3.0,c500=None,p=None,a=None,b=None,c=None):
    """
    Makes an A10 map with automated mapsize.

    Parameters
    ----------
    M500 : quantity
       :math:`M\_{500}` with units of mass.
    z : float
       Redshift
    pixsize : float
       Pixel size, in arcseconds
    h70 : float
       Normalization of the Hubble parameter.
    nb_theta_range : int
       Number of elements in an array of radii.
    Dist : bool
       Assume a disturbed A10 profile? Default is False
    c500 : float, none-type
      If None, adopts the radius scaling value for A10 (full or disturbed) sample
    p : float, none-type
      If None, adopts the normalization value for A10 (full or disturbed) sample
    a : float, none-type
      If None, adopts the alpha value for A10 (full or disturbed) sample
    b : float, none-type
      If None, adopts the beta value for A10 (full or disturbed) sample
    c : float, none-type
      If None, adopts the gamma value for A10 (full or disturbed) sample

    Returns
    -------
    ymap : class:`numpy.ndarray`
       An output Compton y map

    """

    Theta500   = Theta500_from_M500_z(M500,z)
    minpixrad  = (1.0*u.arcsec).to('rad')
    tnx        = [minpixrad.value,10.0*Theta500]  # In radians
    thetas     = np.logspace(np.log10(tnx[0]),np.log10(tnx[1]), nb_theta_range)
    map_vars   = {"thetas":thetas}
    nx         = int( np.round( (Theta500*3600*180/np.pi)*nR500*2/pixsize) )
    mapshape   = (nx,nx)
    zeromap    = np.zeros(mapshape)
    xymap      = get_xymap(zeromap,pixsize=pixsize*u.arcsec)
    ymap       = make_a10_map(M500,z,xymap,Theta500,nx,nx,Dist=Dist,c500=c500,p=p,a=a,b=b,c=c)

    return ymap

def smooth_by_M2_beam(image,pixsize=2.0):
    """
    Smooths an image by a double Gaussian that is representative for MUSTANG-2.

    Parameters
    ----------
    image: float 2D numpy array
         2D array for which we compute the power spectrum
    pixsize: float
         Pixel size, in arcseconds

    Returns
    -------
    bcmap : float 2D numpy array
       beam-convolved map
    
    """

    
    fwhm1,norm1,fwhm2,norm2,fwhm,smfw,freq,FoV = inst_params("MUSTANG2")

    sig2fwhm   = np.sqrt(8.0*np.log(2.0)) 
    pix_sigq1  = fwhm1/(pixsize*sig2fwhm*u.arcsec)
    pix_sigq2  = fwhm2/(pixsize*sig2fwhm*u.arcsec)
    pix_sig1   = pix_sigq1.decompose().value
    pix_sig2   = pix_sigq2.decompose().value
    map1       = filters.gaussian_filter(image, pix_sig1)
    map2       = filters.gaussian_filter(image, pix_sig2)

    bcmap      = map1*norm1 + map2*norm2

    return bcmap

def get_xferfile(size):
    """
    Parameters
    ----------
    size: float
       size of scan (radially, in arcminutes)

    Returns
    -------
    xferfile : str
       The corresponding file name
    
    """

    if size == 2.5:
        xferfile       = "xfer_Function_2p5_21Aonly_PCA5_0f08Filtering.txt"
    if size == 3.0:
        xferfile       = "xfer_Function_3p0_21Aonly_PCA5_0f08Filtering.txt"
    if size == 3.5:
        xferfile       = "xfer_Function_3p5_21Aonly_PCA5_0f08Filtering.txt"
    if size == 4.0:
        xferfile       = "xfer_Function_4p0_21Aonly_PCA5_0f08Filtering.txt"
    if size == 4.5:
        xferfile       = "xfer_Function_4p5_21Aonly_PCA5_0f08Filtering.txt"
    if size == 5.0:
        xferfile       = "xfer_Function_5p0_21Aonly_PCA5_0f08Filtering.txt"

    return xferfile

def xfer_param_fxn(karr,lgkc,lgetac,lgx0):

    #xv   = (pars[0]/karr)**pars[1]
    #xfer = np.exp(-xv)*pars[2]
    kc    = np.exp(lgkc)
    eta_c = np.exp(lgetac)
    x0    = np.exp(lgx0)
    xv    = (kc/karr)**eta_c
    xfer  = np.exp(-xv)*x0

    return xfer

def get_xfer_fit(tab,size,WIKID=True):

    PNGsave = "WIKID" if WIKID else "MUSTANG-2"
    sizestr = "{:.1f}".format(size).replace(".","s")
    newfile = "TransferFunction_"+PNGsave+"_scansize_"+sizestr+".npy"

    if os.path.exists(newfile):
        with open(newfile,'rb') as nf:
            newtab = np.load(nf)

    else:
        k = tab[0,:]
        x = tab[1,:]
    
        gi    = (k > 0)*(k < 0.1)
        xdata = k[gi]
        ydata = x[gi]
        
        p0         = np.log(np.array([0.01,0.5,0.98]))
        popt, pcov = curve_fit(xfer_param_fxn, xdata, ydata,p0=p0)
        if WIKID:
            popt[0] -= np.log(2.0)     # Cutoff is twice as small for WIKID, as its FOV is twice as big.
        kout       = np.logspace(-3.5,1.0,200)
        xfxn       = xfer_param_fxn(kout,*popt)
        
        myfig = plt.figure(10,figsize=(5,4),dpi=200)
        myfig.clf()
        myax  = myfig.add_subplot(111)
        
        kgtz  = (k > 0)
        myax.plot(k[kgtz],x[kgtz],label="MUSTANG-2, measured")
        mylabel = "WIKID" if WIKID else "MUSTANG-2, fit"
        myax.plot(kout,xfxn,"--",label="WIKID")
        myax.set_xscale("log")
        myax.set_xlabel(r"$k = 1/\lambda$ (arcseconds$^{-1}$")
        myax.set_ylabel("Transmission")
        myax.legend()
        myfig.tight_layout()
        myfig.savefig(PNGsave+"_XferFunction.png")
        
        newtab = np.vstack([kout,xfxn])
        with open(newfile,"wb") as nf:
            np.save(nf,newtab)
            
    #print(newtab.shape)
    #print(popt)
    #import pdb;pdb.set_trace()
    
    return newtab

def get_xfertab(size,WIKID=False):
    """
    Parameters
    ----------
    size: float
       size of scan (radially, in arcminutes)

    Returns
    -------
    tab : float 2D numpy array
       An array containing frequency and transfer function values
    
    """

    #mypath  = "src/M2_ProposalTools/"
    path    = os.path.abspath(FI.__file__)
    mypath  = path.replace("FilterImages.py","")
    #print(mypath)
    #import pdb;pdb.set_trace()
    xferfile = get_xferfile(size)
    fullpath = os.path.join(mypath,xferfile)
    tab      = FI.get_xfer(fullpath)

    if WIKID:
        tab = get_xfer_fit(tab,size)

    return tab

def lightweight_filter_ptg(skymap,size,pixsize,WIKID=False):
    """   
    Parameters
    ----------
    skymap: float 2D numpy array
       2D image to be filtered
    size : float
       The size of the scan, such that the appropriate transfer function is applied.
    pixsize: float
       Pixel size, in arcseconds

    Returns
    -------
    yxfer: float 2D numpy array
       The filtered image
    """

    tab   = get_xfertab(size,WIKID=WIKID)
    yxfer = FI.apply_xfer(skymap,tab,pixsize)

    return yxfer

def lightweight_simobs_A10(z,M500,ptgs=[[180,45.0]],sizes=[3.5],times=[10.0],offsets=[1.5],
                           center=[180,45.0],xsize=12.0,ysize=12.0,pixsize=2.0,Dist=True,
                           fwhm=9.0,conv2uK=False,verbose=False,y2k=-3.4,c500=None,p=None,a=None,b=None,c=None):
    """   
    A lightweight mock observation tool. To be lightweight, everything is approximate -- but it's fast!

    Parameters
    ----------
    z : float
       The redshift
    M500 : quantity
       :math:`M\_{500}` with units of mass
    ptgs : list(list)
       A list of 2-element pairs (of RA and Dec, in degrees)
    sizes : list(float)
       A list of scan sizes, in arcminutes. Only 2.5, 3.0, 3.5, 4.0, 4.5, and 5.0 are valid.
    times : list(float)
       A list of integration times for corresponding pointings and scan sizes, in hours.
    offsets : list(float)
       A list of pointing offsets, in arcminutes.
    center : list
       A two-element list corresponding to the RA and Dec of the center of the map
    xsize : float
       The length of the map, in arcminutes, along the RA direction.
    ysize : float
       The length of the map, in arcminutes, along the Dec direction.
    pixsize : float
       The pixel size, in arcseconds
    Dist : bool
       Adopt a disturbed A10 model?
    fwhm : float
       The smoothing kernal for a resultant MIDAS map, in arcseconds. 9" is the default.
    conv2uK : bool
       Convert the resultant images from Compton y to microK_RJ (the standard units for MUSTANG-2 maps).
    verbose : bool
       Have the function print extraneous information?
    c500 : float, none-type
      If None, adopts the radius scaling value for A10 (full or disturbed) sample
    p : float, none-type
      If None, adopts the normalization value for A10 (full or disturbed) sample
    a : float, none-type
      If None, adopts the alpha value for A10 (full or disturbed) sample
    b : float, none-type
      If None, adopts the beta value for A10 (full or disturbed) sample
    c : float, none-type
      If None, adopts the gamma value for A10 (full or disturbed) sample

    """
    
    sig2fwhm       = np.sqrt(8.0*np.log(2.0)) 
    pix_sigma      = fwhm/(pixsize*sig2fwhm)
    ymap           = make_A10Map(M500,z,pixsize=pixsize,Dist=Dist,c500=c500,p=p,a=a,b=b,c=c)
    mymap          = smooth_by_M2_beam(ymap,pixsize=pixsize)
    nx,ny          = mymap.shape
    SkyHDU         = MRM.make_template_hdul(nx,ny,center,pixsize)
    SkyHDU[0].data = mymap*1.0
    Skyhdr         = SkyHDU[0].header
    SkyCoadd       = MRM.make_template_hdul(nx,ny,center,pixsize)

    SkyCoadd       = MRM.Make_ImgWtmap_HDU(SkyCoadd,np.zeros((nx,ny)),np.zeros((nx,ny)))

    SkyMaps        = []
    SkyWtmap       = MRM.make_template_hdul(nx,ny,center,pixsize)
    print("Hi")
    
    for si,(p,s,t,o) in enumerate(zip(ptgs,sizes,times,offsets)):

        wtmap          = np.zeros(mymap.shape)
        npix         = int(np.round((s*60*2)/pixsize))
        cosdec       = np.cos(p[1]*np.pi/180.0)
        if o > 0:
            degoff       = o/60.0 # Offset in degrees
            for i in range(4):
                wtmap        = np.zeros(mymap.shape)
                newx         = p[0] + np.cos(np.pi*i/2)*degoff/cosdec
                newy         = p[1] + np.sin(np.pi*i/2)*degoff
                myptg        = [newx,newy]
                if verbose:
                    print(myptg)
                TemplateHDU  = MRM.make_template_hdul(npix,npix,myptg,pixsize)
                ptghdr       = TemplateHDU[0].header
                ycutout,fp0  = MRM.reproject_fillzeros(SkyHDU,ptghdr)
                wtmap        = MRM.add_to_wtmap(wtmap,Skyhdr,myptg,s,t/4.0,offset=0) # Need to fix
                TemplateHDU[0].data = lightweight_filter_ptg(ycutout,s,pixsize)
                Sky_yxfer,fp = MRM.reproject_fillzeros(TemplateHDU,Skyhdr)
                SkyMap       = MRM.Make_ImgWtmap_HDU(SkyWtmap,Sky_yxfer,wtmap)
                SkyMaps.append(SkyMap)
                SkyCoadd     = MRM.coaddimg_noRP(SkyCoadd,SkyMap)
        else:
            TemplateHDU  = MRM.make_template_hdul(npix,npix,p,pixsize)
            ptghdr       = TemplateHDU[0].header
            ycutout,fp0  = MRM.reproject_fillzeros(SkyHDU,ptghdr)
            wtmap        = MRM.add_to_wtmap(wtmap,Skyhdr,p,s,t,offset=o) # Need to fix
            maxwt        = np.max(wtmap)
            minrms       = 1.0/np.sqrt(maxwt)
            TemplateHDU[0].data = lightweight_filter_ptg(ycutout,s,pixsize)
            Sky_yxfer,fp = MRM.reproject_fillzeros(TemplateHDU,Skyhdr)
            SkyMap       = MRM.Make_ImgWtmap_HDU(SkyWtmap,Sky_yxfer,wtmap)
            SkyMaps.append(SkyMap)
            SkyCoadd     = MRM.coaddimg_noRP(SkyCoadd,SkyMap)

    myFactor         =  y2k*1e6 if conv2uK else 1.0
    SkySmooth        =  filters.gaussian_filter(SkyCoadd[0].data,pix_sigma) * myFactor
    SkyObs           =  SkyCoadd[0].data*1.0
    SkyCoadd[0].data =  SkyObs*myFactor
    SSP              =  fits.PrimaryHDU(SkySmooth,header=SkyCoadd[0].header)
    SSS              =  fits.ImageHDU(SkyCoadd[1].data,header=SkyCoadd[0].header)
    SkySmHDU         =  fits.HDUList([SSP,SSS])
    
    return SkyCoadd, SkySmHDU,SkyHDU

def make_A10_hdu(z,M500,pixsize,center=[180,45.0],nR500=3.0,Dist=True,beamConvolve=True,conv2uK=True,y2k=-3.4,
                 c500=None,p=None,a=None,b=None,c=None):
    """   
    Compute and grid an A10 Compton y profile and put it into an HDUList

    Parameters
    ----------
    z : float
       The redshift
    M500 : quantity
       :math:`M\_{500}` with units of mass
    pixsize : float
       The pixel size, in arcseconds
    center : list
       A two-element list corresponding to the RA and Dec of the center of the map
    Dist : bool
       Adopt a disturbed A10 model?
    conv2uK : bool
       Convert the resultant images from Compton y to microK_RJ (the standard units for MUSTANG-2 maps).
    y2k : float
       What is the conversion factor between Compton y and K_RJ (for MUSTANG-2)? The default is -3.4, which corresponds to the conversion with relativistic corrections for kT_e ~ 7 keV. This factor is -3.5 at kT_e = 2 keV and -3.3 at kT_e = 12 keV.
    verbose : bool
       Have the function print extraneous information?
    c500 : float, none-type
      If None, adopts the radius scaling value for A10 (full or disturbed) sample
    p : float, none-type
      If None, adopts the normalization value for A10 (full or disturbed) sample
    a : float, none-type
      If None, adopts the alpha value for A10 (full or disturbed) sample
    b : float, none-type
      If None, adopts the beta value for A10 (full or disturbed) sample
    c : float, none-type
      If None, adopts the gamma value for A10 (full or disturbed) sample

    """

    ymap           = make_A10Map(M500,z,pixsize=pixsize,Dist=Dist,nR500=nR500,c500=c500,p=p,a=a,b=b,c=c)
    if beamConvolve:
        mymap          = smooth_by_M2_beam(ymap,pixsize=pixsize)
    else:
        mymap          = ymap.copy()
    nx,ny          = mymap.shape
    SkyHDU         = MRM.make_template_hdul(nx,ny,center,pixsize)
    myFactor       =  y2k*1e6 if conv2uK else 1.0
    SkyHDU[0].data = mymap*myFactor

    return SkyHDU

def lightweight_simobs_hdu(SkyHDU,ptgs=[[180,45.0]],sizes=[3.5],times=[10.0],offsets=[1.5],
                           center=None,xsize=12.0,ysize=12.0,pixsize=2.0,fwhm=9.0,verbose=False,WIKID=False):
    """   
    A lightweight mock observation tool. To be lightweight, everything is approximate -- but it's fast!

    Parameters
    ----------
    SkyHDU : HDUList
       An HDUList, for which only the first extension (ext=0) is accessed. That extension should contain a beam-convolved image of the target.
    ptgs : list(list)
       A list of 2-element pairs (of RA and Dec, in degrees)
    sizes : list(float)
       A list of scan sizes, in arcminutes. Only 2.5, 3.0, 3.5, 4.0, 4.5, and 5.0 are valid.
    times : list(float)
       A list of integration times for corresponding pointings and scan sizes, in hours.
    offsets : list(float)
       A list of pointing offsets, in arcminutes.
    fwhm : float
       The smoothing kernal for a resultant MIDAS map, in arcseconds. 9" is the default.
    verbose : bool
       Have the function print extraneous information?
    center : list or None-type
       If supplied, a two-element list corresponding to the RA and Dec of the center of the weight map. Set this if wish to adopt a new astrometry for your weight map, relative to the astrometry of the input SkyHDU. The default is None and as such the weight map will adopt the astrometry of the SkyHDU.
    xsize : float
       The length of the map, in arcminutes, along the RA direction.
    ysize : float
       The length of the map, in arcminutes, along the Dec direction.
    pixsize : float
       The pixel size, in arcseconds

    """
    
    sig2fwhm       = np.sqrt(8.0*np.log(2.0)) 
    pix_sigma      = fwhm/(pixsize*sig2fwhm)
    Skyhdr         = SkyHDU[0].header
    if center is None:
        nx,ny         = SkyHDU[0].data.shape
        SkyC_HDU      = fits.PrimaryHDU(np.zeros((nx,ny)),header=Skyhdr)
        SkyCoadd      = fits.HDUList([SkyC_HDU])
        SkyW          = WCS(Skyhdr)
        #print(SkyW.wcs.crval)
        #import pdb;pdb.set_trace()
        center        = SkyW.wcs.crval
    else:
        nx             = int(np.round(xsize*60/pixsize))
        ny             = int(np.round(ysize*60/pixsize))
        SkyCoadd       = MRM.make_template_hdul(nx,ny,center,pixsize)

    SkyCoadd       = MRM.Make_ImgWtmap_HDU(SkyCoadd,np.zeros((nx,ny)),np.zeros((nx,ny)))

    SkyMaps        = []
    SkyWtmap       = MRM.make_template_hdul(nx,ny,center,pixsize)
    
    for si,(p,s,t,o) in enumerate(zip(ptgs,sizes,times,offsets)):

        wtmap          = np.zeros((nx,ny))
        degoff       = o/60.0 # Offset in degrees
        cosdec       = np.cos(p[1]*np.pi/180.0)
        FOV          = 8.5 if WIKID else 4.2
        npix         = int(np.round((s*60*1.5+FOV)/pixsize))
        if o > 0:
            for i in range(4):
                wtmap        = np.zeros((nx,ny))
                newx         = p[0] + np.cos(np.pi*i/2)*degoff/cosdec
                newy         = p[1] + np.sin(np.pi*i/2)*degoff
                myptg        = [newx,newy]
                if verbose:
                    print(myptg)
                TemplateHDU  = MRM.make_template_hdul(npix,npix,myptg,pixsize)
                ptghdr       = TemplateHDU[0].header
                ycutout,fp0  = MRM.reproject_fillzeros(SkyHDU,ptghdr)
                wtmap        = MRM.add_to_wtmap(wtmap,Skyhdr,myptg,s,t/4.0,offset=0,WIKID=WIKID) # Need to fix
                TemplateHDU[0].data = lightweight_filter_ptg(ycutout,s,pixsize,WIKID=WIKID)
                Sky_yxfer,fp = MRM.reproject_fillzeros(TemplateHDU,Skyhdr)
                SkyMap       = MRM.Make_ImgWtmap_HDU(SkyWtmap,Sky_yxfer,wtmap)
                SkyMaps.append(SkyMap)
                SkyCoadd     = MRM.coaddimg_noRP(SkyCoadd,SkyMap)
        else:
            TemplateHDU  = MRM.make_template_hdul(npix,npix,p,pixsize)
            ptghdr       = TemplateHDU[0].header
            ycutout,fp0  = MRM.reproject_fillzeros(SkyHDU,ptghdr)
            wtmap        = MRM.add_to_wtmap(wtmap,Skyhdr,p,s,t,offset=o,WIKID=WIKID) # Need to fix
            #maxwt        = np.max(wtmap)
            #minrms       = 1.0/np.sqrt(maxwt)
            TemplateHDU[0].data = lightweight_filter_ptg(ycutout,s,pixsize,WIKID=WIKID)
            Sky_yxfer,fp = MRM.reproject_fillzeros(TemplateHDU,Skyhdr)
            SkyMap       = MRM.Make_ImgWtmap_HDU(SkyWtmap,Sky_yxfer,wtmap)
            SkyMaps.append(SkyMap)
            SkyCoadd     = MRM.coaddimg_noRP(SkyCoadd,SkyMap)

    SkySmooth        =  filters.gaussian_filter(SkyCoadd[0].data,pix_sigma)
    SSP              =  fits.PrimaryHDU(SkySmooth,header=SkyCoadd[0].header)
    SSS              =  fits.ImageHDU(SkyCoadd[1].data,header=SkyCoadd[0].header)
    SkySmHDU         =  fits.HDUList([SSP,SSS])
    
    return SkyCoadd, SkySmHDU

def get_SNR_map(hdul):
    """   
    Parameters
    ----------
    hdul : list of HDU class objects 
       First extension is the image; second extension is the weightmap

    Returns
    -------
    SNRmap : 2D numpy array
       A signal-to-noise (ratio) map.
    """
    
    img    = hdul[0].data
    wtmap  = hdul[1].data
    rmsmap = MRM.conv_wtmap_torms(wtmap)
    SNRmap = np.zeros(rmsmap.shape)
    nzwts  = (wtmap > 0)
    SNRmap[nzwts] = img[nzwts]/rmsmap[nzwts]

    return SNRmap

def get_pixarcsec(hdul):
    """   
    Parameters
    ----------
    hdul : list of HDU class objects 
       Assumes the HDUList has a header with relevant astrometric information.

    Returns
    -------
    pixsize : float
       pixel size, in arcseconds
    """

    wcs_inp = WCS(hdul[0].header)
    pixsize = np.sqrt(np.abs(np.linalg.det(wcs_inp.pixel_scale_matrix))) * 3600.0 # in arcseconds

    return pixsize

def get_noise_realization(hdul,pink=True,alpha=2,knee=1.0/60.0,nkbin=100,fwhm=9.0):
    """   
    Parameters
    ----------
    hdul : list of HDU class objects 
       First extension is the image; second extension is the weightmap
    pink : bool
       Make the noise pink (more realistic)
    alpha : float
       The power-law index of the red noise component.
    knee : float
       Where is the knee in the power spectrum, in inverse arcseconds.
    nkbin : int
       Number of bins in making an array of k-values.
    fwhm : float
       FWHM of the smoothing kernel, in arcseconds. Used to determine k_max.

    Returns
    -------
    noise : 2D numpy array
       A (very approximate) noise realization.
    """

    #img          = hdul[0].data
    wtmap        = hdul[1].data
    rmsmap       = MRM.conv_wtmap_torms(wtmap)
    zwts         = (wtmap == 0)
    maxwts       = np.max(wtmap)
    rmsmap[zwts] = 0
    pixsize      = get_pixarcsec(hdul)

    if pink:
        noise = make_pinknoise_real(rmsmap,pixsize,alpha=alpha,knee=knee,nkbin=nkbin,fwhm=fwhm)
    else:
        noise_init = np.random.normal(size=rmsmap.shape)
        sf         = get_smoothing_factor(fwhm=fwhm)
        noise      = noise_init*sf*rmsmap

    return noise

def get_smoothing_factor(fwhm=9.0):
    """   
    Parameters
    ----------
    fwhm : float
       FWHM of the smoothing kernel, in arcseconds. Used to determine k_max.

    Returns
    -------
    sf : float
       The square root of the beam volume.
    """

    s2f         = np.sqrt(8.0*np.log(2.0))
    sig         = fwhm/s2f
    bv          = 2*np.pi*sig**2
    sf          = np.sqrt(bv)

    return sf

def make_pinknoise_real(rmsmap,pixsize,alpha=2,knee=1.0/120.0,nkbin=100,fwhm=9.0,kmin=1.0/900.0):
    """   
    Parameters
    ----------
    rmsmap : 2D numpy array
       A map of (white noise) RMS.
    pixsize : float
       Pixel size, in arcseconds
    alpha : float
       The power-law index of the red noise component.
    knee : float
       Where is the knee in the power spectrum, in inverse arcseconds.
    nkbin : int
       Number of bins in making an array of k-values.
    fwhm : float
       FWHM of the smoothing kernel, in arcseconds. Used to determine k_max.
    kmin : float
       The minimum k-value accessed (roughly).

    Returns
    -------
    noise : 2D numpy array
       A (very approximate) noise realization.
    """

    nx,ny       = rmsmap.shape
    k_img       = np.logspace(np.log10(1/(pixsize*nx)),np.log10(1.0/pixsize),nkbin)
    if alpha == 2:
        term1   = 2*np.pi * np.log(knee/kmin)
    else:
        term0   = knee**(2-alpha) - kmin**(2-alpha)
        term1   = ( 2*np.pi*term0 )/(2-alpha) # Excess from pink noise
    term2       = (np.pi * knee**2)                     # Relative WN contribution
    pink_renorm = term2 / (term1 + term2)               # Pwn vs. Ptotal
    p_init      = pixsize**2/np.pi                      # Normalization for WN
    pl_part     = (k_img/knee)**(-alpha)
    pink        = (1 + pl_part)*p_init*pink_renorm      # Full pink noise, normalized
    sf          = get_smoothing_factor(fwhm=fwhm)
    
    noise_init  = make_image(k_img,pink,nx=nx,ny=ny,pixsize=pixsize)
    noise       = noise_init*rmsmap*sf

    nzrms       = (rmsmap > 0)
    #print(np.max(rmsmap),np.min(rmsmap[nzrms]))
    #import pdb;pdb.set_trace()

    return noise
    
def make_image(kbin,psbin,nx=1024,ny=1024,pixsize=1.0,verbose=False):
    """   
    Parameters
    ----------
    kbin : 1D numpy array
       Array of frequencies (wavenumbers)
    psbin : 1D numpy array
       Array of power spectrum values
    nx : int
       Number of pixels along axis 0
    ny : int
       Number of pixels along axis 1
    pixsize : float
       Pixel size, in arcseconds
    verbose : bool
       Print extra things?

    Returns
    -------
    noise : 2D numpy array
       A (very approximate) noise realization.
    """

    k,dkx,dky   = get_freqarr_2d(nx, ny, pixsize, pixsize)
    kflat       = k.flatten()
    gki         = (kflat > 0)
    gk          = kflat[gki]

    psout       = np.exp(np.interp(np.log(gk),np.log(kbin),np.log(psbin)))
    psarr       = kflat*0
    psarr[gki]  = psout
    ps2d        = psarr.reshape(k.shape) * nx*ny

    phase       = np.random.uniform(size=(nx,ny))*2*np.pi
    newfft      = np.sqrt(ps2d) * np.exp(1j*phase)
    newps       = np.abs(newfft*np.conjugate(newfft))
    PTsum       = np.sum(newps/pixsize**2)/(nx*ny)
    if verbose:
        print("PTsum: ",PTsum)
    img = np.real(np.fft.ifft2(newfft/pixsize))
    img *= np.sqrt(2.0)
    varsum = np.sum(img**2)
    if verbose:
        print("VARsum: ",varsum)
        #import pdb;pdb.set_trace()

    return img

def get_freqarr_2d(nx, ny, psx, psy):
    """
       Compute frequency array for 2D FFT transform

       Parameters
       ----------
       nx : integer
            number of samples in the x direction
       ny : integer
            number of samples in the y direction
       psx: integer
            map pixel size in the x direction
       psy: integer
            map pixel size in the y direction

       Returns
       -------
       k : float 2D numpy array
           frequency vector
    """
    kx =  np.outer(np.fft.fftfreq(nx),np.zeros(ny).T+1.0)/psx
    ky =  np.outer(np.zeros(nx).T+1.0,np.fft.fftfreq(ny))/psy
    dkx = kx[1:][0]-kx[0:-1][0]
    dky = ky[0][1:]-ky[0][0:-1]
    k  =  np.sqrt(kx*kx + ky*ky)
    #print('dkx, dky:', dkx[0], dky[0])
    return k, dkx[0], dky[0]

def get_cosmo_pars(z):
    """
    Parameters
    ----------
    z : float
       The redshift

    Returns
    -------
    cosmo_pars : dict
       A dictionary of some cosmological parameters for a given redshift
    """

    h         = cosmo.H(z)/cosmo.H(0) # aka E(z) sometimes...
    rho_crit  = cosmo.critical_density(z)
    h70       = (cosmo.H(0) / (70.0*u.km / u.s / u.Mpc))
    d_ang     = get_d_ang(z)

    iv        = h.value**(-1./3)*d_ang.to('Mpc').value
    d_a_kpc   = d_ang.to('kpc').value
    Scale     = d_a_kpc*np.pi/(3600*180)       # kpc per arcsec

    print("kpc per arcsecond: ",Scale)

    cosmo_pars={"hofz":h,"d_ang":d_ang,"d_a":d_a_kpc,"rho_crit":rho_crit,
                "h70":h70,"iv":iv,"z":z,"scale":Scale}

    return cosmo_pars
    
def rMP500_from_y500(yinteg,cosmo_pars,ySZ=True,ySph=True,YMrel=defaultYM):
    """
    Parameters
    ----------
    yinteg : float
       A particular integrated Y
    cosmo_pars : dict
       A dictionary of cosmological parameters for a given redshift.
    ySZ : bool
       Is your integrated Y coming from SZ?
    ySph : bool
       Is your integrated Y a spherical integration?
    YMrel : str
       Which scaling relation are you using?

    Returns
    -------
    r500 : float
       Inferred R500, in radians
    M500_i : quantity
       Inferred M500, with units
    P500 : quantity
       Inferred P500, with units
    msys : float
       Inferred systematic error (value) in units of 1e14 solMass
    """

    h        = cosmo_pars['hofz']
    d_a      = cosmo_pars['d_a']/1000.0
    rho_crit = cosmo_pars['rho_crit']
    E        = h*1.0
    h70      = cosmo_pars['h70']

    ycyl    = not ySph
    AAA,BBB = get_AAA_BBB(YMrel,500,ycyl=ycyl)
    M500_i  = m_delta_from_ydelta(yinteg,cosmo_pars,delta=500,ycyl=ycyl,YMrel=YMrel,h70=h70)*u.Msun
    R500_i  = (3 * M500_i/(4 * np.pi  * 500.0 * rho_crit))**(1/3.)
    Mpc     = R500_i.decompose()
    Mpc     = Mpc.to('Mpc')
    r500    = (Mpc.value / d_a)

    #P500 = (1.65 * 10**-3) * ((E)**(8./3)) * ((
    #    M500_i * h70)/ ((3*10**14) * const.M_sun)
    #    )**(2./3) * h70**2 * u.keV / u.cm**3
    P500 = (1.65 * 10**-3) * ((E)**(8./3)) * ((
        M500_i * h70)/ ((3*10**14 * h70**(-1)) * const.M_sun)
        )**(2./3+0.11) * h70**2 * u.keV / u.cm**3

    #logy  = np.log10(lside)
    if ySZ == True:
        iv      = h**(-1./3)*d_a
        lside   = iv**2
    else:
        lside   = 1.0

    logy  = np.log10(lside*yinteg)
    msys = get_YM_sys_err(logy,YMrel,delta=500,ySph=ySph,h70=h70)
    
    return r500, M500_i, P500, msys

def m_delta_from_ydelta(y_delta,cosmo_pars,delta=500,ycyl=False,YMrel=defaultYM,h70=1.0):
    """
    Parameters
    ----------
    y_delta : float
       A particular integrated Y
    cosmo_pars : dict
       A dictionary of cosmological parameters for a given redshift.
    delta : float
       Which density contrast, 500 or 2500?
    ycyl : bool
       Is your integrated Y a cylindrical integration?
    YMrel : str
       Which scaling relation are you using?
    h70 : float
       Hubble parameter normalization

    Returns
    -------
    Mdelta : quantity
       Inferred M_delta, without units
    """
    h        = cosmo_pars['hofz']
    d_a      = cosmo_pars['d_a']/1000.0
    iv       = h**(-1./3)*d_a

    myYdelta = y_delta * (iv**2)

    #print(YMrel)
    AAA,BBB = get_AAA_BBB(YMrel,delta,ycyl=ycyl,h70=h70)

    m_delta = ( myYdelta.value / 10**BBB )**(1./AAA)

    return m_delta

def get_YM_sys_err(logy,YMrel,delta=500,ySph=True,h70=1.0):
    """
    An attempt to propagate errors based on uncertainties reported in the literature.

    Parameters
    ----------
    logy : float
       The base 10 logarithm of the integrated Y value
    YMrel : str
       Which scaling relation are you using?
    delta : float
       Which density contrast, 500 or 2500?
    ySph : bool
       Is your integrated Y a spherical integration?
    h70 : float
       Hubble parameter normalization

    Returns
    -------
    xer : quantity
       Inferred systematic error, fractional
    """

    #if hasattr(logy,'__len__'):
    #    raise AttributeError
    
    if delta == 500:
        if YMrel == 'A10':
            pivot = 3e14; Jofx  = 0.6145 if ySph else 0.7398
            Norm  = 2.925e-5 * Jofx * h70**(-1); PL = 1.78
            #t1   = ((logy - 1)/PL )*0.024
            t1   = 0.024 / PL
            t2   = ((np.log10(Norm) - logy)/PL**2)*0.08
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            #import pdb;pdb.set_trace()
        elif YMrel == 'A11':
            t1   = 0.29 # Fixed slope
            t2   = 0.1
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            print(xer)
        elif YMrel == 'M12':
            trm1   = np.array([1.0,logy + 5.0])
            #trm1   = np.array([1.0,5.0])
            #t1   = np.array([0.367,0.44])
            tcov = np.array([[0.098**2,-0.012],[-0.012,0.12**2]])
            #tcov = np.array([[0.098**2,-(0.012**2)],[-(0.012**2),0.12**2]])
            #tcov = np.array([[0.098**2,0],[0,0.12**2]])
            t2   = np.abs(np.matmul(trm1,np.matmul(tcov,trm1)))
            xer  = np.sqrt(t2) * np.log(10)
            print(xer)
            raise Exception
        elif YMrel == 'M12-SS':
            t1   = 0.0 # Fixed slope
            t2   = 0.036
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            print(xer)
        elif YMrel == 'P14':
            t1   = 0.06
            t2   = 0.079
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            print(xer)
        elif YMrel == 'P17':
            Norm = -4.305; PL = 1.685
            t1   = 0.009 / PL
            t2   = ((Norm - logy)/PL**2)*0.013
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            #xer = 0.104
        elif YMrel == 'H20':
            pivot = 3e14; 
            Norm  = 10**(-4.739); PL = 1.79
            #t1   = ((logy - 1)/PL )*0.024
            t1   = 0.003 / PL
            t2   = ((np.log10(Norm) - logy)/PL**2)*0.015
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
        else:
            print('No match!')
            import pdb;pdb.set_trace()
    elif delta == 2500:
        if YMrel == 'A10':
            #LogNorm = -28.13; PL = 1.637
            #t1   = 0.88 / PL 
            #t2   = ((logy - LogNorm)/PL**2)*0.062
            #xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            xer  = np.log(1 + 0.23)
        elif YMrel == 'A11':
            t1   = 0.29 # NOT CORRECT! TAKEN FROM DELTA=500!!!
            t2   = 0.1  # NOT CORRECT! TAKEN FROM DELTA=500!!!
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            print(xer)
        elif YMrel == 'M12':
            trm1   = np.array([1.0,logy+5])
            #trm1   = np.array([1.0,5.0])
            #t1   = np.array([0.367,0.44])
            #tcov = np.array([[0.063**2,-0.008],[-0.008,0.14**2]])
            tcov = np.array([[0.063**2,-(0.008**2)],[-(0.008**2),0.14**2]])
            #tcov = np.array([[0.098**2,0],[0,0.12**2]])
            t2   = np.abs(np.matmul(trm1,np.matmul(tcov,trm1)))
            xer  = np.sqrt(t2) * np.log(10)
            print(xer)
            raise Exception
        elif YMrel == 'M12-SS':
            t1   = 0.0 # Fixed slope
            t2   = 0.033
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            print(xer)
        elif YMrel == 'P14':
            t1   = 0.06  ### M500 numbers
            t2   = 0.079
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            print(xer)
        elif YMrel == 'P17':
            Norm = -4.5855; PL = 1.755
            t1   = 0.014 / PL
            t2   = ((Norm - logy)/PL**2)*0.020
            xer  = np.sqrt(t1**2 + t2**2) * np.log(10)
            #xer = 0.104
        elif YMrel == 'H20':
            xer  = np.log(1 + 0.23) ## B/C why not
        else:
            print('No match!')
            import pdb;pdb.set_trace()
    else:
        print('No match for delta!')
        import pdb;pdb.set_trace()

    return xer
        
def r2m_delta(radius,z,delta=500):
    """

    Parameters
    ----------
    radius : float
       :math:`R_{\\delta}`
    z : float
       Redshift
    delta : float
       :math:`\\delta`

    Returns
    -------
    M_delta : float
       :math:`M_{\\delta}`
    """

    rho_crit = cosmo.critical_density(z)
    M_delta = 4 * np.pi / 3 * (radius*u.kpc)**3 * delta * rho_crit
    M_delta = M_delta.to('M_sun').value

    return M_delta

def m2r_delta(mass,z,delta=500):
    """

    Parameters
    ----------
    masss : float
       :math:`M_{\\delta}`
    z : float
       Redshift
    delta : float
       :math:`\\delta`

    Returns
    -------
    R_delta : float
       :math:`R_{\\delta}`
    """

    rho_crit = cosmo.critical_density(z)
    M_delta = mass * u.Msun   # In solar masses
    R_delta = (3 * M_delta/(4 * np.pi  * delta * rho_crit))**(1/3.)
    R_delta = R_delta.to('kpc').value

    return R_delta

