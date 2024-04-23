
'''
This module contains functions for calculating the properties of air based on its temperature.
'''


def calc_air_conductivity(temp_air_k):
    temp_air = temp_air_k - 273.15  # Temperature in Celsius
    return 418.4 * 5.75 * (1 + 0.00317 * temp_air - 0.0000021 * temp_air * temp_air) / 10 ** 5


def calc_air_dyn_viscosity(temp_air_k):
    return 1.716 * (temp_air_k / 273.11) ** (3 / 2) * ((273.11 + 110.56) / (temp_air_k + 110.56)) / 10 ** 5


def calc_air_density(temp_air_k):
    return 101325 / (287.058 * temp_air_k)


def calc_air_heat_capacity(temp_air_k):
    return 717.8 + 0.07075 * (temp_air_k - 300) + 0.00026125 * (temp_air_k - 300) ** 2