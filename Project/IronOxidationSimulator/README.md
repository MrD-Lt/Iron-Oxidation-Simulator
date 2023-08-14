# IronOxidationSimulator

This folder contains all the codes of this IRP.

## Structure:

- [`src/`](./src/): This directory contains all the source code for the project.
- [`assets/`](./assets/): This directory contains any images, references, or other files used in the project.
- [`config/`](./config/): This directory contains configuration files and environmental variables.
- [`docs/`](./docs/): This directory contains all the docs created.

## Getting Started

To run the project, follow these steps:

1. **Clone the Repository**:

    ```
    git clone https://github.com/edsml-dd1522/Iron-Oxidation-Simulator
    ```
    ```
    cd Iron-Oxidation-Simulator
    ```

2. **Set Up a Conda Environment**:

   First, ensure you have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed. 
   
   Once installed, create a new conda environment and activate it using:
   
    ```
    conda env create -f Project/IronOxidationSimulator/config/environment.yml
    ```
    ```
    conda activate irp
    ```

3. **Run the Application**:

    Navigate to the source directory and run the main script:
    
    ```
    cd Project/IronOxidationSimulator/src
    ```
    ```
    python3 mainwindow.py
    ```

4. **(Optional) Build the Application**:

   If you have set up `pyinstaller` and wish to build a standalone version of your application:
   
    ```
    pyinstaller --onefile --paths "./Project/IronOxidationSimulator/src" --add-data "./Project/IronOxidationSimulator/assets:./assets" --add-data "./Project/IronOxidationSimulator/src/ui:./ui" ./Project/IronOxidationSimulator/src/mainwindow.py
    ```
   The executable file will be located in the `dist` directory.

5. **Documentation and Development Logs**:
   - For details on decisions made during development, check the [`Development_Log/decisions`](../Development_Log/decisions) directory.
   - For issues faced during development, refer to the [`Development_Log/issues`](../Development_Log/issues) directory.
   - For logs of the project, see the [`Development_Log/logs`](../Development_Log/logs) directory.

6. **Contact**:

   If you have questions or face any issues, you can reach out to the developer via the contact details provided in the `Contact with developer` section of the application.

Please note that this project is still under development and the structure may change over time.

Version 0.2.1

14 Aug. 2023
