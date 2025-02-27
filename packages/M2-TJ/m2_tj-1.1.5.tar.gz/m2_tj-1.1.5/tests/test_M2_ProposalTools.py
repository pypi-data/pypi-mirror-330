import pytest
import M2_ProposalTools.WorkHorse as WH
import M2_ProposalTools.FilterImages as FI
import M2_ProposalTools.MakeRMSmap as MRM
import M2_ProposalTools.M2_vis_plot_year as M2vis
import numpy as np
import os
import astropy.units as u
import M2_ProposalTools.ModelFitting as MF
from astropy.io import fits                # To read/write fits

def test_locate_xfer_files():

    #xferfile       = "xfer_Function_3p0_21Aonly_PCA5_0f08Filtering.txt"
    xferfile       = "src/M2_ProposalTools/xfer_Function_3p0_21Aonly_PCA5_0f08Filtering.txt"
    fileexists     = os.path.exists(xferfile)
    assert fileexists

    
    
def test_HDU_generation():

    Center  = [280.0, 45.0]                     # Arbitrary RA and Dec
    pixsize = 2.0                               # arcseconds
    xsize   = 12.0                              # arcminutes; this is a bit larger than typical
    ysize   = 12.0                              # arcminutes
    nx      = int(np.round(xsize*60/pixsize))   # Number of pixels (must be an integer!)
    ny      = int(np.round(ysize*60/pixsize))   # Number of pixels (must be an integer!)
    TemplateHDU = MRM.make_template_hdul(nx,ny,Center,pixsize)

    assert len(TemplateHDU) == 1

def test_RMS_generation():    

    Center  = [280.0, 45.0]                     # Arbitrary RA and Dec
    pixsize = 2.0                               # arcseconds
    xsize   = 12.0                              # arcminutes; this is a bit larger than typical
    ysize   = 12.0                              # arcminutes
    nx      = int(np.round(xsize*60/pixsize))   # Number of pixels (must be an integer!)
    ny      = int(np.round(ysize*60/pixsize))   # Number of pixels (must be an integer!)
    Ptgs    = [Center]                          # Pointings should be a list of (RA,Dec) array-like values.
    sizes   = [-3.5]                            # Let's try offset scans! Here, 3.5' scans, offset
    times   = [10.0]                            # 10 hours
    offsets = [1.5]                               # 1.5 arcminute offset (the default, but we may change it)
    Theta500 = 3.5                             # Radius of interest, in arcminutes. If > 0, a circle will be plotted of this radius.

    TemplateHDU = MRM.make_template_hdul(nx,ny,Center,pixsize)
    RMSmap,nscans = MRM.make_rms_map(TemplateHDU,Ptgs,sizes,times,offsets=offsets)

    nPixX,nPixY = RMSmap.shape
    c1          = (nx == nPixX)
    c2          = (ny == nPixY)
    c3          = (np.max(RMSmap) > 0)

    prntinfo = True
    ############## Some inputs are useful if your template HDU has an actual image you want to portray
    ############## with respect to your RMS map. (Do features align with desired map depth?)
    ggm      = False   # Perform Gaussian Gradient Magnitude on the image of the Template HDU
    ncnts    = 0       # Number of contours. 1-3 is good for highlighting features. Contours are automatically created in logarithmic
    # spacing between the minimum (acceptable, see below) and maximum ggm values.
    ggmCut   = 0.01    # This multiplied by the *maximum* of the GGM map is a threshold. So gradients < 1% are ignored/omitted.
    ggmIsImg = False   # If you want to display the ggm image instead of the RMS map, you can set this to True
    # This is primarily useful to get a handle on the values of the GGM image.(So that you may decide on values above)
    ###################################################################################################
    vmin     = 20.0    # uK. Minimum RMS depth expected
    vmax     = 200.0   # uK. Maximum RMS to be colored.
    ###################################################################################################
    tsource  = np.sum(times)        # Total hours on source.
    R500     = Theta500*60/pixsize  # Number of pixels
    R5c      = "k"                  # Black color for the circle drawn at R500 pixels
    zoom     = 1.0                  # Often the map is bigger than needed; you may want to zoom in by some amount.
    noaxes   = True                 # Label the axes? Often not necessary.
    myfs     = 20                   # fontsize
    ###################################################################################################
    outpng   = "Example_rmsmap_OffsetPintings_3p5each_wR500.png"
    
    MRM.plot_rms_general(TemplateHDU,outpng,nscans=nscans,prntinfo=prntinfo,cra=Center[0],cdec=Center[1],
                         ggm=ggm,ncnts=ncnts,vmin=vmin,vmax=vmax,ggmCut=ggmCut,ggmIsImg=ggmIsImg,rmsmap=RMSmap,
                         tsource=tsource,R500=R500,r5col=R5c,zoom=zoom,noaxes=noaxes,myfs=myfs)
    
    assert c1*c2*c3

