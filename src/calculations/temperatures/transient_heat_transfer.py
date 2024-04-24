from src.models import Structure, MeshSpace, MeshTime, Results, Loads
import numpy as np
import numpy.typing as npt
from src.calculations.temperatures.material_properties import steel_conductivity, concrete_conductivity

np.set_printoptions(linewidth=200)


def get_material_conductivity(temp: float, index: int, structure: Structure, mesh_space: MeshSpace) -> float:
    print(mesh_space.slice_index_steel_in)
    if structure.has_inner_steel and (index < mesh_space.slice_index_steel_in):
        print('steel in')
        return steel_conductivity(temp)
    elif structure.has_outer_steel and (index >= mesh_space.slice_index_steel_out):
        return steel_conductivity(temp)
    else:
        return concrete_conductivity(temp)


def create_element_conductivity_matrix(temp: float, index: int, structure: Structure, mesh_space: MeshSpace) -> npt.NDArray[np.float64]:
    mat_conduc = get_material_conductivity(temp, index, structure, mesh_space)
    element_from_zero = mesh_space.element_centers_from_zero[index]
    element_matrix = element_from_zero * mat_conduc * np.matrix('1 -1; -1 1') / mesh_space.element_length
    print(element_matrix)
    return element_matrix


def create_conduc_mat(temp_vect: npt.NDArray[np.float64], mesh_space: MeshSpace, structure: Structure) -> npt.NDArray[np.float64]:
    global_matrix: npt.NDArray[np.float64] = np.zeros((mesh_space.node_count, mesh_space.node_count))
    for i in range(mesh_space.element_count):
        elem_mean_temp = (float(temp_vect[i]) + float(temp_vect[i + 1])) / 2
        element_matrix = create_element_conductivity_matrix(elem_mean_temp, i, structure, mesh_space)
        for j in range(2):
            for k in range(2):
                global_matrix[i + j, i + k] += element_matrix[j, k]
    return global_matrix



def transient_heat_transfer(structure: Structure, mesh_space: MeshSpace, mesh_time: MeshTime, loads: Loads, results: Results) -> None:
    for current_step in mesh_time.time_steps_range:
        curr_temps_vect: npt.NDArray[np.float64] = results.temp_matrix[current_step]
        curr_conduc_mat: npt.NDArray[np.float64] = create_conduc_mat(curr_temps_vect, mesh_space, structure)

        # TODO: Continue here

        # capac_mat = get_capac_mat(curr_temps, mesh_space, structure, results)
        #
        # time_jump = get_time_step(mesh_time, current_step)
        #
        # time = time + time_jump
        #
        # ftr_temp_gas = evol_temp(time)
        # ftr_temps = curr_temps_vect
        #
        # flux_vect = get_flux_vect(ftr_temps, ftr_temp_gas, structure)
        # flux_vect_dx = get_flux_vect_deriv(ftr_temps, ftr_temp_gas, structure)
        #
        # resid_vect = get_residuum(conduc_mat, capac_mat, flux_vect, ftr_temps, curr_temps, time_jump)
        # resid_vect_dx = get_residuum_dx(conduc_mat, capac_mat, flux_vect_dx, time_jump)
        # resid_max = numpy.amax(numpy.absolute(resid_vect))
        #
        # while resid_max > (1 / 1000):
        #     ftr_temp_corr = numpy.linalg.solve(resid_vect_dx, resid_vect)
        #     ftr_temps = ftr_temps - ftr_temp_corr
        #
        #     flux_vect = get_flux_vect(ftr_temps, ftr_temp_gas, structure)
        #     flux_vect_dx = get_flux_vect_deriv(ftr_temps, ftr_temp_gas, structure)
        #
        #     resid_vect = get_residuum(conduc_mat, capac_mat, flux_vect, ftr_temps, curr_temps, time_jump)
        #     resid_vect_dx = get_residuum_dx(conduc_mat, capac_mat, flux_vect_dx, time_jump)
        #     resid_max = numpy.amax(numpy.absolute(resid_vect))
        #
        # results.temp_matrix[current_step + 1] = ftr_temps

    pass







