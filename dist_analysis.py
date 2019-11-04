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
        true_positives = np.sum(np.logical_and(
            test_labels == 1, class_labels == 1))
        false_positives = positives - true_positives

        negatives = len(test_labels) - positives
        true_negatives = np.sum(np.logical_and(
            test_labels == 0, class_labels == 0))
        false_negatives = negatives - true_negatives

        precision = true_positives / positives if positives != 0 else 1
        accuracy = (true_negatives + true_positives) / (positives + negatives)
        return true_positives, false_positives, true_negatives, false_negatives, accuracy, precision

    def print_results(coord_types, class_labels):
        dist_names = ["x_y distance", "x_y_t non whitened distance",
                      "x_y_t whitened distance", "x_y_lx_ly_rx_ry distance"]

        print("#####Results#####:")
        print(f"     {coord_types}:")
        for ind, labels in enumerate(class_labels):
            true_positives, false_positives, true_negatives, false_negatives, accuracy, precision = find_metrics(
                labels)
            print("     " + dist_names[ind])
            print(f"        true_positives  :{true_positives}")
            print(f"        false_positives :{false_positives}")
            print(f"        true_negatives  :{true_negatives}")
            print(f"        false_negatives :{false_negatives}")
            print(f"        Accuracy        :{accuracy}")
            print(f"        Precision       :{precision}")

    avg_distances = np.array(
        [distance.distances(reference_files, f, 'avg') for f in test_files]).T
    print(avg_distances)
    class_labels = np.zeros(avg_distances.shape)
    for i in range(4):
        print(avg_thresholds[i])
        class_labels[i][avg_distances[i] < avg_thresholds[i]] = 1

    print(class_labels)
    print_results('avg', class_labels)

    # raw_distances = np.array(
    #     [distance.distances(reference_files, f, 'raw') for f in test_files])
    # raw_classifications = 1 if avg_distances < raw_thresholds else 0
    # print_results('raw', raw_classifications)


raw_thresholds, avg_thresholds = determine_thresholds()
test_files = ["data/k1.txt", "data/k2.txt", "data/youkuan1.txt"]
labes = np.array([1, 1, 0])
test_with_files(test_files, labes, raw_thresholds, avg_thresholds)
