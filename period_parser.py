import numpy as np 
import datetime

class PeriodParser:
  def __init__(self, fp):
    self.start_dates = self._parse_dates(fp)
    self.intervals = self._gen_intervals()
    self.probability_dist = self._gen_dist()

  def _parse_dates(self, fp):
    periods = []
    with open(fp, 'r') as f:
      for line in f:
        if line.endswith('Period Starts\n'):
          line = line.split('	')[0]
          periods.append(datetime.datetime.strptime(line, '%b %d, %Y'))
    return periods

  def _gen_intervals(self):
    intervals = []
    previous_period = self.start_dates[0] 
    for period in self.start_dates[1:]:
      delta = period-previous_period
      intervals.append(delta.days)
      previous_period = period
    return intervals

  def _gen_dist(self):
    counts = [0] * (max(*self.intervals)+1)
    for period in self.intervals:
      counts[period] += 1

    counts_sum = sum(counts)
    for i, val in enumerate(counts):
      counts[i] = val/counts_sum

    return counts

  @property
  def avg(self):
    return np.mean(self.intervals)

  @property
  def std(self):
    return np.std(self.intervals)