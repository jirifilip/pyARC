from .transforms import (
    RuleRefitter,
    RuleLiteralPruner,
    RuleTrimmer,
    RuleExtender,
    RulePostPruner,
    RuleOverlapPruner
)


class QCBATransformation:


    def __init__(self, quantitative_dataset, transaction_based_drop=True):
        self.transaction_based_drop = transaction_based_drop

        self.dataset = quantitative_dataset

        self.refitter = RuleRefitter(self.dataset)
        self.literal_pruner = RuleLiteralPruner(self.dataset)
        self.trimmer = RuleTrimmer(self.dataset)
        self.extender = RuleExtender(self.dataset)
        self.post_pruner = RulePostPruner(self.dataset)
        self.overlap_pruner = RuleOverlapPruner(self.dataset)


    def transform(self, rules, transformation_dict={}):

        if not transformation_dict:
            print("applying all transformations")
            refitted = self.refitter.transform(rules)
            literal_pruned = self.literal_pruner.transform(refitted)
            trimmed = self.trimmer.transform(literal_pruned)
            extended = self.extender.transform(trimmed)
            post_pruned, default_class = self.post_pruner.transform(extended)
            overlap_pruned = self.overlap_pruner.transform(post_pruned, default_class, transaction_based=self.transaction_based_drop)
        
        else:
            print("applying selected transformations")
            transformed_rules = rules
 
            if transformation_dict.get("refitting", False):
                print("refitting")
                transformed_rules = self.refitter.transform(transformed_rules)
            if transformation_dict.get("literal_pruning", False):
                print("literal pruning")
                transformed_rules = self.literal_pruner.transform(transformed_rules)
            if transformation_dict.get("trimming", False):
                print("trimming")
                transformed_rules = self.trimmer.transform(transformed_rules)
            if transformation_dict.get("extension", False):
                print("extending")
                transformed_rules = self.extender.transform(transformed_rules)

            print("post pruning")
            transformed_rules, default_class = self.post_pruner.transform(transformed_rules)
            
            if transformation_dict.get("overlap_pruning", False):
                print("overlap pruning")
                transaction_based = transformation_dict["transaction_based_drop"]

                transformed_rules = self.overlap_pruner.transform(transformed_rules, default_class, transaction_based=transaction_based)

            return transformed_rules, default_class


        return overlap_pruned, default_class

