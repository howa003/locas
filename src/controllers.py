from src.models import Structure, MeshSpace
from src.calculations.temperatures.steadystate_heat_transfer import calc_operating_temperatures

# Define the function that will be called from the GUI
def run_analysis(gui_inputs):
    structure = Structure(gui_inputs)
    mesh_space = MeshSpace(structure)
    # print(structure.steel_thick_in)
    # print(mesh_space.node_ids)
    print(calc_operating_temperatures(structure, mesh_space))
    return 0
