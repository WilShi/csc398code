import os
import re
import sys
import json
import math
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.stats.weightstats as sw
import scipy.stats

def hyp_test(size1, year1, size2, year2):
    print("Null Hypothesis H0:  year1 == year2")
    print("Alternative Hypothesis HA: year1 != year2")
    alpha = 0.05/2
    p_h = (year2 + year1)/(size2 + size1)
    stdd = ((p_h * (1 - p_h))/size2) + ((p_h * (1 - p_h))/size1)
    z_value = (year2/size2 - year1/size1) / math.sqrt(stdd)
    print("z value: ", z_value)
    p_value = scipy.stats.norm.sf(abs(z_value))*2
    print("p value: ", p_value)
    if p_value > alpha:
        print("H0 is correct: year1 == year2")
    else:
        print("Reject H0: year1 != year2")

    # data = pd.Series([year1/size1, year2/size2])
    # sns.distplot(data)
    # plt.title('data distribution')
    # plt.show()

def run_test():

    print("Female proportion does not change in 2016 and 2019 in CCS")
    hyp_test(1310, 231, 1543, 313)

    print("\nWhite participants proportion does not change in 2016 and 2019 in CCS")
    hyp_test(1310, 462, 1543, 513)

    print("\nHispano participants proportion does not change in 2016 and 2019 in CCS")
    hyp_test(1310, 123, 1543, 149)

    print("\nAsian participants proportion does not change in 2016 and 2019 in CCS")
    hyp_test(1310, 648, 1543, 823)

    print("\nBlack participants proportion does not change in 2016 and 2019 in CCS")
    hyp_test(1310, 77, 1543, 58)

    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change in 2014 and 2019 in SP")
    hyp_test(390, 67, 1209, 278)

    print("\nWhite participants proportion does not change in 2014 and 2019 in SP")
    hyp_test(390, 145, 1209, 417)

    print("\nHispano participants proportion does not change in 2014 and 2019 in SP")
    hyp_test(390, 33, 1209, 119)

    print("\nAsian participants proportion does not change in 2014 and 2019 in SP")
    hyp_test(390, 190, 1209, 616)

    print("\nBlack participants proportion does not change in 2014 and 2019 in SP")
    hyp_test(390, 22, 1209, 57)

    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change in 2016 and 2019 in EuroSP")
    hyp_test(216, 31, 418, 76)

    print("\nWhite participants proportion does not change in 2016 and 2019 in EuroSP")
    hyp_test(216, 114, 418, 155)

    print("\nHispano participants proportion does not change in 2016 and 2019 in EuroSP")
    hyp_test(216, 26, 418, 66)

    print("\nAsian participants proportion does not change in 2016 and 2019 in EuroSP")
    hyp_test(216, 58, 418, 169)

    print("\nBlack participants proportion does not change in 2016 and 2019 in EuroSP")
    hyp_test(216, 18, 418, 28)

    print('\n', '*'*70)
    print('\nCompare two different conferences')
    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change between EuroSP and CCS in 2019")
    hyp_test(418, 76, 1543, 313)

    print("\nWhite participants proportion does not change between EuroSP and CCS in 2019")
    hyp_test(418, 115, 1543, 513)

    print("\nHispano participants proportion does not change between EuroSP and CCS in 2019")
    hyp_test(418, 66, 1543, 149)

    print("\nAsian participants proportion does not change between EuroSP and CCS in 2019")
    hyp_test(418, 169, 1543, 823)

    print("\nBlack participants proportion does not change between EuroSP and CCS in 2019")
    hyp_test(418, 28, 1543, 58)


    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change between SP and CCS in 2019")
    hyp_test(1209, 278, 1543, 313)

    print("\nWhite participants proportion does not change between SP and CCS in 2019")
    hyp_test(1209, 417, 1543, 513)

    print("\nHispano participants proportion does not change between SP and CCS in 2019")
    hyp_test(1209, 119, 1543, 149)

    print("\nAsian participants proportion does not change between SP and CCS in 2019")
    hyp_test(1209, 616, 1543, 823)

    print("\nBlack participants proportion does not change between SP and CCS in 2019")
    hyp_test(1209, 57, 1543, 58)

    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change between SP and EuroSP in 2019")
    hyp_test(1209, 278, 418, 76)

    print("\nWhite participants proportion does not change between SP and EuroSP in 2019")
    hyp_test(1209, 417, 418, 155)

    print("\nHispano participants proportion does not change between SP and EuroSP in 2019")
    hyp_test(1209, 119, 418, 66)

    print("\nAsian participants proportion does not change between SP and EuroSP in 2019")
    hyp_test(1209, 616, 418, 169)

    print("\nBlack participants proportion does not change between SP and EuroSP in 2019")
    hyp_test(1209, 57, 418, 28)