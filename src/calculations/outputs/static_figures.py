from src.models import Structure, MeshSpace, MeshTime, Results, Loads
from pathlib import Path
from src.general_functions import double_print
import matplotlib.pyplot as plt
from src.calculations.stresses.general_functions import split_array_concrete_and_steel
import datetime
from src.general_functions import num_to_str_1_dec
from numpy import amin, amax, array
import os



def subplot_stress_distr(ax, subplot_title, x_axis, y_axis, x_min, x_max, y_min, y_max, mesh_space, structure) -> None:
    """
    This function configures the subplot axes.

    :param ax: The axes of the subplot.
    :type ax: class:`matplotlib
    :param x_axis: The x-axis values.
    :type x_axis: numpy array
    :param y_axis: The y-axis values.
    :type y_axis: numpy array
    :param subplot_title: The title of the subplot.
    :type subplot_title: str
    :param x_min: The minimum value of the x-axis.
    :type x_min: float
    :param x_max: The maximum value of the x-axis.
    :type x_max: float
    :param y_min: The minimum value of the y-axis.
    :type y_min: float
    :param y_max: The maximum value of the y-axis.
    :type y_max: float
    :param mesh_space: A handle to the :class:`models.MeshSpace` object containing information about the space mesh.
    :type mesh_space: class:`MeshSpace`
    :param structure: A handle to the :class:`models.Structure` object containing information about the structure.
    :type structure: class:`Structure`
    :return: None
    :rtype: None
    """

    # Split the thickness into concrete and steel
    x_axis_split = split_array_concrete_and_steel(x_axis, mesh_space, structure)
    x_axis_steel_inner = x_axis_split[0]
    x_axis_concrete = x_axis_split[1]
    x_axis_steel_outer = x_axis_split[2]

    # Split the stress distribution into concrete and steel
    y_axis_split = split_array_concrete_and_steel(y_axis, mesh_space, structure)
    y_axis_steel_inner = y_axis_split[0]
    y_axis_concrete = y_axis_split[1]
    y_axis_steel_outer = y_axis_split[2]

    # Prepare the subplot
    ax.set_title(subplot_title)
    ax.grid()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')


    # Plot the stress distribution for concrete
    legend_label = 'Stress in concrete: <' + num_to_str_1_dec(amin(y_axis_concrete)) + ',' + num_to_str_1_dec(
        amax(y_axis_concrete)) + '> MPa'
    ax.plot(x_axis_concrete, y_axis_concrete, 'b--', label=legend_label , clip_on=False)

    # Plot the stress distribution for the inner steel liner
    if structure.has_inner_steel:
        legend_label = 'Stress in inner steel: <' + num_to_str_1_dec(amin(y_axis_steel_inner)) + ',' + num_to_str_1_dec(
            amax(y_axis_steel_inner)) + '> MPa'
        ax.plot(x_axis_steel_inner, y_axis_steel_inner, 'r-', label=legend_label, clip_on=False)
        ax.plot(array([x_axis_steel_inner[-1], x_axis_concrete[0]]), array([y_axis_steel_inner[-1], y_axis_concrete[0]]),
                linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])

    # Plot the stress distribution for the outer steel liner
    if structure.has_outer_steel:
        legend_label = 'Stress in outer steel: <' + num_to_str_1_dec(amin(y_axis_steel_outer)) + ',' + num_to_str_1_dec(
            amax(y_axis_steel_outer)) + '> MPa'
        ax.plot(x_axis_steel_outer, y_axis_steel_outer, 'g-', label=legend_label, clip_on=False)
        ax.plot(array([x_axis_concrete[-1], x_axis_steel_outer[0]]), array([y_axis_concrete[-1], y_axis_steel_outer[0]]),
                linestyle=(0, (1, 3)), color=[0.5, 0.5, 0.5])

    # Configure the plot
    ax.legend(loc='lower right')
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))
    ax.set_xlabel('Thickness [mm]')
    ax.set_ylabel('Stress [MPa]')


# Plot průběhu napětí v konstrukci v daných časech
def plot_stress_distributions(folder_path, file_name, figure_title, step_fixed: int, step_clamped: int, step_free: int, structure: Structure, results: Results, mesh_space: MeshSpace, mesh_time: MeshTime) -> str:
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
    :param mesh_space: A handle to the :class:`models.MeshSpace` object containing information about the space mesh.
    :type mesh_space: class:`MeshSpace`
    :return: String indicating the successful/unsuccessful saving of the figure.
    :rtype: str
    """

    # Create a figure with a specific size and resolution
    fig = plt.figure(figsize=(16, 7), dpi=300)
    fig.suptitle(figure_title, fontsize=16)

    # Create three subplots within the figure
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)

    # Declare the y-axis and its limits
    y_stress_fixed = results.stress_total_fixed[step_fixed]
    y_stress_clamped = results.stress_total_clamped[step_clamped]
    y_stress_free = results.stress_total_free[step_free]
    y_min = int((min(min(y_stress_fixed) ,min(y_stress_clamped) ,min(y_stress_free) ) /1 ) - 1)
    y_max = int((max(max(y_stress_fixed) ,max(y_stress_clamped) ,max(y_stress_free) ) /1 ) + 1)

    # Declare the x-axis and its limits
    x_axis = mesh_space.x_axis_thickness
    x_min = 0
    x_max = max(x_axis)


    # Plot the stress distributions for the fixed boundary condition
    subplot_time = mesh_time.time_axis[step_fixed]
    subplot_title = 'Stress for fixed BC in ' + str(datetime.timedelta(seconds=subplot_time))
    subplot_stress_distr(ax1, subplot_title, x_axis, y_stress_fixed, x_min, x_max, y_min, y_max, mesh_space, structure)

    # Plot the stress distributions for the clamped boundary condition
    subplot_time = mesh_time.time_axis[step_clamped]
    subplot_title = 'Stress for clamped-guided BC in ' + str(datetime.timedelta(seconds=subplot_time))
    subplot_stress_distr(ax2, subplot_title, x_axis, y_stress_clamped, x_min, x_max, y_min, y_max, mesh_space, structure)

    # Plot the stress distributions for the free boundary condition
    subplot_time = mesh_time.time_axis[step_free]
    subplot_title = 'Stress for free BC in ' + str(datetime.timedelta(seconds=subplot_time))
    subplot_stress_distr(ax3, subplot_title, x_axis, y_stress_free, x_min, x_max, y_min, y_max, mesh_space, structure)

    # Save the figure
    file_path = Path(folder_path, file_name)
    plt.savefig(file_path, bbox_inches="tight")
    plt.close(fig)
    return 'Figure saved as ' + str(file_path)





def plot_all_figures(structure: Structure, results: Results, mesh_space: MeshSpace, mesh_time: MeshTime) -> str:
    """
    This function plots all the figures.

    :return: None
    :rtype: None
    """

    try:
        folder_path = os.path.join('analysis_results', results.analysis_identifier, 'figures')
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        double_print('Folder ' + folder_path + ' was created.')

        # Plot the stress distributions when minimal stress (maximal tension) is reached in concrete
        plot_stress_distributions(folder_path,
                                  'stress_distributions.png',
                                  'Stress distributions in the structure',
                                  results.extreme_steps['min_stress_fixed_concrete'],
                                  results.extreme_steps['min_stress_clamped_concrete'],
                                  results.extreme_steps['min_stress_free_concrete'],
                                  structure, results, mesh_space, mesh_time)

        # TODO: Plot more figures and add gif creation

        result_message = "Figures saved successfully."

    except Exception as exception:
        result_message = "Plotting of figures FAILED: " + str(exception)

    return result_message


