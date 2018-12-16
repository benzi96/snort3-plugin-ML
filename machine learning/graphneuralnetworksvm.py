import matplotlib.pyplot as plt
import numpy as np
# from neuralnetwork import NeuralNetworkNSL
from svm import SVM_NSL
# %matplotlib inline

# neuralnetworknsl = NeuralNetworkNSL()
# neuralnetworknsl.load_training_data('datasets/KDDTrain+.csv')
# neuralnetworknsl.train_clf()
# neuralnetworknsl.load_test_data('datasets/KDDTest+.csv')

svmnsl = SVM_NSL()
svmnsl.load_training_data('datasets/KDDTrain+.csv')
svmnsl.train_clf()
svmnsl.load_test_data('datasets/KDDTest+.csv')

test_preds, test_cat_labels = svmnsl.test_clf()

# print(test_preds)
cats = {'U2R':[0, 0], 'DoS':[0, 0], 'R2L':[0, 0], 'Probe':[0, 0], 'normal':[0, 0]}

# for cat, pred in zip(test_cat_labels, test_preds):
#     cats[cat][pred=='normal'] += 1
# print(cats)

for cat, pred in zip(test_cat_labels, test_preds):
    if(cat=='DoS'):
        cats[cat][pred=='DoS'] += 1
    if(cat=='Probe'):
        cats[cat][pred=='Probe'] += 1
    if(cat=='U2R'):
        cats[cat][pred=='U2R'] += 1
    if(cat=='R2L'):
        cats[cat][pred=='R2L'] += 1
    if(cat=='normal'):
        cats[cat][pred=='normal'] += 1

print(cats)

ind = np.arange(5)
width = .25
fig, ax = plt.subplots(figsize=(14,8))
# del cats['normal']
anoms = [values[0] for key, values in cats.items()]
norms = [values[1] for key, values in cats.items()]
rect1 = ax.bar(ind, anoms, width, color='crimson')
rect2 = ax.bar(ind + width, norms, width, color='grey')
ax.set_ylabel('Number of Rows')
ax.set_title('Accuracy by Category')
ax.set_xlabel('Categories')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(cats.keys())
ax.legend((rect1[0], rect2[0]), ('Số lượng phát hiện sai(FP)', 'Số lượng phát hiện đúng(TP)'))

def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
autolabel(rect1, ax)
autolabel(rect2, ax)
plt.show()