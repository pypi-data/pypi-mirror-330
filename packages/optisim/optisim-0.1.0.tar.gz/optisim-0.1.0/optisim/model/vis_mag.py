import math
import numpy as np
from ..constants import *
from ..config import config

def calc_extinction_factor(sensor_loc, el_ang):
    '''Calculate the extinction factor for a given sensor location and elevation angle'''
    if sensor_loc == 'space':
        return 1
    else:
        k = config.get("k")
        X = pow((1-0.96*pow((math.cos(el_ang)),2)), -0.5)
        return math.pow(10, -0.4*k*(X-1))
    
def calc_mag(obj_photons, sun_photons):
    '''Calculate magnitude using photons'''
    return -26.74-2.5*np.log10(obj_photons/sun_photons)

def mag2obj_size(mag, range_val, phase_ang, el_ang, obj_reflectivity, sensor_loc):
    '''Calculate object size using magnitude'''
    mu = obj_reflectivity               #object reflectivity
    extinction_fac = calc_extinction_factor(sensor_loc, el_ang)

    ref_fac = np.power(10,(-(mag+26.74)/2.5))/extinction_fac
    obj_size = np.sqrt(np.divide(np.multiply(3*math.pi*np.power(range_val,2),ref_fac),2*mu*(math.sin(phase_ang)+(math.pi-phase_ang)*math.cos(phase_ang))))
    obj_size = np.multiply(2e5, obj_size)      # object diameter
    return obj_size

def calc_obj_size_ranges(alt, f, ranges, sensor_loc):
    '''Calculate object size ranges for a given range values and angular velocities'''
    ref_phase_ang = config.get("ref_phase_ang")
    ref_el_ang = config.get("ref_el_ang")
    obj_reflectivity = config.get("obj_reflectivity")
    obs_sat_speed = math.sqrt(G*M_E/((alt+R_E)*1000))/1000             # km/sec
    target_sat_speed = np.sqrt(np.divide(G*M_E,((ranges+alt+R_E)*1000)))/1000             # km/sec
    max_ang_vels = np.rad2deg(np.divide((target_sat_speed+obs_sat_speed),ranges))
    min_ang_vels = np.zeros(len(max_ang_vels))
    min_lim_mags = f(max_ang_vels)
    max_lim_mags = f(min_ang_vels)
    max_obj_sizes = mag2obj_size(min_lim_mags, ranges, ref_phase_ang, ref_el_ang, obj_reflectivity/100, sensor_loc)/100
    min_obj_sizes = mag2obj_size(max_lim_mags, ranges, ref_phase_ang, ref_el_ang, obj_reflectivity/100, sensor_loc)/100
    return [min_obj_sizes, max_obj_sizes], max_ang_vels