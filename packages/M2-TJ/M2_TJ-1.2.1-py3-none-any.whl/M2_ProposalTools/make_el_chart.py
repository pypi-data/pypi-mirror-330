import numpy as np
import astropy.coordinates as apc  # http://www.astropy.org/
from astropy import wcs
from astropy.io import fits
from astropy import units as u
from astropy.time import Time as APT
from astropy.visualization.wcsaxes import WCSAxes
from astropy.coordinates import Angle
#from wcsaxes import WCSAxes        # http://wcsaxes.rtfd.org/
import matplotlib.pyplot as plt
import matplotlib.dates
from matplotlib import colors
from matplotlib import colorbar as cb
import pytz, datetime, os, pdb
import shelve

tmlon = apc.Angle('3:23:55.51 degrees')    # Longitude
tmlat = apc.Angle('37:04:06.29 degrees')   # Latitude
tmalt = 2850.0 * u.m                       # Altitude (meters)
tmpre = 740.0  * u.Pa                      # Pressure (Pascals)
### Create a Earth-Location object:
thirtym = apc.EarthLocation.from_geodetic(tmlon,tmlat, tmalt)
############################################################
gblon = apc.Angle('-79:50:23.406 degrees')    # Longitude
gblat = apc.Angle('38:25:59.236 degrees')   # Latitude
gbalt = 840.0 * u.m                       # Altitude (meters)
gbpre = 780.0  * u.Pa                      # Pressure (Pascals)
### Create a Earth-Location object:
gbt   = apc.EarthLocation.from_geodetic(gblon,gblat, gbalt)

### Should deprecate this. Looks about ready for deprecation.
def_ra = apc.Angle('12h00m00.0s')
def_dec= apc.Angle('37d00m00s')   # Will need to incorporate elevation limits
defsky = apc.SkyCoord(def_ra, def_dec, equinox = 'J2000')

### Where to write files (by default)
cwd    = os.getcwd()  # Get current working directory

def get_dt(tz="Europe/Madrid"):
    local = pytz.timezone (tz)
    my_dt = datetime.datetime.now()
    #   test_dt = my_dt + datetime.timedelta(days=2)
    #   local_dt = local.localize(test_dt, is_dst=None)
    local_dt = local.localize(my_dt, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)

    return utc_dt

def astropyTime_from_datetime(dt):

    myAPT = APT(dt.strftime("%Y-%m-%d %H:%M:%S"))

    return myAPT

################################################################################
### Some simple PWV-to 

def t225_from_pwv(pwv):

    tau = pwv*0.058 + 0.004

    return tau

def pwv_from_t225(tau_225):

    pwv = (tau_225 - 0.004)/0.058

    return pwv

################################################################################
### Astrometry Routines

def get_parallactic_angle(ha, dec, lat=gblat):
    """
    Calculates the parallactic angle. Many astronomy books will provide info,
    or for info easily retrieved on the internet, look here:
    http://www.gb.nrao.edu/~rcreager/GBTMetrology/140ft/l0058/gbtmemo52/memo52.html

    ---------------
    INPUTS:
    ha:         Hour angle of the source (RA - LST)
    dec:        Declination of the source
    lat:        Latitude of the observing site

    """
    
    #pa = np.arctan(np.cos(lat)*np.sin(az), 
    #               np.sin(lat)*np.cos(el) - np.cos(lat)*np.sin(el)*np.cos(az))
    pa = np.arctan(np.sin(ha)/(np.cos(dec)*np.tan(lat)-np.sin(dec)*np.cos(ha)))

    # cos(z) = np.sin(tmlat)*np.sin(dec) + np.cos(tmlat)*np.cos(dec)*np.cos(ha)
    ### If we needed something beyond +/- pi/2:
    #pa = np.arctan2(np.sin(ha),np.cos(dec)*np.tan(lat)-np.sin(dec)*np.cos(ha))

    return pa

