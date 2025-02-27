import numpy as np
import astropy.units as u
from scipy.interpolate import interp1d # numpy should be faster...
import scipy.special as sps
#import warnings

def log_profile(args,r_bins,radii,alphas=[],rintmax=[],finite=False):
    """   
    Performs logarithmic interpolation and extrapolation. This can easily be improved, but hasn't been the bottleneck.
    
    r_bins and radii must be in the same units.
    Parameters
    ----------
    args : class:`numpy.ndarray`
       binned values (assumed to be pressure)
    r_bins : class:`numpy.ndarray`
       bin edges
    radii : class:`numpy.ndarray`
       radial points onto which you will interpolate or extrapolate
    alphas: array-like, optional
       If zeros or an empty list, this function will calculate power law index between bins.
    rintmax : array-like, optional
       If zeros or an empty list, integration extends to infinity. Default is [].
    finite : bool
       Do not integrate to infinity; stop at last value in r_bins.

    Returns
    -------
    presprof : Interpolated (pressure) profile
    alphas : The power-law indices between bins (e.g. pressures)
    """

    #warnings.showwarning = handle_warning
    
    #r_uniqe = np.unique(r_bins)
    #mybins=[0] + r_bins
    if not finite:
        mybins=np.insert(r_bins,0,0)
        mybins[-1]=-1
        #import pdb;pdb.set_trace()
    else:
        mybins = r_bins.copy()
        #import pdb;pdb.set_trace()
        
    presprof=np.zeros(len(radii))
    #        ifht=('alphas' in dir())
    ifht=('alphas' in locals())
    if ifht: 
        if sum(alphas) != 0:
            aset=1
        else:
            aset=0
            alphas = np.zeros(len(r_bins))
    else:
        aset=0
        alphas = np.zeros(len(r_bins))
        
    ycyl=0.0 # Y_500,cyl integration.
    ### Actually, I am not calculating Ycyl here!!! Stupid me. I could 
    ### calculate Ysph here though...

    badind = 0
    nfor = len(r_bins)-1 if finite else len(r_bins)
    for idx in range(nfor):
        rin=mybins[idx]
        if idx+1 == len(mybins):
            import pdb;pdb.set_trace()
        rout=mybins[idx+1]
        epsnot=args[idx]
        alpha=alphas[idx]
        if rin == rout:
            badind = idx
            continue        
        if rin == 0:
            lr=np.log10(mybins[idx+2]/mybins[idx+1])
            lp=np.log10(args[idx+1]/args[idx])
            if aset == 0:
                alpha=-lp/lr
                #                myind=np.where((radii < rout) & (radii >= rin))
            myind=(radii < rout) & (radii >= rin)
            myrad=radii[myind]
            mypres=epsnot*(myrad/rout)**(-alpha)
            # I'm often not using the integrated y; but we can keep it for now.
            yint = 0 if rin == 0 else 1.0 - (rin/rout)**(2-alpha)
            # but this ensures an error if alpha >2 ...
            rnot=rout
        elif rout == -1:
            lr=np.log10(r_bins[idx]/r_bins[idx-1])
            lp=np.log10(args[idx]/args[idx-1])
            if aset == 0:
                alpha=-lp/lr
            epsnot=args[idx-1]
            #                myind=(radii >= rin)
            myind=np.where(radii >= rin)
            myrad=radii[myind]
            mypres=epsnot*(myrad/rin)**(-alpha)
            rnot=rin
            yint = -1.0
            if np.sum(rintmax) > 0:
                yint = (rintmax/rnot)**(2-alpha) - 1.0

        else:
            lr=np.log10(mybins[idx+1]/mybins[idx])
            lp=np.log10(args[idx]/args[idx-1])
            if aset == 0:
                alpha=-lp/lr
            myind=np.where((radii < rout) & (radii >= rin))
            #                myind=(radii < rout) & (radii >= rin)
            myrad=radii[myind]
            mypres=epsnot*(myrad/rout)**(-alpha)
            rnot=rin
            yint = (rout/rin)**(2-alpha) - 1.0
            
        presprof[myind]=mypres
        if aset == 0:
            alphas[idx]=alpha

        ypref = 2*np.pi*epsnot*(rnot**2)/(2-alpha)
        if np.sum(rintmax) > 0:
            if rin < rintmax:
                if (rout > 0) & (rout <= rintmax):
                    yint=(rintmax/rnot)**(2-alpha)-1.0
                ycyl=ycyl + ypref*yint

            return presprof,alphas,ycyl
        # back to this placent

    if badind > 0:
        alphas = np.delete(alphas,badind)
        
    if aset == 0:
        return presprof,alphas
    else:
        return presprof

def binsky(args,r_bins,theta_range,theta,inalphas=[]):
    """
    Returns a surface brightness map for a binned profile, slopes, and radial integrals.
    
    Parameters
    ----------
     args : class:`numpy.ndarray`
       Pressure for each bin used
    r_bins: class:`numpy.ndarray`
       bin edges
    theta_range : class:`numpy.ndarray`
       Highly sampled array of radii.
    theta : class:`numpy.ndarray`
       A map of azimuthal angles.
    inalphas : list
       Generally best to leave as an empty list.

    Returns
    -------
    outmap: class:`numpy.ndarray`
    alphas: class:`numpy.ndarray`
    integrals: class:`numpy.ndarray`
    """
    Int_Pres,alphas,integrals = analytic_shells(r_bins,args,theta_range,alphas=inalphas)
    fint = interp1d(theta_range, Int_Pres, bounds_error = False, 
                    fill_value = 0)
    nx, ny = theta.shape
    #map = np.float64(fint(theta.reshape(nx * ny))) # Type 17 = float? (Implicitly float 32?)
    map = fint(theta.reshape(nx * ny)) # Type 17 = float? (Implicitly float 32?)
    outmap = map.reshape(nx,ny)

    return outmap,alphas,integrals

