import numpy as np
from src.models import Structure, MeshSpace, MeshTime, Results, Loads
from pathlib import Path
from src.general_functions import double_print
import csv
import json
import os


def save_object_properties(folder_name, obj) -> None:
    """
    This function saves the properties of an object into CSV files.

    :param folder_name: The name of the folder where the CSV files will be saved.
    :type folder_name: str
    :param obj: The object whose properties will be saved.
    :type obj: class:`object`
    """

    # Iterate over each attribute in the object
    for attr_name in obj.__dict__:
        values = getattr(obj, attr_name)
        file_path = os.path.join(folder_name, f"{attr_name}.csv")

        # Write the attribute values into individual CSV files
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')

            if isinstance(values, (int, float, str)):
                # Wrap the value in a list
                writer.writerow([values])
            elif isinstance(values, dict):
                # Write each dictionary key-value pair on a new row
                for key, val in values.items():
                    writer.writerow([key, val])
            elif isinstance(values, list):
                # Write the list as rows in the CSV file
                writer.writerow(values)
            elif isinstance(values, np.ndarray):
                if values.ndim == 1:
                    # Write the entire 1D array as one row
                    writer.writerow(values)
                elif values.ndim >= 2:
                    # Write each row of the 2D (or higher) array
                    for row in values:
                        writer.writerow(row)
            else:
                double_print(f"Skipped: {attr_name} was not saved as it has an unsupported type of {type(values)}.")


def save_results_into_csv(
        results: Results) -> str:
    """
    This function saves the results of the calculations into CSV files.

    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    :return: String indicating the successful/unsuccessful saving of the results into CSV files.
    :rtype: str
    """

    try:
        folder_path = os.path.join('analysis_results', results.analysis_identifier, 'csv_files')
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        double_print('Folder ' + folder_path + ' was created.')

        save_object_properties(folder_path, results)

        result_message = "Results saved into CSV files successfully."

    except Exception as exception:
        result_message = "Saving of results into CSV files FAILED: " + str(exception)

    return result_message
