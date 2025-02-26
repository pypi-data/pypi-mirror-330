import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#from matplotlib import cm
#from matplotlib import colormaps
from reproject import reproject_interp
from astropy.wcs import WCS
from astropy.io import fits
import scipy.ndimage

def get_rms_cmap():
    """
    Tiny function to get a colormap with desired indexing, and importantly make values above or below it white.

    :return: colormap
    :rtype: object
    """
    #mycmap=cm.get_cmap('tab20b').copy()
    #mydcm=cm.get_cmap('tab20b',256)
    mycmap=plt.get_cmap('tab20b',256)
    #mycmap=colors.Colormap('tab20b')
    #mydcm = colors.Colormap('tab20b',256)
    #newcolors = mydcm(np.linspace(0,1,256))
    mycmap.set_under('w')
    mycmap.set_over('w')
    
    return mycmap

def conv_wtmap_torms(wtmap):

    """
    Converts a weightmap to an rms map.

    :param wtmap: a weightmap
    :type wtmap: numpy.ndarray
    :return: rmsmap
    :rtype: numpy.ndarray
    """

    gi         = (wtmap > 0)
    rmsmap     = np.zeros(wtmap.shape)
    rmsmap[gi] = 1.0/np.sqrt(wtmap[gi])

    return rmsmap

