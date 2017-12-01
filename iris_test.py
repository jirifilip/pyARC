import pandas as pd
import random
from CBA import CBA

iris = pd.read_csv("iris_dataset.csv", sep=";", header = None)

iris_data = iris.values

iris_y = iris.loc[:,4].values.tolist()
iris_x = iris.loc[:, 0:3].values.tolist()
random.shuffle(iris_x)
random.shuffle(iris_y)

def transform_row(row):
    sep_l, sep_w, pet_l, pet_w = row
    return [
        ("sep_l", sep_l),
        ("sep_w", sep_w),
        ("pet_l", pet_l),
        ("pet_w", pet_w)
    ]

def transform_class(row):
    class_val = row
    return ("class", class_val)

i_x = list(map(transform_row, iris_x))
i_y = list(map(transform_class, iris_y))

iris_len = len(i_x)
split = int(0.75 * iris_len)
i_train_x = i_x[:split]
i_test_x = i_x[split:]
i_train_y = i_y[:split]
i_test_y = i_y[split:]

correct_classes = list(map(lambda x: int(x[1]), i_test_y))

rules = []

cba = CBA(0.5, 0.5)
cba.fit(i_train_x, i_train_y)

classes = list(map(int, cba.predict_all(i_test_x)))
print(classes)
print(correct_classes)
"""
mistakes = 0
test_len = len(i_test_x)
for idx, case in enumerate(i_test_x):
    prediction = cba.predict(frozenset(case))
    if not (i_test_y[idx][1] == prediction):
        mistakes += 1
    else:
        pass

print("{0}/{1} classified correctly".format(test_len - mistakes, test_len))

def _print_rules(rules):
    for rule in rules:
        print(rule)

_print_rules(rules)

_print_rules(cba.list_classifier_rules())
"""