def find_transit(skyobj,myAPT,myloc,):

    mylon   = myloc.to_geodetic()[0]
    #import pdb;pdb.set_trace()
    try:
        mylst   = myAPT.sidereal_time('apparent',longitude=mylon)
    except:
        decyr   = myAPT.decimalyear
        DOY     = (decyr - np.floor(decyr))*365.25
        mylst   = Angle((DOY - 79.0)*4.0/(60.0), unit='hourangle')
        
    ha      = (skyobj.ra - mylst).to("hourangle").value * u.hour
    Transit = myAPT + ha

    return Transit

def find_times_above_el(skyobj,myAPT,myloc,elMin=40):

    Transit  = find_transit(skyobj,myAPT,myloc)
    npts     = 240
    dTransit = np.linspace(-12, 12, npts)*u.hour
    mytimes  = Transit + dTransit
    ### Can delete the line below, and move to the plotting routine.
    dt_arr   = mytimes.datetime    # Datetime array - for plotting...

    myframe  = apc.AltAz(obstime=mytimes, location=myloc)
    objaltazs = skyobj.transform_to(myframe)
    
    GoodEl = (objaltazs.alt.value > elMin)
    if any(GoodEl):
        elStart= np.min(mytimes[GoodEl])
        elStop = np.max(mytimes[GoodEl])
    else:
        elStart=0
        elStop =0

    return elStart, elStop, mytimes
 
def plot_altaz(ScanAz,ScanEl,TestRaDec,format='png',mydir=cwd):

    plt.figure()
    plt.plot(ScanAz.value,ScanEl.value,'.')
    filename = "AltAz_map_v2";fullbase = os.path.join(mydir,filename)
    fulleps = fullbase+'.eps'; fullpng = fullbase+'.png'
    if format == 'png':
        plt.savefig(fullpng,format='png')
    else:
        plt.savefig(fulleps,format='eps')
        
    plt.figure()
    plt.plot(TestRaDec.ra.value,TestRaDec.dec.value,'.')
    filename = "TestRaDec_map_v2";fullbase = os.path.join(mydir,filename)
    fulleps = fullbase+'.eps'; fullpng = fullbase+'.png'
    if format == 'png':
        plt.savefig(fullpng,format='png')
    else:
        plt.savefig(fulleps,format='eps')

