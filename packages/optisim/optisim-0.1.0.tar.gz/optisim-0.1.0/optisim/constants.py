# -*- coding: utf-8 -*-
"""
Constants File
==============
All the constants used in the code must be called from here
"""
import math
import numpy as np

R_E = 6378.137                  # equatorial radius of earth in km
R_P = 6356.752                  # polar radius of earth in km
M_E = 5.97219e24                # mass of earth in kg
G = 6.67430e-11                 # Universal gravitational constant in N-m2/kg2
NIGHT_SKY_BRIGHTNESS = 22       # in magnitude
H = 6.62607015e-34              # planck constant in J-s
C = 2.99792458e8                # speed of light in m/s
K = 1.380649e-23                # Boltzman constant in J/K
SUN_TEMPERATURE=5778            # Temperature of sun in K
R_S = 696340                    # Radius of Sun in km
R_SE = 1.496*10**8              # Distance of Earth from Sun in km
L_MEAN = 589e-9                 # mean wavelength of sodium light

DEFAULT_CONFIG = {
    "sbs_sky_brightness": 21, 
    "nir_coat_lens": 0.9,
    "n_fpn": 0, 
    "n_row_tempo_noise": 4.25, 
    "n_prnu_factor": 0, 
    "obj_reflectivity": 10,
    "snr_threshold": 5.0,
    "ref_el_ang": math.radians(90),
    "ref_phase_ang": math.radians(0),
    "qe_noise": 0.6,
    "lens_filter_eff": 0.9,
    "lens_opts_eff": 0.9,
    "sensor_cover_glass_eff": 0.91,
    "seeing_fwhm_arcsec": 1.5,
    "k": 0.116,
    "lamda_res": list(np.linspace(0.45, 1.1, 13)),
    "sensor_qe": [0.53, 0.58, 0.6, 0.58, 0.56, 0.45, 0.37, 0.28, 0.2, 0.14, 0.07, 0.04, 0.02]
}