def plot_rms_general(hdul,savefile,vmin=18,vmax=318,myfs=15,rmsmap=None,nscans=None,
                     prntinfo=False,cmark=True,ggmIsImg=False,tlo=True,wtcut=0.1,
                     cra=0,cdec=0,ggm=False,ggmCut=0.05,cc='k',ncnts=0,title=None,
                     tsource=0,R500=0,r5col="c",zoom=1,noaxes=False,verbose=False,
                     imgext=0,ggmPix=5.0,mask=None):

    """
    Make a nice image (via imshow) of the RMS map.

    Parameters
    ----------
    hdul : list(obj)
       Any list of objects obtained from fits.open()

    savefile : str
       A string with the full path of where to save the output image (assumed to be a png).

    vmin : float
       Minimum RMS value (in the colorbar).
    vmax : float
       Maximum RMS value (in the colorbar).
    myfs : float
       Fontsize for labels and such.
    rmsmap : numpy.ndarray
       An 2D array constituting the RMSmap. The assumption is that ext=1 in the input hdul is the weightmap. If this is not the case, then the RMSmap can be supplied here.
    nscans : int
       Number of Lissajous Daisy scans to achieve integration time. (optional)
    prntinfo : bool
       Set this to print information on the figure.
    cmark : bool
       Mark the center of the cluster. To be used in tandem with cra and cdec.
    ggmIsImg : bool
       If you want to display the GGM image instead of the RMS map, set this
    tlo : bool
       Hard-coded application of a tight layout for the figure.
    wtcut : float
       A weight cut for selecting regions in the map.
    cra : float
       The center RA, in degrees, if marking the center of the target.
    cdec : float
       The center Dec, in degrees, if marking the center of the target.
    ggm : bool
       Option to perform a GGM filter on the input (ext=imgext) image, from hdul.
    ggmCut : float
       Determine a minimum level of the ggm map, with respect to its maximum, for use with contours.
    cc : str
       Contour color.
    ncnts : int
       Number of contours
    title : str
       Provide a title for the figure, if desired.
    tsource : float
       Time on source (to be printed on the figure, if prntinfo is set)
    R500 : float
       Intended to be :math:`R_{500}` for clusters, provided in the same units as pixelsize. Can be used as a circle of interest for any target, with radius :math:`R_{500}`.
    r5col : str
       A string corresponding to the color of the circle to be drawn for :math:`R_{500}`, if provided.
    zoom : float
       If you wish to zoom in, set this to some value greater than 1.
    noaxes : bool
       Hide the image axes.
    verbose : bool
       Print a few things to stdout.
    imgext : int
       Extension of the image (to show, or of which to take the GGM). Default is 0.
    """
    
    #norm=colors.Normalize(vmin=vmin, vmax=vmax)
    #norm=colors.LogNorm(vmin=vmin, vmax=vmax)
    norm=colors.SymLogNorm(linthresh=vmin*2.2,vmin=vmin, vmax=vmax)
    tmin = np.round(vmin/10)*10
    tmax = 40
    lticks = np.arange(tmin,tmax+10,10)
    lgfull = np.array([40,100,200,400,800])
    lgticks = lgfull[(lgfull <=vmax)]
    myticks = np.hstack((lticks,lgticks))
    mycmap = get_rms_cmap()

    img = hdul[imgext].data
    hdr = hdul[imgext].header
    if rmsmap is None:
        wtmap  = hdul[1].data
        rmsmap = conv_wtmap_torms(wtmap)    # Convert to microK
        nzwts  = (wtmap > 0)
        medwt  = np.median(wtmap[nzwts])
    else:
        medwt  = 1.0
        
    w   = WCS(hdr)
    pixsize = np.sqrt(np.abs(np.linalg.det(w.pixel_scale_matrix))) * 3600.0 # in arcseconds

    figsize = (7,5)
    dpi     = 200 # default??
    myfig = plt.figure(1,figsize=figsize)
    myfig.clf()
    if tlo:
        ax = myfig.add_subplot(1,1,1, projection=w,position=[0.05,0.05,0.8,0.8])
    else:
        ax = myfig.add_subplot(1,1,1, projection=w)
    
    gi = (rmsmap > 0)
    minrms = np.min(rmsmap[gi])

    if ggm:
        ggmImg = scipy.ndimage.gaussian_gradient_magnitude(img*1e6,ggmPix)
        if not mask is None:
            ggmImg = ggmImg*mask
        #im     = ax.imshow(ggmImg,cmap=mycmap)
        ggmMax = np.max(ggmImg)
        gi     = (ggmImg > ggmMax*ggmCut)
        ggmStd = np.std(ggmImg[gi])
        if ncnts > 0:
            clvls  = np.logspace(np.log10(ggmStd*2),np.log10(ggmMax),ncnts)
        else:
            clvls  = np.arange(ggmStd*3,ggmMax,ggmStd)
    else:
        if ncnts > 0:
            maxval = np.max(-1*img)
            #clvls  = -np.flip(np.logspace(np.log10(minrms),np.log10(maxval),ncnts))
            clvls  = np.arange(2,2+ncnts)*minrms
            ax.contour(-img,clvls,linestyles='--',colors=cc)
            #print("Tried to plot contours: ",clvls)
            #print(maxval)
            #import pdb;pdb.set_trace()


    whitemap = np.ones(rmsmap.shape)*vmax + 1
    im0 = ax.imshow(whitemap,norm=norm,cmap=mycmap)
    if zoom > 1:
        ax_zoom(zoom,ax)
        
    ax.set_xlabel("RA (J2000)",fontsize=myfs)
    ax.set_ylabel("Dec (J2000)",fontsize=myfs)

    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    dx    = xlims[1] - xlims[0]
    dy    = ylims[1] - ylims[0]
    alphas   = np.zeros(rmsmap.shape)
    if prntinfo:
        xpos = int(np.round(xlims[1] - dx*myfs/27.0))
        #xpos = xlims[1] - dx*myfs/30
        ypos = int(np.round(ylims[0] ))
        txthght = int(np.round(dy*myfs/(figsize[1]*25)))
        txtwdth1 = int(np.round(dx*myfs/35.0))
        txtwdth2 = int(np.round(dx*myfs/12.0))
        if verbose:
            print("==========================================")
            print(xpos,ypos,txthght,txtwdth1,dx,myfs)
        #alphas[xpos:xpos+txtwdth1,ypos:ypos+txthght] = 0.2
        alphas[ypos:ypos+txthght,xpos:xpos+txtwdth1] = 0.9
        if tsource > 0:
            xos = int(np.round(xlims[0]))
            yos = int(np.round(ylims[1] - dy*myfs/150.0))
            alphas[yos:yos+txthght,xos:xos+txtwdth2] = 0.9

        truncate_par = 10.0 #do not user lower than 7-10, larger means much slower code
        mode_BC = 'constant' 
        alphas = scipy.ndimage.filters.gaussian_filter(alphas , txthght/10.0,truncate=truncate_par, mode=mode_BC)
    #print(alphas.shape,txthght,ypos,yos,xpos,xos,txtwdth1,txtwdth2)
    #import pdb;pdb.set_trace()
    if ggmIsImg:
        im = ax.imshow(ggmImg,cmap=mycmap)
    else:
        #im = ax.imshow(rmsmap,norm=norm,alpha=alphas,cmap=mycmap)
        im = ax.imshow(rmsmap,norm=norm,cmap=mycmap)
        if ggm and (ncnts > 0):
            ax.contour(ggmImg,clvls,linestyles='--',colors=cc)
        #import pdb;pdb.set_trace()
        
    if R500 > 0:
        goodrad = R500/pixsize
        plot_circ(ax,hdr,cra,cdec,goodrad,color=r5col,lw=4)

    im0 = ax.imshow(whitemap,norm=norm,alpha=alphas,cmap=mycmap)

    #if zoom > 1:
    #    ax_zoom(zoom,ax)
            
    if prntinfo:
        xpos = xlims[1] - dx*myfs/30
        ypos = ylims[0] + dy*0.03
        ax.text(xpos,ypos,"Min. RMS: "+"{:.1f}".format(minrms),fontsize=myfs)
        if tsource > 0:
            xos = xlims[0] + dx*0.03
            yos = ylims[1] - dy*0.08
            ax.text(xos,yos,"t on source (hrs): "+"{:.1f}".format(tsource),fontsize=myfs)
    #ax.set_title(title,fontsize=myfs)
    cbar_num_format = "%d"
    mycb = myfig.colorbar(im,ax=ax,ticks=myticks,format=cbar_num_format)
    mycb.set_label(r"Noise ($\mu$K)",fontsize=myfs)
    #mycb = myfig.colorbar(im,ax=ax,ticks=[20,30,40,100,200],label=r"Noise ($\mu$K)")
    #mycb.ax.set_xticklabels(['20','30','40','100','200'])
    mycb.ax.tick_params(labelsize=myfs)

    if noaxes:
        ax.set_axis_off()
    
    if not (title is None):
        ax.set_title(title)

    if cmark:
        mark_radec(ax,hdr,cra,cdec)

    if prntinfo and not nscans is None:
        nsint = [int(nscan) for nscan in nscans]
        for i,nsi in enumerate(nsint):
            ax.text(5+i*100,5,repr(nsi),fontsize=myfs)

    #if tlo:
        #print("I already did this")
        #myfig.tight_layout()
        #myfig.subplots_adjust(left=0.01,bottom=0.01,top=0.05)
        #myfig.subplots_adjust(left=0.01,bottom=0.01)
        #ax.subplot_adjust(right=0.1,left=0.01,bottom=0.01,top=0.01)
    myfig.savefig(savefile,format='png')
    #myfig.clf()


