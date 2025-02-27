import numpy as np                         # A useful package...
import emcee, os, corner                   # A list of modules to import as-is
from astropy.io import fits                # To read/write fits
import M2_ProposalTools.analytic_integrations as ai         # Integrates ellipsoidal power law distributions
import astropy.units as u                  # Allows variables (quantities) to have units
import M2_ProposalTools.WorkHorse as WH    #
from scipy.optimize import curve_fit
from importlib import reload
from scipy.interpolate import interp1d     
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import scipy.special as scs
import M2_ProposalTools.FilterImages as FI

WH=reload(WH)
    

def fit_spherical_model(z,M500,hdul,model="NP",pink=True,alpha=2,knee=1.0/120.0,nkbin=100,fwhm=9.0,nsteps=1000,
                        y2k=-3.4,uKinput=True,ySph=True,YMrel="A10",outdir="/tmp/",outbase="NP_fit_corner.png",
                        size=3.5,Dist=False,plotPin=True,adPhys=True,WIKID=False,fit_cen=True,addNoise=True):

    """
    :param z: Redshift
    :type z: float
    :param M500: :math:`M\_{500}`
    :type M500: quantity (mass units)
    :param hdul: Astropy/fits HDU list (Make sure wtmap and img have appropriate units)
    :type hdul: list of HDU class objects 
    :param model: Type of model. Can be "NP" (for non-parametric), "GNFW" for generalized NFW, or "BETA" for a beta model.
    :type model: str
    :param pink: noise realization is pink noise
    :type pink: bool
    :param alpha: power-law index for red-noise part of pink noise. Default is 2.
    :type alpha: float
    :param knee: where, in inverse arcseconds, does the knee occur.
    :type knee: float
    :param nkbin: number of k-bins used to generate spectrum for pink noise.
    :type nkbin: int
    :param fwhm: Smoothing kernel for filtered map.
    :type fwhm: float
    :param nsteps: Number of steps to use in MCMC.
    :type nsteps: int
    :param y2k: Conversion factor between Compton y and Kelvin_RJ (for MUSTANG-2). Default is -3.4.
    :type y2k: float
    :param uKinput: The input map is taken to be in units of microKelvin_RJ if set.
    :type uKinput: bool
    :param ySph: Calculate :math:`y_{Sph}` if set; otherwise calculate :math:`y_{cyl}`. Default is True.
    :type ySph: bool
    :param YMrel: Which Y-M relation to use? Default is "A10".
    :type YMrel: str
    :param outdir: A string indicating the output directory, including trailing "/".
    :type outdir: str
    :param outbase: filename, without the directory path.
    :type outbase: str
    :param size: size of Lissajous daisy scan used (for transfer function). Options are 2.5, 3.0, 3.5, 4.0, 4.5, or 5.0
    :type size: float.
    :param fit_cen: Fit for a center? Default is True
    :type fit_cen: bool
    
    """

    ### First, we need to establish the radius out to which we fit and how many bins we want.
    ### This relies on how good our data are.
    
    conv         = 1e-6/y2k if uKinput else 1.0/y2k 
    hdul[0].data = hdul[0].data*conv
    hdul[1].data = hdul[1].data / ( conv**2 )
    hdu4snr      = hdul.copy()
    sf           = WH.get_smoothing_factor(fwhm=fwhm)
    if addNoise:
        print("Making SNR map")
    else:
        pixsize      = WH.get_pixarcsec(hdul)
        SigImg       = FI.fourier_filtering_2d(hdul[0].data,"gauss",fwhm/pixsize)
        SigWts       = FI.fourier_filtering_2d(hdul[1].data,"gauss",fwhm/pixsize)
        SigWts      *= (sf/pixsize)**2
        print(sf/pixsize,conv)
        hdu4snr[0].data = SigImg
        hdu4snr[1].data = SigWts
        sf           = 1.0
    SNRmap       = WH.get_SNR_map(hdu4snr)
    SNRhdu       = fits.PrimaryHDU(SNRmap,header=hdul[0].header)
    SNRhdu.writeto(outdir+"SNRmap.fits",overwrite=True)
    CosmoPars    = WH.get_cosmo_pars(z)
    pixsize      = WH.get_pixarcsec(hdul)
    intSNR,xc,yc,xymap = get_int_SNR(SNRmap,pixsize,maxRad=2.0,bv=120.0,SNRthresh=1.0)
    if addNoise == False:
        intSNR = np.sqrt(intSNR*2)
    print("Integrated SNR taken to be: ",intSNR)
    print("Adopting a center of ",xc,yc)

    if addNoise:
        Noise        = WH.get_noise_realization(hdul,pink=pink,alpha=alpha,knee=knee,nkbin=nkbin,fwhm=fwhm)
    else:
        Noise        = np.zeros(hdul[0].data.shape)
    # Modify HDU list to have mock-data and correctly weighted pixels.
    # Want to work in Compton y for fitting.

    ###############################################################################################

    efv        = get_emcee_fit_vars(CosmoPars,M500,intSNR,xc,yc,pixsize,outdir,fit_cen=fit_cen,
                                    MinRes=pixsize/2.0,model=model,ySph=ySph,YMrel=YMrel,size=size,
                                    Dist=Dist,WIKID=WIKID)
    mask         = automated_mask(xymap,CosmoPars,efv)

    hdul[0].data = hdul[0].data + Noise
    hdul[1].data = hdul[1].data*mask / ( sf**2 )

    hdul.writeto(outdir+"InputHDU.fits",overwrite=True)
    
    run_emcee(hdul,CosmoPars,efv,xymap,outdir+outbase,BSerr=False,nsteps=nsteps,plotPin=plotPin,adPhys=adPhys)

def automated_mask(xymap,cosmo_pars,efv):

    rmap         = WH.make_rmap(xymap)
    r500         = efv["Theta500"]*3600*180/np.pi # arcseconds

    goodind      = (rmap < 1.5*r500)
    mask         = rmap*0
    mask[goodind]= 1.0

    return mask

