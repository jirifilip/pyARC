from CBA import CBA

dataset = [
    [("A", 1), ("B", 1), ("C", 1), ("D", 0), ("E", 0)],
    [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 1)],
    [("A", 1), ("B", 0), ("C", 1), ("D", 1), ("E", 0)],
    [("A", 1), ("B", 0), ("C", 1), ("D", 1), ("E", 1)],
    [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 0)],
    [("A", 1), ("B", 1), ("C", 1), ("D", 0), ("E", 0)],
    [("A", 1), ("B", 0), ("C", 0), ("D", 1), ("E", 1)],
    [("A", 1), ("B", 1), ("C", 0), ("D", 0), ("E", 1)],
    [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 0)],
    [("A", 1), ("B", 0), ("C", 0), ("D", 0), ("E", 1)],
]

test = [
    [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 0)],
    [("A", 1), ("B", 1), ("C", 1), ("D", 0), ("E", 0)],
    [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 1)],
    [("A", 1), ("B", 1), ("C", 0), ("D", 0), ("E", 0)],
]

test_Y = [
    ("Class", 1),
    ("Class", 1),
    ("Class", 0),
    ("Class", 0),
]

Y = [
    ("Class", 1),
    ("Class", 1),
    ("Class", 0),
    ("Class", 0),
    ("Class", 1),
    ("Class", 0),
    ("Class", 0),
    ("Class", 0),
    ("Class", 1),
    ("Class", 1),
]

cba = CBA(1, 1)
cba.fit(dataset, Y)
cba.predict(frozenset([("A", 0), ("B", 1)]))

rules = cba.list_classifier_rules()

def _print_rules(rules):
    for rule in rules:
        print(rule)

_print_rules(rules)