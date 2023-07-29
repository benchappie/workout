"""do data analysis stuff with workout info, eventually based on user desires"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

#import
data = pd.read_csv("fitness_frame.csv", usecols=[1,2,3,4,5])

plt.style.use('seaborn')

#give a chart of dates worked out in past month, requires converting of values
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
data.sort_values('date', inplace=True)

workout_dates = data['date']

#print data for histogram after conversion (view only)
print(workout_dates)

#build the plot
plt.hist(workout_dates, rwidth=0.25)
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
plt.title('Frequency of Workouts')
plt.xlabel('Month')
plt.ylabel('No. Workouts')

plt.show()