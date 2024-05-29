from src.models import Structure, MeshSpace, MeshTime, Results, Loads
import numpy as np
import numpy.typing as npt

'''
This module contains the functions for calculating the stresses caused by the internal pressure.

In steps, the module calculates the stresses caused by the internal pressure.
The stresses are calculated for each node of the mesh and for each time step.

Note for GitHub Copilot: We will refactor the code commented below.
'''

#
# print('===== Overpressure started. =====')
# ri = polomerVnitrni
# re = ri + length
# ri2 = ri * ri
# re2 = re * re
# matrixStrnOvrprss = zeros((steps + 1, nNode))
# matrixStrssOvrprss = zeros((steps + 1, nNode))
# vectStrnOvrprss = zeros((nNode))
# vectStrssOvrprss = zeros((nNode))
# vectMaxStrssOvrprss = zeros((steps + 1))
# for i in range(steps + 1):
#     pi = airPressVect[i]
#     maxStrssOvrprss = 0
#     for j in range(nNode):
#         rAct = ri + (j * Le)
#         strssAct = ((pi * ri2 - pe * re2) / (re2 - ri2)) + ((pi - pe) * re2 * ri2 / ((re2 - ri2) * rAct * rAct))
#         strnAct = strssAct / modulusTotal
#         vectStrnOvrprss[j] = strnAct
#         if ((steelThick != 0) and (j < indSl)):
#             vectStrssOvrprss[j] = strnAct * modulusSteel
#         elif ((steelThickOut != 0) and (j >= indSl2)):
#             vectStrssOvrprss[j] = strnAct * modulusSteel
#         else:
#             vectStrssOvrprss[j] = strnAct * modulusConc
#             maxStrssOvrprss = max(strnAct * modulusConc, maxStrssOvrprss)
#     matrixStrnOvrprss[i] = vectStrnOvrprss
#     matrixStrssOvrprss[i] = vectStrssOvrprss
#     vectMaxStrssOvrprss[i] = maxStrssOvrprss
#
# matrixStrnOvrprss = pretlak * matrixStrnOvrprss
# matrixStrssOvrprss = pretlak * matrixStrssOvrprss
# vectMaxStrssOvrprss = pretlak * vectMaxStrssOvrprss
# print('===== Overpressure ended. =====')



def calculate_pressure_stresses(
        structure: Structure,
        mesh_space: MeshSpace,
        mesh_time: MeshTime,
        loads: Loads,
        results: Results) -> str:

    try:
        # Initialize the matrices for the stresses and strains
        matrix_strain_pressure = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))
        matrix_stress_pressure = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))
        vector_strain_pressure = np.zeros((int(mesh_space.node_count)))
        vector_stress_pressure = np.zeros((int(mesh_space.node_count)))



    except Exception as exception:
        error_message = str(exception)
        print(error_message)
        return error_message



