def mark_radec(ax,hdr,ra,dec):
    """
    Make a nice image (via imshow) of the RMS map.

    Parameters
    ----------
    ax : axes object
       Axes on which to make a mark
    hdr : list(str)
       A fits file header with astrometric information.
    ra : float
       Right Ascension, in degrees
    dec : float
       Declination, in degrees
    """
    w     = WCS(hdr)           
    #pixs  = get_pixs(hdr)/60.0 # In arcminutes
    x0,y0 = w.wcs_world2pix(ra,dec,0)

    ax.plot(x0,y0,'xr')

def plot_circ(ax,hdr,ra,dec,goodrad,color="r",ls='--',lw=2):
    """
    Make a nice image (via imshow) of the RMS map.

    Parameters
    ----------
    ax : axes object
       Axes on which to make a mark
    hdr : list(str)
       A fits file header with astrometric information.
    ra : float
       Right Ascension, in degrees
    dec : float
       Declination, in degrees
    """

    thetas = np.arange(181)*2*np.pi/180
    w      = WCS(hdr)           
    #pixs  = get_pixs(hdr)/60.0 # In arcminutes
    x0,y0  = w.wcs_world2pix(ra,dec,0)

    xs     = x0 + np.cos(thetas)*goodrad
    ys     = y0 + np.sin(thetas)*goodrad

    ax.plot(xs,ys,ls=ls,lw=lw,color=color)
    
def plot_rms(hdul,rmsmap,savefile,vmin=18,vmax=318,myfs=15,nscans=None,
             prntinfo=True,cmark=True):
    """
    Make a nice image (via imshow) of the RMS map.

    Parameters
    ----------
    hdul : list(obj)
       Any list of objects obtained from fits.open()
   rmsmap : numpy.ndarray
       An 2D array constituting the RMSmap. The assumption is that ext=1 in the input hdul is the weightmap. If this is not the case, then the RMSmap can be supplied here.
    savefile : str
       A string with the full path of where to save the output image (assumed to be a png).

    vmin : float
       Minimum RMS value (in the colorbar).
    vmax : float
       Maximum RMS value (in the colorbar).
    myfs : float
       Fontsize for labels and such.
     nscans : int
       Number of Lissajous Daisy scans to achieve integration time. (optional)
    prntinfo : bool
       Set this to print information on the figure.
    cmark : bool
       Set this to make a center mark.
    """
    #norm=colors.Normalize(vmin=vmin, vmax=vmax)
    #norm=colors.LogNorm(vmin=vmin, vmax=vmax)
    norm=colors.SymLogNorm(linthresh=40,vmin=vmin, vmax=vmax)
    mycmap = get_rms_cmap()

    img = hdul[0].data
    hdr = hdul[0].header
    w   = WCS(hdr)

    myfig = plt.figure(1,figsize=(7,5))
    myfig.clf()
    ax = myfig.add_subplot(1,1,1, projection=w)

    
    im = ax.imshow(rmsmap,norm=norm,cmap=mycmap)
    ax.set_xlabel("RA (J2000)",fontsize=myfs)
    ax.set_ylabel("Dec (J2000)",fontsize=myfs)
    gi = (rmsmap > 0)
    minrms = np.min(rmsmap[gi])
    if prntinfo:
        ax.text(500,5,"Min. RMS: "+"{:.1f}".format(minrms))
    #ax.set_title(title,fontsize=myfs)
    #plot_circ(ax,goodcen,goodrad,color=r5col,ls='--',lw=2)
    mycb = myfig.colorbar(im,ax=ax,label=r"Noise ($\mu$K)")
    #mycb = myfig.colorbar(im,ax=ax,ticks=[20,30,40,100,200],label=r"Noise ($\mu$K)")
    #mycb.ax.set_xticklabels(['20','30','40','100','200'])
    mycb.ax.tick_params(labelsize=myfs)

    if prntinfo and not nscans is None:
        nsint = [int(nscan) for nscan in nscans]
        for i,nsi in enumerate(nsint):
            ax.text(5+i*100,5,repr(nsi),fontsize=myfs)
        
    myfig.savefig(savefile,format='png')
    
