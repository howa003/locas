from src.models import Structure, MeshSpace, MeshTime, Results, Loads
from pathlib import Path
from src.general_functions import double_print
import matplotlib.pyplot as plt


# Plot průběhu napětí v konstrukci v daných časech
def plot_stress_distributions(folder_path, file_name, figure_title, step_fixed, step_clamped, step_free, structure: Structure, results: Results) -> str:
    """
    This function plots the stress distributions in the structure at given time steps.

    :param folder_path: The path to the folder where the figure will be saved.
    :type folder_path: str
    :param file_name: The name of the saved file.
    :type file_name: str
    :param figure_title: The title of the figure.
    :type figure_title: str
    :param step_fixed: The time step for the fixed boundary condition.
    :type step_fixed: int
    :param step_clamped: The time step for the clamped boundary condition.
    :type step_clamped: int
    :param step_free: The time step for the free boundary condition.
    :type step_free: int
    :param structure: A handle to the :class:`models.Structure` object containing information about the structure.
    :type structure: class:`Structure`
    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    :return: String indicating the successful/unsuccessful saving of the figure.
    :rtype: str
    """

    # >>>>> Plot declaration <<<<<
    plt.figure(figsize=(16 ,7), dpi=300)
    plt.suptitle(figure_title, fontsize=16)


    # >>>>> Label selection and min/max value calculation <<<<<
    if (strssType == 'T'):
        nameLabel = 'StrssCncrTnsn'
    elif (strssType == 'C'):
        nameLabel = 'StrssCncrCmprsn'
    elif (strssType == 'ST'):
        nameLabel = 'StrssStlTnsn'
    elif (strssType == 'SC'):
        nameLabel = 'StrssStlCmprsn'
    elif (strssType == 'PRESURE'):
        nameLabel = 'StrssMaxPreStrss'
    elif (strssType == 'TIME0'):
        nameLabel = 'StrssInT0'
    elif (strssType == 'TIME0temp'):
        nameLabel = 'StrssInT0temp'
    elif (strssType == 'FIXED'):
        nameLabel = 'StrssAtTime'

    yAxisMin = int((min(min(strssFxE) ,min(strssFrL) ,min(strssFrE) ) /1 ) -1)
    yAxisMax = int((max(max(strssFxE) ,max(strssFrL) ,max(strssFrE) ) /1 ) +1)

    # >>>>> x-axis declaration <<<<<
    xAxisVal = xAxisThick
    xAxisMax = max(xAxisVal)
    xAxisVal1 = cropVectSteelIn(xAxisVal)
    xAxisVal2 = cropVectConcr(xAxisVal)
    xAxisVal3 = cropVectSteelOut(xAxisVal)

    # >>>>> Subplot FxE for time step with max stress <<<<<
    plt.subplot(1, 3, 1)
    timeStep = stepFxE
    plotTime = xAxisTime[timeStep]
    plt.title('Stress for fixed BC in  ' +str(datetime.timedelta(seconds=plotTime)))

    yAxisVal = strssFxE
    yAxisVal1 = cropVectSteelIn(yAxisVal)
    yAxisVal2 = cropVectConcr(yAxisVal)
    yAxisVal3 = cropVectSteelOut(yAxisVal)

    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.grid()
    plt.plot(xAxisVal2, yAxisVal2, 'b--', label = 'Stress in concrete: <' + numToStr1dec(amin(yAxisVal2)) + ',' + numToStr1dec
                 (amax(yAxisVal2)) + '> MPa', clip_on=False)
    if (steelThick != 0):
        plt.plot(array([xAxisVal1[-1] ,xAxisVal2[0]]), array([yAxisVal1[-1] ,yAxisVal2[0]]), linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])
        plt.plot(xAxisVal1, yAxisVal1, 'r-', label = 'Stress in inner steel: <' + numToStr1dec(amin(yAxisVal1)) + ',' + numToStr1dec
                     (amax(yAxisVal1)) + '> MPa', clip_on=False)
    if (steelThickOut != 0):
        plt.plot(array([xAxisVal2[-1] ,xAxisVal3[0]]), array([yAxisVal2[-1] ,yAxisVal3[0]]), linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])
        plt.plot(xAxisVal3, yAxisVal3, 'g-', label = 'Stress in outer steel: <' + numToStr1dec(amin(yAxisVal3)) + ',' + numToStr1dec
                     (amax(yAxisVal3)) + '> MPa', clip_on=False)
    plt.ylabel('Stress [MPa]')
    plt.xlabel('Thickness [mm]')
    plt.xlim((0, xAxisMax))
    plt.ylim((yAxisMin, yAxisMax))
    plt.legend(loc='lower right')

    # >>>>> Subplot FrL for time step with max stress <<<<<
    plt.subplot(1, 3, 2)
    timeStep = stepFrL
    plotTime = xAxisTime[timeStep]
    plt.title('Stress for clamped-guided BC in  ' +str(datetime.timedelta(seconds=plotTime)))

    yAxisVal = strssFrL
    yAxisVal1 = cropVectSteelIn(yAxisVal)
    yAxisVal2 = cropVectConcr(yAxisVal)
    yAxisVal3 = cropVectSteelOut(yAxisVal)

    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.grid()
    plt.plot(xAxisVal2, yAxisVal2, 'b--', label = 'Stress in concrete: <' + numToStr1dec(amin(yAxisVal2)) + ',' + numToStr1dec
                 (amax(yAxisVal2)) + '> MPa', clip_on=False)
    if (steelThick != 0):
        plt.plot(array([xAxisVal1[-1] ,xAxisVal2[0]]), array([yAxisVal1[-1] ,yAxisVal2[0]]), linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])
        plt.plot(xAxisVal1, yAxisVal1, 'r-', label = 'Stress in inner steel: <' + numToStr1dec(amin(yAxisVal1)) + ',' + numToStr1dec
                     (amax(yAxisVal1)) + '> MPa', clip_on=False)
    if (steelThickOut != 0):
        plt.plot(array([xAxisVal2[-1] ,xAxisVal3[0]]), array([yAxisVal2[-1] ,yAxisVal3[0]]), linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])
        plt.plot(xAxisVal3, yAxisVal3, 'g-', label = 'Stress in outer steel: <' + numToStr1dec(amin(yAxisVal3)) + ',' + numToStr1dec
                     (amax(yAxisVal3)) + '> MPa', clip_on=False)
    plt.ylabel('Stress [MPa]')
    plt.xlabel('Thickness [mm]')
    plt.xlim((0, xAxisMax))
    plt.ylim((yAxisMin, yAxisMax))
    plt.legend(loc='lower right')

    # >>>>> Subplot FrE for time step with max stress <<<<<
    plt.subplot(1, 3, 3)
    timeStep = stepFrE
    plotTime = xAxisTime[timeStep]
    plt.title('Stress for free BC in  ' +str(datetime.timedelta(seconds=plotTime)))

    yAxisVal = strssFrE
    yAxisVal1 = cropVectSteelIn(yAxisVal)
    yAxisVal2 = cropVectConcr(yAxisVal)
    yAxisVal3 = cropVectSteelOut(yAxisVal)

    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.grid()
    plt.plot(xAxisVal2, yAxisVal2, 'b--', label = 'Stress in concrete: <' + numToStr1dec(amin(yAxisVal2)) + ',' + numToStr1dec
                 (amax(yAxisVal2)) + '> MPa', clip_on=False)
    if (steelThick != 0):
        plt.plot(array([xAxisVal1[-1] ,xAxisVal2[0]]), array([yAxisVal1[-1] ,yAxisVal2[0]]), linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])
        plt.plot(xAxisVal1, yAxisVal1, 'r-', label = 'Stress in inner steel: <' + numToStr1dec(amin(yAxisVal1)) + ',' + numToStr1dec
                     (amax(yAxisVal1)) + '> MPa', clip_on=False)
    if (steelThickOut != 0):
        plt.plot(array([xAxisVal2[-1] ,xAxisVal3[0]]), array([yAxisVal2[-1] ,yAxisVal3[0]]), linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])
        plt.plot(xAxisVal3, yAxisVal3, 'g-', label = 'Stress in outer steel: <' + numToStr1dec(amin(yAxisVal3)) + ',' + numToStr1dec
                     (amax(yAxisVal3)) + '> MPa', clip_on=False)
    plt.ylabel('Stress [MPa]')
    plt.xlabel('Thickness [mm]')
    plt.xlim((0, xAxisMax))
    plt.ylim((yAxisMin, yAxisMax))
    plt.legend(loc='lower right')

    # >>>>> Save figure <<<<<
    plt.savefig \
        ('figs/ ' +lblTem p +'C_ ' +lblTim e +'_v ' +lblVersio n +'/ ' +lblTem p +'C_ ' +lblTim e +'_v ' +lblVersio n +'_ ' +nameLabe l +'.png', bbox_inches="tight")









def plot_all_figures():
    pass