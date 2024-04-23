from src.models import Structure, MeshSpace
from src.calculations.temperatures.material_properties import steel_conductivity, concrete_conductivity
import numpy as np
from src.calculations.temperatures.surface_heat_transfer_coefficient import calc_surface_resistance


def calc_operating_temperatures(structure: Structure, mesh_space: MeshSpace) -> list[float]:
    temp_air_int = structure.temp_air_int
    temp_air_ext = structure.temp_air_ext
    temp_surf_int = temp_air_int
    temp_surf_ext = temp_air_ext
    while True:
        temperature_distribution = calc_steady_state_heat_transfer(structure, mesh_space, temp_surf_int, temp_surf_ext)
        temp_surf_int_new = temperature_distribution[0]
        temp_surf_ext_new = temperature_distribution[-1]
        error = max(abs(temp_surf_int_new - temp_surf_int), abs(temp_surf_ext_new - temp_surf_ext))
        if error < 0.01:
            break
        else:
            temp_surf_int = temp_surf_int_new
            temp_surf_ext = temp_surf_ext_new
    return temperature_distribution


def calc_steady_state_heat_transfer(structure: Structure, mesh_space: MeshSpace, temp_surf_int: float, temp_surf_ext: float) -> list[float]:
    steel_thick_in = structure.steel_thick_in
    steel_thick_out = structure.steel_thick_out
    concrete_thick = structure.concrete_thick
    char_len = structure.char_len
    emissivity = structure.emissivity
    t_mean = (temp_surf_int + temp_surf_ext) / 2
    steel_in_resistance = steel_thick_in / steel_conductivity(temp_surf_int)
    steel_out_resistance = steel_thick_out / steel_conductivity(temp_surf_ext)
    concrete_resistance = concrete_thick / concrete_conductivity(t_mean)
    temp_air_int = structure.temp_air_int
    temp_air_ext = structure.temp_air_ext
    resistance_air_in = calc_surface_resistance(char_len, emissivity, temp_surf_int, temp_air_int)
    resistance_air_out = calc_surface_resistance(char_len, emissivity, temp_surf_ext, temp_air_ext)
    matrix_steady_state = np.array(
        [
            [-resistance_air_in, -1, 0, 0, 0],
            [-steel_in_resistance, 1, -1, 0, 0],
            [-concrete_resistance, 0, 1, -1, 0],
            [-steel_out_resistance, 0, 0, 1, -1],
            [-resistance_air_out, 0, 0, 0, 1]
        ]
    )
    vector_steady_state = np.array([-temp_air_int, 0, 0, 0, temp_air_ext])
    result_steady_state = np.linalg.solve(matrix_steady_state, vector_steady_state)
    temp_surf_int_new = result_steady_state[1]  # Temperature at the inner surface of the steel liner is in the second position because the first position is the heat flux
    temp_concrete_int = result_steady_state[2]
    temp_concrete_ext = result_steady_state[3]
    temp_surf_ext_new = result_steady_state[4]

    nodes_range = mesh_space.nodes_range
    node_count = mesh_space.node_count
    slice_index_steel_in = mesh_space.slice_index_steel_in
    slice_index_steel_out = mesh_space.slice_index_steel_out
    element_length = mesh_space.element_length
    temperature_distribution = np.zeros(node_count)
    for i in nodes_range:
        if steel_thick_in != 0 and i < slice_index_steel_in:
            temperature_distribution[i] = temp_surf_int_new - (i * element_length / steel_thick_in) * (temp_surf_int_new - temp_concrete_int)
        elif steel_thick_out != 0 and i >= slice_index_steel_out:
            temperature_distribution[i] = temp_concrete_ext - ((i * element_length - steel_thick_in - concrete_thick) / steel_thick_out) * (temp_concrete_ext - temp_surf_ext_new)
        else:
            temperature_distribution[i] = temp_concrete_int - ((i * element_length - steel_thick_in) / concrete_thick) * (temp_concrete_int - temp_concrete_ext)
    return temperature_distribution.tolist()


