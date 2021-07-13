import matplotlib.pyplot as plt
from period_predictor import *

if __name__ == '__main__':
  periods = PeriodParser('sample.txt')
  predictor = PeriodPredictor(periods, 50)

  fig = plt.figure()
  ax1 = fig.add_subplot(221, xlabel='Date', ylabel='Period Interval [days]')
  ax2 = fig.add_subplot(222, xlabel='Days', ylabel='Interval Histogram')
  ax3 = fig.add_subplot(212, xlabel='Date', ylabel='Future Probability Distribution')

  ax = [ax1, ax2, ax3]

  ax1.plot_date(periods.start_dates[0:-1], periods.intervals,lw=0,marker='o')
  ax2.hist(periods.intervals, bins=range(24,35))

  ax3.plot_date(predictor.dates, predictor.cumulative_prob, '-b')

  [a.grid() for a in ax]

  plt.draw()
  plt.pause(0.001)
  
  while(True):
    d1 = input("Enter a start date (YYYY-MM-DD): ")
    d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')
    if not predictor.contains(d1):
      continue

    d2 = input("Enter an end date (YYYY-MM-DD): ")
    d2 = datetime.datetime.strptime(d2, '%Y-%m-%d')
    if not predictor.contains(d2):
      continue

    delta = (d2-d1).days
    for i, date in enumerate(predictor.dates):
      if (d1 - date).total_seconds() == 0:
        break
    
    print("Probability = ", sum(predictor.cumulative_prob[i : i+delta]))