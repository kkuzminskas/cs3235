import distance
import matplotlib
import numpy as np


reference_files = [f"data/k{i+1}.txt" for i in range(8)]


def determine_thresholds():
    # reference files definition
    training_neg_files = ["youkuan1.txt", "youkuan2.txt", "youkuan3.txt", "youkuan4.txt", "youkuan5.txt",
                          "siqi1.txt", "siqi2.txt", "siqi3.txt", "siqi4.txt", "siqi5.txt", "ahmed1.txt"]
    training_pos_files = ["data/k9.txt", "data/k10.txt", "data/k11.txt"]

    training_neg_files = ["data/" + l for l in training_neg_files]
    neg_dist = np.array([distance.distances(reference_files, l, 'raw')
                         for l in training_neg_files])
    pos_dist = np.array([distance.distances(reference_files, l, 'raw')
                         for l in training_pos_files])
    raw_thresholds = (neg_dist.min(axis=0) + pos_dist.max(axis=0)) / 2
    neg_dist = np.array([distance.distances(reference_files, l, 'avg')
                         for l in training_neg_files])
    pos_dist = np.array([distance.distances(reference_files, l, 'avg')
                         for l in training_pos_files])
    avg_thresholds = (neg_dist.min(axis=0) + pos_dist.max(axis=0)) / 2
    return raw_thresholds, avg_thresholds


def test_with_files(test_files, test_labels, raw_thresholds, avg_thresholds):
    def find_metrics(class_labels):
        positives = np.sum(class_labels)
        true_postives = np.sum(np.logical_and(
            test_labels == 1, class_labels == 1))
        false_positives = positives - true_postives

        negatives = len(test_labels) - positives
        true_negatives = np.sum(np.logical_and(
            test_labels == 0, class_labels == 0))
        false_negatives = negatives - true_negatives

    avg_distances = np.array(
        [distance.distances(reference_files, f, 'avg') for f in test_files])
    avg_classifications = 1 if avg_distances < avg_thresholds else 0


    # def determine_thresholds()
np.set_printoptions(suppress=True)
determine_thresholds()
