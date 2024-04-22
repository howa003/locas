
import eel
from src.controllers import run_analysis

eel.init("static_web_folder")



# starting the application
eel.start("index.html", size=(1280, 850))