#
#
#
# def specific_algorithm_transient():
#     for i in range(steps):
#         # 0) Začínáme na i=0.
#         # 1) V daném časovém kroku (nyní) stanovíme teploty Tn a matice K a C.
#         # 1) Stanovíme čas a teplotu požáru v budoucím časovém kroku
#         # 2) Do Tnts (Temperature next time step) vkládáme jako první odhad teploty v t=0.
#         # 4) Vypočítáme F a dF pro teploty v budoucím časovém kroku.
#         # 5) Určíme residuum (chybu).
#         # 6) Pokud je chyba velká, uděláme úpravu Tnts (Tnts = Tnts - R/dR) a přepočítáme 4) a 5).
#         # 7) Pokračujeme na i=i+1.
#
#         Tn = matrixT[i]  # tempertature now; teploty nyní (v čase i)
#         K = matrixK(Tn)  # matice vodivosti nyní (v čase i)
#         C = matrixC(Tn)  # matice kapacity nyní (v čase i)
#
#         if (time < t1):
#             dt = dt1
#         elif (time < t2):
#             dt = dt2
#         elif (time < t3):
#             dt = dt3
#         elif (time < t4):
#             dt = dt4
#         elif (time < t5):
#             dt = dt5
#
#         time = tim
#         e + dt
#
#         if (i % (int(step s / 100) * printPercent) == 0):
#             print('[Temperature] Time:  ' + str(int(tim
#             e / 6 ) / 10 ) +' minutes ( ' + str(int(10
#             0 * i / steps) ) +' %)')
#             eel.print_status('[' + str(datetime.datetime.now().strftime("%H:%M:%S")) + '] [Temperature] Time: ' + str
#             (int(time / 6) / 10) + ' minutes (' + str(int(100 * i / steps)) + ' %)')()
#         ftrAirTemp = airTemp(time)  # teplota požáru v budoucím časovém kroku i+1
#         airTempVect[i + 1] = ftrAirTemp
#         airPressVect[i + 1] = prssSftCoef
#         f * fnctAirTlak(time)
#
#         htcFvect[i + 1] = 1 / clcRprestup(Lair, emiss, sbc, Tn[0], ftrAirTemp)
#         htcCvect[i + 1] = 1 / clcRprestup(Lair, emiss, sbc, Tn[-1], Te)
#
#         Tnts = matrixT[i]  # první odhad budoucích teplot (teploty v čase i+1)
#         F = vectorF(Tnts, ftrAirTemp)  # vektor toků v čase i+1
#         dF = vectordF(Tnts, ftrAirTemp)  # derivace vektoru toků v čase i+1
#
#         R = C.dot((Tnts - Tn) / dt) + K.dot(Tnts) + F  # vektor residua
#         dR = C / dt + K + dF  # derivace vektoru residua
#         maximum = amax(absolute(R))  # největší hodnodnota ve vektoru residua
#
#         pocitadlo = 0
#         while maximum > (1 / 1000):
#             dX = linalg.solve(dR, R)  # změna teplot Tnts (Newton method)
#             Tnts = Tnts - dX  # oprava teplot Tnts
#
#             F = vectorF(Tnts, ftrAirTemp)  # vektor toků v čase i+1
#             dF = vectordF(Tnts, ftrAirTemp)  # derivace vektoru toků v čase i+1
#
#             R = C.dot((Tnts - Tn) / dt) + K.dot(Tnts) + F
#             dR = C / dt + K + dF
#             maximum = amax(absolute(R))
#         matrixT[i + 1] = Tnts  # Uložení teplot v čase i+1 do matice teplot
#         tempGradVect[i + 1] = Tnts[0] - Tnts[-1]
#     print('===== Temperature ended. =====')
#
#
#
#
# def general_algorithm_transient():
#     time: int = 0
#     for i in range(int(time_mesh['step_count'])):
#         curr_temps = temp_mat[i]
#         conduc_mat = get_conduc_mat(curr_temps, space_mesh, inputs, geometry)
#         capac_mat = get_capac_mat(curr_temps, space_mesh, inputs, geometry)
#
#         time_jump = get_time_step(time, time_mesh)
#
#         time = time + time_jump
#
#         ftr_temp_gas = evol_temp(time)
#         ftr_temps = curr_temps
#
#         flux_vect = get_flux_vect(ftr_temps, ftr_temp_gas, inputs)
#         flux_vect_dx = get_flux_vect_deriv(ftr_temps, ftr_temp_gas, inputs)
#
#         resid_vect = get_residuum(conduc_mat, capac_mat, flux_vect, ftr_temps, curr_temps, time_jump)
#         resid_vect_dx = get_residuum_dx(conduc_mat, capac_mat, flux_vect_dx, time_jump)
#         resid_max = numpy.amax(numpy.absolute(resid_vect))
#
#         while resid_max > (1 / 1000):
#             ftr_temp_corr = numpy.linalg.solve(resid_vect_dx, resid_vect)
#             ftr_temps = ftr_temps - ftr_temp_corr
#
#             flux_vect = get_flux_vect(ftr_temps, ftr_temp_gas, inputs)
#             flux_vect_dx = get_flux_vect_deriv(ftr_temps, ftr_temp_gas, inputs)
#
#             resid_vect = get_residuum(conduc_mat, capac_mat, flux_vect, ftr_temps, curr_temps, time_jump)
#             resid_vect_dx = get_residuum_dx(conduc_mat, capac_mat, flux_vect_dx, time_jump)
#             resid_max = numpy.amax(numpy.absolute(resid_vect))
#
#         temp_mat[i + 1] = ftr_temps