def test_A10_generation():

    M500       = 3.9*1e14*u.M_sun
    z          = 0.86
    pixsize    = 2.0
    ymap       = WH.make_A10Map(M500,z,pixsize=pixsize,Dist=True)
    c1         = np.max(ymap) > 0
    c2         = np.max(ymap) < 1e-2
    
    assert c1*c2

def test_AlphaOmega():


    path    = os.path.abspath(FI.__file__)
    outdir  = path.replace("FilterImages.py","")
    M5_14    = 6.0
    M500     = M5_14*1e14*u.M_sun
    z        = 0.5
    pixsize  = 4.0
    
    times    = [10,10]
    ptgs     = [[180,45.0],[180,45.0]]
    sizes    = [3.5,3.5]
    offsets  = [1.5,0]
    
    FilterHDU,SmoothHDU,SkyHDU = WH.lightweight_simobs_A10(z,M500,conv2uK=True,pixsize=pixsize,ptgs=ptgs,sizes=sizes,times=times,offsets=offsets,Dist=True)

    pixstr = "{:.1f}".format(pixsize).replace(".","p")
    zstr   = "{:.1f}".format(z).replace(".","z")
    Mstr   = "{:.1f}".format(M5_14).replace(".","m")
    sss    = ["{:.1f}".format(mysz).replace(".","s") for mysz in sizes]
    sts    = ["{:.1f}".format(mytime).replace(".","h") for mytime in times]
    ssstr  = "_".join(sss)
    ststr  = "_".join(sts)
    InputStr = "_".join([zstr,Mstr,ssstr,ststr,pixstr])

    #filename = "SimulatedObs_Unsmoothed_"+InputStr+".fits"
    #FilterHDU.writeto(outdir+filename,overwrite=True)
    #filename2 = "SimulatedObs_Smoothed_"+InputStr+".fits"
    #SmoothHDU.writeto(outdir+filename2,overwrite=True)
    #filename3 = "SimulatedSky_"+InputStr+".fits"
    #SkyHDU.writeto(outdir+filename3,overwrite=True)

    SkyHDU[0].data *= -3.3e6 # Run once 

    SBfn = "SimulatedObs_SBprofiles_"+InputStr+".png"
    MF.plot_SB_profiles(FilterHDU,SkyHDU,outdir,SBfn)

    pngname  = "SimulatedObservations_"+InputStr+"_RMSimage.png"
    vmin     = 15.0  # uK
    vmax     = 420.0 # uK
    MRM.plot_rms_general(SmoothHDU,outdir+pngname,ncnts=5,vmin=vmin,vmax=vmax)

    #inputHDU = fits.open(outdir+filename)
    inputHDU = FilterHDU.copy()
    nsteps   = 100
    nsstr    = "_"+repr(nsteps)+"steps"
    outbase = "NP_fit_"+InputStr+nsstr+"_corner.png"
    MF.fit_spherical_model(z,M500,inputHDU,outdir=outdir,nsteps=nsteps,outbase=outbase)   # 100 for testing purposes
def test_VisibilityPlot():

    M2vis.get_year_visibilities()
