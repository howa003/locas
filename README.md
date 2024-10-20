# LOCAS - Loss-of-coolant stresses

LOCAS is a software application for the calculation of stresses induced in cylindrical containment vessels create using Python.
Using this software, the user can calculate the stresses induced by temperature, internal pressure, and prestressing.

The graphical user interface is built using the Eel library, which allows the user to interact with the software through a web browser.

This software was created as part of a PhD thesis.
For more information about the library, its usage, and used methods, see the [PhD disseration](https://dspace.cvut.cz/handle/10467/118501). 

<!-- TOC -->
- [LOCAS](#locas---loss-of-coolant-stresses)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Entering input values](#entering-input-values)
    - [Calculation](#calculation)
    - [Outputs](#outputs)
  - [Building your own distributable binary with PyInstaller](#building-your-own-distributable-binary-with-pyinstaller)
<!-- /TOC -->

## Installation

To install the software, follow these steps:

1. Clone the repository to your local machine.
2. Install the required Python packages by running the following command:

```shell
pip install -r requirements.txt
```

3. Run the software by executing the following command:

```shell
python main.py
```

This will start a local web server and open the application in your default web browser.

## Usage

### Entering input values

Input values regarding the containment vessel and its loads must be enterd into the main window which appears after starting the software.
Additionally, the evolution of temperature and pressure inside the vessel during a LOCA must be defined in the two supplementary files loated in the src/source_data directory.

### Calculation

Calculation of the results can be initiated by pressing the "Calculate" button in the GUI.

During the calculation, current progress is printed in the Calculation log at the bottom of the window.

### Outputs

After all calculations are finished,
the results are saved in 3 folders:
- figs (folder with figures containing the most important results),
- gifs (folder contating an animation of the evolution of temperatures, strain, and stresses in the wall during LOCA),
- saved_data (folder containing CSV files with complete results).


## Prebuilt distributable binary (.exe file)

The recommended approach to using this software is to [run it directly](#installation) or [building your own binary](#building-your-own-distributable-binary-with-pyinstaller).

If these options are impractical for you, you can [download the prebuilt binary here](https://people.fsv.cvut.cz/www/holanjak/software/locas/). 


## Building your own distributable binary with PyInstaller

If you want to package the library into a program that can be run on a computer without a Python interpreter installed,
you should use the **PyInstaller** library. 
- In your app's folder, run `python -m eel main.py static_web_folder`. This will create a new folder `dist/`.

If you want to package the library into a standalone executable that can be run on a computer without a Python interpreter installed,
you should use **PyInstaller**.
- In your app's folder, run `python -m eel main.py static_web_folder --onefile --noconsole`

Consult the [documentation for PyInstaller](http://PyInstaller.readthedocs.io/en/stable/) for more options.