def get_scanlen(scansize):
    """
    Return the scan duration, in minutes

    Parameters
    ----------
    scansize : float
       Scan size. Standard options are 2.5, 3.0, 3.5, 4.0, 4.5, or 5.0, but this routine can work for an arbitrary scan size.

    Returns
    -------
    t_minutes: float
       The resultant scan duration
    """

    # Scansize in arcminutes
    t_minutes = 6.56365 + 0.585*scansize

    return t_minutes

def get_rmsprof_from_s(radii,s,WIKID=False):
    """
    Return the RMS (mapping speed) profile as a function of scan size.

    Parameters
    ----------
    radii :  class:`numpy.ndarray`
       Radii (can be 1D or 2D) in arcminutes.
    s : float
       Scan size. Options are 2.5, 3.0, 3.5, 4.0, 4.5, or 5.0

    Returns
    -------
    rms: class:`numpy.ndarray`
       The resultant rms profile
    """

    pars = get_mapspd_pars(s,WIKID=WIKID)
    rms  = get_rmsprofile(radii,pars,s)
    
    return rms

def get_rmsprofile(radii,pars,size,cf=np.sqrt(2)):
    """
    Return the RMS (mapping speed) profile as a function of scan size.

    Parameters
    ----------
    radii :  class:`numpy.ndarray`
       Radii (can be 1D or 2D) in arcminutes.
    pars : list
       A list of 4 parameters that describe the RMS profile.
    size : float
       Scan size, in arcminutes.
    cf : float, optional
       Factor not included in the 4 parameters.

    Returns
    -------
    rms: class:`numpy.ndarray`
       The resultant rms profile
    """
    #P[0] + P[1] + P[3]*exp(R/P[2])
    if len(pars) == 4:
        rawrms = pars[0] + pars[1]*radii + pars[3]*np.exp(radii/pars[2])
    else:
        rawrms = pars[0] + pars[1]*np.exp((radii/size))**2
        
    rms    =cf*rawrms
    
    return rms
       
def get_mapwts(radii,pars,s):
    """
    Return the RMS (mapping speed) profile as a function of scan size.

    Parameters
    ----------
    radii :  class:`numpy.ndarray`
       Radii (can be 1D or 2D) in arcminutes.
    pars : list
       A list of 4 parameters that describe the RMS profile.
    Returns
    -------
    wts: class:`numpy.ndarray`
       The resultant weightmap
    """
    #P[0] + P[1] + P[3]*exp(R/P[2])
    #rawrms = pars[0] + pars[1]*radii + pars[3]*np.exp(radii/pars[2])
    #rms    =cf*rawrms
    rms = get_rmsprofile(radii,pars,s)
    wts = 1.0/rms**2

    return wts
    
