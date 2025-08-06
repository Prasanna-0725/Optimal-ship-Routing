import pandas as pd
import networkx as nx
import folium
from scipy.spatial import cKDTree
import numpy as np
import time
import webbrowser
import os

BASE_DIR = r"C:\g2\sih"

# Function to safely load the CSV file
def load_csv_safe(filepath):
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            raise ValueError("CSV file is empty.")
        df.columns = df.columns.str.strip()  # Ensure column names are clean
        return df
    except (pd.errors.EmptyDataError, ValueError) as e:
        print(f"Error loading CSV file: {e}")
        return None

# Load initial data
df = load_csv_safe(os.path.join(BASE_DIR, "ocean_points.csv"))
if df is None:
    raise SystemExit("Unable to load initial CSV file. Exiting.")

# Load ports coordinates
ports_df = load_csv_safe(os.path.join(BASE_DIR, "ports_coordinates.csv"))
if ports_df is None:
    raise SystemExit("Unable to load ports CSV file. Exiting.")
ports_coords = set((row['Latitude'], row['Longitude']) for _, row in ports_df.iterrows())

# Function to create a graph from the dataframe
def create_graph(df, source, destination, threshold=2.0):
    G = nx.Graph()
    points = df[['lat', 'lon']].values
    tree = cKDTree(points)

    # Add nodes
    for _, row in df.iterrows():
        coord = (row['lat'], row['lon'])
        if coord in ports_coords and coord not in [source, destination]:
            continue
        G.add_node(coord, wind=row['Surface Winds (knots)'], current=row['Currents (knots)'], wave=row['Wave Height (meters)'])

    # Add edges
    for idx, (lat, lon) in enumerate(points):
        dists, idxs = tree.query((lat, lon), k=10, distance_upper_bound=threshold)
        for dist, j in zip(dists, idxs):
            if idx != j and j < len(points):
                row1 = df.iloc[idx]
                row2 = df.iloc[j]
                coord1 = (row1['lat'], row1['lon'])
                coord2 = (row2['lat'], row2['lon'])
                if coord1 in ports_coords and coord1 not in [source, destination]:
                    continue
                if coord2 in ports_coords and coord2 not in [source, destination]:
                    continue
                weight = dist * (1 + row1['Surface Winds (knots)']/20 + row1['Currents (knots)']/2 + row1['Wave Height (meters)']/4)
                G.add_edge(coord1, coord2, weight=weight)
    return G

# Function to find the nearest node using cKDTree for speed
def find_nearest_node(tree, nodes_list, coord):
    dist, idx = tree.query(coord)
    return nodes_list[idx]

# Read source and destination coordinates from the file
with open(os.path.join(BASE_DIR, 'selected_ports.txt'), 'r') as f:
    source_coords = f.readline().strip().split(',')
    destination_coords = f.readline().strip().split(',')

source = (float(source_coords[0]), float(source_coords[1]))
destination = (float(destination_coords[0]), float(destination_coords[1]))

# Function to check if a segment is safe
def is_safe(segment, G):
    wind = G.nodes[segment[1]]['wind']
    current = G.nodes[segment[1]]['current']
    wave = G.nodes[segment[1]]['wave']
    return wind <= 20 and current <= 2 and wave <= 4

