"""
Author: Peter Manko Jr.
Project available at: https://github.com/PeterManko/GeoScripts
"""

import os
from qgis.core import QgsVectorLayer, QgsProcessingFeedback, QgsProject, QgsVectorFileWriter
import processing

# Get list of files in directory and its subdirectories
def list_files(directory):
    """
    Lists all files in a given directory and its subdirectories.

    Args:
        directory (str): The directory to search for files.

    Returns:
        list: A list of file paths.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list

# Create a buffered layer based on parameters
def buffer_layer(input_layer_path, distance):
    """
    Creates a buffered layer from an input layer.

    Args:
        input_layer_path (str): Path to the input layer.
        distance (float): Buffer distance.

    Returns:
        QgsVectorLayer: Buffered layer.
    """
    parameters = {
        'INPUT': input_layer_path,
        'DISTANCE': distance,
        'SEGMENTS': 5,
        'END_CAP_STYLE': 0,
        'JOIN_STYLE': 0,
        'MITER_LIMIT': 2,
        'DISSOLVE': False,
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }
    feedback = QgsProcessingFeedback()
    result = processing.run("native:buffer", parameters, feedback=feedback)
    buffered_layer = result['OUTPUT']
    return buffered_layer

# Add layer to the map
def add_layer_to_map(layer, name):
    """
    Adds a layer to the QGIS project.

    Args:
        layer (QgsVectorLayer): The layer to add.
        name (str): The name to assign to the layer.
    """
    if not layer.isValid():
        print("Layer failed to load!")
        return
    layer.setName(name)
    QgsProject.instance().addMapLayer(layer)
    print("Layer added to the map!")

# Save the project to the given path with the given name
def save_project(project_path, name):
    """
    Saves the QGIS project to the specified path with the given name.

    Args:
        project_path (str): The path to save the project.
        name (str): The name to assign to the project file.
    """
    QgsProject.instance().write(project_path + name)

# Save the given layer as a GeoJSON file
def save_layer_as_geojson(layer, output_path, name):
    """
    Saves the given layer as a GeoJSON file.

    Args:
        layer (QgsVectorLayer): The layer to save.
        output_path (str): The directory to save the file.
        name (str): The name to assign to the saved file.

    Returns:
        None
    """
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, output_path + name + '.geojson', "UTF-8", layer.crs(), "GeoJSON")
    if writer[0] == QgsVectorFileWriter.NoError:
        print("Layer saved as GeoJSON successfully!")
    else:
        print("Error occurred while saving layer as GeoJSON:", writer)

#############################
### Change to your specs: ###
#############################

input_path = 'path/to/inputs'  # Replace with your input layer path
outputh_path = 'path/to/outputs' # Replace with your output layer path
distance = 0.01 # distance setting for buffer
save_project_with_layers = False # save each layer as a qgis project

# Get all files in input path
files = list_files(input_path)

# Process each file individually
for file in files:
    layer_name, _ = os.path.splitext(os.path.basename(file))  # Get name of file, ignoring extension
    
    # Create new buffered layer
    buff_layer = buffer_layer(file, distance)
    
    # Add layer to project
    add_layer_to_map(buff_layer, layer_name)
    
    # Save the buffered layer as GeoJSON
    save_layer_as_geojson(buff_layer, outputh_path, layer_name)
    if save_project_with_layers:
        # Save the whole project automatically
        save_project(outputh_path, layer_name)
    
        # Remove all layers from the project so each project will only have current layer
        QgsProject.instance().removeAllMapLayers()