def get_mapspd_pars(size,WIKID=False):
    #rawrms = pars[0] + pars[1]*radii + pars[3]*np.exp(radii/pars[2])
    """
    Return parameters describing the RMS profile by scan size.

    Parameters
    ----------
    size : float
       Scan size. Options are 2.5, 3.0, 3.5, 4.0, 4.5, or 5.0

    Returns
    -------
    p : list
       A list of 4 parameters describing the RMS profile.
    """

    if size == 2.5:
        p = [39.5533, 1.0000, 1.0000, 2.2500]
    if size == 3.0:
        p = [37.3425, 1.5000, 1.5000, 6.9000]
    if size == 3.5:
        p = [27.9775, 2.0000, 2.0000, 11.5500]
    if size == 4.0:
        p = [32.3852, 2.5000, 2.5000, 16.2000]
    if size == 4.5:
        p = [28.5789, 3.0000, 3.0000, 20.8500]
    if size == 5.0:
        p = [43.2951, 3.5000, 3.5000, 25.5000]

    if WIKID:
        #print(p)
        p[0] = p[0]/10.0
        p[1] = p[1]/2.0
        p[2] = p[2]*2.0
        p[3] = p[3]/2.0
        if size == 2.5:
            p = [2.9*3.3,0.26]
        if size == 3.0:
            p = [3.1*3.3,0.26]
        if size == 3.5:
            #print("Heya")
            p = [3.4*3.3, 0.18]
        if size == 4.0:
            p = [3.85*3.3,0.17]
        if size == 4.5:
            p - [4.2*3.3,0.128]
        if size == 5.0:
            p - [5.02*3.3,0.12]
            
        #print(p)
        ### To be confirmed

    return p
        
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
        
def make_xymap(img,hdr,ra,dec):
    """
    Return a tuple of x- and y-coordinates.

    Parameters
    ----------
    img : class:`numpy.ndarray`
       The image (or template of it) with which you are working
    hdr : list(str)
       A header with associated astrometric information
    ra : float
       Right Ascension, in degrees, to be the center of your map.
    dec : float
       Declination, in degrees, to be the center of your map.
    Returns
    -------
    xymap : tuple(class:`numpy.ndarray`)
       A tuple of x- and y-coordinates

    """
    
    w     = WCS(hdr)           
    pixs  = get_pixs(hdr)/60.0 # In arcminutes
    x0,y0 = w.wcs_world2pix(ra,dec,0)
    #print(pixs,x0,y0)
    #pdb.set_trace()
    xsz, ysz = img.shape
    xar = np.outer(np.arange(xsz),np.zeros(ysz)+1.0)
    yar = np.outer(np.zeros(xsz)+1.0,np.arange(ysz))
    xarr = xar.transpose()
    yarr = yar.transpose()
    ####################
    dxa = (xarr - x0)*pixs
    dya = (yarr - y0)*pixs
    
    return (dxa,dya)
    #return (dya,dxa)

def get_pixs(hdr):
    """
    Return the pixel size in arcseconds.

    Parameters
    ----------
    hdr : list(str)
       A header with associated astrometric information

    Returns
    -------
    pixs : float
       Pixel size, in arcseconds

    """

    if 'CDELT1' in hdr.keys():
        pixs= abs(hdr['CDELT1'] * hdr['CDELT2'])**0.5 * 3600.0    
    if 'CD1_1' in hdr.keys():
        pixs= abs(hdr['CD1_1'] * hdr['CD2_2'])**0.5 * 3600.0
    if 'PC1_1'  in hdr.keys():
        if 'PC2_1'  in hdr.keys():
            pc21 = hdr['PC2_1']
            pc12 = hdr['PC1_2']
        else:
            pc21 = 0.0; pc12 = 0.0
            
        pixs= abs(hdr['PC1_1']*hdr['CDELT1'] * \
                  hdr['PC2_2']*hdr['CDELT2'])**0.5 * 3600.0

    return pixs

def reproject_fillzeros(hduin,hdrout,hdu_in=0):
    """
    Return a reprojected image

    Parameters
    ----------
    hduin : class:`astropy.io.fits.HDUList`
       A Header-Data-Unit list
    hdrout : list(str)
       A header with associated astrometric information
    hduin : int
       Specify the fits extension (HDUList index)

    Returns
    -------
    imgout : class:`numpy.ndarray`)
       The reprojected image
    fpout : class:`numpy.ndarray`)
       The footprint of the original image

    """

    imgout, fpout = reproject_interp(hduin,hdrout,hdu_in=hdu_in)
    foo           = np.isnan(imgout)
    badind        = np.where(foo)
    imgout[foo]   = 0.0

    return imgout, fpout
         