def prep_SZ_binsky(pressure, temp_iso, geoparams=None):
    """
    Small function, intended to do more (for relativistic corrections), but currently only allows for one ICM temperature.

    Parameters
    ----------
    pressure : array-like
        array of electron pressures
    temp_iso : float
       isothermal temperature
    geoparams : array-like
        [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]

    Returns
    -------
    edensity: class:`numpy.ndarray`
       Proxy for electron density (per cubic cm)
    etemperature: class:`numpy.ndarray`
       Proxy for electron temperature (times Bolzmann Constant; keV)
    geoparams: array-like
       [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    """
    edensity = np.array(pressure) / temp_iso
    etemperature = np.array(pressure)*0 + temp_iso
    if geoparams == None:
        geoparams = [0,0,0,1,1,1,0,0] # Spherical Geometry

    return edensity, etemperature, geoparams

def integrate_profiles(epressure, geoparams,r_bins,theta_range,inalphas=[],
                       beta=0.0,betaz=None,finint=False,narm=False,fixalpha=False,strad=False,
                       array="2",fullSZcorr=False,SZtot=False,columnDen=False,Comptony=True,
                       instrument='MUSTANG2',negvals=None,tmax=0):
    """
    Returns a Compton y profile for an input pressure profile.
    
    Parameters
    ----------
    epressure :  class:`numpy.ndarray`
       Electron pressure in units such that its integral over theta_range (itself in radians), results in the unitless Compton y parameter.
    geoparams : array-like
       [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    r_bins : array-like
       The (elliptical) bins, in radians, for the profile. 
    theta_range : class:`numpy.ndarray` 
       The range of angles for which to create a 1D profile (which can then be interpolated)
    inalphas :  array-like, optional
       This should generally be an empty list, unless modelling shocks.
    beta :float
       Fraction of the speed of light of the cluster bulk (peculiar) motion.
    betaz : float
       Fraction of the speed of light of the cluster along the line of sight.
    finint : bool
       Integrate out to last finite (defined) bin. Defaults to False
    narm : bool
       Normalized at R_Min. Defaults to False
    fixalpha : bool
       Fix alpha (to whatever inalpha is); useful for shocks.
    strad : bool
       STrict RADii; if the pressure model has to obey strict placements of radii, use this!
    array :str
       only used with NIKA2 data; which detector array is being used?
    fullSZcorr : bool
       integrate relativistic corrections along line of sight?
    SZtot : bool
       total SZ signal... not really useful
    columnDen : bool
       Set to true if you want to return the column density...?
    Comptony : bool
       When set (by default), returns Comptony profile
    instrument : str
       MUSTANG-2 by default. Used in relativistic calculations.
    negvals : class:`numpy.ndarray`(dtype=bool)
       Boolean array, the length of density_proxy.

    Returns
    -------
    Int_Pres : class:`numpy.ndarray`
       The combined los integrals over theta_range
    alphas : class:`numpy.ndarray`
       The power-law indices between bins (e.g. pressures)
    integrals : class:`numpy.ndarray`
       The los integral per bin (e.g. per shell), each across theta_range

    Notes
    __________
    * Ella should be set to 1. Therefore, define Ellb relative to Ella (and likewise with Ellc)
    * Xi is a sneaky gem.
    * integrals allows for sneakiness.
    """
    if betaz == None:
        betaz = beta
### If geoparams[6] > 0, then we are modelling some non-ellipsoid...perhaps a shock. If the opening angle
### is not set, then this will create a bimodal (bipolar) model component, which we almost certainly don't
### want. If we do want a bimodal component, then I think a better override is to use geoparams[7]= 2 pi.

    #eff_pres = np.zeros(len(etemperature)); y_press= np.zeros(len(etemperature))
                       
    Int_Pres,alphas,integrals = analytic_shells(r_bins,epressure,theta_range,alphas=inalphas,shockxi=geoparams[6],
                                                finite=finint,narm=narm,fixalpha=fixalpha,strad=strad,
                                                negvals=negvals,tmax=tmax)
    
    return Int_Pres,alphas,integrals
        
def general_gridding(xymap,theta_range,r_bins,geoparams,finite=False,taper='normal',
                     integrals=0,Int_Pres=0,ell_int=0,tap_int=0,oldvs=False,xyinas=True):
    """
    Returns a surface brightness map for a binned los-integrated profile (Int_Pres).
    
    Parameters
    ----------
    xymap: tuple of class:`numpy.ndarray`
       A tuple (x,y) where x and y are grids of their respective coordinates in << arceconds >>
    theta_range: class:`numpy.ndarray`
       Array of radii for the corresponding Int_Pres
    geoparams:array-like
       [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]

    Notes
    __________
    * Ella should be set to 1. Therefore, define Ellb relative to Ella (and likewise with Ellc)
    
    Returns
    -------
    mymap : class:`numpy.ndarray`
       A 2D map from input radial surface brightness profile
    """
    
    if geoparams[6] > 0.0:
        x,y = xymap;  mymap = np.zeros(x.shape); myrs = r_bins
        if geoparams[7] == 0:
            geoparams[7] = np.pi 
        if finite == True:
            myrs = myrs[:-1]
        #for idx, val in enumerate(myrs):
        #    if val == 0: val=r_bins[idx+1] # Correct units? I think so.
        #    if taper == 'inverse':
        #        mymap += grid_profile(theta_range, ell_int[idx,:], xymap, geoparams=geoparams)
        #        mymap -= grid_profile(theta_range, tap_int[idx,:], xymap, geoparams=geoparams,myscale=val,axis='y')
        #    else:
        #        mymap += grid_profile(theta_range, integrals[idx,:], xymap, geoparams=geoparams,myscale=val,axis='x')
        ######################################################################################
        ### The following has been rewritten 30 Mar 2018, in hopes of being faster.
        if myrs[0] == 0: myrs[0]=myrs[1] # Correct units? I think so.
        if taper == 'inverse':
            for my_int_add, my_int_sub, val in zip(ell_int, tap_int,myrs):
                mymap += grid_profile(theta_range, my_int_add, xymap, geoparams=geoparams,xyinas=xyinas)
                mymap -= grid_profile(theta_range, my_int_sub, xymap, geoparams=geoparams,myscale=val,axis='y',xyinas=xyinas)
        else:
            if oldvs == True:
                for my_int, val in zip(integrals, myrs):
                    mymap += grid_profile(theta_range, my_int, xymap, geoparams=geoparams,myscale=val,axis='x',xyinas=xyinas)
            else:
                mymap=iter_grid_profile_v2(integrals, myrs, theta_range, xymap, geoparams=geoparams,axis='x',xyinas=xyinas)
         ######################################################################################
    else:  
        mymap = grid_profile(theta_range, Int_Pres, xymap, geoparams=geoparams,myscale=1.0,xyinas=xyinas)

    return mymap


