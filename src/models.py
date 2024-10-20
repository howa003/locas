from config import PHASE_ENDS_MAX, SOURCE_DATA_FOLDER_PATH, TEMP_EVOL_FILE, PRES_EVOL_FILE
from scipy.interpolate import interp1d
import pandas as pd
import os
import eel
import numpy as np
import numpy.typing as npt


class Structure:
    """
    Class for storing information about the structure.
    """

    def __init__(
        self,
        gui_inputs: dict,
    ) -> None:
        self.steel_thick_in: float = float(gui_inputs.get('steel_thick'))
        self.concrete_thick: float = float(gui_inputs.get('concrete_thick'))
        self.steel_thick_out: float = 0.0  # Outer steel liner is not used in the software
        self.radius_in: float = float(gui_inputs.get('radius_in'))
        self.tendons_stress: float = float(gui_inputs.get('tendons_stress'))
        self.tendons_area: float = float(gui_inputs.get('tendons_area'))
        self.density: float = float(gui_inputs.get('density'))
        self.water_cont: float = float(gui_inputs.get('water_cont'))
        self.therm_expan_coeff: float = float(gui_inputs.get('therm_expan_coeff'))
        self.modulus_concrete: float = float(gui_inputs.get('modulus_concrete'))
        self.modulus_steel: float = float(gui_inputs.get('modulus_steel'))
        self.emissivity: float = float(gui_inputs.get('emissivity'))
        self.char_len: float = float(gui_inputs.get('char_len'))
        self.poisson: float = float(gui_inputs.get('poisson'))
        self.step_space: float = float(gui_inputs.get('step_space'))
        self.width: float = 1.0  # meter
        self.temp_init: float = float(gui_inputs.get('t_init'))
        self.temp_air_int: float = float(gui_inputs.get('t_in'))
        self.temp_air_ext: float = float(gui_inputs.get('t_out'))
        self.duration: float = float(gui_inputs.get('duration'))
        self.pressure_ext: float = float(gui_inputs.get('pressure_ext'))
        self.pressure_coeff: float = float(gui_inputs.get('pressure_coeff'))
        self.step_time_1: float = float(gui_inputs.get('step_time_1'))
        self.step_time_2: float = float(gui_inputs.get('step_time_2'))
        self.step_time_3: float = float(gui_inputs.get('step_time_3'))
        self.step_time_4: float = float(gui_inputs.get('step_time_4'))
        self.step_time_5: float = float(gui_inputs.get('step_time_5'))

    @property
    def radius_tendons(self) -> float:
        return self.radius_in + self.length/2  # TODO: Change this to an input.

    @property
    def has_inner_steel(self) -> bool:
        return self.steel_thick_in > 0

    @property
    def has_outer_steel(self) -> bool:
        return self.steel_thick_out > 0

    @property
    def length(self) -> float:
        return self.steel_thick_in + self.concrete_thick + self.steel_thick_out

    @property
    def radius_out(self) -> float:
        return self.radius_in + self.length

    @property
    def modulus_ratio(self) -> float:
        return self.modulus_steel / self.modulus_concrete

    @property
    def modulus_total(self) -> float:
        return float((self.modulus_concrete * self.concrete_thick + self.modulus_steel * (self.steel_thick_in + self.steel_thick_out)) / self.length)

    @property
    def section_characteristics(self) -> tuple[float, float, float]:
        b1 = self.width * self.modulus_ratio
        b2 = self.width
        b3 = b1
        h1 = self.steel_thick_in
        h2 = self.concrete_thick
        h3 = 0  # Outer steel liner is not used in the software
        a1 = h1 * b1
        a2 = h2 * b2
        a3 = h3 * b3
        a_tot = a1 + a2 + a3
        c1 = h1 / 2
        c2 = h1 + h2 / 2
        c3 = h1 + h2 + h3 / 2
        c_tot = (a1 * c1 + a2 * c2 + a3 * c3) / a_tot
        i1 = b1 * h1 ** 3 / 12
        i2 = b2 * h2 ** 3 / 12
        i3 = b3 * h3 ** 3 / 12
        d1 = a1 * (c_tot - c1) ** 2
        d2 = a2 * (c_tot - c2) ** 2
        d3 = a3 * (c_tot - c3) ** 2
        i_tot = i1 + i2 + i3 + d1 + d2 + d3
        return c_tot, i_tot, a_tot

    @property
    def center_of_section(self) -> float:
        return self.section_characteristics[0]

    @property
    def inertia_of_section(self) -> float:
        return self.section_characteristics[1]

    @property
    def area_of_section(self) -> float:
        return self.section_characteristics[2]


