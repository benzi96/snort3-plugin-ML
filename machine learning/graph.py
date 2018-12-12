import matplotlib.pyplot as plt
import numpy as np
from kmeans import KMeansNSL
import pandas as pd

kmean = KMeansNSL()

kmean.load_training_data('datasets/KDDTrain+.csv')
kmean.train_clf()
kmean.load_test_data('datasets/KDDTest+.csv')
ind = np.arange(4)
width = 0.1
ans, clusters = kmean.test_clf()
print(clusters)
normal = []
# anom = []
dos = []
probe = []
r2l = []
u2r = []
bin_ans = ans.groupby(['kmean', 'label']).size()
print(bin_ans)
roof = round(bin_ans.max(), -2) + 3000
for i in range(0,4):
    normal.append(bin_ans[i]['normal'])
    # anom.append(bin_ans[i]['anomaly'])
    dos.append(bin_ans[i]['DoS'])
    probe.append(bin_ans[i]['Probe'])
    r2l.append(bin_ans[i]['R2L'])
    if('R2L' in bin_ans.loc[i, :]):
        u2r.append(bin_ans[i]['U2R'])
    else:    
        u2r.append(0)
fig, ax = plt.subplots()
rects1 = ax.bar(ind - width*2, normal, width, color='grey')
# rects2 = ax.bar(ind + width, anom, width=0.1, color='crimson')
rects2 = ax.bar(ind - width, dos, width, color='crimson')
rects3 = ax.bar(ind, probe, width, color='lightblue')
rects4 = ax.bar(ind + width, r2l, width, color='yellow')
rects5 = ax.bar(ind + width*2, u2r, width, color='orange')
ax.set_ylabel('Number of Rows')
ax.set_title('Distribution of Clusters')
ax.set_yticks(np.arange(roof, step=roof/6))
ax.set_xlabel('Clusters')
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('1', '2', '3', '4'))
# ax.legend((rects1[0], rects2[0]), ('Normal', 'Anomaly'))
ax.legend((rects1[0], rects2[0], rects3[0], rects4[0], rects5[0]), ('Normal', 'Dos', 'Probe', 'R2L', 'U2R'))

def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
autolabel(rects1, ax)
autolabel(rects2, ax)
autolabel(rects3, ax)
autolabel(rects4, ax)
autolabel(rects5, ax)
plt.show()