def plot_visibility(date_obs,skyobj,Coverage=0,elMin=40,mylabel="Target",
                    dpi=200,filename = "Visibility_Chart",format='png',
                    myloc=gbt,mydir=cwd):

    mydate = astropyTime_from_datetime(date_obs)
    elStart, elStop, mytimes = find_times_above_el(skyobj,mydate,myloc,elMin=elMin)
    # mytimes is an array of +/- 12 hours from transit
    myframe  = apc.AltAz(obstime=mytimes, location=myloc)
    sunaltazs = apc.get_sun(mytimes).transform_to(myframe)
    #moonaltazs= apc.get_moon(mytimes).transform_to(myframe)
    objaltazs = skyobj.transform_to(myframe)

    sunbelowh = sunaltazs.alt.value < 0.0
    suntimes1 = mytimes[sunbelowh]
    sunset1   = np.min(suntimes1)
    sunrise1  = np.max(suntimes1)
    
    sunaboveh = sunaltazs.alt.value > 0.0
    suntimes2 = mytimes[sunaboveh]
    #sunset2   = np.min(suntimes2)
    #sunrise2  = np.max(suntimes2)
    sunset2   = np.max(suntimes2)
    sunrise2  = np.min(suntimes2)
    
    sunset=sunset1; sunrise=sunrise1
    if (sunrise1-sunset1).value >= 0.8:
        sunset=sunset2; sunrise=sunrise2

    obsstart  = sunset + 3.0*u.hr
    obsend    = sunrise+ 0.5*u.hr
    if obsstart > np.max(mytimes):
        obsstart -= 1.0*u.day
    if obsend > np.max(mytimes):
        obsend -= 1.0*u.day

    goodstart = (mytimes > obsstart)
    goodend   = (mytimes < obsend)
    
    if obsend > obsstart:
        sundown = np.array([all([a,b]) for a,b in zip(goodstart,goodend)])
    else:
        sundown = np.array([any([a,b]) for a,b in zip(goodstart,goodend)])
                                    
    #goodtimes = sundown*goodalt

    #import pdb;pdb.set_trace()
    
    #############################

    bt30 = 0; bt40 = 0; bt50 = 0; bteM = 0
    goodbteM   = (objaltazs.alt.value > elMin)
    good30   = (objaltazs.alt.value > 30.0)
    good40   = (objaltazs.alt.value > 40.0)
    good50   = (objaltazs.alt.value > 50.0)
    if any(good30):
        good30t = good30*sundown
        bt30 = 24.0*np.sum(good30t)/len(mytimes)
        #bt30 = (np.max(mytimes[(objaltazs.alt.value > 30.0)]) - \
        #        np.min(mytimes[(objaltazs.alt.value > 30.0)])).to("hour").value
    if any(good40):
        goodtimes = good40*sundown
        bt40 = 24.0*np.sum(goodtimes)/len(mytimes)
        #bt40 = (np.max(mytimes[(objaltazs.alt.value > 40.0)]) - \
        #   np.min(mytimes[(objaltazs.alt.value > 40.0)])).to("hour").value
    if any(good50):
        goodtimes = good50*sundown
        bt50 = 24.0*np.sum(goodtimes)/len(mytimes)
        #print(np.sum(good50))
        #import pdb;pdb.set_trace()
        #bt50 = (np.max(mytimes[(objaltazs.alt.value > 50.0)]) - \
        #        np.min(mytimes[(objaltazs.alt.value > 50.0)])).to("hour").value
    if any(goodbteM):
        goodtimes = goodbteM*sundown
        bteM = 24.0*np.sum(goodtimes)/len(mytimes)
        #bteM = (np.max(mytimes[(objaltazs.alt.value > elMin)]) - \
        #        np.min(mytimes[(objaltazs.alt.value > elMin)])).to("hour").value

    if bteM == 0:
        print("On ",mydate.strftime('%Y-%m-%d'),' your source never rises above the minimum source elevation you requested.')
        #print('Your source never rises above the minimum source elevation you requested.')
        #print('Therefore, this code will not have run successfully.')
        #print('Change the minimum elevation, or change the source.')

        
    plt.figure(1,dpi=dpi,figsize=(8,8));    plt.clf();    fig1,ax1 = plt.subplots()

    date_arr = mytimes.datetime       # Convert to datetime array, for plotting
    
    ax1.fill_between(date_arr, 0, 90,
                     sunaltazs.alt < -0*u.deg, color='0.5', zorder=0)
    ax1.fill_between(date_arr, 0, 90,
                     sunaltazs.alt < -18*u.deg,color='k', zorder=0)
    ax1.plot_date(date_arr, sunaltazs.alt.value, '-',color='y',lw=3, label='Sun')
