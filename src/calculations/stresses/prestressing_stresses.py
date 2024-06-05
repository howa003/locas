'''
This module contains the functions for calculating the stresses caused by concrete prestressing.

In steps, the module calculates the stresses caused by the concrete prestressing.
The stresses are calculated for each node of the spatial mesh.
'''

from src.models import Structure, MeshSpace, MeshTime, Results, Loads
import numpy as np
import numpy.typing as npt
from src.calculations.stresses.thermal_stresses import calc_stress_from_strain
from src.calculations.stresses.general_functions import concrete_stress_distribution
from src.calculations.stresses.general_functions import init_empty_space_time_matrix, init_empty_space_array, init_empty_time_array

def calc_distr_factor(structure: Structure) -> float:
    '''
    This function calculates the distribution factor for the concrete prestressing.

    :param structure: A handle to the :class:`models.Structure` object containing information about the structure.
    :type structure: class:`Structure`
    :return: The distribution factor for the concrete prestressing.
    :rtype: float
    '''
    ri = structure.radius_in
    re = structure.radius_out
    rt = structure.radius_tendons
    distr_fact = ((re**2 - rt**2) / (2 * (re**2 - ri**2) * (1 - structure.poisson))) * ((1 - 2 * structure.poisson) + (ri**2 / rt**2))
    return distr_fact


def calc_circumferential_stress(
        structure: Structure,
        mesh_space: MeshSpace,
        mesh_time: MeshTime,
        loads: Loads,
        results: Results) -> str:
    '''
    This function calculates the circumferential stress induced by concrete prestressing
    and saves the results in the results object.

    :param structure: A handle to the :class:`models.Structure` object containing information about the structure.
    :type structure: class:`Structure`
    :return: String indicating the successful/unsuccessful calculation of the circumferential stress.
    :rtype: str
    '''

    pt = structure.tendons_stress
    at = structure.tendons_stress
    ri = structure.radius_in
    re = structure.radius_out
    rt = structure.radius_tendons

    p_e = pt * at / rt
    distr_fact = calc_distr_factor(structure)

    # Initialize the matrices for the stresses and strains
    matrix_strain_pressure = init_empty_space_time_matrix(mesh_space, mesh_time)
    matrix_stress_pressure = init_empty_space_time_matrix(mesh_space, mesh_time)

    # Initialize the vector for the maximum stresses
    max_stress_concrete_evol = init_empty_time_array(mesh_time)

    # TODO: Continue


#     print('===== Prestress started. =====')
#
#     # DISER2 vvv
#
#     ri = polomerVnitrni
#     rt = polomerVnitrni + 0.75
#     re = ri + length
#     ri2 = ri * ri
#     rt2 = rt * rt
#     re2 = re * re
#
#     p_e = predpinaciNapeti * plochaPredp / rt
#
#     distr_fact = ((re2 - rt2) / (2 * (re2 - ri2) * (1 - poisson))) * (
#                 (1 - 2 * poisson) + (ri2 / rt2))  # Distribution factor according to Acharya and Menon (2003)
#
#     matrixStrnPrstrss = zeros((steps + 1, nNode))
#     matrixStrssPrstrss = zeros((steps + 1, nNode))
#     vectMaxStrssPrstrss = zeros((steps + 1))
#
#     for i in range(steps + 1):
#         valMaxStrss = 0  # Inicializace hodnoty maximálního předpětí v daném časovém kroku
#         for j in range(nNode):
#             rAct = ri + (j * Le)
#             rAct2 = rAct * rAct
#
#             if rAct < rt:  # inner region
#                 strssAct = - (1 - distr_fact) * p_e * rt2 * (1 / (rt2 - ri2)) * (1 + ri2 / rAct2)
#
#             if rAct > rt:  # outer region
#                 strssAct = - distr_fact * p_e * rt2 * (1 / (re2 - rt2)) * (1 + re2 / rAct2)
#
#             if rAct == rt:  # region threshold
#                 stress_inner = - (1 - distr_fact) * p_e * rt2 * (1 / (rt2 - ri2)) * (1 + ri2 / rAct2)
#                 stress_outer = - distr_fact * p_e * rt2 * (1 / (re2 - rt2)) * (1 + re2 / rAct2)
#                 strssAct = (stress_inner + stress_outer) / 2
#
#             valMaxStrss = min(strssAct, valMaxStrss)
#             strnAct = strssAct / modulusTotal
#             matrixStrnPrstrss[i][j] = strnAct
#             if ((steelThick != 0) and (j < indSl)):
#                 matrixStrssPrstrss[i][j] = strnAct * modulusSteel
#             elif ((steelThickOut != 0) and (j >= indSl2)):
#                 matrixStrssPrstrss[i][j] = strnAct * modulusSteel
#             else:
#                 matrixStrssPrstrss[i][j] = strnAct * modulusConc
#         vectMaxStrssPrstrss[i] = valMaxStrss
#
#     matrixStrnPrstrss = predpeti * matrixStrnPrstrss
#     matrixStrssPrstrss = predpeti * matrixStrssPrstrss
#     vectMaxStrssPrstrss = predpeti * vectMaxStrssPrstrss
#
#     # DISER2 ^^^
#
#     print('===== Prestress ended. =====')