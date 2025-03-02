import math
import numpy as np
from .functions import calc_fov
from ..constants import *
from ..config import config

def calc_eff_QE(payload):
    '''Computes the effective QE of the detector'''
    lens_filter_eff = config.get("lens_filter_eff")
    lens_opts_eff = config.get("lens_opts_eff")
    lamda_res = config.get("lamda_res")
    sensor_cover_glass_eff = config.get("sensor_cover_glass_eff")
    sensor_qe = config.get("sensor_qe")
    if payload.sensor_loc == 'ground':
        #atmos_filter = [ 0.84, 0.88, 0.9, 0.92, 0.95, 0.98]
        atmos_filter = [0.75, 0.84, 0.88, 0.9, 0.92, 0.95, 0.98, 1, 1, 1, 1, 1, 1]
    else:
        atmos_filter = 1 
    
    eff_qe = np.multiply(atmos_filter, np.multiply(lens_filter_eff, np.multiply(lens_opts_eff, np.multiply(sensor_cover_glass_eff, sensor_qe))))

    return eff_qe, lamda_res


def calculate_effective_image_size(sensor_image_size_H, sensor_image_size_V, image_format, pixel_size):
    '''Computes the effective image size'''
    if sensor_image_size_H > image_format:
        if sensor_image_size_V > image_format:
            eff_image_size_V = image_format
            eff_image_size_H = image_format
            fov_cs = 'circle'
        else:
            eff_image_size_H = image_format
            eff_image_size_V = sensor_image_size_V
            fov_cs = 'square'
    else:
        eff_image_size_H = sensor_image_size_H
        eff_image_size_V = sensor_image_size_V
        fov_cs = 'square'
        if sensor_image_size_V > image_format:
            eff_image_size_V = image_format
            eff_image_size_H = sensor_image_size_H
            fov_cs = 'square'

    eff_no_pixel_H, eff_no_pixel_V = calculate_effective_number_of_pixels(pixel_size, eff_image_size_H, eff_image_size_V)
    return eff_no_pixel_H, eff_no_pixel_V, eff_image_size_H, eff_image_size_V, fov_cs

def calculate_effective_number_of_pixels(pixel_size, eff_image_size_H, eff_image_size_V):
    "Computes the effective number of pixels in image"
    eff_no_pixel_H = math.floor(eff_image_size_H * 1000 / pixel_size)
    eff_no_pixel_V = math.floor(eff_image_size_V * 1000 / pixel_size)
    return eff_no_pixel_H, eff_no_pixel_V


def calculate_sensor_size_and_fov(sensor_size_H, sensor_size_V, focal_length, image_format):
    '''Compute FOVs'''
    FOV_H = calc_fov(sensor_size_H, focal_length)
    FOV_V = calc_fov(sensor_size_V, focal_length)
    FOV_lens = calc_fov(image_format, focal_length)
    FOV_diag = calc_fov(math.sqrt(sensor_size_H**2+ sensor_size_V**2), focal_length)
    return FOV_H, FOV_V, FOV_lens, FOV_diag


def calc_effective_sensor(payload):
    '''Compute effective sensor size and FOV'''
    # focal_length = lens_par[0]
    # image_format = lens_par[3]

    # pixel_size = sensor_par[3]
    # no_pixel_H = sensor_par[1]
    # no_pixel_V = sensor_par[2]

    sensor_image_size_H = payload.pixel_size*payload.no_pixel_H*(1/1000)
    sensor_image_size_V = payload.pixel_size*payload.no_pixel_V*(1/1000)

    #pixel_area = (payload.pixel_size/1000)**2

    _, _, eff_image_size_H, eff_image_size_V, fov_cs = calculate_effective_image_size(sensor_image_size_H, sensor_image_size_V, payload.img_fmt, payload.pixel_size)

    FOV_H, FOV_V, FOV_lens, FOV_diag = calculate_sensor_size_and_fov(eff_image_size_H, eff_image_size_V, payload.focal_length, payload.img_fmt)
    pixel_pitch = calc_fov(payload.pixel_size/1000, payload.focal_length)
    if fov_cs == 'circle':
        FOV_scene = FOV_lens
    else:
        FOV_scene = FOV_diag
    # sensor_area = math.pi*(payload.img_fmt/2)**2
    # tot_pixels = int(sensor_area/pixel_area)

    return fov_cs, FOV_H, FOV_V, FOV_lens, FOV_scene, pixel_pitch