def get_emcee_fit_vars(cosmo_pars,M500,SNRint,xc,yc,pixsize,outdir,
                       MinRes=1.0,model="NP",ySph=True,YMrel="A10",nb_theta_range=150,SNRperbin=5.0,
                       n_at_rmin=False,fit_mnlvl=True,fit_cen=True,fit_geo=False,size=3.5,Dist=False,
                       WIKID=False):
    """
    :param cosmo_pars: a dictionary of cosmological parameters
    :type cosmo_pars: dict
    :param M500: :math:`M\\_{500}`
    :type M500: quantity (mass units)
    :param SNRint: Integrated SNR (how many sigma detection).
    :type SNRint: float
    :param xc: x-centroid, in pixels
    :type xc: float
    :param yc: y-centroid, in pixels
    :type yc: float
    :param pixsize: pixel size, in arcseconds
    :type pixsize: float
    :param outdir: A string indicating the output directory, including trailing "/".
    :type outdir: str
    :param MinRes: minimum resolution (in defining radial profile). Default is 1 arcsecond.
    :type MinRes: float
    :param model: Type of model. Can be "NP" (for non-parametric), "GNFW" for generalized NFW, or "BETA" for a beta model.
    :type model: str
    :param ySph: Calculate :math:`y_{Sph}` if set; otherwise calculate :math:`y_{cyl}`. Default is True.
    :type ySph: bool
    :param YMrel: Which Y-M relation to use? Default is "A10".
    :type YMrel: str
    :param nb_theta_range: number of points in theta_range array.
    :type nb_theta_range: int
    :param SNRperbin: minimum desired SNR per bin. Default is 4.0.
    :type SNRperbin: float
    :param n_at_rmin: Normalize at r_min. Default is False. (Unless you know what you are doing, leave this.)
    :type n_at_rmin: bool
    :param fit_mnlvl: Fit for a mean level? Default is True
    :type fit_mnlvl: bool
    :param fit_cen: Fit for a center? Default is True
    :type fit_cen: bool
    :param fit_geo: Fit for a an elliptical geometry? Default is False
    :type fit_geo: bool
    :param size: size of Lissajous daisy scan used (for transfer function). Options are 2.5, 3.0, 3.5, 4.0, 4.5, or 5.0
    :type size: float.
    
    """
    Theta500    = WH.Theta500_from_M500_z(M500,cosmo_pars["z"])
    minpixrad   = (MinRes*u.arcsec).to('rad')
    
    tnx         = [minpixrad.value,10.0*Theta500]  # In radians
    thetas      = np.logspace(np.log10(tnx[0]),np.log10(tnx[1]), nb_theta_range)
    
    Pdl2y       = WH.get_Pdl2y(cosmo_pars["z"],cosmo_pars["d_ang"])
    
    m500s       = WH.r2m_delta(thetas*cosmo_pars["d_a"],cosmo_pars["z"],delta=500)
    y500s       = WH.y_delta_from_mdelta(m500s,cosmo_pars["z"],delta=500,ycyl=(not ySph),YMrel=YMrel,h70=cosmo_pars["h70"])
    #geom     = [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    default_geo = [0,0,0,1,1,1,0,0]

    nBins       = int(np.round( (SNRint/SNRperbin)**2 ))
    if nBins < 4:
        print(SNRint,SNRperbin)
        print("Oh no, nBins is less than 4! Your data is probably not sufficient for this analysis")
        nBins   = 4
        
    radmin      = 5.0 *np.pi / (180*3600)                # 5" in radians
    radminmax   = np.array( [radmin,Theta500] )          # Between 5" and R500, in radians
    nMax        = np.floor(Theta500*3600*180/np.pi/12.0) # I want a bit larger than 10" bins.
    if nBins >= nMax:
        radminmax   = np.array( [radmin,Theta500*1.5] )          # Between 5" and R500, in radians
        nBins       = int(np.round(nMax))-2
    print(radminmax,nBins,SNRint,SNRperbin)
    #import pdb;pdb.set_trace()
    
    bins        = improved_bin_spacing(radminmax,nBins,mway=False) # in radians
    binkpc      = bins*cosmo_pars["d_a"]
    
    myval     = []   # 
    sbepos    = []   # Boolean array indicating whether myval should be positive or not.
    labels    = []
    uppbnd    = []
    lowbnd    = []
    
    ######################################################################################
    if fit_mnlvl:
        myval.append(1e-6)
        sbepos.append(False)
        labels.append("MnLvl")
        uppbnd.append(1e-5)
        lowbnd.append(-1e-5)

    if model == "NP":
        PresProf  = WH.a10_from_m500_z(M500, cosmo_pars["z"],binkpc*u.kpc,Dist=False)
        uless_p = (PresProf*Pdl2y).decompose().value
        sbepos.extend([True]*nBins)
        #NPlabels = [rf'''P_{sub}''' for sub in range(nBins)]
        NPlabels = [rf'''P$_{{{sub}}}$''' for sub in range(nBins)]
        labels.extend(NPlabels)
    if model == 'BETA':
        r500, p500 = WH.R500_P500_from_M500_z(M500, cosmo_pars["z"])
        uless_p = np.array([p500.to('keV / cm**3').value*10.0 ,Theta500/10.0,1.0])
        sbepos.extend(np.ones((len(uless_p)),dtype=bool))
        BetaLabels = [r"P$_0$",r"r$_c$",r"$\beta$"]
        labels.extend(BetaLabels)
    myval.extend(uless_p)
    pmult = np.ones(uless_p.shape)*10
    pmult[-1] *= 2
    uppbnd.extend(uless_p*pmult)
    lowbnd.extend(uless_p/pmult)

    if fit_cen:
        fcval = np.array([1.0,1.0])
        myval.extend(fcval)
        sbepos.extend([False,False])
        centLabels = [r"$\delta_x$",r"$\delta_y$"]
        labels.extend(centLabels)
        uppbnd.extend(fcval*20)
        lowbnd.extend(-fcval*20)

    ######################################################################################

    zstr   = "{:.1f}".format(cosmo_pars["z"]).replace(".","z")
    Mstr   = "{:.1f}".format(M500.to("M_sun").value/1e14).replace(".","m")


    efv         = {"Thetas":thetas,"y500s":y500s,"model":model,"ySph":ySph,"Pdl2y":Pdl2y,"geo":default_geo,
                   "M500":M500,"Theta500":Theta500,"YMrel":YMrel,"bins":bins,"nBins":nBins,"fit_mnlvl":fit_mnlvl,
                   "fit_cen":fit_cen,"fit_geo":fit_geo,"narm":n_at_rmin,"fixalpha":False,"finite":False,
                   "pinit":myval,"sbepos":sbepos,"pixsize":pixsize,"labels":labels,"outdir":outdir,
                   "size":size,"Mstr":Mstr,"zstr":zstr,"lowbnd":lowbnd,"uppbnd":uppbnd,"Dist":Dist,
                   "WIKID":WIKID}    

    return efv

