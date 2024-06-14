'''
This module contains the functions for calculating the stresses caused by the internal pressure.

In steps, the module calculates the stresses caused by the internal pressure.
The stresses are calculated for each node of the spatial mesh and for each time step.
'''

from src.models import Structure, MeshSpace, MeshTime, Results, Loads
import numpy as np
import numpy.typing as npt
from src.calculations.stresses.thermal_stresses import calc_stress_from_strain
from src.calculations.stresses.general_functions import concrete_stress_distribution
from src.calculations.stresses.general_functions import init_empty_space_time_matrix, init_empty_space_array, init_empty_time_array


def get_lame_stress(gas_pressure: float, current_radius: float, structure: Structure) -> float:
    '''
    This function calculates the Lame stress for a given gas pressure and current radius.
    :param gas_pressure:
    :param current_radius:
    :param structure:
    :return:
    '''
    pe = structure.pressure_ext
    ri = structure.radius_in
    re = structure.radius_out
    ri2 = ri * ri
    re2 = re * re
    stress_lame = ((gas_pressure * ri2 - pe * re2) / (re2 - ri2)) + ((gas_pressure - pe) * re2 * ri2 / ((re2 - ri2) * current_radius * current_radius))
    return stress_lame


def calculate_pressure_stresses(
        structure: Structure,
        mesh_space: MeshSpace,
        mesh_time: MeshTime,
        loads: Loads,
        results: Results) -> str:

    # TODO: Clean it up (use functions and objects more).
    try:
        # Initialize the matrices for the stresses and strains
        matrix_strain_pressure = init_empty_space_time_matrix(mesh_space, mesh_time)
        matrix_stress_pressure = init_empty_space_time_matrix(mesh_space, mesh_time)

        # Initialize the vector for the maximum stresses
        max_stress_concrete_evol = init_empty_time_array(mesh_time)

        # Calculate the internal pressure stresses
        node_centers_list = mesh_space.node_centers_from_zero
        for i in range(int(mesh_time.time_steps_count) + 1):
            current_time = mesh_time.time_axis[i]
            if i == 0:
                gas_pressure = loads.get_current_air_pres(current_time)  # During normal operations (first time step), the pressure coefficient should not be used.
            else:
                gas_pressure = structure.pressure_coeff * loads.get_current_air_pres(current_time)
            results.pres_air_int_vect[i] = gas_pressure
            for j in mesh_space.nodes_range:
                current_radius = node_centers_list[j]
                stress_lame = get_lame_stress(gas_pressure, current_radius, structure)
                equivalent_strain = stress_lame / structure.modulus_total
                matrix_strain_pressure[i][j] = equivalent_strain
                real_stress = calc_stress_from_strain(equivalent_strain, j, mesh_space, structure)
                matrix_stress_pressure[i][j] = real_stress
            max_stress_concrete_evol[i] = max(concrete_stress_distribution(matrix_stress_pressure[i], mesh_space, structure))

        results.strain_internal_pressure = matrix_strain_pressure
        results.stress_internal_pressure = matrix_stress_pressure

        result_message = "Internal pressure stresses calculated successfully."

    except Exception as exception:
        result_message = "Internal pressure stresses calculation FAILED: " + str(exception)

    return result_message



















