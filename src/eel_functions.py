import eel
from src.controllers import run_analysis

@eel.expose
def get_python_result(gui_inputs):
    eel.print_status('Progress: Python function starting.')()
    calc_info = run_analysis()
    print(gui_inputs)
    return (calc_info)