def run_emcee(hdul,cosmo_pars,efv,xymap,outfile,BSerr=False,nsteps=1000,plotPin=True,adPhys=True):
    """
    Run the actual fitting procedure.

    :param hdul: an input fits HDUList with extension=0 being the data and extension=1 being the weights.
    :type hdul: list
    :param cosmo_pars: Dictionary of cosmological parameters
    :type cosmo_pars: dict
    :param efv: Dictionary of emcee fitting variables
    :type efv: dict
    :param xymap: tuple of arrays of x- and y-coordinates.
    :type xymap: tuple
    :param outfile: output file (full path)
    :type outfile: str
    :param BSerr: Bootstrap error?
    :type BSerrL bool
    :param nsteps: Number of fitting steps. Default is 1000.
    :type nsteps: int

    """

    # Call this once outside of the MCMC
    tab = WH.get_xfertab(efv["size"],WIKID=efv["WIKID"])

    def lnlike(pos):                          ### emcee_fitting_vars
        outmap,yint,outalpha,mnlvl = make_skymodel_map(hdul,pos,cosmo_pars,efv,xymap)
        #model   = WH.lightweight_filter_ptg(outmap,efv["size"],efv["pixsize"],WIKID=efv["WIKID"]) + mnlvl
        # Then just apply the transfer function (rather than reading in the file each iteration)
        model   =  FI.apply_xfer(outmap,tab,efv["pixsize"]) + mnlvl
        loglike = 0.0
        data    = hdul[0].data
        weights = hdul[1].data       # Best to mask weights (not use the entire map!)
        loglike-= 0.5 * (np.sum(((model - data)**2) * weights))

        return loglike, outalpha,yint

    def fprior(pos):

        prespos = pos[efv["sbepos"]]
        if all([param > 0.0 for param in prespos]):
            return True
        else:
            return False

    def lnprior(pos,outalphas,ycyl):        

        plike = 0.0
        
        for myouts in outalphas:
            if len(myouts) == 0:
                slopeok = True
            else:
                if myouts[-1] > 2.0: slopeok = True
                if myouts[-1] <= 2.0:
                    slopeok = False
                    break
            
        #prespos = pos[efv.sbepos]
        winbnd = np.less(pos,efv["uppbnd"])*np.greater(pos,efv["lowbnd"])
        
        if all(winbnd) and (slopeok == True):
            return plike
        else:
            return -np.inf
        
        
    def lnprob(pos):
        if fprior(pos):
            likel,outalphas,ycyl = lnlike(pos)
            plike                = lnprior(pos,outalphas,ycyl)
            if np.any(np.isnan(likel)):
                print(pos)
                likel = -np.inf
        else:
            likel = -np.inf
            plike = 0
            ycyl  = [0]
        return likel+plike , [ycyl]

    ndim     = len(efv["pinit"])
    nwalkers = 5*ndim
    p0       = efv["pinit"] * (1 + 3e-2*np.random.randn(nwalkers, ndim))
    efv["nburn"]    = nsteps//20
    efv["nwalkers"] = nwalkers
    efv["ndim"]     = ndim
    efv["p0"]       = p0
    efv["nsteps"]   = nsteps

    sampler  = emcee.EnsembleSampler(nwalkers, ndim,lnprob,threads = 1)
    state    = sampler.run_mcmc(p0, nsteps,progress=True)
    post_mcmc_products(hdul,sampler,cosmo_pars,efv,xymap,outfile,plotPin=plotPin,adPhys=adPhys)
    
 
def post_mcmc_products(hdul,sampler,cosmo_pars,efv,xymap,outfile,plotPin=True,adPhys=True):
    """
    After the fitting, make plots and stuff

    :param hdul: an input fits HDUList with extension=0 being the data and extension=1 being the weights.
    :type hdul: list
    :param sampler: sampler from emcee
    :type sampler: class
    :param cosmo_pars: Dictionary of cosmological parameters
    :type cosmo_pars: dict
    :param efv: Dictionary of emcee fitting variables
    :type efv: dict
    :param xymap: tuple of arrays of x- and y-coordinates.
    :type xymap: tuple
    :param outfile: output file (full path)
    :type outfile: str
    """

    flat_samples = sampler.get_chain(discard=efv["nburn"], thin=efv["nwalkers"],flat=True)
    mysolns = np.array(list(map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),
                             zip(*np.percentile(flat_samples, [16, 50, 84],
                                                axis=0)))))
    blobarr     = sampler.get_blobs(flat=True,discard=efv["nburn"], thin=efv["nwalkers"])
    blobarr     = blobarr[np.isfinite(blobarr)]        # No need for NANs or infs.
    Yints       = np.percentile(blobarr, [16, 50, 84],axis=0)
    yinteg      = Yints[1]       # This is the median...i.e. the best-fit value
    #print(yinteg)
    #import pdb;pdb.set_trace()
    r500,m500,p500, msys     = WH.rMP500_from_y500(yinteg,cosmo_pars)
    r500l,m500l,p500l, msysl = WH.rMP500_from_y500(Yints[0],cosmo_pars)
    r500u,m500u,p500u, msysu = WH.rMP500_from_y500(Yints[2],cosmo_pars)
    m_unc_array  = np.array([m500l.to("M_sun").value,m500u.to("M_sun").value])
    m_unc_values = (m_unc_array-m500.to("M_sun").value)/1e14
    m_unc        = np.mean(np.abs(m_unc_values))
    m500v        = m500.to("M_sun").value/1e14
    print("###########################################################################")
    print("R500 found to be: ",r500," radians")
    print("M500 found to be: ",m500v,r" \pm ",m_unc," 1e14 M_sun")
    print("P500 found to be: ",p500.to("keV cm**-3"))
    print("Systematic error on M500: ",msys.value," 1e14 M_sun")
    print("###########################################################################")
    #solnstack[:,:,i] = mysolns
    
    print(mysolns)
    npysave = outfile.replace("corner","solutions")
    npysave = npysave.replace(".png",".npy")
    np.save(npysave,mysolns)
    chains_save = npysave.replace("solutions","chains")
    np.save(chains_save,flat_samples)
    if not outfile is None:
        fig = corner.corner(flat_samples, labels=efv["labels"], quantiles=[0.16,0.84])
        fig.savefig(outfile)

    #return mysolns  

    pos     = mysolns[:,0]
    outmap,yint,outalpha,mnlvl = make_skymodel_map(hdul,pos,cosmo_pars,efv,xymap)
    model   = WH.lightweight_filter_ptg(outmap,efv["size"],efv["pixsize"],WIKID=efv["WIKID"]) + mnlvl

    OutHDU1 = fits.PrimaryHDU(outmap,header=hdul[0].header)
    OutHDU2 = fits.ImageHDU(model,header=hdul[1].header)
    OutHDU  = fits.HDUList([OutHDU1,OutHDU2])
    OutName = "FittedModel_"+efv["Mstr"]+"_"+efv["zstr"]+"_"+repr(efv["nsteps"])+"steps.fits"
    OutHDU.writeto(efv["outdir"]+OutName,overwrite=True)

    m500_res = np.abs(np.array([m500v,m_unc_values[0],m_unc_values[1]])) * 1e14
    if np.any(np.isnan(m500_res)) or np.any(np.isinf(m500_res)):
         m500_res = np.ones(3)*1e10
    plot_pressure_profiles(mysolns,efv,cosmo_pars,m500_res,plotPin=plotPin,adPhys=adPhys)

