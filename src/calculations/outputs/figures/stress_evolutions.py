from src.models import Structure, MeshSpace, MeshTime, Results, Loads
from pathlib import Path
import matplotlib.pyplot as plt
import numpy.typing as npt
import numpy as np
from src.general_functions import double_print


def subplot_stress_evolutions(ax: plt.Axes, subplot_title: str, x_axis: npt.NDArray[np.float64], x_label: str,
                              y_fixed: npt.NDArray[np.float64],
                              y_clamped: npt.NDArray[np.float64],
                              y_free: npt.NDArray[np.float64]) -> None:
    """
    This function plots the evolution of stress in the structure.

    :param ax: The axes of the subplot.
    :type ax: class:`matplotlib
    :param subplot_title: The title of the subplot.
    :type subplot_title: str
    :param x_axis: The x-axis values.
    :type x_axis: numpy array
    :param y_fixed: The y-axis values for the fixed boundary condition.
    :type y_fixed: numpy array
    :param y_clamped: The y-axis values for the clamped boundary condition.
    :type y_clamped: numpy array
    :param y_free: The y-axis values for the free boundary condition.
    :type y_free: numpy array
    """

    # Prepare the subplot
    ax.set_title(subplot_title)
    ax.grid()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    clip_state = False

    # Plot the stress evolution
    ax.plot(x_axis, y_fixed, linestyle='dashed', color=[1, 0, 0], label='Fixed BC', clip_on=clip_state)
    ax.plot(x_axis, y_clamped, linestyle=(0, (3, 3, 1, 3)), color='m', label='Clamped-guided BC', clip_on=clip_state)
    ax.plot(x_axis, y_free, linestyle=(0, (3, 3, 1, 3, 1, 3)), color=[0, 0, 1], label='Free BC', clip_on=clip_state)

    # Calculate x-axis limits
    x_min = 0
    x_max = max(x_axis)

    # Calculate y-axis limits
    y_min_accurate = min(min(y_fixed), min(y_clamped), min(y_free))
    y_max_accurate = max(max(y_fixed), max(y_clamped), max(y_free))
    y_spread = y_max_accurate - y_min_accurate
    if y_spread < 11:
        round_base = 0.5
    elif y_spread < 21:
        round_base = 1
    elif y_spread < 101:
        round_base = 10
    else:
        round_base = int(y_spread/10)
    y_min = round_base * int((y_min_accurate / round_base) - 1)
    y_max = round_base * int((y_max_accurate / round_base) + 1)

    # Configure the plot
    ax.legend(loc='upper right')
    ax.set_xlabel(x_label)
    ax.set_ylabel('Stress [MPa]')
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))
    ax.set_yticks(np.arange(y_min, y_max, round_base))


def plot_stress_evolutions(folder_path, file_name, figure_title,
                           results: Results, mesh_time: MeshTime) -> None:
    """
    This function plots the evolutions of minimal/maximal stresses in the structure.

    :param folder_path: The path to the folder where the figure will be saved.
    :type folder_path: str
    :param file_name: The name of the saved file.
    :type file_name: str
    :param figure_title: The title of the figure.
    :type figure_title: str
    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    :param mesh_time: A handle to the :class:`models.MeshTime` object containing the time mesh.
    :type mesh_time: class:`MeshTime`
    """

    try:
        # Create a figure with a specific size and resolution
        fig = plt.figure(figsize=(15, 6), dpi=300)
        fig.suptitle(figure_title, fontsize=16)

        # Create three subplots within the figure
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)

        # Declare and adjust the x-axis
        x_axis = mesh_time.time_axis
        x_max = max(x_axis)
        if x_max < 600:
            x_label = 'Time [s]'
            time_reduction_coefficient = 1
        elif x_max < 86400:
            x_label = 'Time [min]'
            time_reduction_coefficient = 60
        else:
            x_label = 'Time [h]'
            time_reduction_coefficient = 3600
        x_axis = x_axis / time_reduction_coefficient

        # Plot the stress evolution for maximal tension in concrete
        subplot_title = 'Maximal tensile stress in concrete'
        subplot_stress_evolutions(ax1, subplot_title, x_axis, x_label,
                                  results.stress_evolution_concrete_tension_fixed,
                                  results.stress_evolution_concrete_tension_clamped,
                                  results.stress_evolution_concrete_tension_free)

        # Plot the stress evolution for maximal compression in concrete
        subplot_title = 'Maximal compressive stress in concrete'
        subplot_stress_evolutions(ax2, subplot_title, x_axis, x_label,
                                  results.stress_evolution_concrete_compression_fixed,
                                  results.stress_evolution_concrete_compression_clamped,
                                  results.stress_evolution_concrete_compression_free)

        # Plot the stress evolution for extreme stresses in steel
        subplot_title = 'Maximal stress in steel'
        subplot_stress_evolutions(ax3, subplot_title, x_axis, x_label,
                                  results.stress_evolution_steel_merged_fixed,
                                  results.stress_evolution_steel_merged_clamped,
                                  results.stress_evolution_steel_merged_free)

        # Save the figure
        file_path = Path(folder_path, file_name)
        plt.savefig(file_path, bbox_inches="tight")
        plt.close(fig)
        double_print(f'Figure {file_name} saved to {folder_path}.')

    except Exception as exception:
        double_print(f'Plotting of {file_name} FAILED:' + str(exception))

    return None