def make_rms_map(hdul,ptgs,szs,time,offsets=[1.5]):
    """
    Return a map of RMS sensitivites based on input set of scans.

    Parameters
    ----------
    hdul : class:`astropy.io.fits.HDUList`
       A Header-Data-Unit list
    ptgs : list(list)
       A list of 2-element array-like objects containing the RA and Dec of pointings to be used.
    szs : array_like
       A list of scan sizes to be used.
    time : array_like
       A list of times to be spent with corresponding pointing and scan size
    offsets : array_like
       A corresponding list of scan offsets. If 0 then just a central pointing is used. If anything greater than zero, the a 4-scan offset pattern is assumed, using the given offset, in arcminutes.

    Returns
    -------
    imgout : class:`numpy.ndarray`
       A map of the resultant RMS
    ns : class:`numpy.ndarray`
       An array of the (non-rounded) number of scans required to reach the specified time(s).

    """
    
    img  = hdul[0].data
    hdr  = hdul[0].header

    sll = []
    for sz in szs:
        sl  = get_scanlen(sz)
        sll.append(sl)

    sla = np.array(sll)
    times = np.asarray(time)

    ns   = times*60/sla

    wtmap  = np.zeros(img.shape)
    rmsmap = np.zeros(img.shape)
    for p,s,t,o in zip(ptgs,szs,time,offsets):
        wtmap = add_to_wtmap(wtmap,hdr,p,s,t,offset=o)
    gi = (wtmap > 0)
    rmsmap[gi] = 1.0/np.sqrt(wtmap[gi])

    return rmsmap, ns

def add_to_wtmap(wtmap,hdr,p,s,t,offset=1.5,WIKID=False):
    """
    For a given scan set, add weights to a given weightmap.

    Parameters
    ----------
    wtmap : class:`numpy.ndarray`
       A weight map.
    hdr : list(str)
       A header with associated astrometric information
    p : array_like
       A list of 2-elements containing the RA and Dec of pointings to be used.
    s : float
       Scan size. Options are 2.5, 3.0, 3.5, 4.0, 4.5, or 5.0
    t : float
       The time to be spent with corresponding pointing and scan size
    offset : float
       If 0 then just a central pointing is used. If anything greater than zero, the a 4-scan offset pattern is assumed, using the given offset, in arcminutes.

    Returns
    -------
    wtmap : class:`numpy.ndarray`
       A map of the resultant weights
    """

    degoff = offset/60.0 # Offset in degrees
    rFOV   = 4.2 if WIKID else 2.1
    if s>0:
        pars = get_mapspd_pars(s,WIKID=WIKID)
        xymap = make_xymap(wtmap,hdr,p[0],p[1])
        rmap  = make_rmap(xymap)
        edge  = (s+rFOV) # arcseconds
        gi = (rmap < edge)
        wts = get_mapwts(rmap[gi],pars,s)
        wtmap[gi] = wtmap[gi]+wts*t
    else:
        pars   = get_mapspd_pars(-s,WIKID=WIKID)
        cosdec = np.cos(p[1]*np.pi/180.0)
        #if offset > 0:
        for i in range(4):
            newx = p[0] + np.cos(np.pi*i/2)*degoff/cosdec
            newy = p[1] + np.sin(np.pi*i/2)*degoff
            xymap = make_xymap(wtmap,hdr,newx,newy)
            rmap  = make_rmap(xymap) # arcminutes
            edge  = (rFOV-s) # arcminutes
            gi = (rmap < edge)
            wts = get_mapwts(rmap[gi],pars,-s)
            wtmap[gi] = wtmap[gi]+wts*t/4.0
        #else:
        #    xymap = make_xymap(wtmap,hdr,p[0],p[1])
        #    rmap  = make_rmap(xymap) # arcminutes
        #    edge  = (2.1-s) # arcminutes
        #    gi = (rmap < edge)
        #    wts = get_mapwts(rmap[gi],pars)
        #    wtmap[gi] = wtmap[gi]+wts*t

            
    return wtmap

def ax_zoom(zoom,ax):
    """
    For a given axes object (with an image), zoom in.

    Parameters
    ----------
    zoom : float
       A factor by which you wish to zoom in (zoom > 1).
    ax : class:`matplotlib.pyplot.axes`
       The axes object with the image.
    """
    ax_x = ax.get_xlim()
    ax_y = ax.get_ylim()
    dx   = (ax_x[1] - ax_x[0])/2
    dy   = (ax_y[1] - ax_y[0])/2
    newd = (1.0 - 1.0/zoom)
    newx = [ax_x[0]+newd*dx,ax_x[1]-newd*dx]
    newy = [ax_y[0]+newd*dy,ax_y[1]-newd*dy]
    ax.set_xlim(newx)
    ax.set_ylim(newy)

