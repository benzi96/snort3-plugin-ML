"""Linear SVM Classifier"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import LinearSVC

from default_clf import DefaultNSL, COL_NAMES, USE_COL_NAMES, ATTACKS

class SVM_NSL(DefaultNSL):

    def __init__(self):
        super(SVM_NSL, self).__init__()

    @staticmethod
    def load_data(filepath):
        # Preselected features using InfoGain Ranker
        infogain_ind = [3, 4, 5, 6, 10, 11, 12, 13, 16, 17, 18, 19,
                        20, 21, 22, 23, 24, 25, 26]
        data = pd.read_csv(filepath, names=COL_NAMES, usecols=USE_COL_NAMES, index_col=False)
        # Shuffle data
        data = data.sample(frac=1).reset_index(drop=True)
        labels = data['labels']
        data = data.iloc[:, infogain_ind]
        nom_ind = [0]
        # Convert nominal to category codes
        for num in nom_ind:
            data.iloc[:, num] = data.iloc[:, num].astype('category')
            data.iloc[:, num] = data.iloc[:, num].cat.codes
        # Scale all data to [0-1]
        scaler = MinMaxScaler()
        data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
        return [data, labels]

    def train_clf(self):
        train_data, train_labels = self.training
        bin_labels = train_labels.apply(lambda x: ATTACKS[x])
        self.clf = LinearSVC(C=8)
        self.clf.fit(train_data, bin_labels)

    def test_clf(self, train=False):
        if train:
            data, labels = self.training
        else:
            data, labels = self.testing
        #bin_labels = labels.apply(lambda x: ATTACKS[x])
        test_preds = self.clf.predict(data)
        #test_acc = sum(test_preds == bin_labels)/len(test_preds)
        return [test_preds, 10]
    
    def predict(self, packet):
        # Preselected features using InfoGain Ranker
        infogain_ind = [3, 4, 5, 6, 10, 11, 12, 13, 16, 17, 18, 19,
                        20, 21, 22, 23, 24, 25, 26]
        data = pd.DataFrame(packet, columns=USE_COL_NAMES)
        # Shuffle data
        data = data.sample(frac=1).reset_index(drop=True)
        labels = data['labels']
        data = data.iloc[:, infogain_ind]
        nom_ind = [0]
        # Convert nominal to category codes
        for num in nom_ind:
            data.iloc[:, num] = data.iloc[:, num].astype('category')
            data.iloc[:, num] = data.iloc[:, num].astype('category').cat.codes
        # Scale all data to [0-1]
        scaler = MinMaxScaler()
        data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
        predict = self.clf.predict(data)
        return predict
