import numpy as np
import math
from scipy.interpolate import interp1d, RegularGridInterpolator

from .constants import *
from .config import config
from .model.vis_mag import calc_mag
from .model.functions import generate_exp_time
from .model.noise import calc_noise_consts, calc_bgn_noise
from .model.signal import calc_total_signal_SNR, calc_photons, sun2obj_photons
from .model.spot import calc_moving_spot_correction, calc_spot_size, calc_std_dev, calc_moving_psf_correction



def main_compute_sensitivity(PL, mode, exp, ang_vel, angle, min_exp, max_exp):
    """
    Computes the sensitivity of the optical system.

    Parameters:
    - mode: str, the mode of sensitivity computation ('default', 'const_Exp', 'const_AngVel', 'const_Exp_AngVel', 'const_Exp_Angle', 'const_AngVel_Angle')
    - exp: float, sensor exposure time.
    - ang_vel: float, target angular velocity.
    - angle: float, the target angle with camera pointing.
    - min_exp: float, the minimum exposure time for sensitivity calculation.
    - max_exp: float, the maximum exposure time for sensitivity calculation.

    Returns:
    - interpolator: function, a function to interpolate the limiting magnitude.
    """
    SNR_threshold = config.get("snr_threshold")
    SBS_SKY_BRIGHTNESS = config.get("sbs_sky_brightness")
    N_fpn = config.get("n_fpn")
    N_row_tempo_noise = config.get("n_row_tempo_noise")
    N_prnu_factor = config.get("n_prnu_factor")
    exp, ang_vel, angle = _get_sensitivity_params(PL, mode, exp, ang_vel, angle, min_exp, max_exp)
    #breakpoint()
    relilm, transmission = PL.f_relilm(angle), PL.f_trans(angle)
    N_bgn = calc_bgn_noise(PL, SBS_SKY_BRIGHTNESS if PL.sensor_loc == "space" else NIGHT_SKY_BRIGHTNESS, exp)
    noise_const, noise_signal_dep = calc_noise_consts([PL.n_read, PL.n_dc, N_bgn, N_fpn, N_row_tempo_noise, N_prnu_factor], exp)
    
    # Compute Total Signal using SNR Value in Total Number of Electrons
    signal_perpx = calc_total_signal_SNR(SNR_threshold if PL.cam_focus == 'focused' else 20.0, noise_signal_dep, noise_const)
    photons_perpx, no_photons_at_sun, _ = calc_photons(PL, signal_perpx)
    c2c_moving_target = calc_c2c_moving_target(PL, exp, ang_vel, angle)
    
    photons_perspot_persec = _apply_c2c_corrections(mode, c2c_moving_target, photons_perpx, relilm, transmission)       
    photons_persec_m2 = np.divide(photons_perspot_persec,(PL.ap_eff*math.pi*((PL.aperture_mm)/2000)**2))
    
    sun_photons_at_earth = sun2obj_photons(no_photons_at_sun, R_S, R_SE)
    lim_mag = calc_mag(photons_persec_m2, sun_photons_at_earth).T
    ang_vel = np.degrees(ang_vel)
    return _get_interpolator(mode, ang_vel, angle, exp, lim_mag)
    
def _get_interpolator(mode, ang_vel, angle, exp, lim_mag):
    """
    Returns an interpolator function based on the mode selected.

    Parameters:
    - mode: str, the mode of interpolation.
    - ang_vel: float, target angular velocity.
    - angle: float, target angle.
    - exp: float, sensor exposure time.
    - lim_mag: float, the limiting magnitude.

    Returns:
    - interpolator: function, the appropriate interpolator based on the mode.
    """
    if mode in ["default", "const_Exp"]:
        interpolator = RegularGridInterpolator((ang_vel, angle), lim_mag, bounds_error=False, fill_value=None)
        return lambda av, a: interpolator((av, a))

    elif mode == "const_AngVel":
        interpolator = RegularGridInterpolator((exp, angle), lim_mag, bounds_error=False, fill_value=None)
        return lambda e, a: interpolator((e, a))

    elif mode == "const_Exp_AngVel":
        interpolator = interp1d(angle, lim_mag, kind='cubic', bounds_error=False, fill_value="extrapolate")
        return lambda a: interpolator(a)

    elif mode == "const_Exp_Angle":
        interpolator = interp1d(ang_vel, lim_mag, kind='cubic', bounds_error=False, fill_value="extrapolate")
        
        return lambda av: interpolator(av)

    elif mode == "const_AngVel_Angle":
        interpolator = interp1d(exp, lim_mag, kind='cubic', bounds_error=False, fill_value="extrapolate")
        return lambda e: interpolator(e)