def make_template_hdul(nx,ny,cntr,pixsize,cx=None,cy=None):
    """
    Return a map of RMS sensitivites based on input set of scans.

    Parameters
    ----------
    nx : int
       Number of pixels along axis 0
    ny : int
       Number of pixels along axis 1
    cntr : array_like
       Two-element object specifying the RA and Dec of the center.
    pixsize : float
       Pixel size, in arcseconds
    cx : float
       The pixel center along axis 0
    cy : float
       The pixel center along axis 1

    Returns
    -------
    TempHDU : class:`astropy.io.fits.HDUList`
       A Header-Data-Unit list (only one HDU)

    """

    if cx is None:
        cx = nx/2.0
    if cy is None:
        cy = ny/2.0
    ### Let's make some WCS information as if we made 1 arcminute pixels about Coma's center:
    w = WCS(naxis=2)
    w.wcs.crpix = [cx,cy]
    w.wcs.cdelt = np.array([-pixsize/3600.0,pixsize/3600.0])
    w.wcs.crval = [cntr[0], cntr[1]]
    #w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    w.wcs.ctype = ["RA---SIN", "DEC--SIN"]
    hdr = w.to_header()

    zero_img    = np.zeros((nx,ny))
    Phdu        = fits.PrimaryHDU(zero_img,header=hdr)
    TempHdu     = fits.HDUList([Phdu])

    return TempHdu

def calc_RMS_profile(hdul,rmsmap,Cntr,rmax=None):
    """
    Return a map of RMS sensitivites based on input set of scans.

    Parameters
    ----------
    hdul : class:`astropy.io.fits.HDUList`
       A list of HDUs
    Cntr : array_like
       Two-element object specifying the RA and Dec of the center.
   rmsmap : class:`numpy.ndarray`
       A map of achieved RMS.
    rmax : float
       Maximum radius out to which a profile is calculated.

    Returns
    -------
    rbin : class:`numpy.ndarray`
       Binned radii
    ybin : class:`numpy.ndarray`
       Binned RMS values

    """

    img                    = hdul[0].data
    hdr                    = hdul[0].header
    xymap                  = make_xymap(img,hdr,Cntr[0],Cntr[1])
    xmap                   = xymap[0]
    #pixs                   = np.median(xmap[1:,0]-xmap[:-1,0]) # in arcminutes
    pixs                   = np.median(xmap[0,1:]-xmap[0,:-1]) # in arcminutes
    rmap                   = make_rmap(xymap) # arcminutes
    rbin,ybin,yerr,ycnts   = bin_two2Ds(rmap,rmsmap,binsize=pixs*2.0)

    return rbin,ybin

def bin_two2Ds(independent,dependent,binsize=1,witherr=False,withcnt=False):
    """
    Bins two 2D arrays based on the independent array (e.g. one of radii).

    Parameters
    ----------
    independent : class:`numpy.ndarray`
       An array of independent variables (e.g. radii)
    dependent : class:`numpy.ndarray`
       An array of dependent variables (e.g. RMS or surface brightness)
    binsize : float
       Binsize, relative to independent array.
    witherr : bool
       Calculate the corresponding uncertainties (of the mean)
    withcnt : bool
       Calculate the number of elements (e.g. pixels) within each bin.

    Returns
    -------
    abin : class:`numpy.ndarray`
       Binned absisca values
    obin : class:`numpy.ndarray`
       Binned ordinate values
    oerr : class:`numpy.ndarray`
       Binned uncertainties of the mean
    cnts : class:`numpy.ndarray`
       Binned counts

    """

    flatin = independent.flatten()
    flatnt = dependent.flatten()
    inds = flatin.argsort()

    abscissa = flatin[inds]
    ordinate = flatnt[inds]

    nbins = int(np.ceil((np.max(abscissa) - np.min(abscissa))/binsize))
    abin  = np.zeros(nbins)
    obin  = np.zeros(nbins)
    oerr  = np.zeros(nbins)
    cnts  = np.zeros(nbins) 
    for i in range(nbins):
        blow = i*binsize
        gi = (abscissa >= blow)*(abscissa < blow+binsize)
        abin[i] = np.mean(abscissa[gi])
        obin[i] = np.mean(ordinate[gi])
        if witherr:
            oerr[i] = np.std(ordinate[gi]) / np.sqrt(np.sum(gi))
        if withcnt:
            cnts[i] = np.sum(gi)

    return abin,obin,oerr,cnts

