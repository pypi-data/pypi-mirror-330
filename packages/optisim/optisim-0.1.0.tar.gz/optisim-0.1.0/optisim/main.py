"""
This module is used for sensitivity analysis of an optical system 
in context of observing the night Sky from Ground/Space. Given a 
few lens and sensor related inputs, this module outputs the limiting
magnitude for different sensor exposures, target angular velocities 
and target angles with satellite pointing. It also outputs a performance
sheet.

    - Class: Optical_System: Main Class to define the optical payload
    - Functions:
        - Optical_Payload.compute_sensitivity(): Computes various sensitivity (limiting magnitude) functions based on input
 
"""

import os

from .constants import *
from .utils import _set_lens, _set_sensor, _compute_sensor_effectiveness
from .utils import _get_c2c_functions, _save_system_vars, _calc_lim_mag_stars, _calc_sun_electrons
from .sensitivity import main_compute_sensitivity
from .performance import main_add_performance_sheet


class Optical_System():
    """
    A class to represent an optical payload in a space or telescope on ground.

    Attributes:
    - name: str, the name of the optical system.
    - sensor_loc: str, location of the sensor ('space' or 'ground').
    - lens_params: list, parameters related to the lens.
    - sensor_params: list, parameters related to the sensor.
    - mission_name: str, the name of the mission. Decides the output folder
    - orbit_specs: list, specifications for the orbit including altitude and elevation angle. Only needed when sensor_loc = 'space'
    - dir: str, the directory where the payload data will be saved.
    - compute_sensitivity: method to compute the limiting magnitude based on certain inputs
    - add_performance_sheet: method to output xlsx file with sensitivity
    """
    def __init__(self, name, sensor_loc, lens_params, sensor_params, mission_name, orbit_specs = [500,15]):
        """
        Initializes an instance of the Optical_System class.

        Parameters:
        - name: str, the name of the optical payload.
        - sensor_loc: str, location of the sensor ('space' or 'ground').
        - lens_params: list, lens-related parameters.
        - sensor_params: list, sensor-related parameters.
        - mission_name: str, the mission name. Decides the output folder
        - orbit_specs: list, contains altitude and elevation angle for orbit specifications. Only needed when sensor_loc = 'space'
        """
        # Create Output Directory
        self.dir = os.path.join(os.getcwd(), mission_name, "Payloads", name)
        os.makedirs(self.dir, exist_ok = True)
        
        # Compute Payload Parameters
        self.name = name
        self.sensor_loc = sensor_loc
        self.alt, self.att_el = orbit_specs
        
        self = _set_sensor(self, sensor_params)
        self = _set_lens(self, lens_params)
        self = _compute_sensor_effectiveness(self)
        self = _get_c2c_functions(self)
        self.add_performance_sheet()
        self.lim_mag_stars = _calc_lim_mag_stars(self)
        self.sun_electrons_perspot_persec = _calc_sun_electrons(self)
        _save_system_vars(self)
    
    def compute_sensitivity(self, mode = "default", exp = 1.0, ang_vel = 0.0, angle = 0.0, min_exp = 0.1, max_exp = 10.0):
        return main_compute_sensitivity(self, mode, exp, ang_vel, angle, min_exp, max_exp)
    
    def add_performance_sheet(self):
        main_add_performance_sheet(self)
    
if __name__ == "__main__":
    mission_name =  'test_new_psf'
    
    payload_name = 'onyx_el_check'
    output_dir = os.path.join(mission_name, "Payloads")
    dir = os.path.join(os.getcwd(), output_dir, payload_name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    Alt = 500

    # Pointing Direction
    att_el = 16
    att_az = 270                        # 270 for LTAN < 12, 90 for LTAN > 12

    ## Sample TDM Payload Inputs
    sensor_loc = 'space'                # Location on Payload ('space', 'ground')
    
    # Lens Specifications
    focal_length = 25                 # mm
    f_no = 0.95
    aperture_mm = focal_length/f_no                           
    image_format = 16               # mm
    aperture_eff = 1
    lens_func = 'focused'
    img_heights = [0, 5.25, 9.767, 13.424]
    aberration_lim_spot_size = [4, 4, 4, 4]     # microns
    
    transmission = [100, 100]
    if_filter = 0
    rel_ilm = [100] 
    distortion_param = [-0.0004491, -0.0000326, 0.0001229]
    
    # Sensor Specifications
    sensor_type = 'CMOS'
    no_pixel_H = 8192
    no_pixel_V = 5460
    pixel_size = 3.2                # micrometer
    fps = 10
    
    FWC = 10100
    N_read = 7
    N_dark_current = 100            # e-/s
    
    # For different orbital planes, this should be different
    orbit_specs = [Alt, att_el]
    
    psf_input_type = ""
    psf_filenames = ["onaxis_psf.csv", "onaxis_psf.csv"]

    lens_par = [focal_length, f_no, aperture_mm, image_format, aperture_eff, if_filter, distortion_param, rel_ilm , lens_func, aberration_lim_spot_size, transmission, img_heights, psf_input_type, psf_filenames]
    sensor_par = [sensor_type, no_pixel_H, no_pixel_V, pixel_size, fps, N_read, N_dark_current, FWC]
    pl1 = Optical_System(payload_name, sensor_loc, lens_par, sensor_par, mission_name, orbit_specs)
    func = pl1.compute_sensitivity(mode = "const_AngVel_Angle", ang_vel = 0.1)
    
        