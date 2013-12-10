

import csv
import plot
import sys


def _plot_vals_from_list(to_plot, title, ylabel, xlabel='Date'):
  with open(to_plot, mode='r') as infile:
    reader = csv.reader(infile)
    data = {rows[0]:rows[1] for rows in reader}

  plot.plot_frequency_map(data, title=title, xlabel=xlabel, ylabel=ylabel, show=True)








if __name__ == '__main__':
  to_plot = '../csv_data/' + sys.argv[1]
  name = sys.argv[2]
  ylabel = sys.argv[3]
  _plot_vals_from_list(to_plot, name, ylabel)