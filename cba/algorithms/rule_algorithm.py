class RuleBuilderAlgorithm:
    def __init__(self, rules, dataset):
        self.rules = rules
        self.dataset = dataset
        self.y = dataset.class_labels
        
