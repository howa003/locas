from src.calculations.stresses.general_functions import split_matrix_concrete_and_steel
from src.models import Structure, MeshSpace, Results
import numpy.typing as npt
import numpy as np


def row_with_max_value(matrix: npt.NDArray[np.float64]) -> int:
    """
    This function finds the row in a matrix with the maximum value.
    """
    return np.argmax(np.amax(matrix, axis=1))


def row_with_min_value(matrix: npt.NDArray[np.float64]) -> int:
    """
    This function finds the row in a matrix with the minimum value.
    """
    return np.argmin(np.amin(matrix, axis=1))


def merge_tensile_and_compressive_stresses(
        stresses_tensile: npt.NDArray[np.float64],
        stresses_compressive: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """
    This function merges the compressive and tensile stresses into one array.
    If the maximal tensile stress is positive, the tensile stresses are taken.
    Otherwise, the compressive stresses are taken.

    :param stresses_tensile: The tensile stresses.
    :type stresses_tensile: numpy array
    :param stresses_compressive: The compressive stresses.
    :type stresses_compressive: numpy array
    :return: The merged stresses.
    :rtype: numpy array
    """
    stresses_merged = np.copy(stresses_tensile)
    for i in range(len(stresses_merged)):
        if stresses_merged[i] < 0:
            stresses_merged[i] = stresses_compressive[i]
    return stresses_merged


def create_submatrices(structure: Structure, mesh_space: MeshSpace, results: Results) -> None:

    # Split the temperature matrix into matrices for steel and concrete
    temperatures = results.temp_matrix
    temperatures_split = split_matrix_concrete_and_steel(temperatures, mesh_space, structure)
    results.temp_matrix_steel_inner = temperatures_split[0]
    results.temp_matrix_concrete = temperatures_split[1]
    results.temp_matrix_steel_outer = temperatures_split[2]

    # Split the fixed stress matrix into matrices for steel and concrete
    stresses_fixed = results.stress_total_fixed
    stresses_fixed_split = split_matrix_concrete_and_steel(stresses_fixed, mesh_space, structure)
    results.stress_fixed_steel_inner = stresses_fixed_split[0]
    results.stress_fixed_concrete = stresses_fixed_split[1]
    results.stress_fixed_steel_outer = stresses_fixed_split[2]

    # Split the clamped stress matrix into matrices for steel and concrete
    stresses_clamped = results.stress_total_clamped
    stresses_clamped_split = split_matrix_concrete_and_steel(stresses_clamped, mesh_space, structure)
    results.stress_clamped_steel_inner = stresses_clamped_split[0]
    results.stress_clamped_concrete = stresses_clamped_split[1]
    results.stress_clamped_steel_outer = stresses_clamped_split[2]

    # Split the free stress matrix into matrices for steel and concrete
    stresses_free = results.stress_total_free
    stresses_free_split = split_matrix_concrete_and_steel(stresses_free, mesh_space, structure)
    results.stress_free_steel_inner = stresses_free_split[0]
    results.stress_free_concrete = stresses_free_split[1]
    results.stress_free_steel_outer = stresses_free_split[2]

    # TODO: Add strains? Maybe not necessary for now.

    return None


def find_extreme_steps(results: Results) -> None:
    """
    This function finds the steps in which the extreme values of
    temperatures and stresses and strains are reached.

    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    """

    results.extreme_steps['max_internal_pressure'] = np.argmax(results.pres_air_int_vect)
    results.extreme_steps['max_temp_air'] = np.argmax(results.temp_air_int_vect)

    results.extreme_steps['max_temp_concrete'] = row_with_max_value(results.temp_matrix_concrete)
    results.extreme_steps['max_temp_steel'] = row_with_max_value(results.temp_matrix_steel_inner)

    results.extreme_steps['max_stress_fixed_concrete'] = row_with_max_value(results.stress_fixed_concrete)
    results.extreme_steps['max_stress_fixed_steel_inner'] = row_with_max_value(results.stress_fixed_steel_inner)
    results.extreme_steps['max_stress_clamped_concrete'] = row_with_max_value(results.stress_clamped_concrete)
    results.extreme_steps['max_stress_clamped_steel_inner'] = row_with_max_value(results.stress_clamped_steel_inner)
    results.extreme_steps['max_stress_free_concrete'] = row_with_max_value(results.stress_free_concrete)
    results.extreme_steps['max_stress_free_steel_inner'] = row_with_max_value(results.stress_free_steel_inner)

    results.extreme_steps['min_stress_fixed_concrete'] = row_with_max_value(results.stress_fixed_concrete)
    results.extreme_steps['min_stress_fixed_steel_inner'] = row_with_max_value(results.stress_fixed_steel_inner)
    results.extreme_steps['min_stress_clamped_concrete'] = row_with_max_value(results.stress_clamped_concrete)
    results.extreme_steps['min_stress_clamped_steel_inner'] = row_with_max_value(results.stress_clamped_steel_inner)
    results.extreme_steps['min_stress_free_concrete'] = row_with_max_value(results.stress_free_concrete)
    results.extreme_steps['min_stress_free_steel_inner'] = row_with_max_value(results.stress_free_steel_inner)

    return None


def create_stress_evolutions(results: Results) -> None:
    """
    This function creates arrays with evolutions of minimal and maximal stresses for steel and concrete.

    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    """

    # Evolution of maximal stress (maximal tension) in concrete
    results.stress_evolution_concrete_tension_fixed = np.amax(results.stress_fixed_concrete, axis=1)
    results.stress_evolution_concrete_tension_clamped = np.amax(results.stress_clamped_concrete, axis=1)
    results.stress_evolution_concrete_tension_free = np.amax(results.stress_free_concrete, axis=1)

    # Evolution of minimal stress (maximal compression) in concrete
    results.stress_evolution_concrete_compression_fixed = np.amin(results.stress_fixed_concrete, axis=1)
    results.stress_evolution_concrete_compression_clamped = np.amin(results.stress_clamped_concrete, axis=1)
    results.stress_evolution_concrete_compression_free = np.amin(results.stress_free_concrete, axis=1)

    # Evolution of maximal stress (maximal tension) in steel
    results.stress_evolution_steel_tension_fixed = np.amax(results.stress_fixed_steel_inner, axis=1)
    results.stress_evolution_steel_tension_clamped = np.amax(results.stress_clamped_steel_inner, axis=1)
    results.stress_evolution_steel_tension_free = np.amax(results.stress_free_steel_inner, axis=1)

    # Evolution of minimal stress (maximal compression) in steel
    results.stress_evolution_steel_compression_fixed = np.amin(results.stress_fixed_steel_inner, axis=1)
    results.stress_evolution_steel_compression_clamped = np.amin(results.stress_clamped_steel_inner, axis=1)
    results.stress_evolution_steel_compression_free = np.amin(results.stress_free_steel_inner, axis=1)

    # Evolution of extreme stress in steel
    results.stress_evolution_steel_merged_fixed = merge_tensile_and_compressive_stresses(results.stress_evolution_steel_tension_fixed, results.stress_evolution_steel_compression_fixed)
    results.stress_evolution_steel_merged_clamped = merge_tensile_and_compressive_stresses(results.stress_evolution_steel_tension_clamped, results.stress_evolution_steel_compression_clamped)
    results.stress_evolution_steel_merged_free = merge_tensile_and_compressive_stresses(results.stress_evolution_steel_tension_free, results.stress_evolution_steel_compression_free)

    return None


def process_results(structure: Structure, mesh_space: MeshSpace, results: Results) -> str:
    """
    This function processes the results of the analysis.
    """
    try:
        # Create separate submatrices for steel and concrete
        create_submatrices(structure, mesh_space, results)

        # Find the steps with extreme values
        find_extreme_steps(results)

        # Create arrays with evolutions of minimal and maximal stresses for steel and concrete
        create_stress_evolutions(results)

        result_message = "Results processes successfully."

    except Exception as exception:
        result_message = "Processing of results FAILED: " + str(exception)

    return result_message