def bin_log2Ds(independent,dependent,nbins=10,witherr=False,withcnt=False):
    """
    Bins two 2D arrays based on the independent array (e.g. one of radii).
    Do this if both arrays are better distributed in log-space.

    Parameters
    ----------
    independent : class:`numpy.ndarray`
       An array of independent variables (e.g. radii)
    dependent : class:`numpy.ndarray`
       An array of dependent variables (e.g. RMS or surface brightness)
    nbins : float
       Number of bins
    witherr : bool
       Calculate the corresponding uncertainties (of the mean)
    withcnt : bool
       Calculate the number of elements (e.g. pixels) within each bin.

    Returns
    -------
    abin : class:`numpy.ndarray`
       Binned absisca values
    obin : class:`numpy.ndarray`
       Binned ordinate values
    oerr : class:`numpy.ndarray`
       Binned uncertainties of the mean
    cnts : class:`numpy.ndarray`
       Binned counts

    """

    flatin = independent.flatten()
    flatnt = dependent.flatten()
    inds   = flatin.argsort()

    abscissa = flatin[inds]
    ordinate = flatnt[inds]

    #nbins = int(np.ceil((np.max(abscissa) - np.min(abscissa))/binsize))
    agtz    = (abscissa > 0)
    lgkmin  = np.log10(np.min(abscissa[agtz]))
    lgkmax  = np.log10(np.max(abscissa))
    bins  = np.logspace(lgkmin,lgkmax,nbins+1)
    abin  = np.zeros(nbins)
    obin  = np.zeros(nbins)
    oerr  = np.zeros(nbins)
    cnts  = np.zeros(nbins) 
    for i,(blow,bhigh) in enumerate(zip(bins[:-1],bins[1:])):
        gi = (abscissa >= blow)*(abscissa < bhigh)
        abin[i] = np.mean(abscissa[gi])
        obin[i] = np.mean(ordinate[gi])
        if witherr:
            oerr[i] = np.std(ordinate[gi]) / np.sqrt(np.sum(gi))
        if withcnt:
            cnts[i] = np.sum(gi)

    return abin,obin,oerr,cnts

def calculate_RMS_within(Rads,RMSprof,Rmaxes=[2,3,4]):
    """
    Bins two 2D arrays based on the independent array (e.g. one of radii).
    Do this if both arrays are better distributed in log-space.

    Parameters
    ----------
    Rads : class:`numpy.ndarray`
       An array  radii
    RMSprof : class:`numpy.ndarray`
       An array of RMS values
    Rmaxes : list
       Calculates the average RMS within circles of these radii, in arcminutes

    Returns
    -------
    RMSwi : list
       Average RMS within the specified radii.
    """

    Variance = RMSprof**2
    Rstack   = np.hstack([0,Rads])
    Area     = Rstack[1:]**2 - Rstack[:-1]**2

    VarCum   = np.cumsum(Variance*Area)
    AreCum   = np.cumsum(Area)
    VarAvg   = VarCum/AreCum

    RMSwi    = []
    for Rmax in Rmaxes:
        gi = (Rads < Rmax)
        MyVars = VarAvg[gi]
        RMSwi.append(np.sqrt(MyVars[-1]))

    return RMSwi

def Make_ImgWtmap_HDU(HDUTemplate,Img,Wtmap):
    """
    Return a map of RMS sensitivites based on input set of scans.

    Parameters
    ----------
    HDUTemplate : class:`astropy.io.fits.HDUList`
       A list of HDUs
    Img : class:`numpy.ndarray`
       An image
    Wtmap : class:`numpy.ndarray`
       A corresponding weightmap

    Returns
    -------
    ImgWtsHDUs : class:`astropy.io.fits.HDUList`
       A list of HDUs; first extension is the image; second extension is the weight map.
    """

    Phdu        = HDUTemplate[0]
    Phdu.data   = Img*1.0
    Shdu        = fits.ImageHDU(Wtmap,header=Phdu.header)
    ImgWtsHDUs  = fits.HDUList([Phdu,Shdu])

    return ImgWtsHDUs

def coaddimg_noRP(hdu1,hdu2):

    """
    This version assumes no reprojection. That is, you had better have the same astrometry between the two!
    A more general version to be written...

    Parameters
    ----------
    hdu1 : class:`astropy.io.fits.HDUList`
       A list of HDUs
    hdu2 : class:`astropy.io.fits.HDUList`
       A list of HDUs

    Returns
    -------
    hdu1 : class:`astropy.io.fits.HDUList`
       A list of HDUs, with the coadded image.

    """

    img1 = hdu1[0].data *1.0
    wtm1 = hdu1[1].data *1.0
    img2 = hdu2[0].data *1.0
    wtm2 = hdu2[1].data *1.0

    #c1   = np.any(np.isnan(img1))
    #c2   = np.any(np.isnan(wtm1))
    #c3   = np.any(np.isnan(img2))
    #c4   = np.any(np.isnan(wtm2))
    #print(c1,c2,c3,c4)
   
    NewWtm     = wtm1 + wtm2
    WtdImg     = (img1*wtm1 + img2*wtm2)
    NewImg     = np.zeros(NewWtm.shape)
    gi         = (NewWtm > 0)
    NewImg[gi] = WtdImg[gi]/NewWtm[gi]

    hdu1[0].data = NewImg *1.0
    hdu1[1].data = NewWtm *1.0

    return hdu1