def _get_sensitivity_params(PL, mode, exp, ang_vel, angle, min_exp, max_exp):
    
    """
    Returns the sensitivity parameters based on the mode selected.

    Parameters:
    - mode: str, the mode of sensitivity calculation.
    - exp: float, exposure time.
    - ang_vel: float, angular velocity.
    - angle: float, the observation angle.
    - min_exp: float, minimum exposure time.
    - max_exp: float, maximum exposure time.

    Returns:
    - exp: float/array, sensor exposure time after adjustments.
    - ang_vel: float/array, target angular velocities after adjustments.
    - angle: float/array, target angles for sensitivity calculation.
    """
    if mode == "default":
        # compute sensitivty for PL.FPS
        exp = 1/PL.fps
        ang_vel_stop = math.radians(90) if PL.sensor_loc == 'space' else math.radians(1)
        ang_vel = np.linspace(0, ang_vel_stop, 1000)
        angle = np.degrees(np.linspace(0, PL.FOV_lens, 100))
    elif mode == "const_Exp":
        ang_vel_stop = math.radians(90) if PL.sensor_loc == 'space' else math.radians(1)
        ang_vel = np.linspace(0, ang_vel_stop, 1000)
        angle = np.degrees(np.linspace(0, PL.FOV_lens, 100))
    elif mode == "const_AngVel":
        ang_vel = np.radians(ang_vel)
        exp = generate_exp_time(min_exp, max_exp)
        angle = np.degrees(np.linspace(0, PL.FOV_lens, 100))
    elif mode == "const_Exp_AngVel":
        ang_vel = np.radians(ang_vel)
        angle = np.degrees(np.linspace(0, PL.FOV_lens, 100))
    elif mode == "const_Exp_Angle":
        ang_vel_stop = math.radians(90) if PL.sensor_loc == 'space' else math.radians(1)
        ang_vel = np.linspace(0, ang_vel_stop, 1000)
    elif mode == "const_AngVel_Angle":
        ang_vel = np.radians(ang_vel)
        exp = generate_exp_time(min_exp, max_exp)
    return exp, ang_vel, angle

def _apply_c2c_corrections(mode, c2c_moving_target, photons_perpx, relilm, transmission):
    """
    Applies corrections for c2c (center-to-corner) effects.

    Parameters:
    - mode: str, the mode of sensitivity computation.
    - c2c_moving_target: float/array, the moving target correction.
    - photons_perpx: float/array, photons per pixel.
    - relilm: array, relative illumination correction.
    - transmission: array, transmission correction.

    Returns:
    - photons_perspot_persec: array, corrected photons per second per spot.
    """
    
    photons_perspot_persec = np.multiply(c2c_moving_target,photons_perpx) if isinstance(photons_perpx, float) or mode == "const_AngVel_Angle" else c2c_moving_target*photons_perpx[np.newaxis, :]
    if photons_perspot_persec.ndim == 2:
        photons_perspot_persec = np.einsum('i, ij -> ij', 1/relilm, photons_perspot_persec)
        photons_perspot_persec = np.einsum('i, ij -> ij', 1/transmission, photons_perspot_persec)
    else:
        photons_perspot_persec = np.divide(photons_perspot_persec,relilm)
        photons_perspot_persec = np.divide(photons_perspot_persec,transmission)
    return photons_perspot_persec 
    
    
def calc_c2c_moving_target(PL, exp, ang_vels, angle):
    """
    Calculates the c2c (center-to-corner) moving target correction.

    Parameters:
    - exp: float/array, sensor exposure time.
    - ang_vels: float/array, target angular velocities.
    - angle: float/array, observation angle.

    Returns:
    - moving_target: float/array, the c2c correction value for moving target.
    """
    
    spot_size = PL.f_spots(angle)  
    c2c_spots, _ = calc_spot_size(PL.sensor_loc, PL.pixel_pitch, PL.f_no, spot_size, PL.pixel_size)
    c2c_std_devs, c2c_spot_fracs = calc_std_dev(c2c_spots, PL.pixel_size)
    
    if isinstance(angle, float):
        if PL.psf_input_type == "psf":
            c2c_moving_target = calc_moving_psf_correction(PL, angle, ang_vels, exp)
        else:
            c2c_moving_target=calc_moving_spot_correction(PL, c2c_std_devs, c2c_spot_fracs, ang_vels, exp)
    else:
        c2c_moving_target = []
        if PL.psf_input_type == "psf":
            for i in range(len(angle)):
                c2c_moving_target.append(calc_moving_psf_correction(PL, angle[i], ang_vels, exp))
        else:
            for i in range(len(c2c_spots)):
                c2c_moving_target.append(calc_moving_spot_correction(PL, c2c_std_devs[i], c2c_spot_fracs[i], ang_vels, exp)) 
        c2c_moving_target = np.array(c2c_moving_target)
    return c2c_moving_target