# # Matice vodivosti K a kapacity C
# def matrixK(vectorT):
#     struct = zeros((nNode,nNode))                          # matice konstrukce
#     for i in elemID:                                       # Výpočet matice prvku a její lokalizace od matice konstrukce
#         tempElem = (vectorT[i]+vectorT[i+1])/2
#         matConduc = conduc(tempElem)                       # vodivost betonu
#         if ((steelThick != 0) and (i <= (indSl-1))):
#             matConduc = conducSteel(tempElem)                   # vodivost oceli
#         elif ((steelThickOut != 0) and (i >= (indSl2))):
#             matConduc = conducSteel(tempElem)                   # vodivost oceli
#         element = matConduc * matrix([[1, -1],[-1, 1]]) / Le  # matice prvku; W/Km2
#         if (radialni == 1):
#             element = vectElemCentAbs[i] * element
#         struct[i,i] = struct[i,i] + element[0,0]
#         struct[i,i+1] = struct[i,i+1]+element[0,1]
#         struct[i+1,i] = struct[i+1,i]+element[1,0]
#         struct[i+1,i+1] = struct[i+1,i+1]+element[1,1]
#     return struct
#
# def matrixC(vectorT):
#     struct = zeros((nNode,nNode))                         # matice konstrukce
#     for i in elemID:                                      # výpočet matice prvku a její lokalizace od matice konstrukce
#         tempElem = (vectorT[i]+vectorT[i+1])/2
#         matVHC = volHeatCap(tempElem)                     # objemová teplotní kapacita betonu
#         if ((steelThick != 0) and (i <= (indSl-1))):
#             matVHC = volHeatCapSteel(tempElem)                 # objemová teplotní kapacita oceli
#         elif ((steelThickOut != 0) and (i >= (indSl2))):
#             matVHC = volHeatCapSteel(tempElem)                 # objemová teplotní kapacita oceli
#         element = matVHC * matrix([[1/3, 1/6],[1/6, 1/3]]) * Le # matice elementu; Ws/Km3
#         if (radialni == 1):
#             element = vectElemCentAbs[i] * element
#         struct[i,i] = struct[i,i] + element[0,0]
#         struct[i,i+1] = struct[i,i+1]+element[0,1]
#         struct[i+1,i] = struct[i+1,i]+element[1,0]
#         struct[i+1,i+1] = struct[i+1,i+1]+element[1,1]
#     return struct