def plot_pressure_profiles(solns,efv,cosmo_pars,m500,myfs=10,plotPin=True,adPhys=True):

    """
    For now, assuming model == "NP"... need to add others

    :param solns: Array of solutions (with uncertainties)
    :type solns: np.ndarray
    :param efv: emcee fitting variables.
    :type efv: dict
    :param m500: Inferred M500 with uncertainties (3-element array)
    :type m500: array-like
    :param myfs: fontsize; default is 10
    :type myfs: float
    """
    
    Pressures = (solns[1:efv["nBins"]+1]/efv["Pdl2y"]).to("keV cm**-3").value         # keV/cm**3
    BinArcmin = efv["bins"]*60*180/np.pi                            # Arcminutes
    Radii     = efv["Thetas"]*60*180/np.pi                          # Arcminutes

    Pminmax   = [np.min(Pressures[:,0])/10.0,np.max(Pressures[:,0])*5]
    #print(Pressures.shape)
    #import pdb;pdb.set_trace()
    PinterFxn = interp1d(np.log(BinArcmin),np.log(Pressures[:,0]),fill_value="extrapolate")
    Pinterp   = np.exp(PinterFxn(np.log(Radii)))

    myfig     = plt.figure(3,figsize=(5,4),dpi=200)
    myfig.clf()
    myax      = myfig.add_subplot(111)
    yerrs     = np.asarray([Pressures[:,2],Pressures[:,1]])
    myax.errorbar(BinArcmin,Pressures[:,0],yerr=yerrs,linestyle="none",color="C0")
    gi1       = (Radii < np.min(BinArcmin))
    myax.plot(Radii[gi1],Pinterp[gi1],"--",color="C0")
    gi2       = (Radii >= np.min(BinArcmin))*(Radii <= np.max(BinArcmin))
    myax.plot(Radii[gi2],Pinterp[gi2],"-",color="C0",label="Recovered Pressure Profile")
    gi3       = (Radii >= np.max(BinArcmin))
    myax.plot(Radii[gi3],Pinterp[gi3],"--",color="C0")
    myax.set_xscale("log")
    myax.set_yscale("log")
    myax.set_ylim(Pminmax)
    myax.set_xlabel(r"Radius (arcmin)",fontsize=myfs)
    myax.set_ylabel(r"P$_e$ (keV cm$^{-3}$)",fontsize=myfs)

    M500_out    = m500[0]*u.Msun
    Theta500    = WH.Theta500_from_M500_z(M500_out,cosmo_pars["z"])
    Arcmin500   = Theta500 * 60 * 180 / np.pi

    
    mYM_pm   = pos_neg_formatter(m500[0],m500[1],m500[2])
    
    xpos = 10**(np.dot(np.log10(myax.get_xlim()),[0.90,0.10]))
    ypos = 10**(np.dot(np.log10(myax.get_ylim()),[0.60,0.40]))
    #print(xpos,ypos)
    myax.axvline(Arcmin500,linestyle="--",color="c")
    myax.text(Arcmin500*0.98,ypos,r"R$_{500}$",rotation=90,color="c",fontsize=myfs)    
    myax.text(xpos,ypos,r'M$_{500}$: '+mYM_pm,fontsize=myfs)

    if plotPin:
        radkpc    = Radii * 60 * cosmo_pars["scale"] * u.kpc
        PresProf  = WH.a10_from_m500_z(efv["M500"], cosmo_pars["z"],radkpc,Dist=efv["Dist"])
        Pin       = PresProf.to("keV cm**-3").value
        myax.plot(Radii,Pin,"--",label="Input Pressure Profile",color="g")

    if adPhys:
        xlims = myax.get_xlim()
        myax.set_xlim(xlims)
        phax = myax.twiny()
        phax.set_xlim([xlim*cosmo_pars["scale"]*60 for xlim in xlims])
        phax.set_xlabel("Radius (kpc)")
        phax.set_xscale("log")
    else:
        myax.set_title("Recovered Pressure Profile (Simulated)",fontsize=myfs)  

    myax.grid()
    myax.legend(fontsize=myfs)
    myfig.tight_layout()
    myfig.savefig(efv["outdir"]+"RecoveredPressureProfile_"+efv["Mstr"]+"_"+efv["zstr"]+".png")
    
def make_skymodel_map(hdul,pos,cosmo_pars,efv,xymap):
    """
    Run the actual fitting procedure.

    :param hdul: an input fits HDUList with extension=0 being the data and extension=1 being the weights.
    :type hdul: list
    :param pos: parameters fit with mcmc
    :type pos: array-like
    :param cosmo_pars: Dictionary of cosmological parameters
    :type cosmo_pars: dict
    :param efv: Dictionary of emcee fitting variables
    :type efv: dict
    :param xymap: tuple of arrays of x- and y-coordinates.
    :type xymap: tuple

    """

    posind = 0
    yint=[]; outalphas=[]
    alp=np.zeros(len(pos))

    if efv["fit_mnlvl"]:
        mnlvl = pos[posind]       
        posind+=1
    else:
        mnlvl = 0
            
    mymap,posind,ynt,myalphas = ellipsoidal_ICM(cosmo_pars,efv,pos,xymap,alp,posind,fixalpha=efv["fixalpha"])
    outmap = mymap
    yint.extend([np.real(ynt)]); outalphas.extend([np.real(myalphas)])

    return outmap,yint,outalphas,mnlvl

