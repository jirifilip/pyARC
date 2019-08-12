from .data_structures import QuantitativeCAR
from .transformation import QCBATransformation
from .classifier import QuantitativeClassifier

class QCBA:

    def __init__(self, quantitative_dataset, cba_rule_model=None, rules=None):
        if rules and cba_rule_model:
            raise Exception("rules and cba_rule_model cannot be specified together")

        if not rules and not cba_rule_model:
            raise Exception("either rules and cba_rule_model need to be specified")

        self.quantitative_dataset = quantitative_dataset
        self.__quant_rules = None

        if cba_rule_model:
            self.__quant_rules = [ QuantitativeCAR(r) for r in cba_rule_model.clf.rules ]
        if rules:
            self.__quant_rules = [ QuantitativeCAR(r) for r in rules ]
         

        self.qcba_transformation = QCBATransformation(quantitative_dataset)

        self.clf = None

    def fit(
            self, 
            refitting=True,
            literal_pruning=True,
            trimming=True,
            extension=True,
            overlap_pruning=True,
            transaction_based_drop=True
        ):

        transformation_dict = {
            "refitting": refitting,
            "literal_pruning": literal_pruning,
            "trimming": trimming,
            "extension": extension,
            "overlap_pruning": overlap_pruning,
            "transaction_based_drop": transaction_based_drop
        }

        transformed_rules, default_class = self.qcba_transformation.transform(self.__quant_rules, transformation_dict)

        self.clf = QuantitativeClassifier(transformed_rules, default_class)

        return self.clf


    def score(self, quantitative_dataset):
        actual = quantitative_dataset.dataframe.iloc[:, -1]
        
        return self.clf.rule_model_accuracy(quantitative_dataset, actual)