#    ax1.plot_date(date_arr, moonaltazs.alt.value,'-',color='b',lw=3, label='Moon')
    ax1.plot_date(date_arr, objaltazs.alt.value, '-',color='b',lw=5, label=mylabel)
    #ax1.plot_date(date_arr[good30t], (objaltazs.alt.value)[good30t], '-',color='g',lw=3, label=mylabel)
    #import pdb;pdb.set_trace()
    myxlim = ax1.get_xlim(); ax1.set_xlim(myxlim)
    ax1.plot(myxlim,[30,30],'--',color ='0.75',label="{:.1f}".format(bt30)+" hrs")
    ax1.plot(myxlim,[40,40],'--',color ='0.5' ,label="{:.1f}".format(bt40)+" hrs")
    ax1.plot(myxlim,[50,50],'--',color ='0.25',label="{:.1f}".format(bt50)+" hrs")
    myStart = elStart.datetime; myStop = elStop.datetime
    
    myylim = ax1.get_ylim(); ax1.set_ylim(myylim)
    ax1.plot(myxlim,[elMin,elMin],'--',color ='c',
             label="{:.1f}".format(bteM)+" hrs above "+str(int(elMin)))
    ax1.plot_date([myStart,myStart],[0,90],'--',color='b')
    ax1.plot_date([myStop,myStop],[0,90],'--',color='b')
    ax1.plot_date([obsstart.datetime,obsstart.datetime],[0,90],'--',color='g')
    ax1.plot_date([obsend.datetime,obsend.datetime],[0,90],'--',color='r')

    
    gi = np.array([])
    #if isinstance(Coverage,CovMap):
    #    for start,stop in zip(Coverage.scanstart,Coverage.scanstop):
    #        mgi = np.where(((mytimes > start) & (mytimes < stop)) == True)
    #        gi = np.append(gi,mgi)
    #
    #    gi = int_arr(gi)
    #    ax1.plot_date(date_arr[gi], objaltazs.alt.value[gi],color='orange',ms=2,
    #                  label="Obs. ("+"{:.1f}".format(Coverage.tint.to('hour').value)+' hrs)')

        
#    plt.colorbar().set_label('Azimuth [deg]')
    plt.legend(loc='upper left')
    plt.title("Visibility of "+mylabel)
    plt.ylim(0, 90)
    plt.xlabel('UTC (MM-DD HH)')
    plt.ylabel('Altitude [deg]')  
    plt.gcf().autofmt_xdate()  # Hopefully make the x-axis (dates) look better
    fullbase = os.path.join(mydir,filename)
    fulleps = fullbase+'.eps'; fullpng = fullbase+'.png'
    if format == 'png':
        plt.savefig(fullpng,format='png')
    else:
        plt.savefig(fulleps,format='eps')






