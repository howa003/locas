from matplotlib import pyplot as plt
import datetime
from src.models import MeshSpace, MeshTime, Results, Structure
from src.general_functions import num_to_str_1_dec, num_to_str_4_dec
import numpy as np
import gif
from pathlib import Path
from src.general_functions import double_print
from src.calculations.stresses.general_functions import split_array_concrete_and_steel


def get_x_tick_spacing(x_max: float) -> int:
    if x_max < 100:
        return 5
    elif x_max < 200:
        return 10
    elif x_max < 1000:
        return 50
    elif x_max < 2000:
        return 100
    else:
        return int(x_max / 20)


def round_down(number: float, decimal_places: int = 0) -> float:
    if decimal_places == 0:
        return int(number)
    else:
        return int(number * (10 ** decimal_places)) / (10 ** decimal_places)


def round_up(number: float, decimal_places: int = 0) -> float:
    if decimal_places == 0:
        return int(number) + 1
    else:
        return int(number * (10 ** decimal_places) + 1) / (10 ** decimal_places)


def set_subplot_properties(ax: plt.Axes, title: str,
                           x_label: str, y_label: str,
                           x_min: float, x_max: float, x_tick_spacing: int,
                           y_min: float, y_max: float) -> None:
    ax.set_title(title)
    ax.grid()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim((x_min, x_max))
    ax.set_xticks(np.arange(x_min, int(x_max), x_tick_spacing))
    ax.set_ylim((y_min, y_max))
    ax.legend(loc='lower right')
    return None


