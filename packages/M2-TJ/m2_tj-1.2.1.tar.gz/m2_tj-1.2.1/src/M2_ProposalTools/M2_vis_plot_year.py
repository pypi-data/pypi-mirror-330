import make_el_chart as mec
import astropy.coordinates as apc
import numpy as np
from astropy import units as u
from datetime import datetime
import os
from astropy.time import Time

from importlib import reload
mec=reload(mec)
### Just some testing lines:
times = ['1999-01-01T00:00:00.123456789', '2010-01-01T00:00:00']
t = Time(times, format='isot', scale='utc')
t.sidereal_time('apparent', 'greenwich')

#########################################################################
### Define the coordinates and name of your object:
#obj_ra = apc.Angle('2h00m00s')
#obj_dec= apc.Angle('-3d00m00s')
### GEMS
#obj_ra = apc.Angle('3h30m00s')
#obj_dec= apc.Angle('-27d49m00s')
#skyobj = apc.SkyCoord(obj_ra, obj_dec, equinox = 'J2000')
#target='GEMS'

#obj_ra = apc.Angle('2h42m46s')
#obj_dec= apc.Angle('-21d32m00s')
#skyobj = apc.SkyCoord(obj_ra, obj_dec, equinox = 'J2000')
#target='PKS0240-217'

#obj_ra = apc.Angle('3h18m00s')
#obj_dec= apc.Angle('41d30m00s')
#skyobj = apc.SkyCoord(obj_ra, obj_dec, equinox = 'J2000')
#target='Perseus'

#obj_ra = apc.Angle('22h42m48s')
#obj_dec= apc.Angle('53d01m00s')
#skyobj = apc.SkyCoord(obj_ra, obj_dec, equinox = 'J2000')
#target='Sausage'

#obj_ra = apc.Angle('02h17m00s')
#obj_dec= apc.Angle('70d30m00s')
#skyobj = apc.SkyCoord(obj_ra, obj_dec, equinox = 'J2000')
#target='CL0217'




#date_obs  = [datetime.strptime('15-01-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-02-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-03-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-04-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-05-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-06-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-07-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-08-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-09-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-10-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-11-2025 23:00:00', '%d-%m-%Y %H:%M:%S'),
#             datetime.strptime('15-12-2025 23:00:00', '%d-%m-%Y %H:%M:%S')]


current_year = datetime.now().year
date_obs  = [datetime.strptime('15-{:02d}-{:d} 23:00:00'.format(mm,current_year), '%d-%m-%Y %H:%M:%S') for mm in np.arange(12,dtype=int)+1]

def get_year_visibilities(elMin=23.0):
    
    obj_ra = apc.Angle('09h30m15.6s')
    obj_dec= apc.Angle('06d15m33.2s')
    skyobj = apc.SkyCoord(obj_ra, obj_dec, equinox = 'J2000')
    target='ACT0930_0615'

    elStr = str(int(elMin))
    mydir = os.getcwd()    # If you want to specify a directory, do so here.

    for i,my_obs_date in enumerate(date_obs):

        monstr = "{:02d}".format(i+1)
        Tag    = "_"+monstr+"Visibility_above"
        mec.plot_visibility(my_obs_date,skyobj,elMin=elMin,mylabel=target,
                            filename = target+Tag+elStr,mydir=mydir)

#mec.plot_contours(elMin=25.0,mylabel="General",filename = "GeneralContourPlot")
