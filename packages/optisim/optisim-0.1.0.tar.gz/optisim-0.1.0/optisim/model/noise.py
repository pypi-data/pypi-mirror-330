
import math
import numpy as np
from colorama import Fore, Style

from ..constants import *
from ..config import config


def calc_background_noise_perpx_persec(payload, brightness_mag):
    '''Compute background noise per pixel per second'''
    qE_noise = config.get("qe_noise")
    
    pixel_fov_arcsec2 = (math.degrees(payload.pixel_pitch)*3600)**2
    
    aperture_m2 = math.pi/4*math.pow((payload.aperture_mm/1000),2)*payload.ap_eff
    lamda = L_MEAN
    h = H
    c = C
    
    brightness_Wperm2 = 1366/math.pow(10,(brightness_mag+26.74)/2.5)
    N_bgn_perpxsec = qE_noise*brightness_Wperm2*aperture_m2*pixel_fov_arcsec2*lamda/((h*c))
    return N_bgn_perpxsec

def calc_bgn_noise(payload, brightness_mag, exposure_time):
    '''Compute background noise per pixel'''

    N_bgn_perpxsec = calc_background_noise_perpx_persec(payload, brightness_mag)
    
    if N_bgn_perpxsec > 500:
        print(Fore.YELLOW + 'Warning: Background Noise seems to be very high. Check Input!' + Style.RESET_ALL)
        
    N_bgn = np.multiply(N_bgn_perpxsec,exposure_time)
    return N_bgn


def calc_noise_consts(noise_info, inte_time):
    '''Compute noise constants for a given exposure time'''
    # Compute all Noise parameters
    N_bgn = noise_info[2]
    N_read = np.power(noise_info[0],2)
    N_dark = np.multiply(noise_info[1], inte_time)
    N_fpn  = np.power(noise_info[3],2)
    N_row_tempo_noise = np.power(noise_info[4],2)
    noise_const = (N_bgn + N_read + N_dark + N_fpn + N_row_tempo_noise).astype(float)
    noise_signal_dep = (1.0 + noise_info[5])
    
    return noise_const, noise_signal_dep


def calc_noise(noise_info, signal, signal_mid, fps):
    '''Calculate Noise for a given signal'''
    N_read = np.power(noise_info[0],2)
    N_dark = noise_info[1]/fps
    N_bgn  = noise_info[2]
    N_fpn  = np.power(noise_info[3],2)
    N_row_tempo_noise = np.power(noise_info[4],2)
    N_prnu = noise_info[5]*signal

    N_shot = signal
    N_fluct = N_fpn + N_prnu + N_row_tempo_noise
    noise_tot = (N_bgn + N_read + N_dark + N_shot + N_fluct).astype(float)
    noise_tot = np.sqrt(noise_tot)
    
    N_fluct_mid = N_fpn + noise_info[5]*signal_mid + N_row_tempo_noise
    noise_tot_mid = (N_bgn + N_read + N_dark + signal_mid + N_fluct_mid).astype(float)
    noise_tot_mid = np.sqrt(noise_tot_mid)
    
    return noise_tot, noise_tot_mid