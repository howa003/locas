from src.models import Structure, MeshSpace, MeshTime, Results, Loads
from src.calculations.temperatures.steadystate_heat_transfer import calc_operating_temperatures
import eel
from src.general_functions import get_timestamp
from src.calculations.temperatures.surface_heat_transfer_coefficient import calc_surface_resistance
import numpy as np
from src.calculations.temperatures.transient_heat_transfer import transient_heat_transfer
from src.general_functions import double_print
from src.calculations.stresses.thermal_stresses import calc_thermal_stresses
from src.calculations.stresses.internal_pressure_stresses import calculate_pressure_stresses
from src.calculations.stresses.prestressing_stresses import calc_circumferential_stress
from src.calculations.stresses.total_stresses import sum_all_stresses
from src.calculations.outputs.data_files import save_results_into_csv


# Define the function that will be called from the GUI
def run_analysis(gui_inputs):
    try:
        double_print('Python function started.')
        double_print('Loading inputs...')

        # Prepare the data for the analysis
        structure = Structure(gui_inputs)
        mesh_space = MeshSpace(structure)
        mesh_time = MeshTime(structure)

        # Initialize the loads object
        loads = Loads(structure)

        # Initialize the results object
        results = Results(mesh_space, mesh_time)

        double_print('Inputs loaded.')

        # Calculate the distribution of initial temperatures in the wall
        results.temp_init = np.full(mesh_space.node_count, structure.temp_init, dtype=float)

        # Calculate the distribution of operating temperatures in the wall
        results.temp_oper = calc_operating_temperatures(structure, mesh_space)

        # Fill results from time_step = 0 (i.e., operating temperatures)
        # TODO: Refactor this part (make it a separate function)
        results.temp_air_int_vect[0] = loads.temp_air_int_0
        results.pres_air_int_vect[0] = loads.get_current_air_pres(0)
        results.temp_grad_vect[0] = (float(results.temp_oper[0]) - float(results.temp_oper[-1]))
        results.heat_coef_int_vect[0] = 1 / calc_surface_resistance(structure, float(results.temp_oper[0]), loads.temp_air_int_0)
        results.heat_coef_ext_vect[0] = 1 / calc_surface_resistance(structure, float(results.temp_oper[-1]), loads.temp_air_ext_0)
        results.temp_matrix[0] = results.temp_oper
        # print(results.temp_matrix[0])
        # print(results.temp_matrix[1])

        double_print('Calculation of transient heat transfer started.')
        double_print(transient_heat_transfer(structure, mesh_space, mesh_time, loads, results))

        double_print('Calculation of thermal stresses started.')
        double_print(calc_thermal_stresses(structure, mesh_space, mesh_time, loads, results))

        double_print('Calculation of internal-pressure stresses started.')
        double_print(calculate_pressure_stresses(structure, mesh_space, mesh_time, loads, results))

        double_print('Calculation of prestressing stresses started.')
        double_print(calc_circumferential_stress(structure, mesh_space, mesh_time, loads, results))

        double_print('Calculation of total stresses started.')
        double_print(sum_all_stresses(results))

        # Save the results into CSV files
        double_print('Saving results into CSV files...')
        double_print(save_results_into_csv(structure, results))

        # TODO: Print graphs

        double_print('Python function finished.')

        return 0
    except FileNotFoundError as exception:
        error_message = str(exception)
        print(error_message)
        return error_message
