import eel
from src.controllers import run_analysis


@eel.expose
def get_python_result(gui_inputs):
    eel.print_status('Progress: Python function starting.')()
    analysis_result = run_analysis()
    print(gui_inputs)
    return analysis_result