#########################################################################################################
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
###+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +###
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
###+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +###
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
###+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +###
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
###                                                                                                   ###
###                         Let's try to do things in a more general way                              ###
###                                                                                                   ###
###+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +###
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
###+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +###
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
###+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +###
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
###+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +###
#########################################################################################################


def binsky_SZ_general(epressure, geoparams,r_bins,theta_range,xymap,
                      inalphas=[],beta=0.0,betaz=None,finite=False,narm=False,fixalpha=False,
                      strad=False,array="2",instrument='MUSTANG2',taper='normal'):
    """
    Returns a surface brightness map for a binned profile fit, with far more generality than previously done.
    
    Parameters
    ----------
    epressure : array-like
       The electron pressure (no units in Python, but otherwise should be in cm**-3 keV**-1)
    geoparams : array-like
       [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    r_bins : array-like
       The (elliptical) bins for the profile. 
    theta_range : class:`numpy.ndarray`
       Array of radii for the corresponding Int_Pres
    xymap : tuple of class:`numpy.ndarray`
       A tuple (x,y) where x and y are grids of their respective coordinates in << arceconds >>
    inalphas : array-like
       Nothing to see here. Move along.
    beta : float
       Fraction of the speed of light of the cluster bulk (peculiar) motion.
    betaz : float
       Fraction of the speed of light of the cluster along the line of sight.
    finite : bool
       Integrate out to last finite (defined) bin.
    narm : bool
       Normalized at R_Min. This is important for integrating shells.
    strad : bool
       STrict RADii; if the pressure model has to obey strict placements of radii, use this!

    Notes
    __________
    * Ella should be set to 1. Therefore, define Ellb relative to Ella (and likewise with Ellc)
    
    Returns
    -------
    mymap : class:`numpy.ndarray`
       A 2D map from input radial surface brightness profile   
    """
    if betaz == None:
        betaz = beta
### If geoparams[6] > 0, then we are modelling some non-ellipsoid...perhaps a shock. If the opening angle
### is not set, then this will create a bimodal (bipolar) model component, which we almost certainly don't
### want. If we do want a bimodal component, then I think a better override is to use geoparams[7]= 2 pi.

    if geoparams[6] > 0:
        if geoparams[7] == 0:
            geoparams[7] = np.pi 
    
    map,alphas,integrals = binsky_general(epressure,geoparams,r_bins,theta_range,xymap,inalphas=inalphas,
                                          finite=finite,narm=narm,taper=taper,fixalpha=fixalpha,strad=strad)

    return map,alphas,integrals
        
def binsky_general(vals,geoparams,r_bins,theta_range,xymap,inalphas=[],
                   finite=False,narm=False,taper='normal',fixalpha=False,strad=False):
    """
    Returns a surface brightness map for a binned profile fit 
    
    Parameters
    __________
    vals : array-like
       The electron pressure (no units in Python, but otherwise should be in cm**-3 keV**-1)
    geoparams : array-like
       [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    r_bins : array-like
       The (elliptical) bins for the profile. 
    theta_range  : array-like
       The range of angles for which to create a 1D profile (which can then be interpolated)
    xymap : tuple
       A tuple (x,y) where x and y are grids of their respective coordinates in << arceconds >>
    inalphas : array-like
       Nothing to see here. Move along.
    beta : float
       Fraction of the speed of light of the cluster bulk (peculiar) motion.
    betaz : float
       Fraction of the speed of light of the cluster along the line of sight.
    finite : bool
       Integrate out to last finite (defined) bin.
    narm : bool
       Normalized at R_Min. This is important for integrating shells.
    strad : bool
       STrict RADii; if the pressure model has to obey strict placements of radii, use this!
    
    Notes:
    __________
    --> We should consider Ella to be RESTRICTED to 1. That is, Ellb and Ellc should always be calculated
    relative to the x-axis parameter.
    
    Returns
    -------
    mymap : class:`numpy.ndarray`
       A map that accounts for a range of geometrical restrictions. The integrals may not be applicable.

    """

    if taper == 'inverse':
        Ell_Pres,alphas,ell_int = analytic_shells(r_bins,vals,theta_range,alphas=inalphas,finite=finite,
                                                  narm=narm,fixalpha=fixalpha,strad=strad)
        Tap_Pres,tap_alph,tap_int = analytic_shells(r_bins,vals,theta_range,alphas=inalphas,
                                                    shockxi=geoparams[6],finite=finite,narm=narm,
                                                    fixalpha=fixalpha,strad=strad)
        integrals = ell_int - tap_int
    else:
        Int_Pres,alphas,integrals = analytic_shells(r_bins,vals,theta_range,alphas=inalphas,
                                                    shockxi=geoparams[6],finite=finite,narm=narm,
                                                    fixalpha=fixalpha,strad=strad)

############################################################################

    map = general_gridding(xymap,r_bins,geoparams,finite,narm,taper,strad,
                           integrals,Int_Pres,ell_int,tap_int)

    return map,alphas,integrals

