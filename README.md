# GeoScripts

**Author:** Peter Manko Jr.  
**Project available at:** https://github.com/PeterManko/GeoScripts

## Overview

GeoScripts is a collection of Python scripts designed to automate GIS tasks using `QGIS` and Python libraries like `geopanda`. Below is the documentation for each script in the repository.

### Scripts

- [qgis_buffer_folder.py](#qgis_buffer_folder)
- [spatial_layer_processor.py](#spatial_layer_processor)

## qgis_buffer_folder

### Overview

The `qgis_buffer_folder.py` script processes a set of GeoJSON files, buffers each layer, adds them to a QGIS project, and saves the buffered layers as new GeoJSON files.

### Dependencies

To run this script, you will need:

- QGIS (3.x)
- Python 3.x
- QGIS Python API (`qgis.core`, `qgis.analysis`, `qgis.processing`)

### Installation

1. **Install QGIS**:
   - Download and install QGIS from [QGIS official website](https://qgis.org/).

2. **Set up QGIS Python environment**:
   - Ensure that QGIS's Python is in your system PATH. You can usually find QGIS Python in the QGIS installation directory.

3. **Clone the repository**:
   ```bash
   git clone https://github.com/PeterManko/GeoScripts.git
   cd GeoScripts # change to repository directory
   ```
### Usage

1. **Configure the script**:
    - Configure the script:
    ```bash
    input_path = 'path/to/inputs'  # Replace with your input layer path directory
    output_path = 'path/to/outputs' # Replace with your output layer path directory
    distance = 0.01  # Distance setting for buffer
    save_project_with_layers = False  # Set to True if you want to save each layer as a QGIS project
    ```
2. **Run the script:**
    - Make sure QGIS and its Python environment are properly set up.
    - Execute the script within the QGIS Python environment.

## spatial_layer_processor

### Overview

The `spatial_layer_processor.py` script processes spatial layers by performing spatial selections of rivers that intersect points, then saves the resulting selections of rivers as new GeoJSON files. 

### Dependencies

To run this script, you will need:

- Python 3.x
- Geopandas
- Shapely
- Tqdm
- Argparse

### Installation

1. **Install Python**:
   - Download and install Python from [Python official website](https://www.python.org/).

2. **Set up the environment**:
   - Install the required Python libraries:
     ```bash
     pip install geopandas shapely tqdm
     ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/PeterManko/GeoScripts.git
   cd GeoScripts
### Usage

1. **Parameters**:
    - `--input_path`:
        - **Description:** Path to the directory containing the input layers.
        - **Example:** `--input_path path/to/input_layers`
        - **Usage:** Required parameter.

    - `--river_path`:
        - **Description:** Path to the directory containing the river layers.
        - **Example:** `--river_path path/to/river_layers`
        - **Usage:** Required parameter.

    - `--save_path`:
        - **Description:** Path to the directory where the output layers will be saved.
        - **Example:** `--save_path path/to/save_output`
        - **Usage:** Required parameter.

    - `--verbose`:
        - **Description:** Enable verbose output for detailed logging.
        - **Example:** `--verbose`
        - **Usage:** Optional parameter. Include this flag to enable verbose mode.

2. **Execution**:
    - Suppose you have the following directory structure for your spatial data:
    ```bash
    points/
        point1.geojson
        point2.geojson
        ...
    rivers/
        river1.geojson
        river2.geojson
        ...
    output/
        
    spatial_layer_processor.py
    ```
    - You can run the `spatial_layer_processor.py` script with the following command:

    ```bash
    python spatial_layer_processor.py --input_path data/points --river_path data/rivers --save_path data/output
    ```
