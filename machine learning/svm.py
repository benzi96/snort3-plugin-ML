"""Linear SVM Classifier"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import LinearSVC

from default_clf import DefaultNSL, COL_NAMES, ATTACKS

class SVM_NSL(DefaultNSL):

    @staticmethod
    def load_data(filepath):
        # Preselected features using InfoGain Ranker
        infogain_ind = [3, 4, 5, 6, 12, 23, 24, 25, 26, 29, 30, 31, 32,
                        33, 34, 35, 36, 37, 38, 39]
        data = pd.read_csv(filepath, names=COL_NAMES, index_col=False)
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
        # bin_labels = train_labels.apply(lambda x: x if x == 'normal' else 'anomaly')
        bin_labels = train_labels.apply(lambda x: ATTACKS[x])
        self.clf = LinearSVC(C=8)
        self.clf.fit(train_data, bin_labels)

    def test_clf(self, train=False):
        if train:
            data, labels = self.training
        else:
            data, labels = self.testing
        # bin_labels = labels.apply(lambda x: x if x == 'normal' else 'anomaly')
        test_cat_labels = labels.apply(lambda x: ATTACKS[x])
        test_preds = self.clf.predict(data)
        # test_acc = sum(test_preds == bin_labels)/len(test_preds)
        # return [test_preds, test_acc]
        return [test_preds, test_cat_labels]
    
    def predictSvm(self, packet):
        # Preselected features using InfoGain Ranker
        infogain_ind = [3, 4, 5, 6, 12, 23, 24, 25, 26, 29, 30, 31, 32,
                        33, 34, 35, 36, 37, 38, 39]
        data = pd.read_csv([packet], names=COL_NAMES)
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
        predict = self.clf.predict(data)
        return predict[0]