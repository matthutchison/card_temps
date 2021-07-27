from card_temps import Temps, preprocess_rows
from datetime import datetime
from itertools import groupby
import math
import matplotlib.pyplot as plt

def plot(temps: Temps):
    vals = sorted(preprocess_rows(temps), key=lambda x: (x['processor'], x['date']))
    vals = [(k, list(g)) for k,g in groupby(vals, lambda x: x['processor'])]
    fig, ax = plt.subplots(ncols=2, nrows=math.ceil(len(vals)/2), sharey=True)
    for val, a in zip(vals, ax.flatten()):
        for key in ('min', 'max', 'avg'):
            x = [datetime.strptime(v['date'], '%Y-%m-%d').date() for v in val[1]]
            y = [v[key] for v in val[1]]
            a.plot_date(x, y, '-', label=f'{key}')
            a.set_xlim(x[0], x[-1])
            a.set_title(f'Processor {val[0]}')
    fig.autofmt_xdate()
    fig.text(0.04, 0.5, 'Temperature (Celsius)', va='center', rotation='vertical')
    fig.text(0.5, 0.04, 'Date', ha='center')
    fig.legend(ax[0][0].get_lines(), ['min', 'max', 'avg'], loc='upper center', ncol=3)
    plt.show()