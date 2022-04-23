import csv
from default_clf import DefaultNSL
from itertools import chain
from time import process_time

import numpy as np
import pandas as pd

NUM_PASSES = 100
NUM_ACC_PASSES = 50
TRAIN_PATH = 'data/KDDTrain+.csv'
TEST_PATH = 'data/KDDTest+.csv'

ATTACKS = {
    'normal': 'normal',

    'back': 'DoS',
    'land': 'DoS',
    'neptune': 'DoS',
    'pod': 'DoS',
    'smurf': 'DoS',
    'teardrop': 'DoS',
    'mailbomb': 'DoS',
    'apache2': 'DoS',
    'processtable': 'DoS',
    'udpstorm': 'DoS',

    'ipsweep': 'Probe',
    'nmap': 'Probe',
    'portsweep': 'Probe',
    'satan': 'Probe',
    'mscan': 'Probe',
    'saint': 'Probe',

    'ftp_write': 'R2L',
    'guess_passwd': 'R2L',
    'imap': 'R2L',
    'multihop': 'R2L',
    'phf': 'R2L',
    'spy': 'R2L',
    'warezclient': 'R2L',
    'warezmaster': 'R2L',
    'sendmail': 'R2L',
    'named': 'R2L',
    'snmpgetattack': 'R2L',
    'snmpguess': 'R2L',
    'xlock': 'R2L',
    'xsnoop': 'R2L',
    'worm': 'R2L',

    'buffer_overflow': 'U2R',
    'loadmodule': 'U2R',
    'perl': 'U2R',
    'rootkit': 'U2R',
    'httptunnel': 'U2R',
    'ps': 'U2R',
    'sqlattack': 'U2R',
    'xterm': 'U2R'
}


def get_current_charge():
    try:
        with open('/sys/class/power_supply/BAT0/charge_now') as f:
            return int(f.readline())
    except IOError:
        print("Cannot find current battery charge.")
        return 0


def check_load_training(clf, path):
    start = process_time()
    clf.load_training_data(path)
    end = process_time()
    return end - start


def check_load_testing(clf, path):
    start = process_time()
    clf.load_test_data(path)
    end = process_time()
    return end - start


def check_training(clf):
    start = process_time()
    clf.train_clf()
    end = process_time()
    return end - start


def check_testing_entire_dataset(clf, train=False):
    start = process_time()
    clf.test_clf(train)
    end = process_time()
    return end - start


def check_predict_row(clf, row):
    start = process_time()
    clf.predict(row)
    end = process_time()
    return end - start


def get_stats(arr, function, *args, **kwargs):
    charge_start = get_current_charge()
    for i in range(NUM_PASSES):
        arr[i] = function(*args, **kwargs)
    charge_end = get_current_charge()
    mean = arr.mean()
    std = arr.std()
    return [mean, std, (charge_start - charge_end)]


def evaluate_power(clf):
    res = np.empty(shape=(NUM_PASSES, 1))
    load_train = get_stats(res, check_load_training, clf, TRAIN_PATH)
    print('Loading Training: ', load_train)
    load_test = get_stats(res, check_load_testing, clf, TEST_PATH)
    print('Loading Testing: ', load_test)
    train = get_stats(res, check_training, clf)
    print('Training: ', train)
    test_dataset = get_stats(res, check_testing_entire_dataset, clf)
    print('Testing dataset: ', test_dataset)
    row = clf.testing[0].iloc[0].values.reshape(1, -1)
    test_row = get_stats(res, check_predict_row, clf, row)
    print('Testing one row: ', test_row)
    with open('results.csv', 'a', newline='') as csvf:
        csv_writer = csv.writer(csvf)
        csv_writer.writerow([clf.__class__.__name__, 'Number of Passes:', NUM_PASSES, 'Power'])
        csv_writer.writerow(['Function', 'Time (s) Mean', 'Time Std',
                             'Total Power (microwatt-hour)'])
        csv_writer.writerow(['Loading Training Data'] + load_train)
        csv_writer.writerow(['Loading Testing Data'] + load_test)
        csv_writer.writerow(['Training Classifier'] + train)
        csv_writer.writerow(['Testing Dataset'] + test_dataset)
        csv_writer.writerow(['Testing One Row'] + test_row)


def evaluate_accuracy(clf):
    acc = np.empty(shape=(NUM_ACC_PASSES, 1))
    clf.load_training_data(TRAIN_PATH)
    clf.load_test_data(TEST_PATH)
    cat_labels = clf.testing[1].apply(lambda x: ATTACKS[x])
    cats = {'U2R':[np.zeros(shape=(NUM_ACC_PASSES, 1)), np.zeros(shape=(NUM_ACC_PASSES, 1))],
            'DoS':[np.zeros(shape=(NUM_ACC_PASSES, 1)), np.zeros(shape=(NUM_ACC_PASSES, 1))],
            'R2L':[np.zeros(shape=(NUM_ACC_PASSES, 1)), np.zeros(shape=(NUM_ACC_PASSES, 1))],
            'Probe':[np.zeros(shape=(NUM_ACC_PASSES, 1)), np.zeros(shape=(NUM_ACC_PASSES, 1))],
            'normal':[np.zeros(shape=(NUM_ACC_PASSES, 1)), np.zeros(shape=(NUM_ACC_PASSES, 1))]}
    for i in range(0, NUM_ACC_PASSES):
        clf.train_clf()
        preds, acc[i] = clf.test_clf()
        for cat, pred in zip(cat_labels, preds):
            cats[cat][pred == 'normal'][i] += 1
        clf.shuffle_training_data()
    conf = calculate_category_accuracy(cats)
    mean = acc.mean()
    std = acc.std()
    write_acc_to_csv([mean, std], cats, conf, clf.__class__.__name__)
    return [mean, std]


def calculate_category_accuracy(cats):
    conf = {'TN':np.zeros(shape=(NUM_ACC_PASSES, 1)), 'TP':np.zeros(shape=(NUM_ACC_PASSES, 1)),
            'FN':np.zeros(shape=(NUM_ACC_PASSES, 1)), 'FP':np.zeros(shape=(NUM_ACC_PASSES, 1))}
    for key, values in cats.items():
        correct = values[0]
        wrong = values[1]
        if key == 'normal':
            correct, wrong = wrong, correct
            conf['TN'] += correct
            conf['FP'] += wrong
        else:
            conf['TP'] += correct
            conf['FN'] += wrong
        avg = correct/(correct+wrong)
        cats[key] = [avg.mean(), avg.std()]
    return conf


def write_acc_to_csv(acc, cats, conf, name):
    with open('results.csv', 'a', newline='') as csvf:
        csv_writer = csv.writer(csvf)
        csv_writer.writerow([name, 'Number of Passes:', NUM_ACC_PASSES, 'Accuracy'])
        csv_writer.writerow(['Statistic', 'Mean', 'STD'])
        csv_writer.writerow(['Accuracy'] + acc)
        for key, values in cats.items():
            csv_writer.writerow([key] + values)
        for key, values in conf.items():
            csv_writer.writerow([key, values.mean(), values.std()])