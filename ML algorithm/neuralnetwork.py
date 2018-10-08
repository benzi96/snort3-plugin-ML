"""K-Means Classifier"""
import pandas as pd
from sklearn.preprocessing import minmax_scale
from sklearn.neural_network import MLPClassifier

from default_clf import DefaultNSL, COL_NAMES, ATTACKS

class NeuralNetworkNSL(DefaultNSL):

     def __init__(self):
        super(NeuralNetworkNSL, self).__init__()

    @staticmethod
    def load_data(filepath):
        data = pd.read_csv(filepath, names=COL_NAMES, index_col=False)
        # Shuffle data
        data = data.sample(frac=1).reset_index(drop=True)
        NOM_IND = [1, 2, 3]
        BIN_IND = [6, 11, 13, 14, 20, 21]
        # Need to find the numerical columns for normalization
        NUM_IND = list(set(range(40)).difference(NOM_IND).difference(BIN_IND))
        # Convert nominal to category codes
        for num in NOM_IND:
            data.iloc[:, num] = data.iloc[:, num].astype('category')
            data.iloc[:, num] = data.iloc[:, num].astype('category').cat.codes
        # Scale all numerical data to [0-1]
        data.iloc[:, NOM_IND] = minmax_scale(data.iloc[:, NOM_IND])
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
        # data = pd.DataFrame([packet], columns=COL_NAMES)
        data = pd.DataFrame(packet, columns=COL_NAMES)
        # Shuffle data
        data = data.sample(frac=1).reset_index(drop=True)
        NOM_IND = [1, 2, 3]
        BIN_IND = [6, 11, 13, 14, 20, 21]
        # Need to find the numerical columns for normalization
        NUM_IND = list(set(range(40)).difference(NOM_IND).difference(BIN_IND))
        # Convert nominal to category codes
        for num in NOM_IND:
            data.iloc[:, num] = data.iloc[:, num].astype('category')
            data.iloc[:, num] = data.iloc[:, num].astype('category').cat.codes
        # Scale all numerical data to [0-1]
        data.iloc[:, NOM_IND] = minmax_scale(data.iloc[:, NOM_IND])
        data.iloc[:, NUM_IND] = minmax_scale(data.iloc[:, NUM_IND])
        labels = data['labels']
        del data['labels']
        predict = self.clf.predict(data)
        # return predict[0]
        return predict