def ellipsoidal_ICM(cosmo_pars,efv,pos,xymap,alphas,posind=0,fixalpha=False):
    """
    Run the actual fitting procedure.

    :param cosmo_pars: Dictionary of cosmological parameters
    :type cosmo_pars: dict
    :param efv: Dictionary of emcee fitting variables
    :type efv: dict
    :param pos: emcee fitting parameters
    :type pos: array-like
    :param xymap: tuple of arrays of x- and y-coordinates.
    :type xymap: tuple
    :param alphas: power-law indices
    :type alphas: np.ndarray
    :param posind: index for emcee parameters
    :type posind: int
    :param fixalpha: Fix the power-law indices to input values? Default is False.
    :type fixalpha: bool

    """

    szcv,szcu  = WH.get_sz_values()
    geom       = efv["geo"]
    bins       = efv["bins"]

    nbins = len(bins)
    if efv["finite"] == True:
        nbins-=1     # Important correction!!!
    ulesspres = pos[posind:posind+nbins]
    myalphas = alphas   
    ulessrad  = bins #.to("rad").value
    posind = posind+nbins
    if efv["fit_cen"] == True:
        geom[0:2] = pos[posind:posind+2]  # I think this is what I want...
        posind = posind+2
        
    if efv["fit_geo"] == True:
        geom[2]     = pos[posind]           # Rotation angle
        geom[4]     = pos[posind+1]     # Major axis (should be > 1.0, if minor is defined as 1).
        geom[5]     = np.sqrt(pos[posind+1])     # Assume that the axis along the l.o.s. is geom. mean of maj,min axes.
        pos[posind] = pos[posind] % (np.pi) #if tdtheta > np.pi b/c symmetry reduces it to just pi. (July 2018)
        posind      = posind+2
            
    if efv["model"] == 'NP':
        Int_Pres,outalphas,integrals = ai.integrate_profiles(ulesspres, geom,bins,efv["Thetas"],inalphas=myalphas)

    if efv["model"] == 'GNFW':
        print("Under construction")
        unitless_profile = 0.0
        
    if efv["model"] == 'BETA':
            radii    = efv["Thetas"]
            pprof     = ulesspres[0]*(1.0+(radii/ulesspres[1])**2)**(-1.5*ulesspres[2])        ### Beta model
            #scaling  = scs.gamma(1.5*ulesspres[2] - 0.5)/scs.gamma(1.5*ulesspres[2]) * ulesspres[1] * ulesspres[0]
            scaling  = scs.gamma(1.5*ulesspres[2]-0.5)/scs.gamma(1.5*ulesspres[2])*ulesspres[1] * cosmo_pars["d_a"]
            scaling *= ulesspres[0] * np.sqrt(np.pi) *(szcu['thom_cross'] * u.kpc / szcu['m_e_c2']).to('cm**3 / keV')
            Int_Pres    = scaling.value * (1.0+(radii/ulesspres[1])**2)**(0.5-1.5*ulesspres[2])
            outalphas = Int_Pres*0.0+2.0
            integrals = Int_Pres
            
    #############################################################################################3
        
    if efv["model"] == 'NP':
        pprof,alphas   = ai.log_profile(ulesspres,list(bins),efv["Thetas"]) # Last pos is mn lvl
    elif efv["model"] == 'GNFW':
        pprof = unitless_profile * efv["d_a"]
            
    if efv["ySph"]:
        yint ,newr500=Y_SZ_v2(pprof,efv,retcurvs=False) # As of Aug. 31, 2018
    else:
        yint ,newr500=Y_SZ_v2(Int_Pres,efv,retcurvs=False) # As of Aug. 31, 2018

    #r500,m500,p500, msys = rMP500_from_y500(yinteg,cosmo_pars
    ### Int_Pres natively is in Compton y. If you want a map in different units, one may convert Int_Pres to IntProf
    ### and feed that in instead of Int_Pres below:
    mymap = ai.general_gridding(xymap,efv["Thetas"],bins,geom,finite=efv["finite"],integrals=integrals,
                                            Int_Pres=Int_Pres,oldvs=False)

    return mymap,posind,yint,outalphas

def Y_SZ_v2(yProf,efv,retcurvs=False):
    """
    :param yProf: an integrated profile, i.e. in Compton y that matches theta_range
    :type yProf: np.ndarray
    :param efv: emcee fitting variables
    :type efv: dict
    :param retcurvs: option to return curves; default is False.
    :type retcurvs: bool 

    I'm adopting equations 25-27 in Arnaud+ 2010, which makes use of Y_SZ, or Y_cyl and the
    Universal Pressure Profile (UPP). I tried to find just a straight empirical Y_cyl(R500)-M_500,
    but that doesn't seem to exist?!?

    """

    rProf     = efv["Thetas"]
    r_max     = efv["Theta500"]
    ylist     = efv["y500s"]
    geom      = efv["geo"]
    
    alpha,norm  = ai.ycyl_prep(yProf,rProf)
    
    if not efv["ySph"]:
        yinteg, root,yR,yM = ycyl_simul_v2(rProf,yProf,alpha,r_max,ylist,geom,r_thresh=3e-2,retcurvs=True)
        #import pdb;pdb.set_trace()
    else:
        ### yProf is ***NOT*** a Compton y profile!!! IT IS A PRESSURE PROFILE! -- May 2019
        yinteg, root,yR,yM = ysph_simul(ylist,rProf,yProf,alpha,geom,ythresh=3e-8,retcurvs=True)

    if retcurvs:
        return yinteg, root,yR,yM
    else:
        return yinteg, root

