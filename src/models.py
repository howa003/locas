from config import PHASE_ENDS_MAX


class Structure:
    """
    Class for storing information about the structure.
    """

    def __init__(
        self,
        gui_inputs: dict,
    ) -> None:
        self.steel_thick_in = gui_inputs.get('steel_thick')
        self.concrete_thick = gui_inputs.get('concrete_thick')
        self.steel_thick_out = 0  # Outer steel liner is not used in the software
        self.radius_in = gui_inputs.get('radius_in')
        self.tendons_stress = gui_inputs.get('tendons_stress')
        self.tendons_area = gui_inputs.get('tendons_area')
        self.density = gui_inputs.get('density')
        self.water_cont = gui_inputs.get('water_cont')
        self.therm_expan_coeff = gui_inputs.get('therm_expan_coeff')
        self.modulus_concrete = gui_inputs.get('modulus_concrete')
        self.modulus_steel = gui_inputs.get('modulus_steel')
        self.emissivity = gui_inputs.get('emissivity')
        self.char_len = gui_inputs.get('char_len')
        self.poisson = gui_inputs.get('poisson')
        self.step_space = gui_inputs.get('step_space')
        self.width = 1  # meter
        self.t_init = gui_inputs.get('t_init')
        self.temp_air_int = gui_inputs.get('t_in')
        self.temp_air_ext = gui_inputs.get('t_out')
        self.duration = gui_inputs.get('duration')
        self.pressure_ext = gui_inputs.get('pressure_ext')
        self.step_time_1 = gui_inputs.get('step_time_1')
        self.step_time_2 = gui_inputs.get('step_time_2')
        self.step_time_3 = gui_inputs.get('step_time_3')
        self.step_time_4 = gui_inputs.get('step_time_4')
        self.step_time_5 = gui_inputs.get('step_time_5')

    @property
    def length(self) -> float:
        return self.steel_thick_in + self.concrete_thick

    @property
    def modulus_ratio(self) -> float:
        return self.modulus_steel / self.modulus_concrete

    def modulus_total(self) -> float:
        return (self.modulus_concrete * self.concrete_thick + self.modulus_steel * (self.steel_thick_in + self.steel_thick_out)) / self.length

    @property
    def section_characteristics(self) -> tuple[float, float]:
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
        return c_tot, i_tot

    @property
    def center_of_section(self) -> float:
        return self.section_characteristics[0]

    @property
    def inertia_of_section(self) -> float:
        return self.section_characteristics[1]


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
    def x_axis_thickness(self) -> list[float]:
        return [1000 * node_id * self.element_length for node_id in self.node_ids]

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
    def slice_index_steel_in(self) -> int:
        return int((self.steel_thick / self.element_length) + 1)

    @property
    def slice_index_steel_out(self) -> int:
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
    def time_axis(self) -> list[float]:
        phase_1_end = min(PHASE_ENDS_MAX[0], self.duration)
        phase_2_end = min(PHASE_ENDS_MAX[1], self.duration)
        phase_3_end = min(PHASE_ENDS_MAX[2], self.duration)
        phase_4_end = min(PHASE_ENDS_MAX[3], self.duration)
        time = 0
        time_axis = []
        while time < self.duration:
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
        return time_axis

    @property
    def time_steps_count(self) -> int:
        return int(len(self.time_axis))







class Loads:
    """
    Class for storing information about the loads.
    """

    def __init__(
        self,
        gui_inputs: dict,
    ) -> None:
        self.t_init = gui_inputs.get('t_init')
        self.t_in = gui_inputs.get('t_in')
        self.t_out = gui_inputs.get('t_out')
        self.duration = gui_inputs.get('duration')
        self.pressure_ext = gui_inputs.get('pressure_ext')
        self.step_time_1 = gui_inputs.get('step_time_1')
        self.step_time_2 = gui_inputs.get('step_time_2')
        self.step_time_3 = gui_inputs.get('step_time_3')
        self.step_time_4 = gui_inputs.get('step_time_4')
        self.step_time_5 = gui_inputs.get('step_time_5')
