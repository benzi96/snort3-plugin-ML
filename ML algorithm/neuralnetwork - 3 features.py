"""K-Means Classifier"""
import pandas as pd
from sklearn.preprocessing import minmax_scale
from sklearn.neural_network import MLPClassifier

from default_clf import DefaultNSL, COL_NAMES, USE_COL_NAMES, ATTACKS

class NeuralNetworkNSL(DefaultNSL):

    def __init__(self):
       	super(NeuralNetworkNSL, self).__init__()

    @staticmethod
    def load_data(filepath):
        data = pd.read_csv(filepath, names=COL_NAMES, usecols=USE_COL_NAMES, index_col=False)
        # Shuffle data
        data = data.sample(frac=1).reset_index(drop=True)
        # Need to find the numerical columns for normalization
        NUM_IND = [1, 2, 3]
        # Convert nominal to category codes
        
        data.iloc[:, NUM_IND] = minmax_scale(data.iloc[:, NUM_IND])
        labels = data['labels']
        del data['labels']
        return [data, labels]

    def train_clf(self):
        train_data, train_labels = self.training
        bin_labels = train_labels.apply(lambda x: ATTACKS[x])
        self.clf = MLPClassifier(hidden_layer_sizes=(20,), alpha=.7,
                                 beta_1=.8, beta_2=.8)
        self.clf.fit(train_data, bin_labels)

    def test_clf(self, train=False):
        if train:
            data, labels = self.training
        else:
            data, labels = self.testing
        bin_labels = labels.apply(lambda x: ATTACKS[x])
        test_preds = self.clf.predict(data)
        test_acc = sum(test_preds == bin_labels)/len(test_preds)
        return [test_preds, test_acc]

    def predict(self, packet):
        data = pd.DataFrame(packet, columns=USE_COL_NAMES)
        # Shuffle data
        data = data.sample(frac=1).reset_index(drop=True)
        NUM_IND = [1, 2, 3]
        
        data.iloc[:, NUM_IND] = minmax_scale(data.iloc[:, NUM_IND])
        labels = data['labels']
        del data['labels']
        predict = self.clf.predict(data)
        return predict
