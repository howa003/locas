from src.models import Structure, MeshSpace, MeshTime, Results, Loads
import numpy as np
import numpy.typing as npt
from src.calculations.stresses.general_functions import calc_stress_from_strain


def calc_thermal_stresses(
        structure: Structure,
        mesh_space: MeshSpace,
        mesh_time: MeshTime,
        loads: Loads,
        results: Results) -> str:

    try:
        mat_stress_fixed = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))
        mat_stress_clamped = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))
        mat_stress_free = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))

        mat_strain_theor = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))
        # mat_strain_fixed = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))
        mat_strain_clamped = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))
        mat_strain_free = np.zeros((int(mesh_time.time_steps_count + 1), int(mesh_space.node_count)))

        therm_coeff = structure.therm_expan_coeff
        poisson = structure.poisson

        for current_step in range(int(mesh_time.time_steps_count) + 1):
            curr_temps = results.temp_matrix[current_step]
            curr_temp_diff = np.zeros(int(mesh_space.node_count))

            # Calculate temperature differences for each node
            for j in mesh_space.nodes_range:
                curr_temp_diff[j] = (curr_temps[j] - results.temp_init[j])

            theor_strains_list = np.zeros(int(mesh_space.node_count))
            fixed_stresses_list = np.zeros(int(mesh_space.node_count))

            # Calculate fixed stresses for each node
            for j in mesh_space.nodes_range:
                theor_strain = float(curr_temp_diff[j] * therm_coeff)
                theor_strains_list[j] = theor_strain
                fixed_stress = - calc_stress_from_strain(theor_strain, j, mesh_space, structure)
                fixed_stresses_list[j] = fixed_stress

            mat_strain_theor[current_step] = theor_strains_list

            # print(current_step)
            # print(fixed_stresses_list)

            # Calculate thermal resultants
            normal_force = 0
            bending_moment = 0
            for j in mesh_space.element_range:
                stress = (fixed_stresses_list[j] + fixed_stresses_list[j + 1]) / 2
                force = stress * mesh_space.element_length * structure.width
                arm = (structure.center_of_section - mesh_space.element_centers[j])
                # print('Force1: ' + str(force))
                # print(arm)
                normal_force += force
                bending_moment += force * arm
                # print('Forces sum: ' + str(normal_force))
                # print(bending_moment)
            # print('Forces sum final: ' + str(normal_force))
            # print('Moment sum final: ' + str(bending_moment))

            # Calculate strain and curvature
            # TODO: Rollback to modulus_total
            strain = -normal_force / (structure.modulus_concrete * structure.area_of_section)
            curvature = -bending_moment / (structure.modulus_concrete * structure.inertia_of_section)

            # print(strain*1000000)
            # print(curvature*1000000)

            stresses_clamped_list = np.zeros(int(mesh_space.node_count))
            stresses_free_list = np.zeros(int(mesh_space.node_count))

            # Calculate clamped and free stresses for each node
            nodes_positions = mesh_space.nodes_positions
            for j in mesh_space.nodes_range:
                theor_strain = float(theor_strains_list[j])
                node_loc = nodes_positions[j]
                strain_real_clamped = strain
                strain_real_free = strain + curvature * (structure.center_of_section - node_loc)
                strain_prev_clamped = strain_real_clamped - theor_strain
                strain_prev_free = strain_real_free - theor_strain
                stresses_clamped_list[j] = calc_stress_from_strain(strain_prev_clamped, j, mesh_space, structure)
                stresses_free_list[j] = calc_stress_from_strain(strain_prev_free, j, mesh_space, structure)

            mat_strain_free[current_step] = strain_real_free
            mat_strain_clamped[current_step] = strain_real_clamped

            mat_stress_fixed[current_step] = (1 / (1 - poisson)) * fixed_stresses_list
            mat_stress_clamped[current_step] = (1 / (1 - poisson)) * stresses_clamped_list
            mat_stress_free[current_step] = (1 / (1 - poisson)) * stresses_free_list

        results.stress_temp_fixed = mat_stress_fixed
        results.stress_temp_clamped = mat_stress_clamped
        results.stress_temp_free = mat_stress_free

        results.strains_thermal_theoretical = mat_strain_theor
        results.strains_real_clamped = mat_strain_clamped
        results.strains_real_free = mat_strain_free

        # print(results.stress_temp_fixed[-1])
        # print(results.stress_temp_clamped[-1])
        # print(results.stress_temp_free[-1])

        result_message = "Thermal stresses calculated successfully."

    except Exception as exception:
        result_message = "Thermal stresses calculation FAILED: " + str(exception)

    return result_message














