import math
from scipy.integrate import quad
from scipy.interpolate import interp1d
import numpy as np

from ..constants import *
from ..config import config

def integrand(t, mx, x1, x2, sigma):
    k1 = 1/( math.exp( -358*(x1-mx*t)/(23*sigma) + 111*math.atan( 37*(x1-mx*t)/(294*sigma) ) ) + 1)
    k2 = 1/( math.exp( -358*(x2-mx*t)/(23*sigma) + 111*math.atan( 37*(x2-mx*t)/(294*sigma) ) ) + 1)
    k = k2 - k1
    
    l1 = 1/( math.exp( -358*(-0.5-0)/(23*sigma) + 111*math.atan( 37*(-0.5-0)/(294*sigma) ) ) + 1)
    l2 = 1/( math.exp( -358*(0.5-0)/(23*sigma) + 111*math.atan( 37*(0.5-0)/(294*sigma) ) ) + 1)
    l = l2 - l1
    return k*l

def integrand2(sigma, x1, x2, cx):
    hx1 = 1/(np.exp(-358*(x1-cx)/(23*sigma) +111*np.arctan(37*(x1-cx)/(294*sigma))) + 1)
    hx2 = 1/(np.exp(-358*(x2-cx)/(23*sigma) +111*np.arctan(37*(x2-cx)/(294*sigma))) + 1)
    hy1 = 1/(np.exp(-358*(-0.5-0)/(23*sigma) +111*np.arctan(37*(-0.5-0)/(294*sigma))) + 1)
    hy2 = 1/(np.exp(-358*(0.5-0)/(23*sigma) +111*np.arctan(37*(0.5-0)/(294*sigma))) + 1)
    
    hx = hx2-hx1
    hy = hy2-hy1
    return hx*hy

def integrand_psf(t, psf_norm, mx, x1, x2):
    # Directly calculate the integral by using the normalized PSF
    # Precompute limits
    lower_limit = x1 - mx * t
    upper_limit = x2 - mx * t

    # Return the value of the integral in one step
    return np.trapz(psf_norm(np.linspace(lower_limit, upper_limit, 1000)), dx=(upper_limit - lower_limit) / 1000)



def calc_moving_spot_correction(payload, std_dev, spot_frac, ang_vels, exp_time):
    '''Calculate Signal for Moving Spot'''
    signal_persec = []
    mx = ang_vels / payload.pixel_pitch

    def calculate_half_time(mx, exp_time, spot_frac):
        if mx == 0:
            return exp_time / 2
        return min(spot_frac / (2 * mx) + 0.5 / mx, exp_time / 2)

    # Case 1: Both inte_time and ang_vels are scalars
    if isinstance(exp_time, float) and isinstance(ang_vels, float):
        half_time = calculate_half_time(mx, exp_time, spot_frac)
        I = quad(integrand, -half_time, half_time, args=(mx, -0.5, 0.5, std_dev))
        signal_persec = np.array(np.divide(1, I[0]))

    # Case 2: inte_time is scalar, ang_vels is array
    elif isinstance(exp_time, float) and isinstance(ang_vels, (list, np.ndarray)):
        for ang_vel in ang_vels:
            mx = ang_vel / payload.pixel_pitch
            half_time = calculate_half_time(mx, exp_time, spot_frac)
            I = quad(integrand, -half_time, half_time, args=(mx, -0.5, 0.5, std_dev))
            signal_persec.append(1 / I[0])

    # Case 3: inte_time is array, ang_vels is scalar
    elif isinstance(exp_time, (list, np.ndarray)) and isinstance(ang_vels, float):
        for exp in exp_time:
            half_time = calculate_half_time(mx, exp, spot_frac)
            I = quad(integrand, -half_time, half_time, args=(mx, -0.5, 0.5, std_dev))
            signal_persec.append(1 / I[0])

    # Case 4: inte_time and ang_vels are both arrays
    else:
        rows, columns = len(exp_time), len(ang_vels)
        signal_persec = np.zeros((rows, columns))
        for i in range(rows):
            exp = exp_time[i]
            for j in range(columns):
                mx = ang_vels[j] / payload.pixel_pitch
                half_time = calculate_half_time(mx, exp_time[i], spot_frac)
                I = quad(integrand, -half_time, half_time, args=(mx, -0.5, 0.5, std_dev))
                signal_persec[i][j] = 1 / I[0]

    return signal_persec