def ycyl_simul_v2(rads,yProf,alpha,maxrad,ylist,geom,r_thresh=3e-2,retcurvs=False):

    """
    :param rads: Radius in radians
    :type rads: numpy.ndarray
    :param yProf: Compton y profile
    :type yProf: numpy.ndarray
    :param alpha: list of power-law indices
    :type alpha: array-like
    :param maxrad: maximum radius
    :type maxrad: float
    :param ylist: array of expected y values.
    :type ylist: numpy.ndarray
    :param geom: [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    :type geom: array-like
    :param r_thresh: Threshold value. Default is 3e-2.
    :type r_thresh: float
    :param retcurvs: Return curves? Default is False.
    :type retcurvs: bool
    """

    fgeo          = geom[3]*geom[4] # Scale by ellipsoidal radii scalings.
    Ycyl          = np.arange(10)
    if alpha[0]  <= -2: alpha[0]=-1.9
    badalp        = (alpha == -2)
    alpha[badalp] = -2.01 # Va fanculo.
    rolledrad     = np.roll(rads,-1)
    intupper      = rolledrad**2 * (rolledrad/rads)**(alpha) #* myrads
    intlower      = rads**2
    intlower[0]   = 0.0
    integrand     = intupper - intlower
    Yshell        = 2.0*np.pi*yProf[:-1]*integrand[:-1]/(alpha[:-1]+2.0)
    Ycyl          = np.cumsum(Yshell)*fgeo
    #import pdb;pdb.set_trace()
    Yref          = ylist[:-1].value
    #Yref          = ylist[:-1]
    mydiff        = Yref - Ycyl

    nrbins        = len(rads)
    #mydiff = rads[1:] - r500
    #absdif = np.abs(mydiff)
    posdiffs = (mydiff > 0)
    turnover = mydiff[posdiffs]
    #import pdb;pdb.set_trace()
    bestr = -rads[1]
    bestY = -Ycyl[0]
    bisca = 0
    if len(turnover) > 1:
        besti  = np.where(mydiff == np.min(turnover))
        bisca  = np.ndarray.item(besti[0])
    if bisca < nrbins -3 and bisca > 10: 
        myinds = bisca + np.asarray([-2,-1,0,1,2],dtype='int')
        #myinds = np.intersect1d(naind,
        myrs   = rads[myinds+1]
        myYs   = Ycyl[myinds]
        myds   = mydiff[myinds]
        myp2   = np.polyfit(myrs,myds,2)
        myY2   = np.polyfit(myrs,myYs,2)
        myroot = np.roots(myp2)
        rdiff  = np.abs(myroot - myrs[2])

        bestr  = myroot[0] if rdiff[0] < rdiff[1] else myroot[1]
        Y2fxn  = np.poly1d(myY2)
        bestY  = Y2fxn(bestr)

        
    #import pdb;pdb.set_trace()
    #bestr  = r500[besti]
    #bestY  = Ycyl[besti]
    if retcurvs:
        return bestY,bestr, Yref,Ycyl
    else:
        return bestY,bestr
   
def ysph_simul(ylist,rads,pProf,alpha,geom,ythresh=3e-8,retcurvs=False):

    """
    :param ylist: array of expected y values.
    :type ylist: numpy.ndarray
    :param rads: Radius in radians
    :type rads: numpy.ndarray
    :param pProf: pressure profile
    :type pProf: numpy.ndarray
    :param alpha: list of power-law indices
    :type alpha: array-like
    :param geom: [X_shift, Y_shift, Rotation, Ella*, Ellb*, Ellc*, Xi*, Opening Angle]
    :type geom: array-like
    :param y_thresh: Threshold value. Default is 3e-8.
    :type y_thresh: float
    :param retcurvs: Return curves? Default is False.
    :type retcurvs: bool
    """  

    fgeo          = geom[3]*geom[4]*geom[5] # Scale by ellipsoidal radii scalings.
    Ysph          = np.arange(10)
    if alpha[0]  <= -3: alpha[0]=-2.9
    badalp        = (alpha == -3)
    alpha[badalp] = -3.01 # Va fanculo.
    rolledrad     = np.roll(rads,-1)
    intupper      = rolledrad**3 * (rolledrad/rads)**(alpha) #* myrads
    intlower      = rads**3
    intlower[0]   = 0.0
    integrand     = intupper - intlower
    Yshell        = 4.0*np.pi*pProf[:-1]*integrand[:-1]/(alpha[:-1]+3.0) 
    Ysph          = np.cumsum(Yshell) *fgeo
    Yref          = ylist[:-1].value
    #Yref          = ylist[:-1]
    mydiff        = Yref - Ysph

    ### Look here (April 13, 2019)
    #import matplotlib.pyplot as plt
    #plt.plot(rads[1:]*3600.0*180/np.pi,Yref)
    #plt.plot(rads[1:]*3600.0*180/np.pi,Ysph)
    #plt.yscale('log');plt.xscale('log')
    #plt.show()
    #import pdb;pdb.set_trace()

    #mydiff = rads[1:] - r500
    #absdif = np.abs(mydiff)
    posdiffs = (mydiff > 0)
    turnover = mydiff[posdiffs]
    #import pdb;pdb.set_trace()
    bestr = rads[51]
    bestY = Ysph[50]
    bisca = 0
    nrbins        = len(rads)
    if len(turnover) > 1:
        besti  = np.where(mydiff == np.min(turnover))
        bisca  = np.ndarray.item(besti[0])
    if bisca < nrbins-3 and bisca > 10: 
        myinds = bisca + np.asarray([-2,-1,0,1,2],dtype='int')
        #myinds = np.intersect1d(naind,
        myrs   = rads[myinds+1]
        myYs   = Ysph[myinds]
        myds   = mydiff[myinds]
        myp2   = np.polyfit(myrs,myds,2)
        myY2   = np.polyfit(myrs,myYs,2)
        myroot = np.roots(myp2)
        rdiff  = np.abs(myroot - myrs[2])

        bestr  = myroot[0] if rdiff[0] < rdiff[1] else myroot[1]
        Y2fxn  = np.poly1d(myY2)
        bestY  = Y2fxn(bestr)

        if bestY > ythresh:
            print(bestr, bestY, np.max(rads))
            stupid = np.random.normal(0,1)
            if stupid > 5: import pdb;pdb.set_trace()
            
        
    #import pdb;pdb.set_trace()
    #bestr  = r500[besti]
    #bestY  = Ysph[besti]
    if retcurvs:
        return bestY,bestr, Yref,Ysph
    else:
        return bestY,bestr

def fit_Gaussian_toSNR(SNRmap,pixsize,maxRad=2.0):
    
    """
    close to fitmap as was used in IDL
    :param SNRmap: a 2D numpy array
    :type SNRmap: nump.ndarray
    :param pixsize: pixel size, in arcseconds
    :type pixsize: float
    :param maxRad: Maximum search radius, arcminutes
    :type maxRad: float
    """

    nx,ny   = SNRmap.shape
    numpyx  = np.outer(np.arange(nx),np.ones(ny))
    numpyy  = np.outer(np.ones(nx),np.arange(ny))
    maxSNR  = np.max(SNRmap)
    maxInd  = (SNRmap == maxSNR)
    #maxinds = np.where(SNRmap == maxSNR)
    #print(maxinds)
    xc      = numpyx[maxInd][0]
    yc      = numpyy[maxInd][0]
    #print(xc,yc)
    #import pdb;pdb.set_trace()
    #xc      = maxinds[0][0]
    #yc      = maxinds[0][1]
    xymap   = WH.get_xymap(SNRmap,pixsize*u.arcsec,xcentre=xc,ycentre=yc,oned=True)
    rmap    = WH.make_rmap(xymap)
    SNRflat = SNRmap.flatten()
    xinit   = np.asarray(xymap)
    grads   = (rmap < maxRad*60.0)
    xdata   = xinit[:,grads]
    ydata   = SNRflat[grads]
    #p0      = np.array([x0,y0,amplitude,sigma,mnlvl])
    xshift  = 1.0  # As a guess
    yshift  = 1.0  # in arcseconds
    sigma   = 20.0 # Gaussian sigma, in arcseconds
    mnlvl   = 1e-2 # Plausible, for an SNR map
    p0      = np.array([xshift,yshift,maxSNR,sigma,mnlvl])
    
    popt, pcov = curve_fit(circ_Gauss, xdata, ydata,p0=p0)

    return popt,pcov,xc,yc
    
