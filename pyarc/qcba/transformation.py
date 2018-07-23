from .transforms import (
    RuleRefitter,
    RuleLiteralPruner,
    RuleTrimmer,
    RuleExtender,
    RulePostPruner,
    RuleOverlapPruner
)


class QCBATransformation:


    def __init__(self, quantitative_dataset):
        self.dataset = quantitative_dataset

        self.refitter = RuleRefitter(self.dataset)
        self.literal_pruner = RuleLiteralPruner(self.dataset)
        self.trimmer = RuleTrimmer(self.dataset)
        self.extender = RuleExtender(self.dataset)
        self.post_pruner = RulePostPruner(self.dataset)
        self.overlap_pruner = RuleOverlapPruner(self.dataset)


    def transform(self, rules):
        refitted = self.refitter.transform(rules)
        literal_pruned = self.literal_pruner.transform(refitted)
        trimmed = self.trimmer.transform(literal_pruned)
        extended = self.extender.transform(trimmed)
        post_pruned, default_class = self.post_pruner.transform(extended)

        return post_pruned, default_class