class MeshSpace:
    """
    Class for storing information about the spatial mesh.
    """

    def __init__(
        self,
        structure: Structure,
    ) -> None:
        self.element_length = structure.step_space
        self.total_length = structure.length
        self.radius_in = structure.radius_in
        self.steel_thick = structure.steel_thick_in
        self.steel_thick_out = structure.steel_thick_out

    @property
    def element_count(self) -> int:
        return int(self.total_length / self.element_length)

    @property
    def node_count(self) -> int:
        return int(self.element_count + 1)

    @property
    def element_ids(self) -> list[int]:
        return list(range(int(self.element_count)))

    @property
    def node_ids(self) -> list[int]:
        return self.element_ids + [int(self.element_count)]

    @property
    def x_axis_thickness(self) -> npt.NDArray[np.float64]:
        return np.array([1000 * node_id * self.element_length for node_id in self.node_ids])

    @property
    def nodes_range(self) -> range:
        return range(int(self.node_count))

    @property
    def nodes_positions(self) -> list[float]:
        return [i * self.element_length for i in self.nodes_range]

    @property
    def element_range(self) -> range:
        return range(int(self.element_count))

    @property
    def element_centers(self) -> list[float]:
        return [i * self.element_length + self.element_length / 2 for i in self.element_range]

    @property
    def element_centers_from_zero(self) -> list[float]:
        return [element_center + self.radius_in for element_center in self.element_centers]

    @property
    def node_centers_from_zero(self) -> list[float]:
        return [node_center + self.radius_in for node_center in self.nodes_positions]

    @property
    def slice_index_steel_in(self) -> int:
        return int(self.steel_thick / self.element_length)

    @property
    def slice_index_steel_out(self) -> int:
        '''
        Returns the index of the element where the outer steel liner ends.
        If there is no outer steel liner, returns the total number of elements.
        :return:
        '''
        return int((self.total_length - self.steel_thick_out) / self.element_length)



class MeshTime:
    """
    Class for storing information about the temporal mesh.
    """

    def __init__(
        self,
        structure: Structure,
    ) -> None:
        self.duration = structure.duration
        self.step_time_1 = structure.step_time_1
        self.step_time_2 = structure.step_time_2
        self.step_time_3 = structure.step_time_3
        self.step_time_4 = structure.step_time_4
        self.step_time_5 = structure.step_time_5

    @property
    def time_axis(self) -> npt.NDArray[np.float64]:
        # Note that the time axis contains the initial time (0) and the final time (duration)
        phase_1_end = min(PHASE_ENDS_MAX[0], self.duration)
        phase_2_end = min(PHASE_ENDS_MAX[1], self.duration)
        phase_3_end = min(PHASE_ENDS_MAX[2], self.duration)
        phase_4_end = min(PHASE_ENDS_MAX[3], self.duration)
        time = 0
        time_axis = []
        while time <= self.duration:
            time_axis.append(time)
            if time < phase_1_end:
                time += self.step_time_1
            elif time < phase_2_end:
                time += self.step_time_2
            elif time < phase_3_end:
                time += self.step_time_3
            elif time < phase_4_end:
                time += self.step_time_4
            else:
                time += self.step_time_5
        return np.array(time_axis)

    @property
    def time_steps_count(self) -> int:
        # Note that time steps are -1 compared to the time axis because step 0 is the already known initial state.
        # Moreover, in transient heat transfer, each time step we calculate the temperatures in the next step. Therefore, temperatures at time=duration are calculated in next-to-last step.
        # Thus, stresses (thermal, ipi, and cpi) need to be calculated for time_steps_count+1
        return int(len(self.time_axis)-1)

    @property
    def time_steps_range(self) -> range:
        return range(int(self.time_steps_count))

    def time_to_next_step(self, current_step: int) -> float:
        time_axis = self.time_axis
        return time_axis[current_step + 1] - time_axis[current_step]








