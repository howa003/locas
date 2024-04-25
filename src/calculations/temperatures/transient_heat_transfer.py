from src.models import Structure, MeshSpace, MeshTime, Results, Loads
import numpy as np
import numpy.typing as npt
from src.calculations.temperatures.material_properties import steel_conductivity, concrete_conductivity, steel_volumetric_heat_capacity, concrete_volumetric_heat_capacity
from src.calculations.temperatures.surface_heat_transfer_coefficient import calc_surface_heat_transfer_coef
import eel
from src.general_functions import get_timestamp
from src.general_functions import double_print

np.set_printoptions(linewidth=200)


def get_material_conductivity(temp: float, index: int, structure: Structure, mesh_space: MeshSpace) -> float:
    if structure.has_inner_steel and (index < mesh_space.slice_index_steel_in):
        return steel_conductivity(temp)
    elif structure.has_outer_steel and (index >= mesh_space.slice_index_steel_out):
        return steel_conductivity(temp)
    else:
        return concrete_conductivity(temp)


def create_element_conductivity_matrix(temp: float, index: int, structure: Structure, mesh_space: MeshSpace) -> npt.NDArray[np.float64]:
    material_conduc = get_material_conductivity(temp, index, structure, mesh_space)
    element_from_zero = mesh_space.element_centers_from_zero[index]
    element_matrix = element_from_zero * material_conduc * np.array([[1, -1], [-1, 1]]) / mesh_space.element_length
    return element_matrix


def create_global_conduc_mat(temp_vect: npt.NDArray[np.float64], mesh_space: MeshSpace, structure: Structure) -> npt.NDArray[np.float64]:
    global_matrix: npt.NDArray[np.float64] = np.zeros((mesh_space.node_count, mesh_space.node_count))
    for i in range(mesh_space.element_count):
        elem_mean_temp = (float(temp_vect[i]) + float(temp_vect[i + 1])) / 2
        element_matrix = create_element_conductivity_matrix(elem_mean_temp, i, structure, mesh_space)
        for j in range(2):
            for k in range(2):
                global_matrix[i + j, i + k] += element_matrix[j, k]
    return global_matrix


def get_material_capacity(temp: float, index: int, structure: Structure, mesh_space: MeshSpace) -> float:
    if structure.has_inner_steel and (index < mesh_space.slice_index_steel_in):
        return steel_volumetric_heat_capacity(temp)
    elif structure.has_outer_steel and (index >= mesh_space.slice_index_steel_out):
        return steel_volumetric_heat_capacity(temp)
    else:
        return concrete_volumetric_heat_capacity(temp, structure.density, structure.water_cont)


def create_element_capacity_matrix(temp: float, index: int, structure: Structure, mesh_space: MeshSpace) -> npt.NDArray[np.float64]:
    material_capacity: float = get_material_capacity(temp, index, structure, mesh_space)
    element_from_zero: float = mesh_space.element_centers_from_zero[index]
    element_matrix: npt.NDArray[np.float64] = element_from_zero * material_capacity * np.array([[1/3, 1/6], [1/6, 1/3]]) * mesh_space.element_length
    return element_matrix


def create_global_capac_mat(temp_vect: npt.NDArray[np.float64], mesh_space: MeshSpace, structure: Structure) -> npt.NDArray[np.float64]:
    global_matrix: npt.NDArray[np.float64] = np.zeros((mesh_space.node_count, mesh_space.node_count))
    for i in range(mesh_space.element_count):
        elem_mean_temp = (float(temp_vect[i]) + float(temp_vect[i + 1])) / 2
        element_matrix = create_element_capacity_matrix(elem_mean_temp, i, structure, mesh_space)
        for j in range(2):
            for k in range(2):
                global_matrix[i + j, i + k] += element_matrix[j, k]
    return global_matrix


def get_flux_vect(
        temp_distr: npt.NDArray[np.float64],
        temp_gas_in: float,
        structure: Structure,
        mesh_space: MeshSpace) -> npt.NDArray[np.float64]:
    temp_surf_in: float = float(temp_distr[0])
    temp_surf_out: float = float(temp_distr[-1])
    convection_coef_in = calc_surface_heat_transfer_coef(structure, temp_surf_in, temp_gas_in)
    convection_coef_out = calc_surface_heat_transfer_coef(structure, temp_surf_out, structure.temp_air_ext)
    convection_in = convection_coef_in * (temp_surf_in - temp_gas_in)
    convection_out = convection_coef_out * (temp_surf_out - structure.temp_air_ext)
    flux_vector: npt.NDArray[np.float64] = np.zeros(mesh_space.node_count)
    flux_vector[0] = convection_in * mesh_space.element_centers_from_zero[0]
    flux_vector[-1] = convection_out * mesh_space.element_centers_from_zero[-1]
    return flux_vector


def get_flux_vect_deriv(temp_distr: npt.NDArray[np.float64], temp_gas_in: float, structure: Structure, mesh_space: MeshSpace) -> npt.NDArray[np.float64]:
    temp_surf_in: float = float(temp_distr[0])
    temp_surf_out: float = float(temp_distr[-1])
    convection_coef_in = calc_surface_heat_transfer_coef(structure, temp_surf_in, temp_gas_in)
    convection_coef_out = calc_surface_heat_transfer_coef(structure, temp_surf_out, structure.temp_air_ext)
    convection_in_deriv = convection_coef_in
    convection_out_deriv = convection_coef_out
    flux_vector_deriv: npt.NDArray[np.float64] = np.zeros(mesh_space.node_count)
    flux_vector_deriv[0] = convection_in_deriv * mesh_space.element_centers_from_zero[0]
    flux_vector_deriv[-1] = convection_out_deriv * mesh_space.element_centers_from_zero[-1]
    return flux_vector_deriv


