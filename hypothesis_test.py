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

    print("Female proportion does not change in 2016 and 2020 in CCS")
    hyp_test(1310, 231, 175, 33)

    print("\nWhite participants proportion does not change in 2016 and 2020 in CCS")
    hyp_test(1310, 462, 175, 56)

    print("\nHispano participants proportion does not change in 2016 and 2020 in CCS")
    hyp_test(1310, 123, 175, 24)

    print("\nAsian participants proportion does not change in 2016 and 2020 in CCS")
    hyp_test(1310, 648, 175, 82)

    print("\nBlack participants proportion does not change in 2016 and 2020 in CCS")
    hyp_test(1310, 77, 175, 13)

    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change in 2014 and 2020 in SP")
    hyp_test(390, 67, 1465, 274)

    print("\nWhite participants proportion does not change in 2014 and 2020 in SP")
    hyp_test(390, 145, 1465, 501)

    print("\nHispano participants proportion does not change in 2014 and 2020 in SP")
    hyp_test(390, 33, 1465, 137)

    print("\nAsian participants proportion does not change in 2014 and 2020 in SP")
    hyp_test(390, 190, 1465, 736)

    print("\nBlack participants proportion does not change in 2014 and 2020 in SP")
    hyp_test(390, 22, 1465, 91)

    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change in 2016 and 2020 in EuroSP")
    hyp_test(216, 31, 289, 74)

    print("\nWhite participants proportion does not change in 2016 and 2020 in EuroSP")
    hyp_test(216, 114, 289, 115)

    print("\nHispano participants proportion does not change in 2016 and 2020 in EuroSP")
    hyp_test(216, 26, 289, 56)

    print("\nAsian participants proportion does not change in 2016 and 2020 in EuroSP")
    hyp_test(216, 58, 289, 106)

    print("\nBlack participants proportion does not change in 2016 and 2020 in EuroSP")
    hyp_test(216, 18, 289, 12)

    print('\n', '*'*70)
    print('\nCompare two different conferences')
    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change between EuroSP and CCS in 2020")
    hyp_test(289, 74, 175, 33)

    print("\nWhite participants proportion does not change between EuroSP and CCS in 2020")
    hyp_test(289, 115, 175, 56)

    print("\nHispano participants proportion does not change between EuroSP and CCS in 2020")
    hyp_test(289, 56, 175, 24)

    print("\nAsian participants proportion does not change between EuroSP and CCS in 2020")
    hyp_test(289, 106, 175, 82)

    print("\nBlack participants proportion does not change between EuroSP and CCS in 2020")
    hyp_test(289, 12, 175, 13)


    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change between SP and CCS in 2020")
    hyp_test(1465, 274, 175, 33)

    print("\nWhite participants proportion does not change between SP and CCS in 2020")
    hyp_test(1465, 501, 175, 56)

    print("\nHispano participants proportion does not change between SP and CCS in 2020")
    hyp_test(1465, 137, 175, 24)

    print("\nAsian participants proportion does not change between SP and CCS in 2020")
    hyp_test(1465, 736, 175, 82)

    print("\nBlack participants proportion does not change between SP and CCS in 2020")
    hyp_test(1465, 91, 175, 13)

    print('\n', '*'*70)

    print('\n')
    print("Female proportion does not change between SP and EuroSP in 2020")
    hyp_test(1465, 274, 289, 74)

    print("\nWhite participants proportion does not change between SP and EuroSP in 2020")
    hyp_test(1465, 501, 289, 115)

    print("\nHispano participants proportion does not change between SP and EuroSP in 2020")
    hyp_test(1465, 137, 289, 56)

    print("\nAsian participants proportion does not change between SP and EuroSP in 2020")
    hyp_test(1465, 736, 289, 106)

    print("\nBlack participants proportion does not change between SP and EuroSP in 2020")
    hyp_test(1465, 91, 289, 12)