##################################################################################################
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
##################################################################################################
##################################################################################################
##################################################################################################
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
##################################################################################################
##################################################################################################
##################################################################################################
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
##################################################################################################
##################################################################################################
##################################################################################################
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
##################################################################################################
##################################################################################################
##################################################################################################
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
##################################################################################################
##################################################################################################
##################################################################################################
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +#
#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + #
##################################################################################################
##################################################################################################
##################################################################################################




        
def plot_contours(elMin=30,mylabel="Target",
                  dpi=200,filename = "Contour_Chart",format='png',
                  myloc=gbt,mydir=cwd):

    npydir     = "/home/charles/Python/SimulatedObs/"
    npysave    = npydir+"Above30DegreeArray.npy"
    #ras       = np.array([340.7])
    #decs      = np.array([53.01666667])
    ras       = np.arange(0.0,360.0,5.0)
    decs      = np.arange(-30.0,90.0,5.0)
    #ras       = np.arange(0.0,360.0,30.0)
    #decs      = np.arange(-30.0,90.0,20.0)
    ra2d      = np.outer(ras,np.ones(len(decs)))
    hr2d      = ra2d/15.0
    dec2d     = np.outer(np.ones(len(ras)),decs)
    #date_obs  = datetime.strptime('01-10-2018 15:24:08', '%d-%m-%Y %H:%M:%S')
    #months    = np.array([1,3,5,7,9,11])
    months    = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
    mname     = ["January","February","March","April","May","June","July","August","September","October",
                 "November","December"]
    year      = 2023
    day       = 1

    #bt20s     = np.zeros((len(ras),len(decs),len(months)))
    bt30s     = np.zeros((len(ras),len(decs),len(months)))
    bt40s     = np.zeros((len(ras),len(decs),len(months)))
    bt50s     = np.zeros((len(ras),len(decs),len(months)))
    mycolors  = ['r','b','g',"lightcoral","cornflowerblue","chartreuse","maroon","navy","darkgreen",
                 "fuchsia","orange","violet"]

    npyexists = os.path.exists(npysave)
    if npyexists:
        bt30s = np.load(npysave)
    
    for k,mymonth in enumerate(months):
        date_obs = datetime.datetime(year,mymonth,day)
        print(">>>>>>>>>>>>>>> ",mymonth)
        if not npyexists:
            for i,myra in enumerate(ras):
                print(i)
                obj_ra = apc.Angle(myra,unit='deg')
                for j,mydec in enumerate(decs):
                    obj_dec = apc.Angle(mydec,unit='deg')

                    skyobj = apc.SkyCoord(obj_ra, obj_dec, equinox = 'J2000')

                    mydate = astropyTime_from_datetime(date_obs)
                    elStart, elStop, mytimes = find_times_above_el(skyobj,mydate,myloc,elMin=elMin)
    
                    myframe  = apc.AltAz(obstime=mytimes, location=myloc)
                    sunaltazs = apc.get_sun(mytimes).transform_to(myframe)
                    objaltazs = skyobj.transform_to(myframe)

                    sunbelowh = sunaltazs.alt.value < 0.0
                    suntimes1 = mytimes[sunbelowh]
                    sunset1   = np.min(suntimes1)
                    sunrise1  = np.max(suntimes1)
                
                    sunaboveh = sunaltazs.alt.value > 0.0
                    suntimes2 = mytimes[sunaboveh]
                    #sunset2   = np.min(suntimes2)
                    #sunrise2  = np.max(suntimes2)
                    sunset2   = np.max(suntimes2)
                    sunrise2  = np.min(suntimes2)
                    
                    sunset=sunset1; sunrise=sunrise1
                    if (sunrise1-sunset1).value >= 0.8:
                        sunset=sunset2; sunrise=sunrise2
                    
                    obsstart  = sunset + 3.0*u.hr
                    obsend    = sunrise+ 0.5*u.hr
                    if obsstart > np.max(mytimes):
                        obsstart -= 1.0*u.day
                    if obsend > np.max(mytimes):
                        obsend -= 1.0*u.day

                    goodstart = (mytimes > obsstart)
                    goodend   = (mytimes < obsend)

                    if obsend > obsstart:
                        sundown = np.array([all([a,b]) for a,b in zip(goodstart,goodend)])
                    else:
                        sundown = np.array([any([a,b]) for a,b in zip(goodstart,goodend)])
                    
                    bt30 = 0; bt40 = 0; bt50 = 0; bteM = 0
                
                    goodalt   = (objaltazs.alt.value > 30.0)
                    goodtimes = sundown*goodalt
                    #goodtimes = np.array([all([a,b]) for a, b in zip(sundown,goodalt)])
                    if any(goodtimes):
                        bt30 = 24.0*np.sum(goodtimes)/len(mytimes)
                        #bt30 = (np.max(mytimes[goodtimes])-np.min(mytimes[goodtimes])).to("hour").value

                    goodalt   = (objaltazs.alt.value > 40.0)
                    goodtimes = np.array([all([a,b,c]) for a, b, c, in zip(goodstart,goodend,goodalt)])
                    if any(goodtimes):
                        bt40 = (np.max(mytimes[goodtimes])-np.min(mytimes[goodtimes])).to("hour").value

                    goodalt   = (objaltazs.alt.value > 50.0)
                    goodtimes = np.array([all([a,b,c]) for a, b, c, in zip(goodstart,goodend,goodalt)])
                    if any(goodtimes):
                        bt50 = (np.max(mytimes[goodtimes])-np.min(mytimes[goodtimes])).to("hour").value

                    #if any(objaltazs.alt.value > bteM):
                    #    bteM = (np.max(mytimes[(objaltazs.alt.value > elMin)]) - \
                        #            np.min(mytimes[(objaltazs.alt.value > elMin)])).to("hour").value
                    
                    bt30s[i,j,k] = bt30
                    bt40s[i,j,k] = bt40
                    bt50s[i,j,k] = bt50

        myfs=10
        #import pdb;pdb.set_trace()
        #plt.contour(ras, decs, bt30s[:,:,k], levels=[3,4,5,6,7,8],colors=mycolors[k])
        plt.figure(2,dpi=dpi,figsize=(16,16));    plt.clf();    fig1,ax1 = plt.subplots()
        CS = ax1.contour(hr2d, dec2d, bt30s[:,:,k], levels=[3,4,5,6,7,8],colors="red")
        ax1.clabel(CS, inline=True, fontsize=myfs)
        ax1.set_title('MUSTANG2 Observing Time; '+mname[mymonth-1], fontsize=myfs)
        #ax1.set_xlabel('Right Ascension (degrees)', fontsize=myfs)
        ax1.set_xlabel('Right Ascension (hours)', fontsize=myfs)
        ax1.set_ylabel('Declination (degrees)', fontsize=myfs)
        monstr   = "{:02d}".format(mymonth)
        fullbase = os.path.join(mydir,filename)+"_"+monstr
        fulleps = fullbase+'.eps'; fullpng = fullbase+'.png'
        if format == 'png':
            fig1.savefig(fullpng,format='png')
        else:
            fig1.savefig(fulleps,format='eps')

       #plt.clabel(CS, fontsize=9, inline=1)

    np.save(npysave,bt30s)
    #plt.title('MUSTANG2 Observing Time')
    #plt.xlabel('Right Ascension (degrees)')
    #plt.ylabel('Declination (degrees)')
    #fullbase = os.path.join(mydir,filename)
    #fulleps = fullbase+'.eps'; fullpng = fullbase+'.png'
    #if format == 'png':
    #    plt.savefig(fullpng,format='png')
    #else:
    #    plt.savefig(fulleps,format='eps')