def grid_profile(theta_range, profile, xymap, geoparams=[0,0,0,1,1,1,0,0],myscale=1.0,axis='z',
                 xyinas=True):
    """   
    Grids a sufficiently fine-resolution profile.

    Parameters
    __________
    theta_range: class:`numpy.ndarray`
       Abscisca (radii, in radians) for profile
    profile: class:`numpy.ndarray`
       Ordinate profile values
    xymap: tuple
       A tuple (x,y) where x and y are grids of their respective coordinates in << arceconds >>
    geoparams: array-like
       [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    myscale: float
       Rescale the profile (e.g. to account for elongation along the line of sight)
    axis: str
       scale about x, y, or z
    xyinas: bool
       xymap is in arcseconds (yes)

    Returns
    -------
    mymap : class:`numpy.ndarray`
       A map that accounts for a range of geometrical restrictions.
    """
    
    ### Get new grid:
    (x,y) = xymap
    x,y = rot_trans_grid(x,y,geoparams[0],geoparams[1],geoparams[2])
    x,y = get_ell_rads(x,y,geoparams[3],geoparams[4])
    radmap = np.sqrt(x**2 + y**2)
    theta = radmap*(u.arcsec).to("radian");  theta_min = np.min(theta_range)
#    import pdb;pdb.set_trace()
    bi=np.where(theta < theta_min);   theta[bi]=theta_min

    nx, ny = theta.shape
    fint = interp1d(theta_range, profile, bounds_error = False, fill_value = 0)
    #mymap = np.float64(fint(theta.reshape(nx * ny))) # Type 17 = float? (Implicitly float 32?)
    mymap = fint(theta.reshape(nx * ny)) # Type 17 = float? (Implicitly float 32?)
    mymap = mymap.reshape(nx,ny)
    ### And a couple more *necessary* modification:
    ### Where we want to scale it by a certain r_bin, given in radians. We also want to scale by "Ella", if axis='x':

    a2r   = (u.arcsec).to("radian")
    conv = a2r if xyinas else 1.0  # Is xymap in arcseconds or radions?
    
    if axis == 'x':
        xell = (x/(geoparams[3]*myscale))*conv # x is initially presented in arcseconds
        modmap = geoparams[5]*(xell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'y':
        yell = (y/(geoparams[4]*myscale))*conv # x is initially presented in arcseconds
        modmap = geoparams[5]*(yell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'z':
        modmap = mymap*0.0 + geoparams[5]      # Just the plain old LOS elongation factor
    
    mymap = mymap*modmap   # Very important to be precise here.
#    import pdb;pdb.set_trace()
    if geoparams[7] > 0:
#        angmap = np.arctan2(x,y)
        angmap = np.arctan2(y,x)
        #        gi = np.where(abs(angmap) < geoparams[7]/2.0)
        bi = np.where(abs(angmap) > geoparams[7]/2.0)
        #        import pdb; pdb.set_trace()
        mymap[bi] = 0.0

    return mymap

def get_ell_rads(x,y,ella,ellb):
    """   
    Get ellipsoidal radii from x,y standard

    Parameters
    __________
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
    
def rot_trans_grid(x,y,xs,ys,rot_rad):
    """   
    Shift and rotate coordinates

    Parameters
    __________
    x: class:`numpy.ndarray`
       coordinate along major axis (a) 
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

def ycylfromprof(Int_Pres,theta_range,theta_max):
    """
    Integrate Int_Pres over area to get y_cyl

    Parameters
    __________
    :param Int_Pres: array of Compton y values
    :type Int_Pres: class:`numpy.ndarray`
    :param theta_range: array of radii, in radians
    :type theta_range: class:`numpy.ndarray`
    :param theta_max: perform integral within this radius.
    :type theta_max: float

    """
    i=1 # Start at the second entry!
    Ycyl=0
    while i < len(theta_range):
        if theta_range[i] < theta_max:
            dtheta = theta_range[i]-theta_range[i-1]
            Yshell = 2.0*np.pi*theta_range[i]*dtheta*Int_Pres[i]
            Ycyl = Ycyl + Yshell
        i+=1

    return Ycyl

def analytic_shells(r_bins,vals,theta,alphas=[],shockxi=0.0,fixalpha=False,
                    finite=False,narm=False,strad=False,negvals=None,tmax=0):
    """
    Returns an integrated map of some signal along the line of sight. This routine
    assumes that the pressure within a shell has a power law distribution.
    
    Parameters
    __________
    r_bins    : class:`numpy.ndarray`
       The radial bins (in radians)
    vals      : class:`numpy.ndarray`
       Pressure for each bin used
    theta     : class:`numpy.ndarray`
       An array of radii (in radian) in the map, which will be used for gridding the model
    alphas    : array-like
       An array of power laws (indices) for 3d pressure distribution
    shockxi   : float
       Polar tapering, if used in a shock model.
    finite    : bool
        Set this keyword if you do NOT want to integrate to infinity.
    narm      : bool
       Normalize at R_min (within a bin)
    strad     : bool, optional
       STrict RADii. When using a shock model (e.g. Abell 2146), where specific radii, especially inner radii are defined, this keyword should be set! Note that if the finite keyword is set, then this does not need to be set. 
    negvals   : class:`numpy.ndarray`, optional
       None by default. Otherwise, set as boolean array, same length as r_bins

    Returns
    -------
    out       : class:`numpy.ndarray`
       Map convolved with the beam.          
    """
    if finite == False:
        iadj = 0
        if np.min(r_bins) != 0 and strad == False:
            mybins=np.append([0],r_bins)
            if len(mybins) == 3:
                mybins=np.append(mybins,[-1])
            else:
                mybins[-1]=-1
        else:
            mybins=np.append(r_bins,-1)
    else:
        # This almost looks wrong - but it should be right ( 20Jan2022 )
        # mybins retains the information, but this allows the for loop
        # to go over the correct number of indices.
        mybins = np.asarray(r_bins).copy()
        r_bins = r_bins[:-1]
        iadj   = 1 # 22 Jan 2022 ...OMG
            
#    import pdb; pdb.set_trace()
    nthetas = len(theta)
    integrals = np.zeros((len(r_bins),nthetas))
    if fixalpha == False:
        alphas = np.zeros(len(r_bins))

    badind=0
    for idx, myval in enumerate(r_bins):
        rin=mybins[idx]
        rout=mybins[idx+1]
        mypressure=vals[iadj+idx] # Gah, what a stupid way to do this.
        
        if rin == rout:
            badind = idx
            continue        
        
        if fixalpha == False:                  
            if rin == 0:
                lr=np.log10(mybins[idx+2]/mybins[idx+1])
                lp=np.log10(vals[idx+1]/vals[idx])
                alphas[idx]=-lp/lr
            elif rout == -1:
                lr=np.log10(r_bins[idx]/r_bins[idx-1])
                lp=np.log10(vals[iadj+idx]/vals[idx+iadj-1])
#                    lr=np.log10(mybins[idx]/mybins[idx-1])
#                    lp=np.log10(vals[idx-1]/vals[idx-2])
                alphas[idx]=-lp/lr
                mypressure=vals[idx+iadj-1]
            else:
                lr=np.log10(mybins[idx+1]/mybins[idx])
                lp=np.log10(vals[idx+iadj]/vals[idx+iadj-1])
                alphas[idx]=-lp/lr
                #if alphas[idx] < -20:
                #    import pdb;pdb.set_trace()
 
### Beware of 2.0*shockxi!!! (26 July 2017)
        #import pdb;pdb.set_trace()
        #integrals[idx] = shell_pl(mypressure,alphas[idx]+2.0*shockxi,rin,rout,theta,narm=narm) #R had been in here.
        ### 2*shockxi doesn't seem correct (17 Dec 2021)
        
        #if np.any(np.isnan(alphas)):
        #    import pdb;pdb.set_trace()

        integrals[idx] = shell_pl(mypressure,alphas[idx]+shockxi,rin,rout,theta,narm=narm,tmax=tmax) #R had been in here.

    #import pdb;pdb.set_trace()
    if negvals is None or np.sum(negvals) == 0:
        totals = np.sum(integrals,axis=0)  # This should accurately produce Compton y values.
    else:
        pdint  = integrals.copy()
        #import pdb;pdb.set_trace()
        pdint[negvals,:] *= -1
        totals = np.sum(pdint,axis=0)  # This should accurately produce Compton y values.
        #print("Hi")

    if badind > 0:
        alphas    = np.delete(alphas,badind)
        integrals = np.delete(integrals,badind,0)
        
    return totals,alphas,integrals

def iter_grid_profile(integrals, myrs, theta_range, xymap, geoparams=[0,0,0,1,1,1,0,0],axis='z'):
    """
    This largely copies the functionality of grid_profile, but is designed to be much faster for
    iterative applications (same geoparams)

    :param integrals: array of los-integrated values (i.e. SB profiles)
    :type integrals: class:`numpy.ndarray`
    :param myrs: array of bin radii
    :type myrs: array-like
    :param theta_range: profile of radii
    :type theta_range: class:`numpy.ndarray`
    :param xymap: tuple of arrays of x and y coordinates
    :type xymap: tuple
    :param geoparams   :  [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    :type geoparams    : array-like
    :param axis        :  scale about x, y, or z
    :type axis         : str
    """

    ### Get new grid:
    (x,y) = xymap
    x,y = rot_trans_grid(x,y,geoparams[0],geoparams[1],geoparams[2])
    x,y = get_ell_rads(x,y,geoparams[3],geoparams[4])
    radmap = np.sqrt(x**2 + y**2)
    theta = radmap*(u.arcsec).to("radian");  theta_min = np.min(theta_range)
    bi=np.where(theta < theta_min);   theta[bi]=theta_min
    nx, ny = theta.shape

    rsRads = myrs / np.min(myrs)   # This should be unitless from Python's perspective, but really in arcseconds.
    
    ### And a couple more *necessary* modification:
    ### Where we want to scale it by a certain r_bin, given in radians. We also want to scale by "Ella", if axis='x':
    if axis == 'x':
        xell = (x/(geoparams[3]*np.min(myrs)))*(u.arcsec).to("radian") # x is initially presented in arcseconds
        modmap = geoparams[5]*(xell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'y':
        yell = (y/(geoparams[4]*np.min(myrs)))*(u.arcsec).to("radian") # x is initially presented in arcseconds
        modmap = geoparams[5]*(yell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'z':
        modmap = np.zeros((nx,ny)) + geoparams[5]      # Just the plain old LOS elongation factor

    mymap = np.zeros(x.shape)
    for profile, myscale in zip(integrals, rsRads):
        
        fint = interp1d(theta_range, profile, bounds_error = False, fill_value = 0)
        #map = np.float64(fint(theta.reshape(nx * ny))) # Type 17 = float? (Implicitly float 32?)
        map = fint(theta.reshape(nx * ny)) # Type 17 = float? (Implicitly float 32?)
        map = map.reshape(nx,ny)
        map = map * modmap * (myscale**(-2*geoparams[6]))
        mymap+=map
        
    if geoparams[7] > 0:
        angmap = np.arctan2(y,x)
        bi = np.where(abs(angmap) > geoparams[7]/2.0)
        mymap[bi] = 0.0

    return mymap

def iter_grid_profile_v2(integrals, myrs, theta_range, xymap, geoparams=[0,0,0,1,1,1,0,0],axis='z',
                         xyinas=True):
    """
    This largely copies the functionality of grid_profile, but is designed to be much faster for
    iterative applications (same geoparams)

    :param integrals: array of los-integrated values (i.e. SB profiles)
    :type integrals: class:`numpy.ndarray`
    :param myrs: array of bin radii
    :type myrs: array-like
    :param theta_range: profile of radii
    :type theta_range: class:`numpy.ndarray`
    :param xymap: tuple of arrays of x and y coordinates
    :type xymap: tuple
    :param geoparams   :  [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    :type geoparams    : array-like
    :param axis        :  scale about x, y, or z
    :type axis         : str
    :param xinas       :  xymap is in arcseconds?
    :type xinas        : bool
    """

    a2r    = (u.arcsec).to("radian")
    conv   = a2r*1.0 if xyinas else 1.0
    ### Get new grid:
    (x,y) = xymap
    x,y = rot_trans_grid(x,y,geoparams[0],geoparams[1],geoparams[2])
    x,y = get_ell_rads(x,y,geoparams[3],geoparams[4])
    radmap = np.sqrt(x**2 + y**2)
    theta = radmap*conv;  theta_min = np.min(theta_range)
    bi=np.where(theta < theta_min);   theta[bi]=theta_min
    #nx, ny = theta.shape

    rsRads = myrs / np.min(myrs)   # This should be unitless from Python's perspective, but really in arcseconds.
    ### And a couple more *necessary* modification:
    ### Where we want to scale it by a certain r_bin, given in radians. We also want to scale by "Ella", if axis='x':
    if axis == 'x':
        xell = (x/(geoparams[3]*np.min(myrs)))*conv # x is initially presented in arcseconds
        modmap = geoparams[5]*(xell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'y':
        yell = (y/(geoparams[4]*np.min(myrs)))*conv # x is initially presented in arcseconds
        modmap = geoparams[5]*(yell**2)**(geoparams[6]) # Consistent with model creation??? (26 July 2017)
    if axis == 'z':
        modmap = np.zeros(theta.shape)*0.0 + geoparams[5]      # Just the plain old LOS elongation factor

    Int_Prof = np.zeros((integrals.shape[1]))

    for profile, myscale in zip(integrals, rsRads):
        Int_Prof+=  (myscale**(-2*geoparams[6])) * profile

    #import pdb;pdb.set_trace()
        
    fint = interp1d(np.float64(theta_range),np.float64(Int_Prof), bounds_error = False, fill_value = 0)
    #mymap = np.float64(fint(theta.reshape(theta.size))) # Type 17 = float? (Implicitly float 32?)
    mymap = fint(theta.reshape(theta.size)) # Type 17 = float? (Implicitly float 32?)
    mymap = mymap.reshape(theta.shape)
    mymap = mymap * modmap 
        
    if geoparams[7] > 0:
        angmap = np.arctan2(y,x)
        bi = np.where(abs(angmap) > geoparams[7]/2.0)
        mymap[bi] = 0.0

    return mymap

##############################################################
##############################################################
##############################################################


def shell_pl(epsnot,sindex,rmin,rmax,radarr,c=1.0,ff=1e-3,epsatrmin=0,
             narm=False,tmax=0):

    """
    The heart of this code. This routine calculates analytic los integrals depending on the case.

    :param epsnot: The normalization factor. The default behavior is for this to be defined at RMAX, the outer edge of a sphere or shell. If you integrate to infinity, then this should be defined at RMIN. And of course, RMIN=0, and RMAX as infinity provides no scale on which to define EPSNOT. See the optional variable EPSATRMIN.
    :type epsnot: float
    :param sindex: "Spectral Index". That is, the power law (without the minus sign) that the "emissivity" follows within your bin. If you want to integrate to infinity, you must have SINDEX > 1. All other cases can handle any SINDEX value.
    :type sindex: float
    :param rmin: Minimum radius for your bin. Can be 0.
    :type rmin: float
    :param rmax: Maximum radius for your bin. If you wish to set this to infinity, then set it to a negative value.
    :type rmax: float
    :param radarr: A radial array of projected radii (same units as RMIN and RMAX) for which projected values will be calculated. If the innermost value is zero, its value, in the scaled radius array will be set to FF.
    :type radarr: class:`numpy.ndarray`
    :param c: The scaling axis for an ellipse along the line of sight. Default is 1.0
    :type c: float
    :param ff: Fudge Factor, but more of a thresholding factor. Default is 1e-3.
    :type ff: float
    :param epsatrmin: Set this to a value greater than 0 if you want EPSNOT to be defined at RMIN. This automatically happens if RMAX<0
    :type epsatrmint: float
    :param narm: Normalized At R_Min. This option specifies that you have *already* normalized the bins at R_Min (for a shell case). The other two cases are strictly imposed where the normalization is set. The default is False, because that is just how I started using this.
    :type narm: bool
    :param tmax: Maximum theta (from the nose - of, say, a shock).
    :type tmax: float

    NOTE: If RMIN = 0 and RMAX < 0, then this program will return 0.
    """

    ##############################################################
    ### OUTPUTS:
    #
    # PLINT     - PLINT is the integration along the z-axis (line of sight) for
    #             an ellipsoid (a sphere) where the "emissivity" is governed by
    #             a power law. The units are thus given as the units on EPSNOT
    #             times the units on RADARR (and therefore RMIN and RMAX).
    #
    #             It is then dependent on you to make the appropriate
    #             conversions to the units you would like.
    # 
    ##############################################################
    ### Perform some double-checks.

    if rmin < 0:
        print('found rmin < 0; setting rmin equal to 0')
        rmin = 0

    rrmm = (radarr==np.amin(radarr))
    if (radarr[rrmm] == 0) and (sindex > 0):
        radarr[rrmm]=ff

    ##############################################################
    ### Determine the appropriate case (and an extra double check)

    if rmax < 0:
        if rmin == 0:
            scase=3
        else:
            scase=2
            epsatrmin=1
    else:
        if rmin == 0:
            scase=0
        else:
            if rmin < rmax:
                scase=1
                epsatrmin=1
            else:
                print('You made a mistake: rmin > rmax; sending to infty integration.')
                ### If a mistake is possible, it will happen, eventually.
                scase=3

    ### Direct program to appropriate case:
    shellcase = {0: plsphere, # You are integrating from r=0 to R (finite)
                 1: plshell,  # You are integrating from r=R_1 to R_2 (finite)
                 2: plsphole, # You are integrating from r=R (finite, >0) to infinity
                 3: plinfty,  # You are integrating from r=0 to infinity
                 }

    ##############################################################
    ### Redo some numbers to agree with hand-written calculations

    p = sindex/2.0 # e(r) = e_0 * (r^2)^(-p) for this notation / program

    ### In a way, I actually like having EPSNORM default to being defined at RMIN
    ### (Easier to compare to hand-written calculations.

    if scase ==1 and narm == False:
        epsnorm=epsnot*(rmax/rmin)**(sindex)
    else:
        epsnorm=epsnot

    ### Prefactors change a bit depending on integration method.
    ### These are the only "pre"factors common to all (both) methods.
    prefactors=epsnorm*c
    ### Now integrate for the appropriate case
    myintegration = shellcase[scase](p,rmin,rmax,radarr,tmax=tmax)
  
    answer = myintegration*prefactors  ## And get your answer!
  
    return answer

##############################################################
##### Integration cases, as directed above.              #####
##############################################################

def plsphere(p,rmin,rmax,radarr,tmax=0):
    """
    Analytic los integral for a full sphere.

    :param p: "Spectral Index". That is, the power law (without the minus sign) that the "emissivity" follows within your bin. If you want to integrate to infinity, you must have SINDEX > 1. All other cases can handle any SINDEX value.
    :type p: float
    :param rmin: Minimum radius for your bin. This is 0 for the sphere.
    :type rmin: float
    :param rmax: Maximum radius for your bin. If you wish to set this to infinity, then set it to a negative value.
    :type rmax: float
    :param radarr: A radial array of projected radii (same units as RMIN and RMAX) for which projected values will be calculated. If the innermost value is zero, its value, in the scaled radius array will be set to FF.
    :type radarr: class:`numpy.ndarray`
    :param tmax: Maximum theta (from the nose - of, say, a shock).
    :type tmax: float
    """

    
    c1 = radarr<=rmax              # condition 1
    c2 = radarr>rmax               # condition 2
#    c1 = np.where(radarr<=rmax)     # condition 1
#    c2 = np.where(radarr>rmax)      # condition 2
    sir=(radarr[c1]/rmax)           # scaled radii
    isni=((2.0*p==np.floor(2.0*p)) and (p<=1)) # Special cases -> "method 2"
    plinn = sir**(1.0-2.0*p)
    if tmax > 0:
        ct = np.cos(tmax)
        igi = (sir < ct)
        sir[igi] = ct
    if isni:
      tmax=np.arctan(np.sqrt(1.0 - sir**2)/sir)   # Theta max
      plint=myredcosine(tmax,2.0*p-2.0)*plinn*2.0 # Integration + prefactors
    else:
      cbf=(sps.gamma(p-0.5)*np.sqrt(np.pi))/sps.gamma(p) # complete beta function
      ibir=myrincbeta(sir**2,p-0.5,0.5)               # incomplete beta function
      plint=plinn*(1.0-ibir)*cbf     # Apply appropriate "pre"-factors

    myres=radarr*0          # Just make my array (unecessary?)
    myres[c1]=plint         # Define values for R < RMIN

    #if np.any(np.isnan(myres)):
    #    import pdb;pdb.set_trace()
    
    return myres*rmax               # The results we want

def plshell(p,rmin,rmax,radarr,tmax=0):
    """
    Analytic los integral for a spherical shell.

    :param p: "Spectral Index". That is, the power law (without the minus sign) that the "emissivity" follows within your bin. If you want to integrate to infinity, you must have SINDEX > 1. All other cases can handle any SINDEX value.
    :type p: float
    :param rmin: Minimum radius for your bin. This is 0 for the sphere.
    :type rmin: float
    :param rmax: Maximum radius for your bin. If you wish to set this to infinity, then set it to a negative value.
    :type rmax: float
    :param radarr: A radial array of projected radii (same units as RMIN and RMAX) for which projected values will be calculated. If the innermost value is zero, its value, in the scaled radius array will be set to FF.
    :type radarr: class:`numpy.ndarray`
    :param tmax: Maximum theta (from the nose - of, say, a shock).
    :type tmax: float
    """    
    c1 = radarr<=rmax              # condition 1
    c2 = radarr[c1]<rmin           # condition 2
    c3 = radarr<rmin               # c1[c2] as I would expect in IDL
#    c1 = np.where(radarr<=rmax)     # condition 1
#    c2 = np.where(radarr[c1]<rmin)  # condition 2
    sir=(radarr[c1]/rmin)           # scaled inner radii
    sor=(radarr[c1]/rmax)           # scaled outer radii

    plinn=sir**(1.0-2.0*p)                 # Power law term for inner radii
    
    if tmax > 0:
        ct = np.cos(tmax)
        igi = (sir < ct)
        ogi = (sor < ct)
        sir[igi] = ct
        sor[ogi] = ct
    isni=((2.0*p==np.floor(2.0*p)) and (p<=1)) # Special cases -> "method 2"
    myres=radarr*0                  # Just make my array (unecessary?)
    if isni:
      tmxo=np.arctan(np.sqrt(1.0 - sor**2)/sor)         # Theta max...outer circle
      tmxi=np.arctan(np.sqrt(1.0 - sir[c2]**2)/sir[c2]) # Theta max...inner circle
      plint=myredcosine(tmxo,2.0*p-2.0)              # Integrate for outer circle.
      plint[c2]-=myredcosine(tmxi,2.0*p-2.0) # Integrate and subtract inner circle
#      myres[c1]=plint*(sor**(1.0-2.0*p))*2.0    # Pre-(24 July 2017) line.
      myres[c1]=plint*plinn*2.0    # Apply appropriate "pre"-factors
      
    else:
      cbf=(sps.gamma(p-0.5)*np.sqrt(np.pi))/sps.gamma(p) # complete beta function
      ibir=myrincbeta(sir[c2]**2,p-0.5,0.5) # Inc. Beta for inn. rad.
      ibor=myrincbeta(sor**2,p-0.5,0.5)     # Inc. Beta for out. rad.
      #plinn=(sir**(1.0-2.0*p))                 # Power law term for inner radii
      myres[c1]=plinn*(1.0-ibor)*cbf           # Define values for the enclosed circle
#      import pdb;pdb.set_trace()
#      myres[c1[c2]]=plinn[c2]*(ibir-ibor[c2])*cbf # Correct the values for the
### Changed this March 9, 2018:
      myres[c3]=plinn[c2]*(ibir-ibor[c2])*cbf # Correct the values for the 
      # inner circle
      
    #if np.any(np.isnan(myres)):
    #    import pdb;pdb.set_trace()
                                               
    return myres*rmin                          # The results we want

def plsphole(p,rmin,rmax,radarr,tmax=0):
    """
    Analytic los integral for out to infinity, but missing a spherical core.

    :param p: "Spectral Index". That is, the power law (without the minus sign) that the "emissivity" follows within your bin. If you want to integrate to infinity, you must have SINDEX > 1. All other cases can handle any SINDEX value.
    :type p: float
    :param rmin: Minimum radius for your bin. This is 0 for the sphere.
    :type rmin: float
    :param rmax: Maximum radius for your bin. If you wish to set this to infinity, then set it to a negative value.
    :type rmax: float
    :param radarr: A radial array of projected radii (same units as RMIN and RMAX) for which projected values will be calculated. If the innermost value is zero, its value, in the scaled radius array will be set to FF.
    :type radarr: class:`numpy.ndarray`
    :param tmax: Maximum theta (from the nose - of, say, a shock).
    :type tmax: float
    """    
    
    if p <= 0.5:
        return radarr*0 - 1.0e10

    else:
        c1 = radarr<rmin               # condition 1
        c2 = radarr>=rmin              # condition 2
        #      c1 = np.where(radarr<rmin)     # condition 1
        #      c2 = np.where(radarr>=rmin)    # condition 2
        sr=(radarr/rmin)               # scaled radii
        plinn=(sr**(1.0-2.0*p))          # Power law term
        if tmax > 0:
            ct = np.cos(tmax)
            gi = (sr < ct)
            sr[gi] = ct
        cbf=(sps.gamma(p-0.5)*np.sqrt(np.pi))/sps.gamma(p) # complete beta function
        ibor=myrincbeta(sr[c1]**2,p-0.5,0.5) # Inc. Beta for out. rad.
        myres=radarr*0                 # Just make my array (unecessary?)
        myres[c1]=plinn[c1]*ibor*cbf     # Define values for R < RMIN
        myres[c2]=plinn[c2]*cbf          # Define values for R > RMIN
        #if np.any(np.isnan(myres)):
        #    import pdb;pdb.set_trace()
        
        return myres*rmin

def plinfty(p,rmin,rmax,radarr,tmax=None):
    """
    Analytic los integral for infinity. It doesn't work. Returns 0.

    :param p: "Spectral Index". That is, the power law (without the minus sign) that the "emissivity" follows within your bin. If you want to integrate to infinity, you must have SINDEX > 1. All other cases can handle any SINDEX value.
    :type p: float
    :param rmin: Minimum radius for your bin. This is 0 for the sphere.
    :type rmin: float
    :param rmax: Maximum radius for your bin. If you wish to set this to infinity, then set it to a negative value.
    :type rmax: float
    :param radarr: A radial array of projected radii (same units as RMIN and RMAX) for which projected values will be calculated. If the innermost value is zero, its value, in the scaled radius array will be set to FF.
    :type radarr: class:`numpy.ndarray`
    :param tmax: Maximum theta (from the nose - of, say, a shock).
    :type tmax: float
    """    
    sr=(radarr)                      # scaled radii
    cbf=(sps.gamma(p-0.5)*np.sqrt(np.pi))/sps.gamma(p) # complete beta function
    plt=(sr**(1.0-2.0*p))          # Power law term

### There is no scaling to be done: RMIN=0; RMAX=infinity...
### This is madness, but if you can set >>SOME<< scaling radius, this can work.
### However, the practical implementation of this is not foreseen / understood
### how it should look. Therefore, for now, I will return 0.

    return 0       # Scale invariant. Right. Fail.


def myrincbeta(x,a,b):
    """
    compute the regularized incomplete beta function.
    .. math::

        B(x;a,b) \\equiv \\int_0^x u^{a-1} (1-u)^{b-1} du

    :param x: Reflective of the radius out to which this is computed
    :type x: float
    :param a: Nameless parameter?
    :type a: float
    :param b: Nameless parameter?
    :type b: float
    """
    if a < 0:
        cbf=(sps.gamma(a)*sps.gamma(b))/sps.gamma(a+b)
        res = (x**a * (1.0-x)**b) / (a * cbf)
        #if np.any(np.isnan(res)):
        #    import pdb;pdb.set_trace()
        return myrincbeta(x,a+1.0,b) + res
    else:
        #      cbf=(sps.gamma(a)*sps.gamma(b))/sps.gamma(a+b)
        cbf=1.0 # sps.betainc is the regularized inc. beta fun.
        res=(sps.betainc(a,b,x) / cbf)
        return res
    
def myredcosine(tmax,n):
    """
    computes 
    .. math::

    \int_0^tmax cos^n(x) dx

    :param tmax: :math:`\\theta_{max}`
    :type tmax: float
    :param n: exponent
    :type n: int

    """

    if n < -2:
        res=np.cos(tmax)**(n+1)*np.sin(tmax)/(n+1) 
        return myredcosine(tmax,n+2)*(n+2)/(n+1) - res
    else:
        if n == 0:
            res=tmax
        if n == -1:
            res=np.log(np.absolute(1.0/np.cos(tmax) + np.tan(tmax)) )
        if n == -2:
            res=np.tan(tmax) 

    return res

def ycyl_prep(Int_Pres,theta_range):
    """
    Just preparing some numbers.

    :param Int_Pres: integrated pressures
    :type Int_Pres: class:`numpy.ndarray`
    :param theta_range: radii
    :type theta_range: class:`numpy.ndarray`

    """

    lnp = np.log(Int_Pres)
    ltr = np.log(theta_range)

    alpha = (np.roll(lnp,-1) - lnp ) / (np.roll(ltr,-1) - ltr )
    k     = Int_Pres / theta_range**alpha

    return alpha,k

def handle_warning(message, category, filename, lineno, file=None, line=None):
    print('A warning occurred:')
    print(message)
    print('Do you wish to continue?')

    while True:
        response = input('y/n: ').lower()
        if response not in {'y', 'n'}:
            print('Not understood.')
        else:
            break

    if response == 'n':
        import pdb;pdb.set_trace()
        #raise category(message)
