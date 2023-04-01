import argparse
import pandas as pd
import pyproj
import osmnx as ox
import json
import numpy as np
import networkx as nx
from tqdm import tqdm
from sklearn.preprocessing import normalize

north = 55.9899
south = 55.8784
east = -3.0418
west = -3.3374
G = None

def create_graph():
    return ox.graph_from_bbox(north, south, east, west, network_type='drive_service', simplify=True)

def heu(node, goal):
    return ox.distance.euclidean_dist_vec(G.nodes[node]['x'], G.nodes[node]['y'], G.nodes[goal]['x'], G.nodes[goal]['y'])

def create_map_nonplanar(node_ids):
    #build csv file with all the shortest paths, node1, node2, distance

    to_remove = set()

    adjacency_matrix = np.zeros((len(node_ids), len(node_ids)))


    # build adjacency matrix
    with tqdm(total=len(node_ids)*len(node_ids)) as pbar:
        for i in range(len(node_ids)):
            for j in range(len(node_ids)):
                pbar.update(1)
                try:
                    adjacency_matrix[i, j] = nx.algorithms.shortest_paths.astar.astar_path_length(G, node_ids[i], node_ids[j], heuristic=heu , weight='length')
                except:
                    adjacency_matrix[i, j] = 0



    #remove nodes with more than 5 not found paths
    for i in range(len(node_ids)):
        if np.count_nonzero(adjacency_matrix[i, :] == 0) > 10:
            to_remove.add(node_ids[i])

    for j in range(len(node_ids)):
        if np.count_nonzero(adjacency_matrix[:, j] == 0) > 10:
            to_remove.add(node_ids[j])

    for i in to_remove:
        node_ids.remove(i)

    adjacency_matrix = np.zeros((len(node_ids), len(node_ids)))

    # build adjacency matrix
    with tqdm(total=len(node_ids)*len(node_ids)) as pbar:
        for i in range(len(node_ids)):
            for j in range(len(node_ids)):
                pbar.update(1)
                try:
                    adjacency_matrix[i, j] = nx.algorithms.shortest_paths.astar.astar_path_length(G, node_ids[i], node_ids[j], heuristic=heu , weight='length')
                except:
                    adjacency_matrix[i, j] = 0

    return (normalize(adjacency_matrix, axis=1, norm='l1'), node_ids)


def create_map(node_ids):
    adjacency_matrix = np.zeros((len(node_ids), len(node_ids)))
    for i in range(len(node_ids)):
        for j in range(len(node_ids)):
            adjacency_matrix[i, j] = ox.distance.euclidean_dist_vec(G.nodes[node_ids[i]]['x'], G.nodes[node_ids[i]]['y'], G.nodes[node_ids[j]]['x'], G.nodes[node_ids[j]]['y'])
    return (normalize(adjacency_matrix, axis=1, norm='l1')) 
        

def main():
    # Define the command-line arguments using argparse
    parser = argparse.ArgumentParser(description='Create a map')
    parser.add_argument('-b', '--bin_type', help='Bin type')
    parser.add_argument('-w', '--ward', help='Ward name')

    # Parse the arguments
    args = parser.parse_args()

    # Print each argument if it's set
    if args.bin_type:
        print(f'Bin type: {args.bin_type}')
    if args.ward:
        print(f'Wards: {args.ward}')


    global G
    G = create_graph()
    bins = pd.read_csv('data/Bins_cleaned.csv')

    if args.bin_type:
        bins = bins[bins['feature_type_name'] == args.bin_type]
        if bins.empty:
            print("No bins of that type found")
            return

    if args.ward:
        bins = bins[bins['ward'] == args.ward]
        if bins.empty:
            print("No bins on that ward found")
            return
    
    lon = bins['lon']
    lat = bins['lat']
    node_ids = list(set(ox.distance.nearest_nodes(G, lon, lat, return_dist=False)))

    adjacency_matrix_nonplanar, node_ids = create_map_nonplanar(node_ids)
    print(adjacency_matrix_nonplanar)
    adjacency_matrix_euclidean = create_map(node_ids)
    print(adjacency_matrix_euclidean)
    
    size = len(node_ids)

    save_file_prefix =  "../ACO/maps/bins_normal" + ("_" + args.bin_type if args.bin_type else "") + ("_" + args.ward if args.ward else "")
    save_file_prefix = save_file_prefix.replace(" ", "_")

    save_file_euclidean = save_file_prefix + "_euclidean_" + str(size) +  ".csv"
    save_file_nonplanar = save_file_prefix + "_nonplanar_" + str(size) +  ".csv"

    np.savetxt(save_file_euclidean, adjacency_matrix_euclidean, fmt='%1.8f', delimiter=",")
    np.savetxt(save_file_nonplanar, adjacency_matrix_nonplanar, fmt='%1.8f', delimiter=",")
    
    #save node ids
    node_ids_file = (save_file_prefix[5:]) + "_node_ids_" + str(size) +  ".csv"
    np.savetxt(node_ids_file, node_ids, fmt='%d', delimiter=",")
    

if __name__ == '__main__':
    main()



