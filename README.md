# LOCAS - Loss-of-coolant stresses

LOCAS is a Python library for the calculation of stresses induced in cylindrical containment vessels.
Using this software, the user can calculate the stresses induced by temperature, internal pressure, and prestressing.

The graphical user interface is built using the Eel library, which allows the user to interact with the software through a web browser.

<!-- TOC -->
- [Eel](#eel)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Entering input values](#entering-input-values)
    - [Calculation](#calculation)
    - [Outputs](#outputs)
  - [Building distributable binary with PyInstaller](#building-distributable-binary-with-pyinstaller)
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

GUI and files

### Calculation

### Outputs







## Building distributable binary with PyInstaller

If you want to package the library into a program that can be run on a computer without a Python interpreter installed,
you should use the **PyInstaller** library. 
- In your app's folder, run `python -m eel main.py static_web_folder`. This will create a new folder `dist/`.

If you want to package the library into a standalone executable that can be run on a computer without a Python interpreter installed,
you should use **PyInstaller**.
- In your app's folder, run `python -m eel main.py static_web_folder --onefile --noconsole`

Consult the [documentation for PyInstaller](http://PyInstaller.readthedocs.io/en/stable/) for more options.









