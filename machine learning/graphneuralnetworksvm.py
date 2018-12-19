import matplotlib.pyplot as plt
import numpy as np
from neuralnetwork import NeuralNetworkNSL
from svm import SVM_NSL
# %matplotlib inline

# neuralnetworknsl = NeuralNetworkNSL()
# neuralnetworknsl.load_training_data('datasets/KDDTrain+.csv')
# neuralnetworknsl.train_clf()
# neuralnetworknsl.load_test_data('datasets/KDDTest+.csv')
# neuralnetworknsl.load_test_data('datasets/KDDTrain+.csv')
# neuralnetworknsl.load_test_data('datasets/surfweb.csv')

# svmnsl = SVM_NSL()
# svmnsl.load_training_data('datasets/KDDTrain+.csv')
# svmnsl.train_clf()
# svmnsl.load_test_data('datasets/KDDTest+.csv')

# test_preds, test_cat_labels = neuralnetworknsl.test_clf()

# print(test_preds)
# cats = {'U2R':[0, 0, 0, 0], 'DoS':[0, 0, 0, 0], 'R2L':[0, 0, 0, 0], 'Probe':[0, 0, 0, 0], 'normal':[0, 0, 0, 0]}
cats = {'U2R': [0, 52, 0, 125921], 'DoS': [43178, 2749, 1482, 78564], 'R2L': [0, 995, 1, 124977], 'Probe': [9198, 2458, 2403, 111914], 'normal': [64061, 3282, 5650, 52980]}

# for cat, pred in zip(test_cat_labels, test_preds):
#     cats[cat][pred=='normal'] += 1
# print(cats)

# # for cat, pred in zip(test_cat_labels, test_preds):
#     if(cat=='DoS'and pred=='DoS'):
#         cats[cat][0] += 1
#     if(cat=='Probe' and pred=='Probe'):
#         cats[cat][0] += 1
#     if(cat=='U2R' and pred=='U2R'):
#         cats[cat][0] += 1
#     if(cat=='R2L' and pred=='R2L'):
#         cats[cat][0] += 1
#     if(cat=='normal' and pred=='normal'):
#         cats[cat][0] += 1

#     if(cat=='DoS' and pred!='DoS'):
#         cats[cat][1] += 1
#     if(cat=='Probe' and pred!='Probe'):
#         cats[cat][1] += 1
#     if(cat=='U2R' and pred!='U2R'):
#         cats[cat][1] += 1
#     if(cat=='R2L' and pred!='R2L'):
#         cats[cat][1] += 1
#     if(cat=='normal' and pred!='normal'):
#         cats[cat][1] += 1

#     if(pred=='DoS' and cat!='DoS'):
#         cats['DoS'][2] += 1
#     if(pred=='Probe' and cat!='Probe'):
#         cats['Probe'][2] += 1
#     if(pred=='U2R' and cat!='U2R'):
#         cats['U2R'][2] += 1
#     if(pred=='R2L' and cat!='R2L'):
#         cats['R2L'][2] += 1
#     if(pred=='normal' and cat!='normal'):
#         cats['normal'][2] += 1

#     if(pred!='DoS' and cat!='DoS'):
#         cats['DoS'][3] += 1
#     if(pred!='Probe' and cat!='Probe'):
#         cats['Probe'][3] += 1
#     if(pred!='U2R' and cat!='U2R'):
#         cats['U2R'][3] += 1
#     if(pred!='R2L' and cat!='R2L'):
#         cats['R2L'][3] += 1
#     if(pred!='normal' and cat!='normal'):
#         cats['normal'][3] += 1

# print(cats)

ind = np.arange(5)
width = .20
fig, ax = plt.subplots(figsize=(14, 8))
# del cats['normal']

#True Positives: Positives predicted as Positives
TP = [values[0] for key, values in cats.items()]

#False Negatives: Positives predicted as Negatives
FN = [values[1] for key, values in cats.items()]

#False Positive: Negatives predicted as Positives
FP = [values[2] for key, values in cats.items()]

#True Negatives: Negatives predicted as Negatives
TN = [values[3] for key, values in cats.items()]

rect1 = ax.bar(ind - width, TP, width, color='black', edgecolor = 'black')
rect2 = ax.bar(ind, FN, width, color='silver', edgecolor = 'black')
rect3 = ax.bar(ind + width, FP, width, color='grey', edgecolor = 'black', hatch="o")
rect4 = ax.bar(ind + width + width, TN, width, color='whitesmoke', edgecolor = 'black', hatch="/")

# ax.set_ylabel('Number of Rows')
ax.set_ylabel('Số lượng gói tin')
# ax.set_title('Accuracy by Category')
ax.set_title('Tỉ lệ phân loại chính xác theo từng loại gói tin', y=1.08)
# ax.set_xlabel('Categories')
ax.set_xlabel('Loại gói tin')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(cats.keys())
ax.legend((rect1[0], rect2[0], rect3[0], rect4[0]), ('True Positives', 'False Negatives', 'False Positives', 'True Negatives'))

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
autolabel(rect3, ax)
autolabel(rect4, ax)
plt.show()