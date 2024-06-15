from src.models import Structure, MeshSpace, MeshTime, Results
from pathlib import Path
from src.general_functions import double_print
import os
from src.calculations.outputs.figures.stress_evolutions import plot_stress_evolutions
from src.calculations.outputs.figures.stress_distributions import plot_stress_distributions


def plot_all_figures(structure: Structure, results: Results, mesh_space: MeshSpace, mesh_time: MeshTime) -> str:
    """
    This function plots all the figures.

    :param structure: A handle to the :class:`models.Structure` object containing information about the structure.
    :type structure: class:`Structure`
    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    :param mesh_space: A handle to the :class:`models.MeshSpace` object containing information about the space mesh.
    :type mesh_space: class:`MeshSpace`
    :param mesh_time: A handle to the :class:`models.MeshTime` object containing information about the time mesh.
    :type mesh_time: class:`MeshTime`
    :return: String indicating the successful/unsuccessful saving of the figures.
    :rtype: str
    """

    # try: # TODO: uncomment try and except
    folder_path = os.path.join('analysis_results', results.analysis_identifier, 'figures')
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    double_print('Folder ' + folder_path + ' was created.')

    # Plot the stress distributions when minimal stress (maximal tension) is reached in concrete
    plot_stress_distributions(folder_path,
                              'stress_distributions_concrete_tension.png',
                              'Stress distributions when maximal tension in concrete is reached',
                              results.extreme_steps['min_stress_fixed_concrete'],
                              results.extreme_steps['min_stress_clamped_concrete'],
                              results.extreme_steps['min_stress_free_concrete'],
                              structure, results, mesh_space, mesh_time)

    # Plot the stress distributions when maximal stress (maximal compression) is reached in concrete
    plot_stress_distributions(folder_path,
                              'stress_distributions_concrete_compression.png',
                              'Stress distributions when maximal compression in concrete is reached',
                              results.extreme_steps['max_stress_fixed_concrete'],
                              results.extreme_steps['max_stress_clamped_concrete'],
                              results.extreme_steps['max_stress_free_concrete'],
                              structure, results, mesh_space, mesh_time)

    # Plot the stress distributions when minimal stress (maximal tension) is reached in inner steel
    plot_stress_distributions(folder_path,
                              'stress_distributions_steel_inner_tension.png',
                              'Stress distributions when maximal tension in inner steel is reached',
                              results.extreme_steps['min_stress_fixed_steel_inner'],
                              results.extreme_steps['min_stress_clamped_steel_inner'],
                              results.extreme_steps['min_stress_free_steel_inner'],
                              structure, results, mesh_space, mesh_time)

    # Plot the stress distributions when maximal stress (maximal compression) is reached in inner steel
    plot_stress_distributions(folder_path,
                              'stress_distributions_steel_inner_compression.png',
                              'Stress distributions when maximal compression in inner steel is reached',
                              results.extreme_steps['max_stress_fixed_steel_inner'],
                              results.extreme_steps['max_stress_clamped_steel_inner'],
                              results.extreme_steps['max_stress_free_steel_inner'],
                              structure, results, mesh_space, mesh_time)

    # Plot the stress evolutions in the structure
    plot_stress_evolutions(folder_path,
                           'stress_evolutions.png',
                           'Evolutions of minimal/maximal stresses in the structure',
                           results, mesh_time)


    # TODO: Plot more figures and add gif creation

    result_message = "Figures saved successfully."

    # except Exception as exception:
    #     result_message = "Plotting of figures FAILED: " + str(exception)

    return result_message