class Loads:
    """
    Class for storing information about the loads.
    """

    def __init__(
        self,
        structure: Structure,
    ) -> None:
        self.temp_init = structure.temp_init
        self.temp_air_int_0 = structure.temp_air_int
        self.temp_air_ext_0 = structure.temp_air_ext
        self.evol_air_temp_int: interp1d = self.__internal_air_evolution(TEMP_EVOL_FILE)
        self.evol_air_pres_int: interp1d = self.__internal_air_evolution(PRES_EVOL_FILE)

    @staticmethod
    def __internal_air_evolution(evolution_file: str) -> interp1d:
        file_path: str = SOURCE_DATA_FOLDER_PATH + evolution_file
        if not os.path.isfile(file_path):
            error_message: str = 'ERROR: File ' + evolution_file + ' is missing in folder ' + SOURCE_DATA_FOLDER_PATH
            raise FileNotFoundError(error_message)
        else:
            excel_table = pd.read_excel(file_path, header=None)
            x_axis = excel_table.iloc[:, 0].to_numpy()
            y_axis = excel_table.iloc[:, 1].to_numpy()
            return interp1d(x_axis, y_axis)

    def get_current_air_temp(self, time: float) -> float:
        return float(self.evol_air_temp_int(time))

    def get_current_air_pres(self, time: float) -> float:
        return float(self.evol_air_pres_int(time))

class Results:
    """
    Class for storing results.
    """

    def __init__(
        self,
        mesh_space: MeshSpace,
        mesh_time: MeshTime,
    ) -> None:
        self.analysis_identifier: str = ''
        self.duration: float = mesh_time.duration
        self.temp_init: npt.NDArray[np.float64] = np.zeros(mesh_space.node_count, dtype=float)
        self.temp_oper: npt.NDArray[np.float64] = np.zeros(mesh_space.node_count, dtype=float)
        self.temp_air_int_vect: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.temp_grad_vect: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.pres_air_int_vect: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.heat_coef_int_vect: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.heat_coef_ext_vect: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.temp_matrix: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.temp_matrix_steel_inner: npt.NDArray[np.float64] = np.array([])
        self.temp_matrix_concrete: npt.NDArray[np.float64] = np.array([])
        self.temp_matrix_steel_outer: npt.NDArray[np.float64] = np.array([])
        self.strains_thermal_theoretical: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_temp_fixed: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_temp_clamped: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_temp_free: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_internal_pressure: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.strain_internal_pressure: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_prestressing: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.strain_prestressing: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.strains_real_fixed: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_total_fixed: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_fixed_steel_inner: npt.NDArray[np.float64] = np.array([])
        self.stress_fixed_concrete: npt.NDArray[np.float64] = np.array([])
        self.stress_fixed_steel_outer: npt.NDArray[np.float64] = np.array([])
        self.strains_real_clamped: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_total_clamped: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_clamped_steel_inner: npt.NDArray[np.float64] = np.array([])
        self.stress_clamped_concrete: npt.NDArray[np.float64] = np.array([])
        self.stress_clamped_steel_outer: npt.NDArray[np.float64] = np.array([])
        self.strains_real_free: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_total_free: npt.NDArray[np.float64] = np.zeros((mesh_time.time_steps_count + 1, mesh_space.node_count), dtype=float)
        self.stress_free_steel_inner: npt.NDArray[np.float64] = np.array([])
        self.stress_free_concrete: npt.NDArray[np.float64] = np.array([])
        self.stress_free_steel_outer: npt.NDArray[np.float64] = np.array([])
        self.stress_evolution_concrete_tension_fixed: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_concrete_tension_clamped: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_concrete_tension_free: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_tension_fixed: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_tension_clamped: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_tension_free: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_concrete_compression_fixed: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_concrete_compression_clamped: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_concrete_compression_free: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_compression_fixed: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_compression_clamped: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_compression_free: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_merged_fixed: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_merged_clamped: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.stress_evolution_steel_merged_free: npt.NDArray[np.float64] = np.zeros(mesh_time.time_steps_count + 1, dtype=float)
        self.extreme_steps: dict[str, int] = {
            'max_internal_pressure': 0,
            'max_temp_air': 0,
            'max_temp_steel_inner': 0,
            'max_temp_concrete': 0,
            'max_stress_fixed_concrete': 0,
            'max_stress_clamped_concrete': 0,
            'max_stress_free_concrete': 0,
            'max_stress_fixed_steel_inner': 0,
            'max_stress_clamped_steel_inner': 0,
            'max_stress_free_steel_inner': 0,
            'min_stress_fixed_concrete': 0,
            'min_stress_clamped_concrete': 0,
            'min_stress_free_concrete': 0,
            'min_stress_fixed_steel_inner': 0,
            'min_stress_clamped_steel_inner': 0,
            'min_stress_free_steel_inner': 0,
        }

    @property
    def label_time(self) -> str:
        if self.duration <= 60 * 60:
            return str(int(self.duration / 60)) + 'm'
        return str(int(self.duration / (60 * 60))) + 'h'