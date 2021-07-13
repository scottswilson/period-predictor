from period_parser import *

class PeriodPredictor:
  def __init__(self, period_parser, num_periods):
    if not isinstance(period_parser, PeriodParser):
      raise TypeError("Pass a PeriodParser object into the constructor.")

    self.data = period_parser
    self.max = len(self.data.probability_dist)
    self.probs = self.get_probs(num_periods)

    self.cumulative_prob = self.get_cumulative_prob()

    self.dates = self.get_dates()

  def get_probs(self, num_periods):
    days = range(len(self.data.probability_dist)*num_periods)

    first_prob = [0.0] * len(days)
    for i, val in enumerate(self.data.probability_dist):
      first_prob[i] =  val

    probs = [first_prob]

    for i in range(num_periods):
      new_prob = [0.0] * len(days)
      for day_j, last_prob_day_j in enumerate(probs[-1]):
        for day_k, fundamental_k in enumerate(self.data.probability_dist):
          if day_j+day_k >= len(days):
            continue
          new_prob[day_j+day_k] += last_prob_day_j * fundamental_k
      probs.append(new_prob)
    return probs

  def get_cumulative_prob(self):
    ar = [0.0]*len(self.probs[0])
    for prob in self.probs:
      for i, val in enumerate(prob):
        ar[i] += val
    return ar

  def get_dates(self):
    dates = []
    recent_start_date = self.data.start_dates[-1]
    for i in range(len(self.cumulative_prob)):
      dates.append(recent_start_date + datetime.timedelta(days=i))
    return dates

  def contains(self, date):
    if (date - self.dates[0]).total_seconds() < 0:
      return False
    return (date - self.dates[-1]).total_seconds() < 0