def mybinning(array):

    la     = len(array)
    nXh    = la//24
    binned = np.zeros((24))  
    for i in range(24):
        binned[i] = np.mean(array[i*nXh:i*nXh+nXh])

    return binned
    
def HoursPerLST(Guess=True):

    npydir     = "/home/charles/Python/SimulatedObs/"
    npysave    = npydir+"Above30DegreeArray.npy"
    bt30s      = np.load(npysave)
    b3s        = bt30s.shape

    hrsperlst  = np.zeros((24,3))

    print(b3s[1],b3s[1]/1.5)
    for j in range(b3s[2]):
        jm = j-1
        gfrac  = 0.25+0.25*np.cos((j-0.5)*np.pi/6) if Guess else 1.0
        myhrs  = mybinning(bt30s[:,b3s[1]//2,jm])*gfrac
        myhrs2 = mybinning(bt30s[:,int(b3s[1]/1.5),jm])*gfrac
        myhrs3 = mybinning(bt30s[:,int(b3s[1]/1.2),jm])*gfrac
        hrsperlst[:,2] += myhrs+myhrs2+myhrs3
        if jm < 6:
            hrsperlst[:,0] += myhrs+myhrs2+myhrs3
        else:
            hrsperlst[:,1] += myhrs+myhrs2+myhrs3
        
        
    myfig = plt.figure(1,figsize=(5,4),dpi=200)
    myfig.clf()
    ax = myfig.add_subplot(111)

    hrs = np.arange(24)
    ax.plot(hrs,hrsperlst[:,0],label="A")
    ax.plot(hrs,hrsperlst[:,1],label="B")
    ax.plot(hrs,hrsperlst[:,2],label="Both")

    ax.set_xlabel("LST hour")
    ax.set_ylabel("Proxy for available hours")

    ax.legend()
    ax.grid()

    figtag = "_wQualityGuess" if Guess else "_JustNighttime"
    myfig.savefig("AvailableHoursPerLST"+figtag+".png")

