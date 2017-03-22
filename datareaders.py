#need to return the following data with the corresponding units:
#time [s]
#shock radius [km]
#mass accretion rate [Msun/s; >0]
#Luminosity, lab frame, 500km, nue [10^{51} erg/s]
#Luminosity, lab frame, 500km, anti_nue [10^{51} erg/s]
#Luminosity, lab frame, 500km, nux = 1/4 {numu,antinumu,nutau,anti-nutau} [10^{51} erg/s]
#average energy, lab frame, 500km, nue [10^{51} erg/s]
#average energy, lab frame, 500km, anti_nue [10^{51} erg/s]
#average energy, lab frame, 500km, nux = 1/4 {numu,antinumu,nutau,anti-nutau} [10^{51} erg/s]
import numpy as np
from smooth import smooth


def get_GR1DData(directoryname):
    file = directoryname+"/bounce.dat"
    tbounce = np.loadtxt(file)
    file = directoryname+"/GR1Dshock_full.dat"
    time, rsh  = np.loadtxt(file,usecols=(0,2), unpack=True)
    rsh = rsh/1e5
    file = directoryname+"/GR1Daccretion.dat"
    time, massaccret  = np.loadtxt(file,usecols=(0,11), unpack=True)
    file = directoryname+"/GR1D_lums.dat"
    time, lnue, lanue, lnux = np.loadtxt(file,usecols=(0,1,2,3), unpack=True)
    lnue = lnue/1.0e51
    lanue = lanue/1.0e51
    lnux = lnux/4.0e51
    file = directoryname+"/GR1D_aveen.dat"
    time, enue, eanue, enux = np.loadtxt(file,usecols=(0,1,2,3), unpack=True)
    time = time - tbounce
    win = 5
    time = smooth(time,window_len=win,window="flat")
    rsh = smooth(rsh,window_len=win,window="flat")
    massaccret = smooth(massaccret,window_len=win,window="flat")
    lnue = smooth(lnue,window_len=win,window="flat")
    lanue = smooth(lanue,window_len=win,window="flat")
    lnux = smooth(lnux,window_len=win,window="flat")
    enue = smooth(enue,window_len=win,window="flat")
    eanue = smooth(eanue,window_len=win,window="flat")
    enux = smooth(enux,window_len=win,window="flat")

    for i in range(len(time)):
        if time[i] < -0.001:
            enux[i] = 0.0
            eanue[i] = 0.0
    
    return time,rsh,massaccret,lnue,lanue,lnux,enue,eanue,enux


def get_FLASHData():
    file = "./FLASHdata/s20WH07_SFHo_small.dat"
    time, rsh, massaccret, lnue, lanue, lnux, enue, eanue, enux = np.loadtxt(file,usecols=(0,11,13,33,34,35,36,37,38), unpack=True)
    rsh = rsh/1e5
    massaccret = massaccret/1.9889e33
    lnux = lnux/4.0
    return time,rsh,massaccret,lnue,lanue,lnux,enue,eanue,enux

def get_FLASHIDSAData(type=0):
    tshift = 14.83*1e-3 # [sec]
    file = "./FLASHIDSAdata/s20WH07_GREP_SFHo_IDSA_fluid_iter_170316_small.d"
    mev_to_erg = 1.60217733e-6
    db = np.loadtxt(file,unpack=True)
    time = db[0]+tshift         # [sec]
    rsh  = db[11]/1.e5   # [km]
    massaccret = db[14]  # [msun/sec]
    massaccret = massaccret/1.9889e33
    lnue  = db[33]/1e51  # [B/s]
    lanue = db[34]/1e51  # [B/s]
    lnux  = db[35]/1e51  # [B/s]
    enue  = db[33]/db[36]/mev_to_erg #[MeV]
    eanue = db[34]/db[37]/mev_to_erg #[MeV]
    enux  = db[38]/mev_to_erg  # = 0 
    return time,rsh,massaccret,lnue,lanue,lnux,enue,eanue,enux

