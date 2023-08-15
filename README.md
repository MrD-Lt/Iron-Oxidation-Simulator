# Iron-Oxidation-Simulator

This repository is dedicated to the development of a software tool to simulate and analyze the oxidation process of Fe(II) in water treatment. The tool aims to provide chemists with key parameters and data for the oxidation process, aiding in the treatment of arsenic-contaminated water.

## Structure:

- `Project`: This folder contains all the codes and files of this IRP.
- `Development_Log`: This folder contains records of the development process.
- `SoftWare`: This folder contains the help of how to use the software for users.
- `IndependentResearchProject` This is the [manual](/IndependentResearchProject.pdf) of the software.

## Getting Started

### For Developers:

1. Clone the repository to your local machine.
2. Navigate to `Iron-Oxidation-Simulator/Project/IronOxidationSimulator/src`.
3. Ensure you have the required dependencies installed, preferably in a virtual environment. You can use the provided `environment.yml` in the `config` folder to create a conda environment with all necessary dependencies.
4. Run `mainwindow.py` to launch the application.

### For End Users:

1. Navigate to `Iron-Oxidation-Simulator/Project/SoftWare`.
2. Check the README.

```
.github
   |-- workflows
   |   |-- main.yml
.gitignore
Development_Log
   |-- README.md
   |-- decisions
   |-- issues
   |-- logs
LICENSE
Project
   |-- IronOxidationSimulator
   |   |-- README.md
   |   |-- assets
   |   |   |-- Book3.xlsx
   |   |   |-- Plane3Dplot_fast_kinetic.m
   |   |   |-- reaction_order_analysis_WLSR.m
   |   |-- config
   |   |   |-- environment.yml
   |   |   |-- requirements.txt
   |   |-- docs
   |   |   |-- Makefile
   |   |   |-- build
   |   |   |   |-- latex
   |   |   |   |   |-- IndependentResearchProject.pdf
   |   |   |-- make.bat
   |   |   |-- source
   |   |   |   |-- conf.py
   |   |   |   |-- gui.rst
   |   |   |   |-- index.rst
   |   |   |   |-- src.rst
   |   |   |   |-- utils.rst
   |   |-- src
   |   |   |-- __init__.py
   |   |   |-- gui
   |   |   |   |-- __init__.py
   |   |   |   |-- button_area.py
   |   |   |   |-- help_window.py
   |   |   |   |-- input_window.py
   |   |   |   |-- result_window.py
   |   |   |   |-- settings_window.py
   |   |   |   |-- visual_window.py
   |   |   |-- mainwindow.py
   |   |   |-- ui
   |   |   |   |-- style.qss
   |   |   |   |-- welcome.ui
   |   |   |-- utils
   |   |   |   |-- __init__.py
   |   |   |   |-- initial_rate.py
   |   |   |   |-- input_help.py
   |   |   |   |-- plane3D_plot.py
   |   |   |   |-- rate_const.py
   |   |   |   |-- regression_analysis.py
   |   |   |   |-- save.py
   |-- README.md
   |-- SoftWare
   |   |-- README.md
README.md
```

Please note that this project is still under development and the structure may change over time.

## Contributions

Contributions, issues, and feature requests are welcome!

## License

Distributed under the MIT License. See LICENSE for more information.

Version 1.0.0

14 Aug. 2023
