import os
import json
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator

from .constants import *
from .config import config
from .model.functions import calc_fov
from .model.eff_sensor import calc_effective_sensor
from .model.spot import calc_spot_size, calc_std_dev

from .model.noise import calc_noise_consts, calc_bgn_noise
from .model.signal import calc_total_signal_SNR, calc_photons, sun2obj_photons, sun2spot_electrons

def _calc_lim_mag_stars(PL):
    f = PL.compute_sensitivity(mode = "const_Exp_AngVel", exp = 1/PL.fps, ang_vel = 0)
    lim_mag_stars = f(0).item()
    return lim_mag_stars

def _calc_sun_electrons(PL):
    exp = 1/PL.fps
    SNR_threshold = config.get("snr_threshold")
    SBS_SKY_BRIGHTNESS = config.get("sbs_sky_brightness")
    N_fpn = config.get("n_fpn")
    N_row_tempo_noise = config.get("n_row_tempo_noise")
    N_prnu_factor = config.get("n_prnu_factor")
    
    N_bgn = calc_bgn_noise(PL, SBS_SKY_BRIGHTNESS if PL.sensor_loc == "space" else NIGHT_SKY_BRIGHTNESS, exp)
    noise_const, noise_signal_dep = calc_noise_consts([PL.n_read, PL.n_dc, N_bgn, N_fpn, N_row_tempo_noise, N_prnu_factor], exp)
    
    # Compute Total Signal using SNR Value in Total Number of Electrons
    signal_perpx = calc_total_signal_SNR(SNR_threshold if PL.cam_focus == 'focused' else 20.0, noise_signal_dep, noise_const)
    _, _, no_electrons_at_sun = calc_photons(PL, signal_perpx)
    sun_electrons_at_earth = sun2obj_photons(no_electrons_at_sun, R_S, R_SE)
    sun_electrons_perspot_persec = sun2spot_electrons(sun_electrons_at_earth, PL.aperture_mm, PL.ap_eff) 
    return sun_electrons_perspot_persec


def _set_lens(PL, params):
    """
    Sets the lens-related parameters for the optical system.
    """
    (PL.focal_length, PL.f_no, PL.aperture_mm, PL.img_fmt, PL.ap_eff, 
        PL.if_filter, PL.distortion_param, PL.rel_ilm, PL.cam_focus, PL.spot_size_abb_limit, 
        PL.transmission, PL.spot_img_heights, PL.psf_input_type, PL.psf_filenames) = params
    
    return PL
    
    
def _set_sensor(PL, params):
    """
    Sets the sensor-related parameters for the optical system.
    """
    (PL.sensor_type, PL.no_pixel_H, PL.no_pixel_V, PL.pixel_size, PL.fps, 
        PL.n_read, PL.n_dc, PL.fwc) = params
    PL.read_time = 0 if PL.sensor_type == 'CMOS' else 2
    return PL
    
def _compute_sensor_effectiveness(PL):
    """
    Computes the effective sensor parameters, including field of view, pixel pitch,
    and the spot size characteristics.
    """
    PL.fov_cs, PL.FOV_H, PL.FOV_V, PL.FOV_lens, PL.FOV_rad, PL.pixel_pitch = calc_effective_sensor(PL)
    spot_size, _ = calc_spot_size(PL.sensor_loc, PL.pixel_pitch, PL.f_no, PL.spot_size_abb_limit, PL.pixel_size)
    PL.std_dev, PL.spot_frac = calc_std_dev(spot_size, PL.pixel_size)
    return PL

def _save_system_vars(PL):
    payload_dict = {"sensor_loc":PL.sensor_loc,"no_pixel_H":PL.no_pixel_H,
                    "no_pixel_V":PL.no_pixel_V,"pixel_size":PL.pixel_size, 
                    "fps":PL.fps, "fwc": PL.fwc, "n_dc": PL.n_dc, "n_read": PL.n_read,
                    "focal_length": PL.focal_length, "f_no": PL.f_no, 
                    "img_fmt": PL.img_fmt, "FOV_H": PL.FOV_H, "FOV_V": PL.FOV_V, 
                    "FOV_lens": PL.FOV_lens, "FOV_rad": PL.FOV_rad, 
                    "lim_mag_stars": PL.lim_mag_stars, "rel_ilm": PL.rel_ilm, 
                    "distortion_param":PL.distortion_param, "cam_focus":PL.cam_focus, 
                    "sun_electrons_perspot_persec": PL.sun_electrons_perspot_persec, 
                    'std_dev': PL.std_dev[0], 'ap_eff': PL.ap_eff}

    with open(os.path.join(PL.dir, "char.json"), "w") as outfile: 
        json.dump(payload_dict, outfile)
    
