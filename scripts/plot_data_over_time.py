import sys
import csv
import matplotlib
import matplotlib.pyplot as plt
import graphtools

avg_out_degrees_x = []
avg_out_degrees_y = []
with open('../csv_data/avg_out_degrees', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        avg_out_degrees_x.append(row[0])
        avg_out_degrees_y.append(row[1])
frac_nodes_in_gcc_x = []
frac_nodes_in_gcc_y = []
with open('../csv_data/frac_nodes_in_gcc', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        frac_nodes_in_gcc_x.append(row[0])
        frac_nodes_in_gcc_y.append(row[1])
nodes_vs_edges_x = []
nodes_vs_edges_y = []
with open('../csv_data/nodes_vs_edges') as infile:
    reader = csv.reader(infile)
    for row in reader:
        nodes_vs_edges_x.append(row[0])
        nodes_vs_edges_y.append(row[1])

'''
avg_out_degrees_x = [graphtools.string_to_datetime(str(time)) for time in avg_out_degrees_x]
plt.plot(avg_out_degrees_x, avg_out_degrees_y, 'b.')
plt.xlabel('Date of Transaction')
plt.ylabel('Average Out-degree')
plt.title('Average Node Out-degree Over Time')
plt.show()

frac_nodes_in_gcc_x = [graphtools.string_to_datetime(str(time)) for time in frac_nodes_in_gcc_x]
plt.plot(frac_nodes_in_gcc_x, frac_nodes_in_gcc_y, 'b.')
plt.xlabel('Date of Transaction')
plt.ylabel('Fraction of Nodes in GCC')
plt.title('Fraction of Nodes in GCC Over Time')
plt.show()

plt.loglog(nodes_vs_edges_x, nodes_vs_edges_y, 'b.')
plt.xlabel('Number of Nodes')
plt.ylabel('Number of Edges')
plt.title('Number of Edges Versus Number of Nodes Over Time')
plt.show()
'''
