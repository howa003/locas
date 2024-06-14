"""
This module contains general functions for stress calculations.
"""

from src.models import Structure, MeshSpace, MeshTime
import numpy.typing as npt
import numpy as np


def init_empty_space_time_matrix(mesh_space: MeshSpace, mesh_time: MeshTime) -> npt.NDArray[np.float64]:
    """
    This function initializes an empty (zeros) space-time matrix.
    """
    return np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)), dtype=float)


def init_empty_space_array(mesh_space: MeshSpace) -> npt.NDArray[np.float64]:
    """
    This function initializes an empty (zeros) space array.
    """
    return np.zeros(int(mesh_space.node_count), dtype=float)


def init_empty_time_array(mesh_time: MeshTime) -> npt.NDArray[np.int64]:
    """
    This function initializes an empty (zeros) time array.
    """
    return np.zeros(int(mesh_time.time_steps_count + 1), dtype=float)


def concrete_stress_distribution(stress_distribution: npt.NDArray[np.float64], mesh_space: MeshSpace, structure: Structure) -> npt.NDArray[np.float64]:
    """
    This function obtains the stress distribution for concrete.
    """
    # TODO: Merge with split_concrete_and_steel
    index_1 = int(1 + mesh_space.slice_index_steel_in)
    index_2 = int(1 + mesh_space.slice_index_steel_out)
    if structure.has_inner_steel and structure.has_outer_steel:
        stress_distribution_concrete = stress_distribution[index_1:index_2]
    elif structure.has_inner_steel:
        stress_distribution_concrete = stress_distribution[index_1:]
    elif structure.has_outer_steel:
        stress_distribution_concrete = stress_distribution[:index_2]
    else:
        stress_distribution_concrete = stress_distribution
    return stress_distribution_concrete


def split_array_concrete_and_steel(array_total: npt.NDArray[np.float64], mesh_space: MeshSpace, structure: Structure) -> list:
    """
    This function splits the array of values for whole thickness
    into separate arrays for inner steel liner, concrete, and outer steel liner.
    """
    index_1 = int(1 + mesh_space.slice_index_steel_in)
    index_2 = int(1 + mesh_space.slice_index_steel_out)
    if structure.has_inner_steel and structure.has_outer_steel:
        array_steel_inner = array_total[:index_1]
        array_concrete = array_total[index_1:index_2]
        array_steel_outer = array_total[index_2:]
    elif structure.has_inner_steel:
        array_steel_inner = array_total[:index_1]
        array_concrete = array_total[index_1:]
        array_steel_outer = []
    elif structure.has_outer_steel:
        array_steel_inner = []
        array_concrete = array_total[:index_2]
        array_steel_outer = array_total[index_2:]
    else:
        array_steel_inner = []
        array_concrete = array_total
        array_steel_outer = []
    return [array_steel_inner, array_concrete, array_steel_outer]


def split_matrix_concrete_and_steel(matrix_total: npt.NDArray[np.float64], mesh_space: MeshSpace, structure: Structure) -> list:
    """
    This function splits the matrix of values for whole thickness (columns) and duration of LOCA (rows)
    into separate matrices for inner steel liner, concrete, and outer steel liner.
    """

    index_1 = int(1 + mesh_space.slice_index_steel_in)
    index_2 = int(1 + mesh_space.slice_index_steel_out)
    if structure.has_inner_steel and structure.has_outer_steel:
        matrix_steel_inner = matrix_total[:, :index_1]
        matrix_concrete = matrix_total[:, index_1:index_2]
        matrix_steel_outer = matrix_total[:, index_2:]
    elif structure.has_inner_steel:
        matrix_steel_inner = matrix_total[:, :index_1]
        matrix_concrete = matrix_total[:, index_1:]
        matrix_steel_outer = []
    elif structure.has_outer_steel:
        matrix_steel_inner = []
        matrix_concrete = matrix_total[:, :index_2]
        matrix_steel_outer = matrix_total[:, index_2:]
    else:
        matrix_steel_inner = []
        matrix_concrete = matrix_total
        matrix_steel_outer = []
    return [matrix_steel_inner, matrix_concrete, matrix_steel_outer]



def calc_stress_from_strain(strain: float, index: int, mesh_space: MeshSpace, structure: Structure) -> float:
    if structure.has_inner_steel and (index <= mesh_space.slice_index_steel_in):
    # TODO: Rollback to: if structure.has_inner_steel and (index < mesh_space.slice_index_steel_in):
        modulus = structure.modulus_steel
    elif structure.has_outer_steel and (index >= mesh_space.slice_index_steel_out):
        modulus = structure.modulus_steel
    else:
        modulus = structure.modulus_concrete
    return strain * modulus
