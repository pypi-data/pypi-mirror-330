import numpy as np
import scipy.ndimage
import scipy.signal
from astropy.io import fits

def get_freqarr_2d(nx,ny,psx, psy):
    """
       Compute frequency array for 2 D FFT transform
      
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
    k = np.sqrt(kx*kx + ky*ky)
    return k

def power_spectrum_2d(arr,nbins=10,psx=1,psy=1,logbins=False):
    """
    Compute 2D power spectrum of arr
    
    Parameters
    ----------
    arr: float 2D numpy array
         2D array for which we compute the power spectrum
    nbins: integer, optional
         number of frequency k bins (10)
         
    psx:  integer, optional (1)
    Returns
    -------
    kbin: float 1D numpy array
          bins in k-space
    pkbin: float 1D numpy array
          2D power spectrum for kbin
    """
    farr = np.fft.fft2(arr)/np.double(arr.size)
    nx,ny = arr.shape
    k = get_freqarr_2d(nx,ny,psx, psy)
    pk = np.double(farr * np.conj(farr))
    if logbins:
        kbinarr = np.logspace(0.0,np.log(k.max()),nbins+1) 
    else:
        kbinarr = np.arange(nbins+1)/np.double(nbins)*(k.max()-k.min())
    kbin   = np.zeros(nbins+1)
    pkbin  = np.zeros(nbins+1)
    pkbins = np.zeros(nbins+1)

    for idx in range(0,nbins):
        mylist        = np.nonzero((k > kbinarr[idx]) * (k<= kbinarr[idx+1]))
        kbin[idx+1]   = np.median(k[mylist])
        pkbin[idx+1]  = np.mean(pk[mylist])
        pkbins[idx+1] = np.std(pk[mylist])/np.sqrt(len(mylist[0]))
    return kbin,pkbin,pkbins

def cross_power_spectrum_2d(arr,arr1,nbins=10,psx=1.0,psy=1.0,logbins=False):
    """
    Compute 2D cross-power spectrum of arr and arr1
    
    Parameters
    ----------
    arr: float 2D numpy array
         2D array for which we compute the power spectrum
    arr1: float 2D numpy array
         2D array for which we compute the power spectrum
    nbins: integer, optional
         number of frequency k bins (10)
         
    psx:  integer, optional (1)
    psy:  integer, optional (1)
    logbins: bool, optional (False)

    Returns
    -------
    kbin: float 1D numpy array
          bins in k-space
    pkbin: float 1D numpy array
          2D power spectrum for kbin
    """
    nx,ny = arr.shape
    nx1,ny1 = arr1.shape
    if nx1 == nx:
        if ny1 == ny:
            farr = np.fft.fft2(arr)/np.double(arr.size)
            farr1 = np.fft.fft2(arr1)/np.double(arr1.size)
            k = get_freqarr_2d(nx,ny,psx, psy)
            pk = np.double(farr * np.conj(farr1))
            if logbins:
                kbinarr = np.logspace(0.0,np.log(k.max()),nbins+1) 
            else:
                kbinarr = np.arange(nbins+1)/np.double(nbins)*(k.max()-k.min())
            kbin = np.zeros(nbins+1)
            pkbin = np.zeros(nbins+1)
            pkbins = np.zeros(nbins+1)
            for idx in range(0,nbins):
                mylist = np.nonzero((k > kbinarr[idx]) * (k<= kbinarr[idx+1]))
                kbin[idx+1] = np.median(k[mylist])
                pkbin[idx+1] = np.mean(pk[mylist])
                pkbins[idx+1] = np.std(pk[mylist])/np.sqrt(len(mylist[0]))
    return kbin,pkbin,pkbins

def fourier_conv_2d(arr,kernel):
    """
    From JMP; perform convolution, i.e. (arr * kernel)
    
    Parameters
    ----------
    arr: float 2D numpy array
         input image
    kernel: float 2D numpy array
         input convolution kernel (real-space)
         
    Returns
    -------
    output: float 2D numpy array
         convolved image

    """
    farr = np.fft.fft2(arr)
    fker = np.fft.fft2(kernel)
    farr = farr * fker
    return np.real(np.fft.ifft2(farr))

def fourier_filtering_2d(arr,filt_type,par):
    """
    From JMP; perform parametric Fourier filtering
    
    Parameters
    ----------
    arr: float 2D numpy array
         input image
    filt_type: str
         One of "gauss", "hpcos", "lpcos", "bpcos", or "tab". The options refer to a 2D Gaussian kernel, a high-pass cosine filter, a low-pass cosine filter, a windowed (both hp and lp) cosine filter, or a tabulated filter. 
    par: float, array-like, or tuple of arrays, depending on the filt_type.
         
    Returns
    -------
    output: float 2D numpy array
         filtered image

    """
    farr  = np.fft.fft2(arr)
    nx,ny = arr.shape
    kx    = np.outer(np.fft.fftfreq(nx),np.zeros(ny).T+1.0)
    ky    = np.outer(np.zeros(nx).T+1.0,np.fft.fftfreq(ny))
    k     = np.sqrt(kx*kx + ky*ky)
#    import pdb; pdb.set_trace()
    if filt_type == 'gauss': filter = gauss_filter_2d(k,par)
    if filt_type == 'hpcos': filter = hpcos_filter_2d(k,par)
    if filt_type == 'lpcos': filter = lpcos_filter_2d(k,par)
    if filt_type == 'bpcos': filter = bpcos_filter_2d(k,par)
    if filt_type == 'tab':   filter = table_filter_2d(k,par)
    farr    = farr * filter
    arrfilt = np.real(np.fft.ifft2(farr))
    return arrfilt

def gauss_filter_2d(k,par):
    """
    From JMP; perform parametric Fourier filtering
    
    Parameters
    ----------
    k: float 2D numpy array
         input image
    par: float
        The fwhm of a 2D Gaussian.
         
    Returns
    -------
    output: float 2D numpy array
         The filter, in Fourier space

    """
    fwhm = par
    sigma = fwhm/(2.0*np.sqrt(2.0*np.log(2)))
    filter = np.exp(-2.0*k*k*sigma*sigma*np.pi*np.pi)
    return filter

def lpcos_filter_2d(k,par):
    """
    From JMP; perform parametric Fourier filtering
    
    Parameters
    ----------
    k: float 2D numpy array
         input image
    par: two-element array or list
        par[0] corresponds to the where the filter is still unity. par[1] corresponds to where the filter is zero. (par[1] > par[0])
         
    Returns
    -------
    output: float 2D numpy array
         The filter, in Fourier space

    """
    k1 = par[0]
    k2 = par[1]
    filter = k*0.0
    filter[k < k1]  = 1.0
    filter[k >= k1] = 0.5 * (1+np.cos(np.pi*(k[k >= k1]-k1)/(k2-k1)))
    filter[k > k2]  = 0.0
    return filter

def hpcos_filter_2d(k,par):
    """
    From JMP; perform parametric Fourier filtering
    
    Parameters
    ----------
    k: float 2D numpy array
         input image
    par: two-element array or list
        par[0] corresponds to the where the filter is zero. par[1] corresponds to where the filter is unity. (par[1] > par[0])
         
    Returns
    -------
    output: float 2D numpy array
         The filter, in Fourier space

    """
    k1 = par[0]
    k2 = par[1]
    filter = k*0.0
    filter[k < k1]  = 0.0
    filter[k >= k1] = 0.5 * (1-np.cos(np.pi*(k[k >= k1]-k1)/(k2-k1)))
    filter[k > k2]  = 1.0
    return filter

def bpcos_filter_2d(k,par):
    """
    From JMP; perform parametric Fourier filtering
    
    Parameters
    ----------
    k: float 2D numpy array
         input image
    par: four-element array or list
        par[0:2] is used for the high pass filter; par[2:4] is used for the low pass filter.
         
    Returns
    -------
    output: float 2D numpy array
         The filter, in Fourier space

    """
    filter = hpcos_filter_2d(k,par[0:2]) * lpcos_filter_2d(k,par[2:4])
    return filter


def gauss_2d(sigma,nx,ny):
    """
    From JMP; perform parametric Fourier filtering
    
    Parameters
    ----------
    k: float 2D numpy array
         input image
    par: four-element array or list
        par[0:2] is used for the high pass filter; par[2:4] is used for the low pass filter.
         
    Returns
    -------
    output: float 2D numpy array
         The filter, in Fourier space

    """
    ix =  np.outer(np.arange(nx),np.zeros(ny).T+1)-nx/2
    iy =  np.outer(np.zeros(nx)+1,np.arange(ny).T)-ny/2
    r = ix*ix+iy*iy
    fg = np.exp(-0.5*r/sigma/sigma)    
    return fg

def table_filter_2d(k,par):
    """
    From JMP; perform parametric Fourier filtering
    
    Parameters
    ----------
    k: float 2D numpy array
         input image
    par: four-element array or list
        par[0:2] is used for the high pass filter; par[2:4] is used for the low pass filter.
         
    Returns
    -------
    output: float 2D numpy array
         The filter, in Fourier space

    """
    from scipy import interpolate
    kbin,filterbin = par
    f = interpolate.interp1d(kbin, filterbin)
    kbin_min = kbin.min()
    kbin_max = kbin.max()
    
    filter = k * 0.0
    filter[(k >= kbin_min)  & (k <= kbin_max)] = f(k[(k >= kbin_min)  & (k <= kbin_max)])   # use interpolation function returned by `interp1d`
    filter[(k < kbin_min)] = filterbin[kbin == kbin_min]
    filter[(k > kbin_max)] = filterbin[kbin == kbin_max]

    return filter

def apply_xfer(mymap, tab,pixsize, tabdims="1D",BSerr=False):
    """
    Applies a transfer function based on the instrument for which you want to
    simulate an observation for. This is namely dependent on the format of the
    transfer function. It would be great if the format were standardized...but
    for now, we'll stick with this. 

    Caution
    -------
    The transfer function for MUSTANG2 and NIKA2 are *not* accurate as of 
    June 2017. (They use the old transfer function...just to have something
    defined.)
    
    Parameters
    ----------
    mymap       :  float 2D numpy array
    tab         :  A tabulated (or 2D array) of the transfer function
    pixsize     :  Pixel size (arcseconds)
    tabdims     :  A string ("1D" or "2D") for the dimensions of the tabulated 
                   transfer function
    pixsize     :  Pixel size (arcseconds)
    BSerr       :  Attempt to fold in transfer function error; generally not used.

    Returns
    -------
    mapfilt     :  The filtered mymap (2D array)
    """

    if tabdims == "1D":
        myk        = tab[0,0:]*pixsize
        ### Added Oct. 5, 2018:
        ### Bootstrap error
        if BSerr == True: 
            mytab      = tab[1,0:] + np.random.normal(0,1.0,len(tab[1,0:]))*tab[2,0:]
        else:
            mytab      = tab[1,0:]
        mapfilt    = fourier_filtering_2d(mymap,'tab',(myk,mytab))
    if tabdims == "2D":
        centre     = mymap.shape[0]/2
        mymap      = mymap[centre-21:centre+21,centre-21:centre+21]
        mapfilt_ft = tab*np.fft.fft2(mymap)
        mapfilt    = np.real(np.fft.ifft2(mapfilt_ft))
#    if instrument == "NIKA":
#        mapfilt    = fourier_filtering_2d(mymap,'tab',(tab[0][0],tab[0][1]))
    
    return mapfilt

def get_xfer(tabfile,tabformat='ascii',tabdims="1D",tabcomments="#",instrument="MUSTANG2",tabextend=True):
    """
    Retrieves transfer function information from a relevant file. 

    Caution
    -------
    The transfer functions for MUSTANG2 are only approximate
    
    Parameters
    ----------
    tabfile : str
       A filename containing transfer function information
    tabformat : str
       Either "ascii' or 'fits'
    tabdims : str 
    A string ("1D" or "2D") for the dimensions of the tabulated transfer function
    tabcomments : str
       If the file is ascii, what are the comment characters?
    instrument : str
       For now, only "MUSTANG2" and "MUSTANG" are explicitly supported
    tabextend : bool
       Extrapolate to lower frequencies? Default is True

    Returns
    -------
    tab : a 2-D array for which entries [0,:] correspond to the wavenumber (k) and entries [1,:] correspond to the transfer function values.
    """

    if tabformat == 'ascii':
        tab = np.loadtxt(tabfile, comments=tabcomments)
    if tabformat == 'fits':
        ktab = fits.getdata(tabfile)
        xtab = fits.getdata(tabfile,ext=1)
        tab = np.vstack((ktab,xtab))
        
    if tabdims == '1D':
        if instrument == "MUSTANG" or instrument == "MUSTANG2":
            tab = tab.T            # Transpose the table.
#        import pdb;pdb.set_trace()
        if tabextend==True:
            tdim = tab.shape
            #import pdb;pdb.set_trace()
            pfit = np.polyfit(tab[0,tdim[1]//2:],tab[1,tdim[1]//2:],1)
            addt = np.max(tab[0,:]) * np.array([2.0,4.0,8.0,16.0,32.0])
            extt = np.polyval(pfit,addt)
            ### For better backwards compatability I've editted to np.vstack instead of np.stack
            if tdim[0] == 2:
                foo = np.vstack((addt,extt)) # Mar 5, 2018
            else:
                pfit2 = np.polyfit(tab[0,tdim[1]//2:],tab[2,tdim[1]//2:],1)
                extt2 = np.polyval(pfit2,addt)
                foo = np.vstack((addt,extt,extt2)) # Mar 5, 2018

            #print(tab.shape, foo.shape)
            tab = np.concatenate((tab,foo),axis=1)
#            newt = [np.append(tab[0,:],addt),np.append(tab[1,:],extt)]
            
    return tab