def calc_moving_psf_correction(payload, angle, ang_vels, exp_time):
    '''Calculate Signal for Moving PSF'''
    signal_persec = []
    x = np.linspace(payload.psf_min_px, payload.psf_max_px, 1000)
    y = payload.f_psf(np.array([[angle]*len(x), x]).T)
    psf_norm = interp1d(x, y, kind='linear', fill_value="extrapolate")
    y_int = np.trapz(psf_norm( np.linspace(-0.5, 0.5, 1000)), dx=(0.5 + 0.5) / 1000)
    
    mx = ang_vels / payload.pixel_pitch
    # Calculate mx and halftime
    def calc_halftime(mx, exp_time, min_px, max_px):
        halftime = (max_px - min_px) / (2 * mx) + 0.5 / mx if mx != 0 else exp_time / 2
        halftime = min(exp_time / 2, halftime)
        return halftime
        
    def calcI(psf_norm, mx, halftime):
        integrand_vectorized = np.vectorize(lambda t: integrand_psf(t, psf_norm, mx, -0.5, 0.5))
        t_vals = np.linspace(-halftime, halftime, 1000)  # Generate values for t
        I_vals = integrand_vectorized(t_vals)
        I = np.trapz(I_vals, t_vals)  # Integrate over t using np.trapz
        I = y_int * I
        return I

    # Case 1: Both inte_time and ang_vels are scalars
    if isinstance(exp_time, float) and isinstance(ang_vels, float):
        halftime = calc_halftime(mx, exp_time, payload.psf_min_px, payload.psf_max_px)
        I = calcI(psf_norm, mx, halftime)
        signal_persec = np.array(np.divide(1, I))
        
    # Case 2: inte_time is scalar, ang_vels is array
    elif isinstance(exp_time, float) and isinstance(ang_vels, (list, np.ndarray)):
        for ang_vel in ang_vels:
            mx = ang_vel / payload.pixel_pitch
            halftime = calc_halftime(mx, exp_time, payload.psf_min_px, payload.psf_max_px)
            I = calcI(psf_norm, mx, halftime)
            signal_persec.append(1 / I)
            
    # Case 3: inte_time is array, ang_vels is scalar
    elif isinstance(exp_time, (list, np.ndarray)) and isinstance(ang_vels, float):
        for exp in exp_time:
            halftime = calc_halftime(mx, exp, payload.psf_min_px, payload.psf_max_px)
            I = calcI(psf_norm, mx, halftime)
            signal_persec.append(1 / I)
            
    # Case 4: inte_time and ang_vels are both arrays
    else:
        rows, columns = len(exp_time), len(ang_vels)
        signal_persec = np.zeros((rows, columns))
        for i in range(rows):
            exp = exp_time[i]
            for j in range(columns):
                mx = ang_vels[j] / payload.pixel_pitch
                halftime = calc_halftime(mx, exp, payload.psf_min_px, payload.psf_max_px)
                I = calcI(psf_norm, mx, halftime)
                signal_persec[i][j] = 1 / I
        
    return signal_persec

def calc_spot_size(sensor_loc, ang_acc, f_no, abb_lim_spot_size, pixel_size):
    '''Calculate Spot Size'''
    diff_lim_spot_size = 2.44*0.65*f_no
    abb_lim_spot_size = np.array(abb_lim_spot_size)

    spot_size = np.sqrt(diff_lim_spot_size**2 + np.power(abb_lim_spot_size, 2)) #Root sum of squares with diffraction & aberrations
    seeing_fwhm_arcsec = config.get("seeing_fwhm_arcsec")
    seeing_fwhm = seeing_fwhm_arcsec*0.000277778   # degrees 1arcsec
    
    if sensor_loc == 'ground':
        spot_fov = np.sqrt((spot_size/pixel_size*ang_acc)**2 + (np.radians(seeing_fwhm*2))**2) # Root sum of squares with seeing, seeing input is fwhm hence *2 for spot
        spot_size = spot_fov/ang_acc*pixel_size
    else:
        spot_fov = spot_size/pixel_size*ang_acc
    return spot_size, spot_fov

def calc_std_dev(spot_size, pixel_size):
    '''Calculate Standard Deviation'''
    spot_frac = spot_size/pixel_size
    std_dev = spot_frac/5
    return std_dev, spot_frac
    
    
    