# print('===== Stress started. =====')
# matrixStrnF = zeros((steps + 1, nNode))
# matrixStrnR = zeros((steps + 1, nNode))
# matrixStrnD = zeros((steps + 1, nNode))  # Strain for free displacement (and fixed rotation)
# matrixStrssF = zeros((steps + 1, nNode))
# matrixStrss = zeros((steps + 1, nNode))
# matrixStrssD = zeros((steps + 1, nNode))  # Stress for free displacement (and fixed rotation)
#
# for i in range(steps + 1):
#     temp = matrixT[i]  # Vektor teplot v case t
#     tempDiff = zeros(nNode)  # Vektor zmen teplot od t=0
#     for j in nodesRange:
#         tempDiff[j] = (temp[j] - Tzaklad[j])
#
#     freeStrains = zeros(nNode)  # Volné pretvoreni od teploty
#     fixedStresses = zeros(nNode)  # Volné napeti od teploty
#     for j in nodesRange:
#         temperature = tempDiff[j]
#         freeStrain = temperature * thermExpan
#         freeStrains[j] = freeStrain
#         fixedStresses[j] = -freeStrain * modulusConc
#         if ((steelThick != 0) and (j < indSl)):
#             fixedStresses[j] = -freeStrain * modulusSteel
#         elif ((steelThickOut != 0) and (j >= indSl2)):
#             fixedStresses[j] = -freeStrain * modulusSteel
#
#     # Normalova sila a Moment
#     normalForce = 0  # MN
#     bendingMoment = 0  # MNm
#     for j in elemRange:
#         stress = (fixedStresses[j] + fixedStresses[j + 1]) / 2  # Pro Fixed-end
#         force = stress * Le * beznyMetr
#         normalForce = normalForce + force
#         bendingMoment = bendingMoment + force * (center - elemCenters[j])
#
#     # Skutecne pretvoreni a krivost
#     strain = -normalForce / (modulusConc * areaNahr)  # - = MN / (MPa*m2)
#     curvature = -bendingMoment / (modulusConc * inertiaNahr)  # 1/m = MNm / (MPa*m4)
#
#     # Real strain (free-end a free-displacement)
#     realStrains = zeros(nNode)
#     realStrainsDispl = zeros(nNode)
#     for j in nodesRange:
#         position = j * Le
#         realStrains[j] = strain - curvature * (position - center)  # free-end
#         realStrainsDispl[j] = strain  # free-displacement
#
#     # Real stress
#     realStress = zeros(nNode)
#     realStressDispl = zeros(nNode)
#     for j in nodesRange:
#         strainDiff = realStrains[j] - freeStrains[j]
#         strainDispl = realStrainsDispl[j] - freeStrains[
#             j]  # Strain difference for free displacement (and fixed rotation)
#         realStress[j] = strainDiff * modulusConc
#         realStressDispl[j] = strainDispl * modulusConc
#         if ((steelThick != 0) and (j < indSl)):
#             realStress[j] = strainDiff * modulusSteel
#             realStressDispl[j] = strainDispl * modulusSteel
#         elif ((steelThickOut != 0) and (j >= indSl2)):
#             realStress[j] = strainDiff * modulusSteel
#             realStressDispl[j] = strainDispl * modulusSteel
#
#     # Uprava pro zohledneni vlivu rovinneho chovani - tj. vydeleni (1-v) - DISER2
#     fixedStresses = (1 / (1 - poisson)) * fixedStresses  # Fixed-end napeti - DISER2
#     realStress = (1 / (1 - poisson)) * realStress  # Free-end napeti - DISER2
#     realStressDispl = (1 / (1 - poisson)) * realStressDispl  # Clamped-guided napeti - DISER2
#
#     # Lokalizace do matic
#     matrixStrnF[i] = freeStrains
#     matrixStrnR[i] = realStrains
#     matrixStrnD[i] = realStrainsDispl
#     matrixStrssF[i] = fixedStresses
#     matrixStrss[i] = realStress
#     matrixStrssD[i] = realStressDispl
#
#     if (i % (int(steps / 100) * printPercent) == 0):
#         print('[Stress] Time: ' + str(int(100 * i / steps)) + ' %')
#
# matrixTempStrssF = matrixStrssF
# matrixTempStrss = matrixStrss
# matrixTempStrssD = matrixStrssD
# print('===== Stress ended. =====')
