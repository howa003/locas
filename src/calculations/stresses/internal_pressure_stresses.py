from src.models import Structure, MeshSpace, MeshTime, Results, Loads
import numpy as np
import numpy.typing as npt
from src.calculations.stresses.thermal_stresses import calc_stress_from_strain
from src.calculations.stresses.general_functions import concrete_stress_distribution
from src.calculations.stresses.general_functions import init_empty_space_time_matrix, init_empty_space_array, init_empty_time_array

'''
This module contains the functions for calculating the stresses caused by the internal pressure.

In steps, the module calculates the stresses caused by the internal pressure.
The stresses are calculated for each node of the mesh and for each time step.

Note for GitHub Copilot: We will refactor the code commented below.
'''

#
# print('===== Overpressure started. =====')
# ri = polomerVnitrni
# re = ri + length
# ri2 = ri * ri
# re2 = re * re
# matrixStrnOvrprss = zeros((steps + 1, nNode))
# matrixStrssOvrprss = zeros((steps + 1, nNode))
# vectStrnOvrprss = zeros((nNode))
# vectStrssOvrprss = zeros((nNode))
# vectMaxStrssOvrprss = zeros((steps + 1))
# for i in range(steps + 1):
#     pi = airPressVect[i]
#     maxStrssOvrprss = 0
#     for j in range(nNode):
#         rAct = ri + (j * Le)
#         strssAct = ((pi * ri2 - pe * re2) / (re2 - ri2)) + ((pi - pe) * re2 * ri2 / ((re2 - ri2) * rAct * rAct))
#         strnAct = strssAct / modulusTotal
#         vectStrnOvrprss[j] = strnAct
#         if ((steelThick != 0) and (j < indSl)):
#             vectStrssOvrprss[j] = strnAct * modulusSteel
#         elif ((steelThickOut != 0) and (j >= indSl2)):
#             vectStrssOvrprss[j] = strnAct * modulusSteel
#         else:
#             vectStrssOvrprss[j] = strnAct * modulusConc
#             maxStrssOvrprss = max(strnAct * modulusConc, maxStrssOvrprss)
#     matrixStrnOvrprss[i] = vectStrnOvrprss
#     matrixStrssOvrprss[i] = vectStrssOvrprss
#     vectMaxStrssOvrprss[i] = maxStrssOvrprss
#
# matrixStrnOvrprss = pretlak * matrixStrnOvrprss
# matrixStrssOvrprss = pretlak * matrixStrssOvrprss
# vectMaxStrssOvrprss = pretlak * vectMaxStrssOvrprss
# print('===== Overpressure ended. =====')


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
        print(node_centers_list)
        for i in range(int(mesh_time.time_steps_count) + 1):
            current_time = mesh_time.time_axis[i]
            gas_pressure = loads.get_current_air_pres(current_time)
            for j in mesh_space.nodes_range:
                current_radius = node_centers_list[j]
                stress_lame = get_lame_stress(gas_pressure, current_radius, structure)
                equivalent_strain = stress_lame / structure.modulus_total
                matrix_strain_pressure[i][j] = equivalent_strain
                real_stress = calc_stress_from_strain(equivalent_strain, j, mesh_space, structure)
                matrix_stress_pressure[i][j] = real_stress
            max_stress_concrete_evol[i] = max(concrete_stress_distribution(matrix_stress_pressure[i], mesh_space, structure))

        results.strain_internal_pressure = structure.pressure_coeff * matrix_strain_pressure
        results.stress_internal_pressure = structure.pressure_coeff * matrix_stress_pressure

        result_message = "Internal pressure stresses calculated successfully."

    except Exception as exception:
        result_message = "Internal pressure stresses calculation FAILED: " + str(exception)

    return result_message



















