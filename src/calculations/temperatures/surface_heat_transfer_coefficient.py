from src.config import STEF_BOLT_CONST, AIR_FLOW
from src.calculations.temperatures.air_properties import calc_air_conductivity, calc_air_dyn_viscosity, calc_air_density, calc_air_heat_capacity
from src.models import Structure


def celsius_to_kelvin(temp: float) -> float:
    return temp + 273.15


def calc_convective_coefficient(char_len: float, temp_surf: float, temp_air: float) -> float:
    # Temperatures (in inputs) are in Kelvin
    air_conduc = calc_air_conductivity(temp_air)  # W/mK
    air_dyn_viscosity = calc_air_dyn_viscosity(temp_air)  # Ns/m2
    air_density = calc_air_density(temp_air)  # kg/m3
    air_heat_capac = calc_air_heat_capacity(temp_air)  # J/kgK
    ga = 9.81  # m/s2
    beta = 1 / temp_air  # 1/K
    air_kinematic_viscosity = air_dyn_viscosity / air_density  # m2/s
    air_diffusivity = air_conduc / (air_density * air_heat_capac)  # m2/s
    Ra = (ga * beta / (air_kinematic_viscosity * air_diffusivity)) * abs(temp_surf - temp_air) * char_len ** 3  # dimensionless
    Pr = air_kinematic_viscosity / air_diffusivity  # dimensionless
    if AIR_FLOW == 0:
        conv_coef = (air_conduc / char_len) * (0.68 + 0.67 * Ra ** (1 / 4) / (1 + (0.492 / Pr) ** (9 / 16)) ** (4 / 9))  # W/m2K
    else:
        conv_coef = (air_conduc / char_len) * (0.825 + 0.387 * Ra ** (1 / 6) / (1 + (0.492 / Pr) ** (9 / 16)) ** (8 / 27)) ** 2  # W/m2K
    return conv_coef


def calc_surface_heat_transfer_coef(char_len: float, emissivity: float, temp_surf: float, temp_air: float) -> float:
    # Temperatures (in inputs) are in Celsius
    temp_surf_k = celsius_to_kelvin(temp_surf)
    temp_air_k = celsius_to_kelvin(temp_air)
    conv_coeff = calc_convective_coefficient(char_len, temp_surf_k, temp_air_k)
    rad_coeff = emissivity * STEF_BOLT_CONST * (temp_surf_k + temp_air_k) * (temp_surf_k * temp_surf_k + temp_air_k * temp_air_k)
    total_coeff = conv_coeff + rad_coeff
    return total_coeff


def calc_surface_resistance(structure: Structure, temp_surf: float, temp_air: float) -> float:
    return 1 / calc_surface_heat_transfer_coef(structure.char_len, structure.emissivity, temp_surf, temp_air)



