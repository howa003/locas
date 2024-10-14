import eel
from eel_functions import get_python_result

eel.init("static_web_folder")
eel.start("index.html", size=(1280, 850), port=8323)

