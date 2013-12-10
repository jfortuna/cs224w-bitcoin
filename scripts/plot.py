"""
This file is for generic plotting
"""

import matplotlib.pyplot as plt
import matplotlib
import graphtools


def plot_frequency_map(*maps, **plotargs):
    """                                                               
    A frequency map maps buckets to frequencies. An example would be  amount spent: 
    the bucket of spending 5 bitcoins is a key, and the value is the number of nodes that 
    spent that much.

    -- Parameters --
    maps - As many maps as you would care to plot. List 'em out, we'll pack them up right 
    plotargs - A bunch o' options:
      - title   - The title that you want for the graphs
      - xlabel  - The label for the x axis   
      - ylabel  - The label for the y axis
      - save_as - The name of the file you want to save the graph in. 
                  Only saves the graph if this parameter is specified
      - show    - Specifiy this parameter to be true to display the graph.

    TODO
      - Add log/semilog support
      - Add scatter support
      - Add style options
      _ Suggestions?
    """
    plt.figure()
    # plot all the maps that are given
    for mp in maps:
        xs =  sorted(mp.keys())
        ys = [mp[k] for k in xs]
        time_period = [graphtools.string_to_datetime(str(time)) for time in xs]
        dates = matplotlib.dates.date2num(time_period)
        plt.plot(time_period,ys)

    # look through kwargs, set appropriate plot features
    if 'xlabel' in plotargs:
        plt.xlabel(plotargs['xlabel'])
    if 'ylabel' in plotargs:
        plt.ylabel(plotargs['ylabel'])
    if 'title' in plotargs:
        plt.title(plotargs['title'])

    # display or save the plot
    if 'save_as' in plotargs:
        plt.savefig(plotargs['save_as'])
    if 'show' in plotargs and plotargs['show']:
        plt.show()
