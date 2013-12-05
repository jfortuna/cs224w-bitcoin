
import random
from scripts.graphgen import _days
from scripts import graphtools
import numpy as np

def generate_time_slices(slice_time=1, num_intervals=10, num_in_slice=10):
  """ Returns a list of tuples that represent time slices from the
      graph.

      parameters:
        slice_time: the number of days that should be included in each
                    time slice.
        num_intervals: the number of intervals the entire graph should
                       be sliced into
        num_in_slice: the number of sections to be taken from that slice
      returns:
        list of tuples of (start, end)
  """
  slices = []
  low = 0
  section_length = len(_days) / num_intervals
  high = section_length
  for interval in range(num_intervals):
    valid_days = _days[low:high]
    for section in range(num_in_slice):
      start = random.choice(valid_days)
      end = np.datetime64(graphtools.string_to_datetime(str(start))) + np.timedelta64(slice_time, 'D')
      slices.append((start, int(str(end)[:10].replace('-',''))))
    low += section_length
    high += section_length
  return slices

def random_slices(slice_time=1, num_slices=100):
  slices = []
  for i in range(num_slices):
    start = random.choice(_days)
    end = np.datetime64(graphtools.string_to_datetime(str(start))) + np.timedelta64(slice_time, 'D')
    slices.append((start, str(end)[:10].replace('-','')))
  return slices
