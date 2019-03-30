import tea
import os

base_url = 'https://homes.cs.washington.edu/~emjun/tea-lang/datasets/'
uscrime_data_path = None
states_path = None
cats_path = None
cholesterol_path = None
soya_path = None
co2_path = None
exam_path = None
liar_path = None 
pbcorr_path = None
spider_path = None
drug_path = None
alcohol_path = None
ecstasy_path = None
data_paths = [uscrime_data_path, states_path, cats_path, cholesterol_path, soya_path, co2_path, exam_path, liar_path, pbcorr_path, spider_path, drug_path, alcohol_path, ecstasy_path]
file_names = ['UScrime.csv', 'statex77.csv', 'catsData.csv', 'cholesterol.csv', 'soya.csv', 'co2.csv', 'exam.csv', 'liar.csv', 'pbcorr.csv','spiderLong.csv', 'drug.csv', 'alcohol.csv', 'ecstasy.csv']

def test_load_data():
    global base_url, data_paths, file_names
    global drug_path 

    for i in range(len(data_paths)):
        csv_name = file_names[i]

        csv_url = os.path.join(base_url, csv_name)
        data_paths[i] = tea.download_data(csv_url, csv_name)

# Example from Kabacoff
# Expected outcome: Pearson correlation 
def test_pearson_corr(): 
    print("\nPearson Correlation from Kabacoff")
    print("Expected outcome: Pearson")

    states_path = "/Users/emjun/.tea/data/statex77.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Illiteracy',
            'data type' : 'interval',
            'categories' : [0, 100]
        },
        {
            'name' : 'Life Exp',
            'data type' : 'ratio',
            # 'range' : [0,1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Illiteracy', 'Life Exp'],
                            'outcome variables': ''
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(states_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['Illiteracy', 'Life Exp'])

def test_pearson_corr_2(): 
    print("\nPearson Correlation from Field et al.")
    print("Expected outcome: Pearson")
    exam_path = "/Users/emjun/.tea/data/exam.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Exam',
            'data type' : 'ratio',
            'range' : [0, 100]
        },
        {
            'name' : 'Anxiety',
            'data type' : 'interval',
            'range' : [0, 100]
        },
        {
            'name' : 'Gender',
            'data type' : 'nominal',
            'categories' : ['Male', 'Female']
        },
        {
            'name' : 'Revise',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Anxiety', 'Gender', 'Revise'],
                            'outcome variables': 'Exam'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(exam_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    tea.hypothesize(['Anxiety', 'Exam'])
    tea.hypothesize(['Revise', 'Exam'])
    tea.hypothesize(['Anxiety', 'Revise'])

    # Anxiety, Exam, and Revise are all not normally distributed. Therefore, Tea picks spearman and kendall


def test_spearman_corr(): 
    print("\nPearson Correlation from Field et al.")
    print("Expected outcome: Spearman")

    liar_path = "/Users/emjun/.tea/data/liar.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Creativity',
            'data type' : 'interval'
        },
        {
            'name' : 'Position',
            'data type' : 'ordinal',
            'categories' : [6, 5, 4, 3, 2, 1] # ordered from lowest to highest
        },
        {
            'name' : 'Novice',
            'data type' : 'nominal',
            'categories' : [0, 1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Novice', 'Creativity'],
                            'outcome variables': 'Position'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(liar_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    tea.hypothesize(['Position', 'Creativity'], ['Position:1 > 6']) # TODO: allow for partial orders?

# Same as test for Spearman rho
def test_kendall_tau_corr(): 
    print("\nPearson Correlation from Field et al.")
    print("Expected outcome: Kendall Tau")

    liar_path = "/Users/emjun/.tea/data/liar.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Creativity',
            'data type' : 'interval'
        },
        {
            'name' : 'Position',
            'data type' : 'ordinal',
            'categories' : [6, 5, 4, 3, 2, 1] # ordered from lowest to highest
        },
        {
            'name' : 'Novice',
            'data type' : 'nominal',
            'categories' : [0, 1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Novice', 'Creativity'],
                            'outcome variables': 'Position'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(liar_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    tea.hypothesize(['Position', 'Creativity'], ['Position:1 > 6', 'Position:1 > 2']) # I think this works!?

def test_pointbiserial_corr(): 
    print("\nPearson Correlation from Field et al.")
    print("Expected outcome: Pointbiserial")

    pbcorr_path = "/Users/emjun/.tea/data/pbcorr.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'time',
            'data type' : 'ratio'
        },
        {
            'name' : 'gender',
            'data type' : 'nominal',
            'categories' : [0, 1] # ordered from lowest to highest
        },
        {
            'name' : 'recode',
            'data type' : 'nominal',
            'categories' : [0, 1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['gender', 'recode'],
                            'outcome variables': 'time'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(pbcorr_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    tea.hypothesize(['time', 'gender'], ['gender:1 > 0']) # I think this works!?


def test_indep_t_test():
    print("\nPearson Correlation from Kabacoff")
    print("Expected outcome: Student's t-test")

    global uscrime_data_path
    uscrime_data_path = "/Users/emjun/.tea/data/UScrime.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'So',
            'data type' : 'nominal',
            'categories' : ['0', '1']
        },
        {
            'name' : 'Prob',
            'data type' : 'ratio',
            'range' : [0,1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': 'So',
                            'outcome variables': 'Prob',
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
        'normal distribution': ['So']
    }

    tea.data(uscrime_data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['So', 'Prob'], ['So:1 > 0'])

    # tea.hypothesize(['So', 'Prob'], null='So:1 <= So:0', alternative='So:1 > So:0')
    # import pdb; pdb.set_trace()


def test_paired_t_test(): 
    print("\nPearson Correlation from Field et al.")
    print("Expected outcome: Paired/Dependent t-test")

    global spider_path
    spider_path = "/Users/emjun/.tea/data/spiderLong.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Group',
            'data type' : 'nominal',
            'categories' : ['Picture', 'Real Spider']
        },
        {
            'name' : 'Anxiety',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'Group',
                            'dependent variables': 'Anxiety',
                            'within subjects' : 'Group'

                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05
    }

    tea.data(spider_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['Group', 'Anxiety'], ['Group:Real Spider > Picture'])

def test_wilcoxon_signed_rank(): 
    print("\nPearson Correlation from Field et al.")
    print("Expected outcome: Wilcoxon signed rank test")

    # global alcohol_path
    alcohol_path = "/Users/emjun/.tea/data/alcohol.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'drug',
            'data type' : 'nominal',
            'categories' : ['Alcohol']
        },
        {
            'name' : 'day',
            'data type' : 'nominal',
            'categories': ['sundayBDI', 'wedsBDI']
        },
        {
            'name' : 'value',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'day',
                            'dependent variables': 'value',
                            'within subjects' : 'day'

                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05
    }

    tea.data(alcohol_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['day', 'value'], ['day:sundayBDI > wedsBDI'])

def test_f_test(): 
    cholesterol_path = "/Users/emjun/.tea/data/cholesterol.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'trt',
            'data type' : 'nominal',
            'categories' : ['1time', '2times', '4times', 'drugD', 'drugE']
        },
        {
            'name' : 'response',
            'data type' : 'ratio',
            # 'categories' : ['Yes', 'No']
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'trt',
                            'dependent variables': 'response'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(cholesterol_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['trt', 'response'])
        
def test_kruskall_wallis(): 
    soya_path = "/Users/emjun/.tea/data/soya.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Sperm',
            'data type' : 'interval'
        },
        {
            'name' : 'Soya',
            'data type' : 'ordinal',
            'categories': ['No Soya', '1 Soya Meal', '4 Soya Meals', '7 Soya Meals']
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            # 'study type': 'observational study', # shouldn't change anything
                            'independent variables': 'Soya',
                            'dependent variables': 'Sperm',
                            # 'within subjects': 'Soya' # Correctly does not choose Kruskall Wallis
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(soya_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['Soya', 'Sperm'])

"""
def test_anova_test(): 
    print("\nPearson Correlation from Field et al.")
    print("Expected outcome: Wilcoxon signed rank test")

    global drug_path
    # spider_path = "/Users/emjun/.tea/data/spiderLong.csv"

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'drug',
            'data type' : 'nominal',
            'categories' : ['Ecstasy', 'Alcohol']
        },
        {
            'name' : 'sundayBDI',
            'data type' : 'ratio'
        },
        {
            'name' : 'wedsBDI',
            'data type' : 'ratio'
        },
        {
            'name' : 'BDIchange',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'drug',
                            'dependent variables': '',
                            'within subjects' : 'Group'

                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05
    }

    tea.data(spider_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['Group', 'Anxiety'], ['Group:Real Spider > Picture'])
"""

# def test_chi_square(): 
#     cats_path = "/Users/emjun/.tea/data/catsData.csv"

#     # Declare and annotate the variables of interest
#     variables = [
#         {
#             'name' : 'Training',
#             'data type' : 'nominal',
#             'categories' : ['Food as Reward', 'Affection as Reward']
#         },
#         {
#             'name' : 'Dance',
#             'data type' : 'nominal',
#             'categories' : ['Yes', 'No']
#         }
#     ]
#     experimental_design = {
#                             'study type': 'observational study',
#                             'contributor variables': 'Training',
#                             'outcome variables': 'Dance'
#                         }
#     assumptions = {
#         'Type I (False Positive) Error Rate': 0.05,
#     }

#     tea.data(cats_path)
#     tea.define_variables(variables)
#     tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
#     tea.assume(assumptions)

#     tea.hypothesize(['Training', 'Dance'])





# def test_rm_one_way_anova(): 
#     co2_path = "/Users/emjun/.tea/data/co2.csv"

#     # Declare and annotate the variables of interest
#     variables = [
#         {
#             'name' : 'uptake',
#             'data type' : 'interval'
#         },
#         {
#             'name' : 'Type',
#             'data type' : 'nominal',
#             'categories': ['Quebec', 'Mississippi']
#         },
#         {
#             'name' : 'conc',
#             'data type' : 'ordinal',
#             'categories': [95, 175, 250, 350, 500, 675, 1000]
#         }
#     ]
#     experimental_design = {
#                             'study type': 'experiment',
#                             'independent variables': ['Type', 'conc'],
#                             'dependent variables': 'uptake',
#                             'within subjects': 'conc',
#                             'between subjects': 'Type'
#                         }
#     assumptions = {
#         'Type I (False Positive) Error Rate': 0.05,
#     }

#     tea.data(co2_path)
#     tea.define_variables(variables)
#     tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
#     tea.assume(assumptions)

#     tea.hypothesize(['uptake', 'conc']) # Picks friedman!

# def test_two_way_anova(): 
#     co2_path = "/Users/emjun/.tea/data/co2.csv"

#     # Declare and annotate the variables of interest
#     variables = [
#         {
#             'name' : 'uptake',
#             'data type' : 'interval'
#         },
#         {
#             'name' : 'Type',
#             'data type' : 'nominal',
#             'categories': ['Quebec', 'Mississippi']
#         },
#         {
#             'name' : 'conc',
#             'data type' : 'ordinal',
#             'categories': [95, 175, 250, 350, 500, 675, 1000]
#         }
#     ]
#     experimental_design = {
#                             'study type': 'experiment',
#                             'independent variables': ['Type', 'conc'],
#                             'dependent variables': 'uptake',
#                             'within subjects': 'conc',
#                             'between subjects': 'Type'
#                         }
#     assumptions = {
#         'Type I (False Positive) Error Rate': 0.05,
#     }

#     tea.data(co2_path)
#     tea.define_variables(variables)
#     tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
#     tea.assume(assumptions)

#     tea.hypothesize(['uptake', 'conc', 'Type']) # Fails: not all groups are normal

# def test_indep_t_test():
#     global uscrime_data_path
#     uscrime_data_path = "/Users/emjun/.tea/data/UScrime.csv"

#     # Declare and annotate the variables of interest
#     variables = [
#         {
#             'name' : 'So',
#             'data type' : 'nominal',
#             'categories' : ['0', '1']
#         },
#         {
#             'name' : 'Prob',
#             'data type' : 'ratio',
#             'range' : [0,1]
#         }
#     ]
#     experimental_design = {
#                             'study type': 'observational study',
#                             'contributor variables': 'So',
#                             'outcome variables': 'Prob',
#                         }
#     assumptions = {
#         'Type I (False Positive) Error Rate': 0.05,
#         'normal distribution': ['So']
#     }

#     tea.data(uscrime_data_path)
#     tea.define_variables(variables)
#     tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
#     tea.assume(assumptions)

#     tea.hypothesize(['So', 'Prob'])

#     # tea.hypothesize(['So', 'Prob'], null='So:1 <= So:0', alternative='So:1 > So:0')
#     # import pdb; pdb.set_trace()

# # def test_get_props():
# #     variables = [
# #         {
# #             'name' : 'So',
# #             'data type' : 'nominal',
# #             'categories' : ['0', '1']
# #         },
# #         {
# #             'name' : 'Prob',
# #             'data type' : 'ratio',
# #             'range' : [0,1]
# #         }
# #     ]
# #     experimental_design = {
# #                             'study type': 'observational study',
# #                             'contributor variables': 'So',
# #                             'outcome variables': 'Prob',
# #                         }
# #     assumptions = {
# #         'Type I (False Positive) Error Rate': 0.05
# #     }

# #     tea.define_variables(variables)
# #     tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
# #     tea.assume(assumptions)

# #     tea.divine_properties(vars=['So', 'Prob'], tests=['students_t', 'chi_square'])
# #     tea.divine_properties(vars=['So', 'Prob'], tests=['students_t', 'mannwhitney_u'])
#     # import pdb; pdb.set_trace()
    









#     ## IMPORTANT:
#     # The above example from the tutorial does not explicate all the assumptions. 
#     # We find that t-test is not appropriate because both groups are not normally distributed, 
#     # but this is not discussed in the tutorial. This shows us potential for Tea to be used as 
#     # a validation and learning tool.

#     ## TODO: What happens if we had the assumptions?
#     # --> May need to query the solver twice:
#     # 1. With only data computed propertie
#     # 2. With assumptions


#     # Can always redefine experimental design 
#     # tea.define_study_design(experimental_design)


# def test_dep_t_test():
#     global uscrime_data_path
#     variables = [
#         {
#             'name' : 'So',
#             'data type' : 'nominal',
#             'categories' : ['0', '1']
#         },
#         {
#             'name' : 'Prob',
#             'data type' : 'ratio',
#             'range' : [0,1]
#         },
#         {
#             'name' : 'U1',
#             'data type' : 'ratio'
#         },
#         {
#             'name': 'U2',
#             'data type' : 'ratio'
#         }
#     ]
#     experimental_design = {
#                             'study type': 'observational study',
#                             'contributor variables': ['So', 'U1', 'U2'],
#                             'outcome variables': 'Prob',
#                         }
#     assumptions = {
#         'Type I (False Positive) Error Rate': 0.05
#     }

#     tea.data(uscrime_data_path)
#     tea.define_variables(variables)
#     tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
#     tea.assume(assumptions)
#     tea.hypothesize(['U1', 'U2']) # true hypothesis, false hypo.
#     # tea.hypothesize(['U1', 'U2'], alternative='U1 > 1.2*U2', null='U1 <= 1.2*U2') # true hypothesis, false hypo.
#     # output: P(D |H0), what is null hypothesis that we tested

#     # Test sample size
#     # Test values of tests

# # Wilcoxon rank sum test AKA Mann Whitney U
# # def 




# # ## ADD TO PAPER
# # # What happens when have no participant_id?
# # # --> ask for key
# # # ---> if there is no key, assume that each row is a separate/unique participant/observation 
# # # --> May want to surface this assumption to the user....