# Heuristic for A* (Euclidean distance)
def heuristic(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

initial_path = []
old_paths = []
source_list = [source]

while True:
    df = load_csv_safe(os.path.join(BASE_DIR, "updated_coordinates.csv"))
    if df is None:
        print("Waiting for updated_coordinates.csv to be available...")
        time.sleep(10)
        continue

    df.columns = df.columns.str.strip()

    points = df[['lat', 'lon']].values
    tree = cKDTree(points)
    nodes_list = [(row['lat'], row['lon']) for _, row in df.iterrows()]

    G = create_graph(df, source, destination)

    if initial_path and len(initial_path) > 1:
        source_node = initial_path[1]
    else:
        source_node = find_nearest_node(tree, nodes_list, source)

    if source_node == destination:
        print("Destination reached!")

        m = folium.Map(location=destination, zoom_start=5)

        # Draw all previous source locations path in red
        if len(source_list) > 1:
            folium.PolyLine(source_list, color="red", weight=2, opacity=0.5).add_to(m)

        # Last path segment to destination
        if source_list:
            last_source = source_list[-1]
            folium.PolyLine([last_source, destination], color="red", weight=2, opacity=0.5).add_to(m)

        # Markers on the path
        for coord in initial_path:
            folium.Marker(
                location=coord,
                icon=folium.CustomIcon(os.path.join(BASE_DIR, 'icon.png'), icon_size=(20, 20)),
                popup=f'Lat: {coord[0]}, Lon: {coord[1]}, Wind: {G.nodes[coord]["wind"]} knots, '
                      f'Current: {G.nodes[coord]["current"]} knots, Wave: {G.nodes[coord]["wave"]} meters'
            ).add_to(m)

        folium.Marker(
            location=destination,
            icon=folium.CustomIcon(os.path.join(BASE_DIR, 'icon.png'), icon_size=(30, 30)),
            popup='Destination reached!'
        ).add_to(m)

        map_path = os.path.join(BASE_DIR, 'ship_route.html')
        m.save(map_path)
        webbrowser.open(map_path)
        print(f"Map saved at {map_path}")
        break

    destination_node = find_nearest_node(tree, nodes_list, destination)

    print(f"Source Node: {source_node}")
    print(f"Destination Node: {destination_node}")

    try:
        initial_path = nx.astar_path(G, source=source_node, target=destination_node, heuristic=heuristic, weight='weight')
        print("Initial Path found.")
    except nx.NetworkXNoPath:
        print("No path found between source and destination. Retrying in 10 seconds...")
        time.sleep(10)
        continue

    current_path = initial_path.copy()
    for i in range(len(current_path) - 1):
        segment = (current_path[i], current_path[i + 1])
        if not is_safe(segment, G):
            try:
                new_path = nx.astar_path(G, source=segment[0], target=destination_node, heuristic=heuristic, weight='weight')
                current_path = current_path[:i + 1] + new_path[1:]
                print(f"Path adjusted at segment {segment}: Unsafe conditions encountered.")
            except nx.NetworkXNoPath:
                print(f"Adjustment failed at segment {segment}. Retrying in 10 seconds...")
                break

    print("Final Path determined.")

    m = folium.Map(location=source, zoom_start=5)

    if len(source_list) > 1:
        folium.PolyLine(source_list, color="red", weight=2, opacity=0.5).add_to(m)

    if source_list:
        last_source = source_list[-1]
        current_segment_path = [last_source] + current_path
        folium.PolyLine(current_segment_path, color="red", weight=2, opacity=0.5).add_to(m)

    # Markers on path
    for coord in current_path:
        folium.Marker(
            location=coord,
            icon=folium.CustomIcon(os.path.join(BASE_DIR, 'icon.png'), icon_size=(20, 20)),
            popup=f'Lat: {coord[0]}, Lon: {coord[1]}, Wind: {G.nodes[coord]["wind"]} knots, '
                  f'Current: {G.nodes[coord]["current"]} knots, Wave: {G.nodes[coord]["wave"]} meters'
        ).add_to(m)

    # Current location marker (ship icon)
    folium.Marker(
        location=current_path[0],
        icon=folium.CustomIcon(os.path.join(BASE_DIR, 'ship_icon.png'), icon_size=(30, 30)),
        popup='Current Location'
    ).add_to(m)

    # Destination marker
    folium.Marker(
        location=destination,
        icon=folium.CustomIcon(os.path.join(BASE_DIR, 'destination_icon.png'), icon_size=(30, 30)),
        popup='Destination'
    ).add_to(m)

    # Draw path line in blue
    folium.PolyLine(current_path, color="blue", weight=2.5, opacity=1).add_to(m)

    map_path = os.path.join(BASE_DIR, 'ship_route.html')
    m.save(map_path)
    webbrowser.open(map_path)

    print(f"Map with the ship route saved as '{map_path}'")

    source_list.append(source_node)
    old_paths.append(initial_path)

    time.sleep(3)  # increased to 3 seconds to reduce CPU load
