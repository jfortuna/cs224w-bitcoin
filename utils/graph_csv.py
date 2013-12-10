

import csv
import plot
import sys
import os
from os import listdir
from os.path import isfile, join
from scripts import graphtools


def _plot_vals_from_list(to_plot, title, ylabel, xlabel='Date'):
  with open(to_plot, mode='r') as infile:
    reader = csv.reader(infile)
    data = {rows[0]:rows[1] for rows in reader}

  plot.plot_frequency_map(data, title=title, xlabel=xlabel, ylabel=ylabel, show=True)


def _plot_vals_from_time_slices(prefix, title, ylable):
  files = [ f for f in listdir('../csv_data/') if isfile(join('../csv_data/',f)) ]
  to_graph = {}
  for filename in files:
    if filename.startswith(prefix):
      # if filename[0:1].isdigit():
      start, end = _extract_start_and_end(filename[len(prefix) + 1:])
      # start, end = _extract_start_and_end(filename)
      vals = _get_vals_from_csv(filename)
      graphtools.calc_gini(vals)
      to_graph[start] = graphtools.calc_gini(vals)
  plot.plot_frequency_map(to_graph, title=title, ylabel=ylabel, xlabel='Date', show=True)

def _extract_start_and_end(start_and_end):
  segments = start_and_end.split('_')
  return segments[0], segments[1]

def _get_vals_from_csv(filename):
  with open('../csv_data/' + filename, mode='r') as infile:
    reader = csv.reader(infile)
    data = {float(rows[0]):float(rows[1]) for rows in reader}
  return data.values()

if __name__ == '__main__':
  # to_plot = '../csv_data/' + sys.argv[1]
  # name = sys.argv[2]
  # ylabel = sys.argv[3]
  # _plot_vals_from_list(to_plot, name, ylabel)
  ylabel = 'Gini Value for ' + sys.argv[3]
  _plot_vals_from_time_slices(sys.argv[1], sys.argv[2], ylabel)