def circ_Gauss(xdata,xc,yc,norm,sig,mnlvl):
    """
    Calculate a 2D (circular) Gaussian

    :param xdata: an array of flattened x and y coordinates
    :type xdata: numpy.ndarray
    :param xc: x-center
    :type xc: float
    :param yc: y-center
    :type yc: float
    :param norm: Gaussian amplitude
    :type norm: float
    :param sig: Gaussian width (sigma)
    :type sig: float
    :param mnlvl: mean level (or DC offset, or pedastal)
    :type mnlvl: float
    """

    r1d   = np.sqrt(xdata[0,:]**2 + xdata[1,:]**2)
    Gauss = np.exp(-r1d**2/(2*sig**2))
    model = Gauss*norm + mnlvl
    
    return model

def get_int_SNR(SNRmap,pixsize,maxRad=2.0,bv=120.0,SNRthresh=1.0):
    """
    Get the integrated detection significance.

    :param SNRmap: a 2D numpy array
    :type SNRmap: nump.ndarray
    :param pixsize: pixel size, in arcseconds
    :type pixsize: float
    :param maxRad: Maximum search radius, arcminutes
    :type maxRad: float
    :param bv: beam volume in square arcseconds. Default is 120.
    :type bv: float
    :param SNRthresh: SNR threshold
    :type SNRthresh: float
    """

    popt,pcov,xc,yc        = fit_Gaussian_toSNR(SNRmap,pixsize,maxRad=maxRad)
    xcentre                = xc+popt[0]
    ycentre                = yc+popt[1]
    xymap                  = WH.get_xymap(SNRmap,pixsize*u.arcsec,xcentre=xcentre,ycentre=ycentre,oned=False)
    rmap                   = WH.make_rmap(xymap)
    rbin,ybin,yerr,ycnts   = bin_two2Ds(rmap,SNRmap,binsize=pixsize*2.0)

    badind                 = (ybin < SNRthresh)
    RadThresh              = np.min(rbin[badind])
    goodind                = (rmap < RadThresh)
    goodSNR                = SNRmap[goodind]
    NumberBeams            = np.sum(goodind)*pixsize**2 / bv
    SNRint                 = np.sqrt( np.sum(SNRmap**2)/(NumberBeams) )

    return SNRint,xcentre,ycentre,xymap
    
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

def improved_bin_spacing(radminmax,nbins,mway=False):

    """
    Calculate the bin spacing for MUSTANG-2 based on the number of bins.

    :param radminmax: two-element array or list, of minimum and maximum radii (in arcseconds) to cover.
    :type radminmax: array-like
    :param nbins: Number of bins
    :type nbins: int
    :param mway: An option to try another way. Default (best option) is False.
    :type mway: bool
    """

    m2fwhm    = 10.0 * u.arcsec.to('rad')
    bins      = np.logspace(np.log10(radminmax[0]),np.log10(radminmax[1]), nbins)

    #print(bins)
    
    if mway:
        barr   = bins*1.0
        myinds = np.arange(nbins)
        bsiter = 0
        bspace = barr - np.roll(barr,1)
        bi1    = (bspace < m2fwhm*0.99999)
        bi2    = (myinds > 0)
        badind = [b1 and b2 for b1,b2 in zip(bi1,bi2)]
        while np.sum(badind) > 0:
            minbin = np.min(myinds[badind])
            maxbin = np.max(myinds[badind])
            newbin = (np.arange(np.sum(badind))+1 )*m2fwhm
            stabin = barr[minbin-1]
            barr[badind] = newbin+stabin
            bsiter+=1
            bspace = barr - np.roll(barr,1)
            bi1    = (bspace < m2fwhm*0.99999)
            bi2    = (myinds > 0)
            badind = [b1 and b2 for b1,b2 in zip(bi1,bi2)]
            print("Bin spacing iteration: ",bsiter)

        nlb = nbins-maxbin
        newbin = np.logspace(np.log10(barr[maxbin]),np.log10(radminmax[1]), nlb)
        bins   = barr*1.0
        bins[maxbin:] = newbin
        print("Bins are now: ",barr*3600*180/np.pi,bins*3600*180/np.pi)
        import pdb;pdb.set_trace()

    else:

        print("Bins start with: ",bins*3600*180/np.pi)
        bsiter = 1
        if radminmax[0] == m2fwhm:        
            while bins[1]-bins[0] < m2fwhm:
                #bins   = np.logspace(np.log10(radminmax[0] + m2fwhm*(bsiter-1)),np.log10(radminmax[1]), nbins-bsiter+1)
                bins   = np.logspace(np.log10(m2fwhm*bsiter),np.log10(radminmax[1]), nbins-bsiter+1)
                bsiter+=1
        else:
            while bins[2]-bins[1] < m2fwhm:
                bins   = np.logspace(np.log10(radminmax[0] + m2fwhm*(bsiter-1)),np.log10(radminmax[1]), nbins-bsiter+1)
                bsiter+=1
                
        if bsiter > 2:
            #prebins = np.hstack((np.array([radminmax[0]]),np.arange(1,bsiter-2)*m2fwhm))
            #prebins = np.arange(1,bsiter-1)*m2fwhm
            prebins = np.arange(0,bsiter-2)*m2fwhm + radminmax[0]
            #if radminmax[0] == m2fwhm:
            bins    = np.hstack((prebins,bins))

        print("Bins are now: ",bins*3600*180/np.pi)
    #import pdb;pdb.set_trace()

    return bins