@gif.frame
def plot_gif_frame(time_step,
                   mesh_space: MeshSpace, results: Results, mesh_time: MeshTime, structure: Structure) -> None:
    # Hard inputs
    figure_title = "Evolution of strains and stresses during LOCA"
    clip_state = False

    # Soft inputs
    time = mesh_time.time_axis[time_step]

    # Declare the x-axis and its limits
    x_axis = mesh_space.x_axis_thickness
    x_min = 0
    x_max = max(x_axis)
    x_tick_spacing = get_x_tick_spacing(x_max)

    # Create a figure with a specific size and resolution
    fig = plt.figure(figsize=(20, 10), dpi=300)
    fig.suptitle(figure_title, fontsize=16)

    # Create three subplots within the figure
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    # Subplot 1 - Temperatures
    temperatures = results.temp_matrix[time_step]
    air_temperature = results.temp_air_int_vect[time_step]
    y_lim_min = min(0.0, round_down(np.amin(results.temp_air_int_vect), -1))
    y_lim_max = round_up(np.amax(results.temp_air_int_vect), -1)
    ax1.plot(x_axis, temperatures, 'b-',
             label='Temperature: <' + num_to_str_1_dec(np.amin(temperatures)) + ',' + num_to_str_1_dec(np.amax(temperatures)) + '> °C',
             clip_on=clip_state)
    ax1.plot(0, air_temperature, 'ro',
             label='Air temperature ' + num_to_str_1_dec(air_temperature) + ' °C',
             clip_on=clip_state)
    set_subplot_properties(ax1, 'Temperature in ' + str(datetime.timedelta(seconds=time)),
                           'Thickness [mm]', 'Temperature [°C]',
                           x_min, x_max, x_tick_spacing,
                           y_lim_min, y_lim_max)

    # Subplot 2 - Strains
    # TODO: Naplnit strains matice (asi už hotovo)
    strains_theoretical = results.strains_thermal_theoretical[time_step]
    strains_internal_pressure = results.strain_internal_pressure[time_step]
    strains_prestressing = results.strain_prestressing[time_step]
    strains_fixed = results.strains_real_fixed[time_step]
    strains_clamped = results.strains_real_clamped[time_step]
    strains_free = results.strains_real_free[time_step]
    y_min = min(
        np.amin(strains_theoretical),
        np.amin(strains_internal_pressure),
        np.amin(strains_prestressing),
        np.amin(strains_fixed),
        np.amin(strains_clamped),
        np.amin(strains_free)
    )
    y_max = max(
        np.amax(strains_theoretical),
        np.amax(strains_internal_pressure),
        np.amax(strains_prestressing),
        np.amax(strains_fixed),
        np.amax(strains_clamped),
        np.amax(strains_free)
    )
    y_lim_min = round_down(y_min, 4)
    y_lim_max = round_up(y_max, 4)
    ax2.plot(x_axis, strains_theoretical, 'k--',
             label='Theor. therm. strain: <' + num_to_str_4_dec(np.amin(strains_theoretical)) + ',' + num_to_str_4_dec(np.amax(strains_theoretical)) + '>',
             clip_on=clip_state)
    ax2.plot(x_axis, strains_internal_pressure, linestyle=(0, (3, 3, 1, 3)), color='k',
             label='Internal pressure strain: <' + num_to_str_4_dec(np.amin(strains_internal_pressure)) + ',' + num_to_str_4_dec(np.amax(strains_internal_pressure)) + '>',
             clip_on=clip_state)
    ax2.plot(x_axis, strains_prestressing, linestyle=(0, (3, 3, 1, 3, 1, 3)), color='k',
             label='Prestressing strain: <' + num_to_str_4_dec(np.amin(strains_prestressing)) + ',' + num_to_str_4_dec(np.amax(strains_prestressing)) + '>',
             clip_on=clip_state)
    ax2.plot(x_axis, strains_fixed, 'r-',
             label='Real strain (fixed BC): <' + num_to_str_4_dec(np.amin(strains_fixed)) + ',' + num_to_str_4_dec(np.amax(strains_fixed)) + '>',
             clip_on=clip_state)
    ax2.plot(x_axis, strains_clamped, 'm-',
             label='Real strain (clamped BC): <' + num_to_str_4_dec(np.amin(strains_clamped)) + ',' + num_to_str_4_dec(np.amax(strains_clamped)) + '>',
             clip_on=clip_state)
    ax2.plot(x_axis, strains_free, 'b-',
             label='Real strain (free BC): <' + num_to_str_4_dec(np.amin(strains_free)) + ',' + num_to_str_4_dec(np.amax(strains_free)) + '>',
             clip_on=clip_state)
    set_subplot_properties(ax2, 'Strains in ' + str(datetime.timedelta(seconds=time)),
                           'Thickness [mm]', 'Strain [-]',
                           x_min, x_max, x_tick_spacing,
                           y_lim_min, y_lim_max)

    # Subplot 3 - Stresses
    stresses_fixed = results.stress_total_fixed[time_step]
    stresses_clamped = results.stress_total_clamped[time_step]
    stresses_free = results.stress_total_free[time_step]

    y_min = min(
        np.amin(stresses_fixed),
        np.amin(stresses_clamped),
        np.amin(stresses_free)
    )
    y_max = max(
        np.amax(stresses_fixed),
        np.amax(stresses_clamped),
        np.amax(stresses_free)
    )
    y_lim_min = round_down(y_min, 10)
    y_lim_max = round_up(y_max, 10)
    ax3.plot(x_axis, stresses_fixed, 'r-',
             label='Stress for fixed BC: <' + num_to_str_1_dec(np.amin(stresses_fixed)) + ',' + num_to_str_1_dec(np.amax(stresses_fixed)) + '>',
             clip_on=clip_state)
    ax3.plot(x_axis, stresses_clamped, 'm-',
             label='Stress for clamped BC: <' + num_to_str_1_dec(np.amin(stresses_clamped)) + ',' + num_to_str_1_dec(np.amax(stresses_clamped)) + '>',
             clip_on=clip_state)
    ax3.plot(x_axis, stresses_free, 'b-',
             label='Stress for free BC: <' + num_to_str_1_dec(np.amin(stresses_free)) + ',' + num_to_str_1_dec(np.amax(stresses_free)) + '>',
             clip_on=clip_state)
    set_subplot_properties(ax3, 'Stresses in ' + str(datetime.timedelta(seconds=time)),
                           'Thickness [mm]', 'Stress [MPa]',
                           x_min, x_max, x_tick_spacing,
                           y_lim_min, y_lim_max)

    # Subplot 4 - Stresses in concrete
    stresses_fixed_concrete = results.stress_fixed_concrete[time_step]
    stresses_clamped_concrete = results.stress_clamped_concrete[time_step]
    stresses_free_concrete = results.stress_free_concrete[time_step]

    # Split the thickness into concrete and steel
    x_axis_split = split_array_concrete_and_steel(x_axis, mesh_space, structure)
    x_axis_concrete = x_axis_split[1]

    y_min = min(
        np.amin(stresses_fixed_concrete),
        np.amin(stresses_clamped_concrete),
        np.amin(stresses_free_concrete)
    )
    y_max = max(
        np.amax(stresses_fixed_concrete),
        np.amax(stresses_clamped_concrete),
        np.amax(stresses_free_concrete)
    )
    y_lim_min = round_down(y_min, 1)
    y_lim_max = round_up(y_max, 1)
    ax4.plot(x_axis_concrete, stresses_fixed_concrete, 'r-',
             label='Stress for fixed BC: <' + num_to_str_1_dec(np.amin(stresses_fixed_concrete)) + ',' + num_to_str_1_dec(np.amax(stresses_fixed_concrete)) + '>',
             clip_on=clip_state)
    ax4.plot(x_axis_concrete, stresses_clamped_concrete, 'm-',
             label='Stress for clamped BC: <' + num_to_str_1_dec(np.amin(stresses_clamped_concrete)) + ',' + num_to_str_1_dec(np.amax(stresses_clamped_concrete)) + '>',
             clip_on=clip_state)
    ax4.plot(x_axis_concrete, stresses_free_concrete, 'b-',
             label='Stress for free BC: <' + num_to_str_1_dec(np.amin(stresses_free_concrete)) + ',' + num_to_str_1_dec(np.amax(stresses_free_concrete)) + '>',
             clip_on=clip_state)
    set_subplot_properties(ax4, 'Stresses in concrete in ' + str(datetime.timedelta(seconds=time)),
                           'Thickness [mm]', 'Stress [MPa]',
                           x_min, x_max, x_tick_spacing,
                           y_lim_min, y_lim_max)

    return fig


def create_gif_animation(mesh_space: MeshSpace, mesh_time: MeshTime, results: Results, structure: Structure) -> None:

    # try:
    # Hard inputs
    gif_save_path = 'analysis_results/' + results.analysis_identifier + '/animations/'
    Path(gif_save_path).mkdir(parents=True, exist_ok=True)

    # Soft inputs
    frames = []
    for time_step in range(int(mesh_time.time_steps_count) + 1):
        double_print('Plotting GIF: Step ' + str(time_step) + ' out of ' + str(mesh_time.time_steps_count + 1))
        frame = plot_gif_frame(time_step, mesh_space, results, mesh_time, structure)
        frames.append(frame)

    gif_name = results.analysis_identifier + '.gif'
    gif_path = gif_save_path + gif_name
    gif.save(frames, gif_path, duration=100)

    double_print(f'Animation {gif_name} saved to {gif_path}.')

    # except Exception as exception:
    #     double_print(f'Plotting of the GIF animation FAILED:' + str(exception))

    return None