def get_residuum(
        conduc_mat: npt.NDArray[np.float64],
        capac_mat: npt.NDArray[np.float64],
        flux_vect: npt.NDArray[np.float64],
        ftr_temp_distr: npt.NDArray[np.float64],
        curr_temp_distr: npt.NDArray[np.float64],
        time_jump: float) -> npt.NDArray[np.float64]:
    residuum: npt.NDArray[np.float64] = capac_mat.dot((ftr_temp_distr - curr_temp_distr) / time_jump) + conduc_mat.dot(ftr_temp_distr) + flux_vect
    return residuum


def get_residuum_deriv(
        conduc_mat: npt.NDArray[np.float64],
        capac_mat: npt.NDArray[np.float64],
        flux_vect_deriv: npt.NDArray[np.float64],
        time_jump: float) -> npt.NDArray[np.float64]:
    residuum_deriv: npt.NDArray[np.float64] = capac_mat / time_jump + conduc_mat + flux_vect_deriv
    return residuum_deriv


def transient_heat_transfer(
        structure: Structure,
        mesh_space: MeshSpace,
        mesh_time: MeshTime,
        loads: Loads,
        results: Results) -> npt.NDArray[np.float64]:

    # In a given time step ("current step"), we calculate the temperature distribution for the next time step ("future time step") using the temperature distribution from the current time step.
    for current_step in mesh_time.time_steps_range:

        # 0) Print the progress
        ftr_step = current_step + 1
        ftr_time = mesh_time.time_axis[ftr_step]  # Time of the future time step
        progress_percent = int(1000 * ftr_step / mesh_time.time_steps_count)/10
        double_print('Calculating temperatures for time: ' + str(ftr_time) + ' s (step ' + str(ftr_step) + ' out of ' + str(mesh_time.time_steps_count) + '; ' + str(progress_percent) + '%)')

        # 1) Obtain the current temperatures and calculate the conductivity matrix and capacity matrix
        curr_temp_distr: npt.NDArray[np.float64] = results.temp_matrix[current_step]
        curr_conduc_mat: npt.NDArray[np.float64] = create_global_conduc_mat(curr_temp_distr, mesh_space, structure)
        curr_capac_mat: npt.NDArray[np.float64] = create_global_capac_mat(curr_temp_distr, mesh_space, structure)

        # 2) Create a first guess of the temperature distribution in the future time step
        ftr_temp_distr: npt.NDArray[np.float64] = np.copy(curr_temp_distr)  #

        # 3) Calculate the flux vector and its derivative in the future time step
        ftr_temp_gas = loads.get_current_air_temp(ftr_time)  # Temperature of the inner gas in the future time step
        flux_vect: npt.NDArray[np.float64] = get_flux_vect(ftr_temp_distr, ftr_temp_gas, structure, mesh_space)
        flux_vect_deriv: npt.NDArray[np.float64] = get_flux_vect_deriv(ftr_temp_distr, ftr_temp_gas, structure, mesh_space)

        # 4) Calculate the residua (errors) of the transient heat transfer matrix equation and residua of its derivation
        residuum_vect: npt.NDArray[np.float64] = get_residuum(curr_conduc_mat, curr_capac_mat, flux_vect, ftr_temp_distr, curr_temp_distr, mesh_time.time_to_next_step(current_step))
        residuum_vect_deriv: npt.NDArray[np.float64] = get_residuum_deriv(curr_conduc_mat, curr_capac_mat, flux_vect_deriv, mesh_time.time_to_next_step(current_step))
        max_residuum: float = np.amax(np.absolute(residuum_vect))

        # 5) If the error is large, we will make an adjustment to the temperatures in the future time step and recalculate the flux vector and its derivative
        while max_residuum > (1 / 1000):
            temp_corr = np.linalg.solve(residuum_vect_deriv, residuum_vect)
            ftr_temp_distr = ftr_temp_distr - temp_corr

            flux_vect = get_flux_vect(ftr_temp_distr, ftr_temp_gas, structure, mesh_space)
            flux_vect_deriv = get_flux_vect_deriv(ftr_temp_distr, ftr_temp_gas, structure, mesh_space)

            residuum_vect = get_residuum(curr_conduc_mat, curr_capac_mat, flux_vect, ftr_temp_distr, curr_temp_distr, mesh_time.time_to_next_step(current_step))
            residuum_vect_deriv = get_residuum_deriv(curr_conduc_mat, curr_capac_mat, flux_vect_deriv, mesh_time.time_to_next_step(current_step))
            max_residuum = np.amax(np.absolute(residuum_vect))

        # 6) Save the final future temperature distribution into the temperature matrix
        results.temp_matrix[current_step + 1] = ftr_temp_distr

    # TODO: Simplify the algorithm by moving the first guess of the future temperature distribution to the beginning of the loop
    # TODO: Modify the calculation (use sparse matrices) to improve the performance of the algorithm

    return results.temp_matrix