def pos_neg_formatter(med,high_err,low_err,sys=None,cal=None):
    """
    Input the median (or mode), and the *error bars* (not percentile values, but the
    distance between the +/-1 sigma percentiles and the 0 sigma percentile).

    :param med: median
    :type med: float
    :param high_err: uncertainty (on the high side)
    :type high_err: float
    :param low_err: uncertainty (on the low side)
    :type low_err: float
    :param sys: systematic error. Default is None
    :type sys: float
    :param cal: calibration error. Default is None
    :type cal: float
    """

    mypow = np.floor(np.log10(med))
    myexp = 10.0**mypow

    if np.isfinite(mypow):
        if mypow > 0:
            psign = '+'
            pStr = psign+str(int(mypow))
        else:
            pStr = str(int(mypow))
    else:
        # This captures an exceptional case.
        print(med)
        mypow = 0.0
        myexp = 1.0
        pStr = str(int(mypow))
            
    msig  = med/myexp
    hsig  = high_err/myexp
    lsig  = low_err/myexp

    
    msStr = "{:.2F}".format(msig)
    hsStr = '+'+"{:.2F}".format(hsig)
    lsStr = "{:.2F}".format(-lsig)

    baStr = r'${0}^{{{1}}}_{{{2}}}$'. format(msStr,hsStr,lsStr)
    
    if not (sys is None):
        #myma  = (10**sys - 1) * med
        #mymb  = (10**(-sys) - 1) * med
        #import pdb;pdb.set_trace()
        myma  = (np.exp(sys) - 1) * med
        mymb  = (np.exp(-sys) - 1) * med
        hyStr = '+'+"{:.2F}".format(myma/myexp)
        lyStr = "{:.2F}".format(mymb/myexp)
        #hyStr = '+'+"{:.2F}".format(sys/myexp)
        #lyStr = "{:.2F}".format(-sys/myexp)
        baStr = baStr + r' $^{{{0}}}_{{{1}}}$'.format(hyStr,lyStr)
    if not (cal is None):
        hyStr = '+'+"{:.2F}".format(cal[1]/myexp)
        lyStr = "{:.2F}".format(-cal[0]/myexp)
        baStr = baStr + r' $^{{{0}}}_{{{1}}}$'.format(hyStr,lyStr)
    
    exStr = 'E'+pStr
    coStr = baStr+exStr

    return coStr

def extract_radial_profile(hdul,arcmin=True):
    """
    Extract a radial profile using the CRPIX value in a HDU.


    :param hdul: HDUlist
    :type hdul: list
    :param arcmin: If true, then radius is given in arcminutes; otherwise in arcseconds.
    :type arcmin: bool
    """

    SOw                    = WCS(hdul[0].header)
    factor                 = 60.0 if arcmin else 1.0
    pixsize = np.sqrt(np.abs(np.linalg.det(SOw.pixel_scale_matrix))) * 3600.0
    hdulImg                = hdul[0].data

    #print(SOw)
    #import pdb;pdb.set_trace()
    xc                     = SOw.wcs.crpix[0]
    yc                     = SOw.wcs.crpix[1]
    #print(xc,yc)

    xymap                  = WH.get_xymap(hdulImg,pixsize*u.arcsec,xcentre=xc,ycentre=yc,oned=False)
    rmap                   = WH.make_rmap(xymap) / factor
    rbin,ybin,yerr,ycnts   = bin_two2Ds(rmap,hdulImg,binsize=pixsize*2.0/factor)

    return rbin,ybin,yerr,ycnts

def prntPeak(yProf,inHDU,isUK=True,Tag="SimObs-- "):

    """
    Print the peak of a profile and map to STDOUT.

    :param yProf: the (binned) Compton y profile
    :type yProf: numpy.ndarray
    :param inHDU: a HDUList
    :type: inHDU: list
    :param isUK: are the units microKelvin? Default is True
    :type isUK: bool
    :param Tag: Additional tag
    :type Tag: str
    """

    if isUK:
        ProfPeak = np.min(yProf)
        MapPeak  = np.min(inHDU[0].data)
    else:
        ProfPeak = np.max(yProf)
        MapPeak  = np.max(inHDU[0].data)

    print(Tag+"Peak in binned profile: ",ProfPeak," ; peak in map: ",MapPeak)

def plot_SB_profiles(SimObs,SimSky,outdir,filename,prntPk=True,isUK=True,xmin=0,xmax=2.0,
                     addHDU=None,addLabel=None):

    """
    A routine to plot a simulated sky versus simulated observation, radial profiles.

    :param SimObs: an HDUList object for simulated observations
    :type SimObs: list
    :param SimSky: an HDUList object for simulated sky (beam-convolved; not filtered)
    :type SimSky: list
    :param outdir: Output director, with the trailing "/"
    :type outdir: str
    :param filename: Output filename, without path.
    :type filename: str
    :param prntPk: Print the peaks of profiles and maps? Default is True.
    :type prntPk: bool
    :param isUK: Are the arrays in the HDULists in units of uK? Default is True
    :type isUK: bool

    """
    SOr,SOy,SOe,SOc = extract_radial_profile(SimObs)
    SSr,SSy,SSe,SSc = extract_radial_profile(SimSky)
    #WMr,WMy,WMe,WMc = extract_radial_profile(SimSky)
    #pixsize         = WH.get_pixarcsec(SimObs)
    #bmCnt           = WMc*pixsize**2 / bv
    #UncPerBin       = 1.0/ np.sqrt( WMy*bmCnt )

    myfig     = plt.figure(2,figsize=(5,4),dpi=200)
    myfig.clf()
    myax      = myfig.add_subplot(111)
    myax.plot(SOr,SOy,label="Mock Obs")
    myax.plot(SSr,SSy,label="Sky, bm conv.")
    if not addHDU is None:
        addr,addy,adde,addc = extract_radial_profile(addHDU)
        myax.plot(addr,addy,label=addLabel)
        if prntPk:
            prntPeak(addy,addHDU,isUK=True,Tag="Smoothed Mock Obs-- ")

    #myax.plot(WMr,UncPerBin,label="Corresponding Unc.")

    if prntPk:
        prntPeak(SOy,SimObs,isUK=True,Tag="Mock Obs-- ")
        prntPeak(SOy,SimSky,isUK=True,Tag="Bm. Conv. Sky-- ")
    
    myax.set_xlabel("Radius (arcmin)")
    myax.set_ylabel(r"SB ($\mu$K)")
    myax.set_xlim([xmin,xmax])
    myax.legend()

    myfig.tight_layout()
    myfig.savefig(outdir+filename)