def _get_c2c_functions(PL):
    """
    Calculates and stores the center-to-corner (c2c) functions for various payload parameters, 
    including relative illumination, transmission, spot size and PSF if needed.

    This method interpolates the relative illumination (relilm), transmission, and spot size 
    with respect to image heights and calculates the Point Spread Function (PSF) if the input 
    type is "psf". The interpolated functions are stored as class attributes.

    Attributes:
    - f_relilm: interpolated function for relative illumination as a function of angle.
    - f_trans: interpolated function for transmission as a function of angle.
    - f_spots: interpolated function for spot size as a function of angle.
    - f_psf: RegularGridInterpolator for PSF values as a function of angle, positions on pixel scale, if the PSF input type is "psf".
    """
    img_heights = np.linspace(0, PL.img_fmt/2, 100)
    angles = np.rad2deg(calc_fov(img_heights, PL.focal_length))
    _calc_f_relilm(PL, img_heights, angles)
    _calc_f_trans(PL, img_heights, angles)
    _calc_f_spots(PL, img_heights, angles)
    if PL.psf_input_type == "psf":
        _calc_f_psf(PL) 
        
    return PL
    
    
def _calc_f_relilm(PL, img_heights, angles):
    relilm = PL.rel_ilm + [100] + PL.rel_ilm
    relilm = np.array(relilm)
    x = np.linspace(-1, 1, len(relilm))
    x *= PL.img_fmt / 2
    y1 = relilm/100
    
    f_relilm_height = interpolate.interp1d(x, y1, bounds_error = False, kind = 'quadratic', fill_value="extrapolate")
    relilms = f_relilm_height(img_heights)
    PL.f_relilm = interpolate.interp1d(angles, relilms, bounds_error = False, kind = 'quadratic', fill_value="extrapolate")
    
def _calc_f_trans(PL, img_heights, angles):
    trans = np.array([PL.transmission[1], PL.transmission[0], PL.transmission[1]])
    x = np.linspace(-1, 1, 3)
    x *= PL.img_fmt / 2
    y2 = trans/100
    
    f_trans_height = interpolate.interp1d(x, y2, bounds_error = False, kind = 'quadratic', fill_value="extrapolate")
    transmissions = f_trans_height(img_heights)
    PL.f_trans = interpolate.interp1d(angles, transmissions, bounds_error = False, kind = 'quadratic', fill_value="extrapolate")
    
def _calc_f_spots(PL, img_heights, angles):
    y3 = PL.spot_size_abb_limit
    x = PL.spot_img_heights
    f_spots_height = interpolate.CubicSpline(x, y3, extrapolate=True)
    
    spots = f_spots_height(img_heights)
    PL.f_spots = interpolate.interp1d(angles, spots, bounds_error = False, kind = 'quadratic', fill_value="extrapolate")
    
def _calc_f_psf(PL):
    x = np.array([0, np.degrees(PL.FOV_lens)])
    df_onaxis = pd.read_csv(PL.psf_filenames[0])
    df_offaxis = pd.read_csv(PL.psf_filenames[1])
    df_onaxis["Position (pixel scale)"] = df_onaxis["Position (microns)"]/PL.pixel_size
    #df_offaxis["Position (pixel scale)"] = df_offaxis["Position (microns)"]/PL.pixel_size
    y = np.array(df_onaxis["Position (pixel scale)"])
    z_on = np.array(df_onaxis["Value"])
    z_off = np.array(df_offaxis["Value"])
    
    integral_value = np.trapz(y, z_on)  # Use np.trapz instead of quad for better performance
    z_on_norm = z_on/integral_value
    integral_value = np.trapz(y, z_off)  # Use np.trapz instead of quad for better performance
    z_off_norm = z_off/integral_value
    Z = np.array([z_on_norm, z_off_norm])
    PL.psf_min_px = y[0]
    PL.psf_max_px = y[-1]
    PL.f_psf = RegularGridInterpolator((x, y), Z, bounds_error=False, fill_value=None)