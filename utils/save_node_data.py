import csv

def save_node_map(mp, stamp):
    """Saves data about the nodes to a csv. Note that this assumes
    the key is a node. Stamp is the name of the csv.
    """
    with open('../csv_data/'+stamp, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in mp.items():
            writer.writerow([key, value])
