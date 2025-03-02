import pandas as pd
import numpy as np
import math
import os

from .constants import *
from .config import config
from .model.functions import generate_exp_time
from .model.vis_mag import calc_obj_size_ranges
from .model.excel_methods import write_to_excel

def main_add_performance_sheet(PL):
    """
    Adds the performance sheet to the output Excel file, including calculations for:
    - Sensitivity
    - Object sizes
    - Survey/tracking performance
    """
    
    file_name = _get_output_filename(PL.dir, PL.fps)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    wb = writer.book

    _compute_fps_performance(PL, wb, writer)
    _compute_survey_tracking_performance(PL, wb, writer)
    
    writer._save()
        
def _get_output_filename(dir, fps):
    SNR_threshold = config.get("snr_threshold")
    return os.path.join(
        dir, f'perf_at_SNR{int(SNR_threshold)}_fps_{int(fps)}.xlsx'
    )
    
def _compute_fps_performance(PL, wb, writer):
    sensitivity_func = PL.compute_sensitivity(mode="const_Exp_Angle", angle=0.0, exp=1/PL.fps)
    ang_vel_stop = math.radians(90 if PL.sensor_loc == 'space' else 1)
    ang_vels = np.linspace(0, ang_vel_stop, 1000)
    lim_mags = sensitivity_func(np.degrees(ang_vels))
    
    df = pd.DataFrame({
        'Angular Velocity (deg/sec)': np.degrees(ang_vels),
        'Limiting Magnitude': lim_mags
    })
    write_to_excel(PL, wb, writer, df, 'fps')
    df = df[df['Angular Velocity (deg/sec)'] < 10.0]
    
    # Compute Object Sizes for Ranges
    if PL.sensor_loc == 'space':
        ranges = np.concatenate((np.arange(10, 100, 10),np.arange(100, 41000, 100)) )                                    # km
    else:
        ranges = np.arange(300, 41000, 100)                                     # km
    obj_sizes, max_ang_vels = calc_obj_size_ranges(PL.alt, sensitivity_func, ranges, PL.sensor_loc)
    df = pd.DataFrame({'Ranges (km)': ranges, 'Tracking Object Size Limit (m)': obj_sizes[0],
                        'Orbit Specific Maximum Angular Velocity Object Size limit (m)': obj_sizes[1], 'Orbit Specific Maximum Angular Velocity Limit (deg/sec)': max_ang_vels})
    write_to_excel(PL, wb, writer, df, 'obj_sizes')
    
def _compute_survey_tracking_performance(PL, wb, writer):
    if PL.sensor_loc == 'space':
        ranges = np.array([50, 100, 500, 5000, 10000, 20000, 30000, 40000])
        obs_sat_speed = math.sqrt(G * M_E / ((PL.alt + R_E) * 1000)) / 1000
        target_sat_speed = np.sqrt(G * M_E / ((ranges + PL.alt + R_E) * 1000)) / 1000
        max_ang_vels = (target_sat_speed + obs_sat_speed) / ranges
        ang_vels = np.concatenate(([0.0], max_ang_vels))
    else:
        ang_vels = np.deg2rad([0, 15, 1517, 3124]) / 3600
    
    exp_time = generate_exp_time(0.01, 100)
    df_survey = pd.DataFrame({'Integration Time (sec)': exp_time})

    for i, ang_vel in enumerate(ang_vels):
        sensitivity_func = PL.compute_sensitivity(
            mode="const_AngVel_Angle", angle=0.0, ang_vel=np.degrees(ang_vel), min_exp=0.01, max_exp=100
        )
        col_name = (
            'Tracking Limiting Magnitude' if i == 0 else 
            f'Limiting Magnitude at Range {np.around(ranges[i-1], 0)} km' if PL.sensor_loc == 'space' else 
            f'Limiting Magnitude at {np.around(np.rad2deg(ang_vel), 5)} deg/sec'
        )
        df_survey[col_name] = sensitivity_func(exp_time)
    
    write_to_excel(PL, wb, writer, df_survey, 'survey')