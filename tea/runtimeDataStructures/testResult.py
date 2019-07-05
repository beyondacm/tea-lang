from tea.global_vals import *
from enum import Enum
from .value import Value
from tea.ast import DataType, LessThan, GreaterThan

# Other
import attr

@attr.s(init=True)
class TestResult(Value): 
    name = attr.ib()
    test_statistic = attr.ib()
    p_value = attr.ib()
    # dof = attr.ib() # degrees of freedom, a tuple (numerator, denominator)
    
    def adjust_p_val(self, correction): 
        self.self.adjusted_p_value = attr.ib()
        self.self.adjusted_p_value = self.p_value/correction
    
    def set_adjusted_p_val(self, adjusted_p_value): 
        self.self.adjusted_p_value = attr.ib()
        self.self.adjusted_p_value = adjusted_p_value

    def add_effect_size(self, name, effect_size): 
        if hasattr(self, 'effect_size'):
            self.effect_size[name] = effect_size
        else: 
            self.effect_size = attr.ib()
            self.effect_size = {name : effect_size}
    
    def add_doc(self, name, dof):
        import pdb; pdb.set_trace()

class Significance(Enum): 
        not_significant = 0
        significantly_different = 1
        significantly_greater = 2
        significantly_less = 3

@attr.s(init=False)
class StudentsTResult(TestResult):
    # test_statistic = attr.ib()
    # p_value = attr.ib()
    dof = attr.ib()
    prediction = attr.ib()
    null_hypothesis = attr.ib(default="There is no difference in group means")
    interpretation = attr.ib(default=None)

    def __init__(self, test_statistic, p_value, dof, prediction):
        # call Super class
        TestResult.__init__(self, name="Student\'s T Test", test_statistic=test_statistic, p_value=p_value)
        self.dof = dof
        self.prediction = prediction

    def adjust_p_val(self):
        # Adjust p value
        if self.prediction: 

            one_sided = True if isinstance(self.prediction, GreaterThan) or isinstance(self.prediction, LessThan) else False
                # one_sided = True
            # one_sided = [(isinstance(*v, GreaterThan) or isinstance(*v, LessThan)) for v in self.prediction]

            if one_sided:
                self.adjusted_p_value = self.p_value/2
            else: 
                self.adjusted_p_value = self.p_value

    def specify_null_hypothesis(self, x, y):
        # TODO: Passing x and y seems more modular than passing string? 
        self.null_hypothesis = "Update to be more specific about the particular hypothesis being tested"

    def set_interpretation(self, alpha, x, y):
        """
            Based on https://stats.idre.ucla.edu/other/mult-pkg/faq/general/faq-what-are-the-differences-between-one-tailed-and-two-tailed-tests/
            From the example on this site:
            If t is negative and we are checking a less than relationship, use p/2 as the adjusted p-value.
            If t is negative and we are checking a greater than relationship, use 1 - p/2 as the adjusted p-value.
        """
        self.specify_null_hypothesis(x=x, y=y)
        
        one_sided = True if self.adjusted_p_value else False

        # Start interpretation
        ttest_result = Significance.not_significant
        if self.test_statistic > 0:
            if isinstance(self.prediction, GreaterThan) and self.adjusted_p_value < alpha:
                ttest_result = Significance.significantly_greater
            elif isinstance(self.prediction, LessThan) and 1 - self.adjusted_p_value < alpha:
                ttest_result = Significance.significantly_less
            elif not one_sided and self.adjusted_p_value < alpha:
                ttest_result = Significance.significantly_different
            else:
                ttest_result = Significance.not_significant
        elif self.test_statistic < 0:
            if isinstance(self.prediction, LessThan) and self.adjusted_p_value < alpha:
                ttest_result = Significance.significantly_less
            elif isinstance(self.prediction, GreaterThan) and 1 - self.adjusted_p_value < alpha:
                ttest_result = Significance.significantly_greater
            elif not one_sided and self.adjusted_p_value < alpha:
                ttest_result = Significance.significantly_different
            else:
                ttest_result = Significance.not_significant
        elif not one_sided and self.adjusted_p_value < alpha:
            ttest_result = ttest_result.significantly_different
        else:
            assert False, "test_statistic = 0 and it's not a one-sided test. Not sure under what conditions this is possible."

        self.interpretation = None
        if ttest_result == ttest_result.not_significant:
            self.interpretation = f"The difference in means of {y.metadata[name]} for {x.metadata[name]} = {self.prediction.lhs.value} " \
                f"and {x.metadata[name]} = {self.prediction.rhs.value} is not significant."
        elif ttest_result == ttest_result.significantly_different:
            self.interpretation = f"The difference in means of {y.metadata[name]} for {x.metadata[name]} = {self.prediction.lhs.value} " \
                f"and {x.metadata[name]} = {self.prediction.rhs.value} is significant."
        elif ttest_result == ttest_result.significantly_greater:
            self.interpretation = f"The mean of {y.metadata[name]} for {x.metadata[name]} = {self.prediction.lhs.value} is significantly" \
                f" greater than the mean for {x.metadata[name]} = {self.prediction.rhs.value}"
        elif ttest_result == ttest_result.significantly_less:
            self.interpretation = f"The mean of {y.metadata[name]} for {x.metadata[name]} = {self.prediction.lhs.value} is significantly" \
                f" less than the mean for {x.metadata[name]} = {self.prediction.rhs.value}"
        else:
            assert False, "ttest_result case without an associated self.interpretation."
        