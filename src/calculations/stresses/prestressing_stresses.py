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


def calc_stress_inner_region(distr_fact: float, p_e: float, rt: float, ri: float, r_act: float) -> float:
    '''
    This function calculates the prestressing stress in a given node in the inner region of the wall.

    :param distr_fact: The distribution factor.
    :type distr_fact: float
    :param p_e: The prestressing force.
    :type p_e: float
    :param rt: The radius of the tendons.
    :type rt: float
    :param ri: The inner radius of the structure.
    :type ri: float
    :param r_act: The radius in the node.
    :type r_act: float
    :return: The stress in the given node induced by concrete prestressing.
    :rtype: float
    '''
    stress_act = - (1 - distr_fact) * p_e * rt**2 * (1 / (rt**2 - ri**2)) * (1 + ri**2 / r_act**2)
    return stress_act


def calc_stress_outer_region(distr_fact: float, p_e: float, rt: float, re: float, r_act: float) -> float:
    '''
    This function calculates the prestressing stress in a given node in the outer region of the wall.

    :param distr_fact: The distribution factor.
    :type distr_fact: float
    :param p_e: The prestressing force.
    :type p_e: float
    :param rt: The radius of the tendons.
    :type rt: float
    :param re: The outer radius of the structure.
    :type re: float
    :param r_act: The radius in the node.
    :type r_act: float
    :return: The stress in the given node induced by concrete prestressing.
    :rtype: float
    '''
    stress_act = - distr_fact * p_e * rt**2 * (1 / (re**2 - rt**2)) * (1 + re**2 / r_act**2)
    return stress_act


def calc_node_stress(
        distr_fact: float,
        p_e: float,
        rt: float,
        ri: float,
        re: float,
        r_act: float) -> float:
    '''
    This function calculates the prestressing stress in a given node in the wall according to Acharya and Menon (2003).

    :param distr_fact: The distribution factor.
    :type distr_fact: float
    :param p_e: The prestressing force.
    :type p_e: float
    :param rt: The radius of the tendons.
    :type rt: float
    :param ri: The inner radius of the structure.
    :type ri: float
    :param re: The outer radius of the structure.
    :type re: float
    :param r_act: The radius in the node.
    :type r_act: float
    :return: The stress in the given node induced by concrete prestressing.
    :rtype: float
    '''

    if r_act < rt:
        stress = calc_stress_inner_region(distr_fact, p_e, rt, ri, r_act)
    elif r_act == rt:
        stress_inner = calc_stress_inner_region(distr_fact, p_e, rt, ri, r_act)
        stress_outer = calc_stress_outer_region(distr_fact, p_e, rt, re, r_act)
        stress = (stress_inner + stress_outer) / 2
    else:  # r_act > rt
        stress = calc_stress_outer_region(distr_fact, p_e, rt, re, r_act)

    return stress


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

    try:
        pt = structure.tendons_stress
        at = structure.tendons_area
        ri = structure.radius_in
        re = structure.radius_out
        rt = structure.radius_tendons

        p_e = pt * at / rt  # Prestressing force [N/m2]

        distr_fact = calc_distr_factor(structure)

        # Initialize the arrays for the stresses and strains
        array_strain_prestressing = init_empty_space_array(mesh_space)
        array_stress_prestressing = init_empty_space_array(mesh_space)

        # Calculate the prestressing stresses
        node_centers_list = mesh_space.node_centers_from_zero
        for node in mesh_space.nodes_range:
            r_node = node_centers_list[node]

            stress_acharya = calc_node_stress(distr_fact, p_e, rt, ri, re, r_node)

            strain_act = stress_acharya / structure.modulus_total
            array_strain_prestressing[node] = strain_act

            real_stress = calc_stress_from_strain(strain_act, node, mesh_space, structure)
            array_stress_prestressing[node] = real_stress

        # Evolution of the maximal prestressing in concrete
        max_stress_concrete_evol = init_empty_time_array(mesh_time)
        max_stress_concrete_evol.fill(min(concrete_stress_distribution(array_stress_prestressing, mesh_space, structure)))

        # Save the results into the results object.
        results.strain_prestressing[:] = array_strain_prestressing
        results.stress_prestressing[:] = array_stress_prestressing

        result_message = "Prestressing stresses calculated successfully."

    except Exception as exception:
        result_message = "Prestressing stresses calculation FAILED: " + str(exception)

    return result_message





