"""
Author: Peter Manko Jr.
Project available at: https://github.com/PeterManko/GeoScripts
"""

import os
import geopandas as gpd
from shapely.geometry import Point, MultiPolygon
from shapely.ops import nearest_points
import concurrent.futures
import argparse
from tqdm import tqdm 
import numpy as np

# Global verbose flag
verbose = False

def list_files(directory):
    """
    Lists all .geojson files in a given directory and its subdirectories.

    Args:
        directory (str): The directory to search for files.

    Returns:
        list: A list of file paths.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.geojson'):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

def save_layer_as_geojson(gdf, output_path, name):
    """
    Saves a GeoDataFrame as a GeoJSON file.

    Args:
        gdf (GeoDataFrame): The GeoDataFrame to save.
        output_path (str): The directory to save the file in.
        name (str): The name of the output file (without extension).
    """
    global verbose
    output_file = os.path.join(output_path, name + '.geojson')
    gdf.to_file(output_file, driver='GeoJSON')
    if verbose:
        print(f"Layer {name} saved as GeoJSON successfully!")

def meters_to_degrees(meters, latitude):
    """
    Convert a distance in meters to degrees of latitude and longitude.
    
    Args:
        meters (float): The distance in meters.
        latitude (float): The latitude at which the conversion is to be made.
    
    Returns:
        tuple: A tuple containing the equivalent degrees of latitude and longitude.
    """
    degrees_lat = meters / 111000
    degrees_lon = meters / (111000 * np.cos(np.radians(latitude)))
    return degrees_lat, degrees_lon

def find_nearest_river(point, rivers, radius_meters):
    """
    Finds the nearest river within a given radius from a point.

    Args:
        point (Point): The point to search around.
        rivers (GeoDataFrame): A GeoDataFrame of river geometries.
        radius_meters (float): The radius to search within, in meters.

    Returns:
        GeoSeries: The nearest river within the radius, or None if no river is found.
    """
    latitude = point.y
    degrees_lat, degrees_lon = meters_to_degrees(radius_meters, latitude)
    
    # Create a buffer around the point
    buffer = point.buffer(max(degrees_lat, degrees_lon))
    
    if verbose:
        print(f"Buffer created with radius (degrees): {max(degrees_lat, degrees_lon)}")
    
    # Find rivers intersecting the buffer
    rivers_in_buffer = rivers[rivers.intersects(buffer)]
    
    if verbose:
        print(f"Rivers in buffer: {len(rivers_in_buffer)}")

    if not rivers_in_buffer.empty:
        # Calculate the distance from the point to each river in the buffer
        distances = rivers_in_buffer.geometry.apply(lambda geom: point.distance(nearest_points(point, geom)[1]))
        # Find the river with the minimum distance
        nearest_river = rivers_in_buffer.loc[distances.idxmin()]
        return nearest_river
    else:
        return None

def create_new_layer(river_path, point_path, new_layer_name, save_path, radius):
    """
    Creates a new layer by performing a spatial selection of rivers that intersect points.

    Args:
        river_path (str): Path to the river GeoJSON file.
        point_path (str): Path to the point GeoJSON file.
        new_layer_name (str): The name of the new layer.
        save_path (str): The directory to save the new layer in.
    """
    global verbose
    if verbose:
        print(f"Processing {point_path} and {river_path}")

    # Read the input layers
    river_gdf = gpd.read_file(river_path)
    point_gdf = gpd.read_file(point_path)
    
    # Ensure the CRS is the same
    if river_gdf.crs != point_gdf.crs:
        point_gdf = point_gdf.to_crs(river_gdf.crs)
    
    selected_rivers = []
    # Define the preset radius in meters
    
    if verbose:
        print(f"Using radius: {radius} meters")
        print(f"Number of points: {len(point_gdf)}")
        print(f"Number of rivers: {len(river_gdf)}")

    # Convert MultiPolygon geometries to centroids
    point_gdf['geometry'] = point_gdf['geometry'].apply(lambda geom: geom.centroid if isinstance(geom, MultiPolygon) else geom)

    # Iterate over each point and find the nearest river within the preset radius
    for point in point_gdf.geometry:
        if isinstance(point, Point):
            nearest_river = find_nearest_river(point, river_gdf, radius)
            if nearest_river is not None:
                selected_rivers.append(nearest_river)
        else:
            if verbose:
                print(f"Skipping non-Point geometry: {point}")

    if not selected_rivers:
        if verbose:
            print(f"No features selected for {new_layer_name}")
        return

    # Convert the selected rivers list back to a GeoDataFrame
    selected_rivers_gdf = gpd.GeoDataFrame(selected_rivers, crs=river_gdf.crs)
    
    if verbose:
        print(f"Number of selected rivers: {len(selected_rivers_gdf)}")

    # Save the selected features to a new GeoJSON file
    save_layer_as_geojson(selected_rivers_gdf, save_path, new_layer_name)

def process_layers(river_path, point_path, save_path, radius):
    """
    Processes layers by creating a new layer for a combination of river and point data.

    Args:
        river_path (str): Path to the river GeoJSON file.
        point_path (str): Path to the point GeoJSON file.
        save_path (str): The directory to save the new layer in.
    """
    layer_name = os.path.splitext(os.path.basename(point_path))[0]
    river_name = os.path.splitext(os.path.basename(river_path))[0]
    new_layer_name = f"{layer_name}_{river_name}"
    create_new_layer(river_path, point_path, new_layer_name, save_path, radius)

def main():
    global verbose

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process spatial layers and generate new GeoJSON layers.", epilog="Made by Peter Manko Jr. Available at: https://github.com/PeterManko/GeoScripts")
    parser.add_argument('--input_path', required=True, help="Path to input layers")
    parser.add_argument('--river_path', required=True, help="Path to river layers")
    parser.add_argument('--save_path', required=True, help="Path to save output layers")
    parser.add_argument('--radius', required=True, help="Radius in which to search for intersection")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose output")

    args = parser.parse_args()
    
    verbose = args.verbose

    input_path = args.input_path
    river_path = args.river_path
    save_path = args.save_path
    radius = args.radius
    # List all point and river files
    files = list_files(input_path)
    rivers = list_files(river_path)
    
    # Create the save directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Calculate total tasks for progress bar
    total_tasks = len(files) * len(rivers)
    
    # Use ThreadPoolExecutor to process layers concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        # Initialize the progress bar
        with tqdm(total=total_tasks) as pbar:
            for file in files:
                for river in rivers:
                    # Submit tasks to the executor
                    future = executor.submit(process_layers, river, file, save_path, radius)
                    futures.append(future)
            
            # Update the progress bar as each future completes
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # This will raise an exception if the thread raised one
                except Exception as e:
                    if verbose:
                        print(f"An error occurred: {e}")
                pbar.update()

    if verbose:
        print('Finished calculation')

if __name__ == "__main__":
    main()
