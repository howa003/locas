import numpy as np
from src.models import Structure, MeshSpace, MeshTime, Results, Loads
from pathlib import Path
from src.general_functions import double_print

def save_csv_file(data_object, folder_path, filename):
    """
    This function saves a numpy array into a CSV file.

    :param data_object: The data to be saved into the CSV file.
    :type data_object: numpy.ndarray
    :param folder_path: The path to the folder where the CSV file will be saved.
    :type folder_path: str
    :param filename: The name of the CSV file.
    :type filename: str
    :return: None
    """

    file_path = folder_path + '/' + filename
    np.savetxt(file_path, data_object, delimiter=";")
    pass


def save_results_into_csv(
        structure: Structure,
        results: Results) -> str:
    """
    This function saves the results of the calculations into CSV files.

    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    :param structure: A handle to the :class:`models.Structure` object containing information about the structure.
    :type structure: class:`Structure`
    :return: String indicating the successful/unsuccessful saving of the results into CSV files.
    :rtype: str
    """

    try:
        analysis_identifier = str(int(structure.temp_air_int)) + 'C_' + str(int(structure.duration)) + 's_' + str(int(structure.tendons_stress)) + 'MPa'
        folder_path = 'saved_data/' + analysis_identifier
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        double_print('Folder ' + folder_path + ' was created.')

        # Save the thermal stresses
        save_csv_file(results.stress_temp_fixed, folder_path, 'thermal_fixed.csv')
        save_csv_file(results.stress_temp_clamped, folder_path, 'thermal_clamped.csv')
        save_csv_file(results.stress_temp_free, folder_path, 'thermal_free.csv')

        # Save the internal-pressure stresses
        save_csv_file(results.stress_internal_pressure, folder_path, 'internal_pressure.csv')

        # Save the prestressing stresses
        save_csv_file(results.stress_prestressing, folder_path, 'prestressing.csv')

        # Save the total stresses
        save_csv_file(results.stress_total_fixed, folder_path, 'total_fixed.csv')
        save_csv_file(results.stress_total_clamped, folder_path, 'total_clamped.csv')
        save_csv_file(results.stress_total_free, folder_path, 'total_free.csv')

        # TODO: Save more results.

        result_message = "Results saved into CSV files successfully."

    except Exception as exception:
        result_message = "Saving of results into CSV files FAILED: " + str(exception)

    return result_message
