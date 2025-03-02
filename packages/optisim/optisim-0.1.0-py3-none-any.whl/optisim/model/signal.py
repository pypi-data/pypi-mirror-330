import math
import numpy as np
from colorama import Fore, Style

from ..constants import *
from .eff_sensor import calc_eff_QE


def QE_sunlight(quant_eff, lamda):
    '''Compute photons transmitted from sun reaching earth and then QE corrected photons'''
    h = H*1e34                   # h in units of 1e-34
    c = C*1e-8                   # in units of 1e8
    Boltz_K = K*1e23             # Boltzman constant in units of 10^-23

    Temp = SUN_TEMPERATURE*1e-3                # Temperature of sun in units of Kilo-Kelvin
    
    spect_den = np.exp(np.divide(h*c, np.multiply(lamda,Boltz_K*Temp))) -1
    pre_fac = np.divide((h*(pow(c,2))),np.power(lamda, 5))                      # this pre_fac is in the units of 1e12
    rad_inte = np.divide(2*math.pi*pre_fac, spect_den)          # Radiation intensity in units of 1e12
    
    
    inte_at_sun = np.trapz(np.multiply(quant_eff,rad_inte),x=lamda)      # Total intensity of sun: 1e6 watt/square.m
    no_photons_at_sun_qe_correc = np.trapz(np.divide(np.multiply(np.multiply(quant_eff, rad_inte), lamda), h*c), x=lamda) # total no. of photons per unit time per unit area; in 1e26 (1/square.m-sec) 
    no_photons_at_sun = np.trapz(np.divide(np.multiply(rad_inte, lamda), h*c), x=lamda) # total no. of photons per unit time per unit area (not QE Corrected); in 1e26 (1/square.m-sec) 
    return inte_at_sun, no_photons_at_sun, no_photons_at_sun_qe_correc

def sun2obj_photons(no_photons_at_sun, R_S, R_SO):
    '''Calculate sun transmitted photons at object from sun transmitted photons at earth'''
    return no_photons_at_sun*(np.power(np.divide(R_S, R_SO),2))

def sun2spot_electrons(sun_electrons_at_earth, aperture_mm, ap_eff):
    '''Calculate electrons (on detector) per spot per sec for sun transmitted photons'''
    sun_electrons_perspot_persec = sun_electrons_at_earth*(math.pi*((aperture_mm)/2000)**2*ap_eff)
    return sun_electrons_perspot_persec

def calc_photons(payload, signal):
    ''' Calculate Photons from signal (i.e. electrons)'''

    eff_QE, lamda_res = calc_eff_QE(payload)
    inte_at_sun, no_photons_at_sun, no_electrons_at_sun = QE_sunlight(eff_QE, lamda_res)
    photons = signal*no_photons_at_sun/no_electrons_at_sun
    
    return photons, no_photons_at_sun*(10**26), no_electrons_at_sun*(10**26)

def calc_total_signal_SNR(SNR_threshold, noise_signal_dep, noise_const):
    '''Calculate total signal required to achieve SNR threshold'''
    a = 1
    b = -noise_signal_dep*SNR_threshold**2
    c = -noise_const*SNR_threshold**2
    det = b**2 - 4*a*c
    if isinstance(det, np.ndarray):
        signal = np.zeros(len(det))
        for i in range(len(det)):
            if det[i] < 0:
                print(Fore.YELLOW + "Warning: SNR Threshold is too high!" + Style.RESET_ALL)
            else:
                signal[i] = (-b + np.sqrt(det[i]))/(2*a)
    else:
        if det < 0:
            print(Fore.YELLOW + "Warning: SNR Threshold is too high!" + Style.RESET_ALL)
        else:
            signal = (-b + np.sqrt(det))/(2*a)
    return signal