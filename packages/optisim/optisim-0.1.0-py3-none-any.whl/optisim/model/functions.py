import numpy as np

def calc_fov(sensor_size, focal_length):
    '''Computes FOV from sensor size and focal length'''
    return 2 * np.arctan(sensor_size / (2 * focal_length))
        
def generate_exp_time(min_exp, max_exp, points_per_decade=10):
    """
    Generate an array with logarithmically spaced exposure times between min_exp and max_exp.

    Args:
        min_exp (float): Minimum exposure time.
        max_exp (float): Maximum exposure time.
        points_per_decade (int): Number of points per decade.

    Returns:
        np.array: Logarithmically spaced exposure times.
    """
    # Compute the exponent range from the given exposure times
    min_exponent = np.log10(min_exp)
    max_exponent = np.log10(max_exp)

    # Generate log-spaced values within this range
    exp_time = np.logspace(min_exponent, max_exponent, 
                           int((max_exponent - min_exponent) * points_per_decade) + 1) 

    return exp_time