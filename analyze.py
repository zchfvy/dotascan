import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from data import matches

replays = []

radiant_win_flt = [(1.0 if r['radiant_win'] else 0.0) for r in matches]
radiant_winrate = sum(radiant_win_flt)/len(radiant_win_flt)
print("Radiant Winrate:", radiant_winrate)

times = np.array([r['duration'] for r in matches])
n, bins, patches = plt.hist(times, 50, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Duration')
plt.ylabel('Frequency')
plt.title('Game duraations')
plt.axis([0, 10000, 0, 0.1])
plt.grid(True)
plt.show()
