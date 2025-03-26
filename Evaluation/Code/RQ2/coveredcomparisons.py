import pandas as pd
import ast
from statistics import mean
import numpy as np

def statisticalTests(a, b):
    def a12(lst1, lst2, rev=True):
        more = same = 0.0
        for x in lst1:
            for y in lst2:
                if x == y:
                    same += 1
                elif rev and x > y:
                    more += 1
                elif not rev and x < y:
                    more += 1
        return (more + 0.5 * same) / (len(lst1) * len(lst2))

    ##  Wilcoxon signed-rank test...
    # res = wilcoxon(a, b)
    from scipy.stats import mannwhitneyu
    res = mannwhitneyu(a, b, alternative= 'two-sided' )
    p_value = res.pvalue
    ##  Vargha-Delaney A^12 test...
    a12_value = a12(a, b)
    return p_value, a12_value


def CheckCovered(gpochiai, dr, model):

    if model == 'R121':
        gpcols = ['CoveredRun'+str(i) for i in range(1, 21)]
        drcols = ['CoveredDRRun'+str(i) for i in range(1, 21)]
    else:
        gpcols = ['CoveredgpOchiaiRUN'+str(i) for i in range(1, 21)]
        drcols = ['CovereddrRUN'+str(i) for i in range(1, 21)]
    
    covered = []

    

    for gpcol, drcol in zip(gpcols, drcols):

        failcoveredbyboth = 0
        failcoveredbynone = 0
        failcoveredbygpbutnotdr = 0
        failcoveredbydrbutnotgp = 0
        failcoveredbygpbutwrongdr = 0
        failcoveredbydrbutwronggp = 0

        passcoveredbynone = 0
        passcoveredbyboth = 0
        passcoveredbygpbutnotdr = 0
        passcoveredbydrbutnotgp = 0
        passcoveredbygpbutwrongdr = 0
        passcoveredbydrbutwronggp = 0

        for i in range(len(gpochiai.index)):
            
            try:
                reallabel = gpochiai.loc[i, 'TestOutcome']
            except:
                reallabel = gpochiai.loc[i, 'Label']

            if reallabel == 'FAIL' or reallabel == '0' or reallabel == 0:
                if ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'FAIL' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '0' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 0:
                    if ast.literal_eval(dr.loc[i, drcol ])[0] == 'No':
                        failcoveredbygpbutnotdr = failcoveredbygpbutnotdr + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        failcoveredbyboth = failcoveredbyboth + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                        failcoveredbygpbutwrongdr = failcoveredbygpbutwrongdr + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'No':
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'No':
                        failcoveredbynone = failcoveredbynone + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        failcoveredbydrbutnotgp = failcoveredbydrbutnotgp + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'PASS' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '1' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 1:
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        failcoveredbydrbutwronggp = failcoveredbydrbutwronggp + 1
                    

            elif reallabel == 'PASS' or reallabel == '1' or reallabel == 1:
                if ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'PASS' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '1' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 1:
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'No':
                        passcoveredbygpbutnotdr = passcoveredbygpbutnotdr + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                        passcoveredbyboth = passcoveredbyboth + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        passcoveredbygpbutwrongdr = passcoveredbygpbutwrongdr + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'No':
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'No':
                        passcoveredbynone = passcoveredbynone + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                        passcoveredbydrbutnotgp = passcoveredbydrbutnotgp + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'FAIL' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '0' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 0:
                   if ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                       passcoveredbydrbutwronggp = passcoveredbydrbutwronggp + 1
                      


        covered.append((failcoveredbyboth/len(gpochiai.index), failcoveredbynone/len(gpochiai.index), failcoveredbygpbutnotdr/len(gpochiai.index), failcoveredbydrbutnotgp/len(gpochiai.index), failcoveredbygpbutwrongdr/len(gpochiai.index), failcoveredbydrbutwronggp/len(gpochiai.index), passcoveredbyboth/len(gpochiai.index), passcoveredbynone/len(gpochiai.index), passcoveredbygpbutnotdr/len(gpochiai.index), passcoveredbydrbutnotgp/len(gpochiai.index), passcoveredbygpbutwrongdr/len(gpochiai.index), passcoveredbydrbutwronggp/len(gpochiai.index)))

    coveredavg = tuple(mean(values) for values in zip(*covered))


    return coveredavg, covered




                    




results = pd.DataFrame(columns=['Theta', 'Model', 'FailCoveredbyBoth', 'FailCoveredbyNone', 'FailCoveredbyGPbutnotDR', 'FailCoveredbyDRbutnotGP', 'FailCoveredbyGPbutWrongDR', 'FailCoveredbyDRbutWrongGP', 'PassCoveredbyBoth', 'PassCoveredbyNone', 'PassCoveredbyGPbutnotDR', 'PassCoveredbyDRbutnotGP', 'PassCoveredbyGPbutWrongDR', 'PassCoveredbyDRbutWrongGP'])

#NTSS is missing
models = ['beamng', 'dave2', 'keeplane', 'damage', 'ultra', 'distance', 'R121']

allcovered = [[] for i in range(11)]

allcoveredmodel = [[] for i in range(8)]

for t, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']):
    for m, model in enumerate(models):
        if model != 'R121':

            gpochiai = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\newest experiments - August 7 2024\\considering with and without rep\\coveredpoints2\\GP-Ochiai-coveredpointswithhighestprecisionassertion-withoutrep-'+model+'-theta'+theta+'-testset.xlsx')
            dr = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\newest experiments - August 7 2024\\considering with and without rep\\coveredpoints1\\dr-coveredpointswithhighestprecisionassertion-withoutrep-'+model+'-theta'+theta+'-testset.xlsx')

        elif model == 'R121':

            gpochiai = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\autopilot\\AP121 after adding the condition in code\\GP\\GP covered points\\newGPochiai-coveredpoints-R121-theta'+theta+'-testset.xlsx')
            dr = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\autopilot\\covered points - DTDR\\DR-coveredpointswithhighestprecisionassertion-R121-theta'+theta+'-testset.xlsx')

        coveredavg, covered = CheckCovered(gpochiai, dr, model)
        allcovered[t].append(covered)
        # print(allcovered[t])
        # allcoveredmodel[m].append(covered)

        results.loc[results.shape[0]] = [theta, model, coveredavg[0], coveredavg[1], coveredavg[2], coveredavg[3], coveredavg[4], coveredavg[5], coveredavg[6], coveredavg[7], coveredavg[8], coveredavg[9], coveredavg[10], coveredavg[11]]            



for m, model in enumerate(models):
    for t, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']):
        if model != 'R121':

            gpochiai = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\newest experiments - August 7 2024\\considering with and without rep\\coveredpoints2\\GP-Ochiai-coveredpointswithhighestprecisionassertion-withoutrep-'+model+'-theta'+theta+'-testset.xlsx')
            dr = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\newest experiments - August 7 2024\\considering with and without rep\\coveredpoints1\\dr-coveredpointswithhighestprecisionassertion-withoutrep-'+model+'-theta'+theta+'-testset.xlsx')

        elif model == 'R121':

            gpochiai = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\autopilot\\AP121 after adding the condition in code\\GP\\GP covered points\\newGPochiai-coveredpoints-R121-theta'+theta+'-testset.xlsx')
            dr = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\autopilot\\covered points - DTDR\\DR-coveredpointswithhighestprecisionassertion-R121-theta'+theta+'-testset.xlsx')

        coveredavg, covered = CheckCovered(gpochiai, dr, model)
        # allcovered[t].append(covered)
        # print(allcovered[t])
        allcoveredmodel[m].append(covered)

        # results.loc[results.shape[0]] = [theta, model, coveredavg[0], coveredavg[1], coveredavg[2], coveredavg[3], coveredavg[4], coveredavg[5], coveredavg[6], coveredavg[7], coveredavg[8], coveredavg[9], coveredavg[10], coveredavg[11]]            






print('doneothers')
#NTSS
model = 'NTSS'
for t, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']):
    gpochiai = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\newest experiments - August 7 2024\\considering with and without rep\\coveredpoints2\\GP-Ochiai-coveredpointswithhighestprecisionassertion-withoutrep-NTSS-theta'+theta+'-testset.xlsx')
    drind = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\newest experiments - August 7 2024\\considering with and without rep\\coveredpoints1\\dr-coveredpointswithhighestprecisionassertion-withoutrep-NTSS-ind-theta'+theta+'-testset.xlsx')
    
    coveredindavg, coveredind = CheckCovered(gpochiai, drind, model)
    drsum = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\newest experiments - August 7 2024\\considering with and without rep\\coveredpoints1\\dr-coveredpointswithhighestprecisionassertion-withoutrep-NTSS-sum-theta'+theta+'-testset.xlsx')

    # allcovered[t].append(coveredind)

    coveredsumavg, coveredsum = CheckCovered(gpochiai, drsum, model)

    # allcovered[t].append(coveredsum)

    a = []
    for i in range(len(coveredind)):
        a.append(tuple((a + b) / 2 for a, b in zip(coveredind[i], coveredsum[i])))
        print(a)

    allcovered[t].append(a)

    allcoveredmodel[7].append(a)

    coveredavg = tuple((a + b) / 2 for a, b in zip(coveredindavg, coveredsumavg)) 
    results.loc[results.shape[0]] = [theta, model, coveredavg[0], coveredavg[1], coveredavg[2], coveredavg[3], coveredavg[4], coveredavg[5], coveredavg[6], coveredavg[7], coveredavg[8], coveredavg[9], coveredavg[10], coveredavg[11]]            


print('donentss')



# ###statistical### per theta

# statistical = pd.DataFrame(columns=['Theta', 'Verdict', 'A', 'B', 'Pvalue', 'A12'])

# ###fail covered by GP but not DR VS. fail covered by DR but not GP
# for i, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']): #iterate over theta


#     gp = []
#     dr = []

#     for j in range(len(allcovered[i])): #iterate over models

#         for h in range(len(allcovered[i][j])): #iterate over cols in models

#             # print(allcovered[i][j][h][2], allcovered[i][j][h][4], allcovered[i][j][h][2] + allcovered[i][j][h][4])
#             # gp.append(allcovered[i][j][h][2] + allcovered[i][j][h][4] + allcovered[i][j][h][8] + allcovered[i][j][h][10]) 
#             # gp.append(allcovered[i][j][h][2] + allcovered[i][j][h][4]) 
#             gp.append(allcovered[i][j][h][8] + allcovered[i][j][h][10]) 
#             # gp.append(allcovered[i][j][h][10]) 

#             # dr.append(allcovered[i][j][h][3] + allcovered[i][j][h][5] + allcovered[i][j][h][9] + allcovered[i][j][h][11])
#             # dr.append(allcovered[i][j][h][3] + allcovered[i][j][h][5]) 
#             dr.append(allcovered[i][j][h][9] + allcovered[i][j][h][11]) 
#             # dr.append(allcovered[i][j][h][11]) 

#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical.loc[statistical.shape[0]] = [theta, 'Pass', 'GP', 'DR', pvalue, a12]
#     print('*********')

# statistical.to_excel('statisticalcovered_pass.xlsx')








# ###statistical### per theta ranges

statistical = pd.DataFrame(columns=['Theta', 'Verdict', 'A', 'B', 'Pvalue', 'A12'])

###fail covered by GP but not DR VS. fail covered by DR but not GP
gp = []
dr = []
for i, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']): #iterate over theta

    gp1 = []
    dr1 = []
    for j in range(len(allcovered[i])): #iterate over models

        for h in range(len(allcovered[i][j])): #iterate over cols in models

            # print(allcovered[i][j][h][2], allcovered[i][j][h][4], allcovered[i][j][h][2] + allcovered[i][j][h][4])
            gp1.append(allcovered[i][j][h][2] + allcovered[i][j][h][4] + allcovered[i][j][h][8] + allcovered[i][j][h][10]) 
            # gp.append(allcovered[i][j][h][2] + allcovered[i][j][h][4]) 
            # gp.append(allcovered[i][j][h][8] + allcovered[i][j][h][10]) 
            # gp.append(allcovered[i][j][h][10]) 

            dr1.append(allcovered[i][j][h][3] + allcovered[i][j][h][5] + allcovered[i][j][h][9] + allcovered[i][j][h][11])
            # dr.append(allcovered[i][j][h][3] + allcovered[i][j][h][5]) 
            # dr.append(allcovered[i][j][h][9] + allcovered[i][j][h][11]) 
            # dr.append(allcovered[i][j][h][11]) 
        gp.append(sum(gp1)/len(gp1))
        dr.append(sum(dr1)/len(dr1))
        
    if i == 3 or i == 7 or i == 10:
        pvalue, a12 = statisticalTests(gp, dr)
        print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
        statistical.loc[statistical.shape[0]] = [theta, 'Both', 'GP', 'DR', pvalue, a12]
        print('*********')
        gp = []
        dr = []

    

statistical.to_excel('statisticalcovered_both_thetarange_avg.xlsx')












    # import matplotlib.pyplot as plt

    # plt.figure(figsize=(8, 5))
    # plt.boxplot([gp, dr], labels=['gp', 'dr'], showmeans=True)
    # plt.show()


# ####statistical over model perrun

# statistical1 = pd.DataFrame(columns=['Model', 'Verdict', 'A', 'B', 'Pvalue', 'A12'])

# for i in range(len(allcoveredmodel)): #iterate over model

#     gp = []
#     dr = []

#     for j in range(len(allcoveredmodel[i])): #iterate over theta

#         for h in range(len(allcoveredmodel[i][j])):

#             gp.append(allcoveredmodel[i][j][h][2] + allcoveredmodel[i][j][h][4] + allcoveredmodel[i][j][h][8] + allcoveredmodel[i][j][h][10]) 
#             dr.append(allcoveredmodel[i][j][h][3] + allcoveredmodel[i][j][h][5] + allcoveredmodel[i][j][h][9] + allcoveredmodel[i][j][h][11])

#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical1.loc[statistical1.shape[0]] = ['model'+str(i), 'Both', 'GP', 'DR', pvalue, a12]
#     print('*********')


# for i in range(len(allcoveredmodel)): #iterate over model

#     gp = []
#     dr = []

#     for j in range(len(allcoveredmodel[i])): #iterate over theta

#         for h in range(len(allcoveredmodel[i][j])):

#             gp.append(allcoveredmodel[i][j][h][2] + allcoveredmodel[i][j][h][4]) 
#             dr.append(allcoveredmodel[i][j][h][3] + allcoveredmodel[i][j][h][5])

#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical1.loc[statistical1.shape[0]] = ['model'+str(i), 'Fail', 'GP', 'DR', pvalue, a12]
#     print('*********')


# for i in range(len(allcoveredmodel)): #iterate over model

#     gp = []
#     dr = []

#     for j in range(len(allcoveredmodel[i])): #iterate over theta

#         for h in range(len(allcoveredmodel[i][j])):

#             gp.append(allcoveredmodel[i][j][h][8] + allcoveredmodel[i][j][h][10]) 
#             dr.append(allcoveredmodel[i][j][h][9] + allcoveredmodel[i][j][h][11])

#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical1.loc[statistical1.shape[0]] = ['model'+str(i), 'Pass', 'GP', 'DR', pvalue, a12]
#     print('*********')


# statistical1.to_excel('statisticalcovered-permodel-perrun.xlsx')



# statistical1 = pd.DataFrame(columns=['Model', 'Verdict', 'A', 'B', 'Pvalue', 'A12'])

# for i in range(len(allcoveredmodel)): #iterate over model

#     gp = []
#     dr = []

#     for j in range(len(allcoveredmodel[i])): #iterate over theta

#         gp1 = []
#         dr1 = []

#         for h in range(len(allcoveredmodel[i][j])): #iterate over run

#             gp1.append(allcoveredmodel[i][j][h][2] + allcoveredmodel[i][j][h][4] + allcoveredmodel[i][j][h][8] + allcoveredmodel[i][j][h][10]) 
#             dr1.append(allcoveredmodel[i][j][h][3] + allcoveredmodel[i][j][h][5] + allcoveredmodel[i][j][h][9] + allcoveredmodel[i][j][h][11])

#         gp.append(sum(gp1)/len(gp1))
#         dr.append(sum(dr1)/len(dr1))


#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical1.loc[statistical1.shape[0]] = ['model'+str(i), 'Both', 'GP', 'DR', pvalue, a12]
#     print('*********')


# for i in range(len(allcoveredmodel)): #iterate over model

#     gp = []
#     dr = []

#     for j in range(len(allcoveredmodel[i])): #iterate over theta

#         gp1 = []
#         dr1 = []

#         for h in range(len(allcoveredmodel[i][j])):

#             gp1.append(allcoveredmodel[i][j][h][2] + allcoveredmodel[i][j][h][4]) 
#             dr1.append(allcoveredmodel[i][j][h][3] + allcoveredmodel[i][j][h][5])

#         gp.append(sum(gp1)/len(gp1))
#         dr.append(sum(dr1)/len(dr1))

#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical1.loc[statistical1.shape[0]] = ['model'+str(i), 'Fail', 'GP', 'DR', pvalue, a12]
#     print('*********')


# for i in range(len(allcoveredmodel)): #iterate over model

#     gp = []
#     dr = []

#     for j in range(len(allcoveredmodel[i])): #iterate over theta

#         gp1 = []
#         dr1 = []

#         for h in range(len(allcoveredmodel[i][j])):

#             gp1.append(allcoveredmodel[i][j][h][8] + allcoveredmodel[i][j][h][10]) 
#             dr1.append(allcoveredmodel[i][j][h][9] + allcoveredmodel[i][j][h][11])

#         gp.append(sum(gp1)/len(gp1))
#         dr.append(sum(dr1)/len(dr1))


#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical1.loc[statistical1.shape[0]] = ['model'+str(i), 'Pass', 'GP', 'DR', pvalue, a12]
#     print('*********')


# statistical1.to_excel('statisticalcovered-permodel-avgrun.xlsx')





# print('#############################################')
# ###pass covered by GP but not DR VS. pass covered by DR but not GP
# for i, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']): #iterate over theta

#     gp = []
#     dr = []

#     for j in range(len(allcovered[i])): #iterate over models

#         # print(allcovered[i][j])
#         for h in range(len(allcovered[i][j])): #iterate over cols in models

#             gp.append(allcovered[i][j][h][8])
#             dr.append(allcovered[i][j][h][9])

#     pvalue, a12 = statisticalTests(gp, dr)
#     print(pvalue, a12, len(gp), len(dr), np.mean(gp), np.mean(dr))
#     statistical.loc[statistical.shape[0]] = [theta, 'Pass', 'GP', 'DR', pvalue, a12]
#     print('*********')



###summary - average of averages####

# failcoveredbyboth = 0
# failcoveredbynone = 0
# failcoveredbygpbutnotdr = 0
# failcoveredbydrbutnotgp = 0

# passcoveredbynone = 0
# passcoveredbyboth = 0
# passcoveredbygpbutnotdr = 0
# passcoveredbydrbutnotgp = 0

# summaryresults = pd.DataFrame(columns=['Theta', 'Model', 'FailCoveredbyBoth', 'FailCoveredbyNone', 'FailCoveredbyGPbutnotDR', 'FailCoveredbyDRbutnotGP', 'PassCoveredbyBoth', 'PassCoveredbyNone', 'PassCoveredbyGPbutnotDR', 'PassCoveredbyDRbutnotGP'])

# for theta in ['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']:
#     # print(theta)
#     failcoveredbyboth = 0
#     failcoveredbynone = 0
#     failcoveredbygpbutnotdr = 0
#     failcoveredbydrbutnotgp = 0

#     passcoveredbynone = 0
#     passcoveredbyboth = 0
#     passcoveredbygpbutnotdr = 0
#     passcoveredbydrbutnotgp = 0

#     for i in range(len(results.index)):
#         # print(theta, i)
#         if results.loc[i, 'Theta'] == theta:
#             failcoveredbyboth = failcoveredbyboth + results.loc[i, 'FailCoveredbyBoth']
#             failcoveredbynone = failcoveredbynone + results.loc[i, 'FailCoveredbyNone']
#             failcoveredbygpbutnotdr = failcoveredbygpbutnotdr + results.loc[i, 'FailCoveredbyGPbutnotDR']
#             failcoveredbydrbutnotgp = failcoveredbydrbutnotgp + results.loc[i, 'FailCoveredbyDRbutnotGP']

#             passcoveredbyboth = passcoveredbyboth + results.loc[i, 'PassCoveredbyBoth']
#             passcoveredbynone = passcoveredbynone + results.loc[i, 'PassCoveredbyNone']
#             passcoveredbygpbutnotdr = passcoveredbygpbutnotdr + results.loc[i, 'PassCoveredbyGPbutnotDR']
#             passcoveredbydrbutnotgp = passcoveredbydrbutnotgp + results.loc[i, 'PassCoveredbyDRbutnotGP']

#     summaryresults.loc[summaryresults.shape[0]] = [theta, 'summary', failcoveredbyboth/8, failcoveredbynone/8, failcoveredbygpbutnotdr/8, failcoveredbydrbutnotgp/8, passcoveredbyboth/8, passcoveredbynone/8, passcoveredbygpbutnotdr/8, passcoveredbydrbutnotgp/8]            





###summary - averages per run###



# summaryresults = pd.DataFrame(columns=['Theta', 'Model', 'FailCoveredbyBoth', 'FailCoveredbyNone', 'FailCoveredbyGPbutnotDR', 'FailCoveredbyDRbutnotGP', 'FailCoveredbyGPbutwrongDR', 'FailCoveredbyDRbutwrongGP', 'PassCoveredbyBoth', 'PassCoveredbyNone', 'PassCoveredbyGPbutnotDR', 'PassCoveredbyDRbutnotGP', 'PassCoveredbyGPbutwrongDR', 'PassCoveredbyDRbutwrongGP'])

# for i, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']): #iterate over theta

#     failcoveredbyboth = []
#     failcoveredbynone = []
#     failcoveredbygpbutnotdr = []
#     failcoveredbydrbutnotgp = []
#     failcoveredbygpbutwrongdr = []
#     failcoveredbydrbutwronggp = []

#     passcoveredbynone = []
#     passcoveredbyboth = []
#     passcoveredbygpbutnotdr = []
#     passcoveredbydrbutnotgp = []
#     passcoveredbygpwrongdr = []
#     passcoveredbydrbutwronggp = []

#     for j in range(len(allcovered[i])): #iterate over models

#         # print(allcovered[i][j])
#         for h in range(len(allcovered[i][j])): #iterate over cols in models

#             failcoveredbyboth.append(allcovered[i][j][h][0])
#             failcoveredbynone.append(allcovered[i][j][h][1])
#             failcoveredbygpbutnotdr.append(allcovered[i][j][h][2])
#             failcoveredbydrbutnotgp.append(allcovered[i][j][h][3])
#             failcoveredbygpbutwrongdr.append(allcovered[i][j][h][4])
#             failcoveredbydrbutwronggp.append(allcovered[i][j][h][5])

#             passcoveredbynone.append(allcovered[i][j][h][6])
#             passcoveredbyboth.append(allcovered[i][j][h][7])
#             passcoveredbygpbutnotdr.append(allcovered[i][j][h][8])
#             passcoveredbydrbutnotgp.append(allcovered[i][j][h][9])
#             passcoveredbygpwrongdr.append(allcovered[i][j][h][10])
#             passcoveredbydrbutwronggp.append(allcovered[i][j][h][11])


#     summaryresults.loc[summaryresults.shape[0]] = [theta, 'summary', np.mean(failcoveredbyboth), np.mean(failcoveredbynone), np.mean(failcoveredbygpbutnotdr), np.mean(failcoveredbydrbutnotgp), np.mean(failcoveredbygpbutwrongdr), np.mean(failcoveredbydrbutwronggp), np.mean(passcoveredbyboth), np.mean(passcoveredbynone), np.mean(passcoveredbygpbutnotdr), np.mean(passcoveredbydrbutnotgp), np.mean(passcoveredbygpwrongdr), np.mean(passcoveredbydrbutwronggp)]

# summaryresults.to_excel('coveredsummary-perrun.xlsx')






# results.to_excel('coveredcomparisons_2.xlsx')
# # summaryresults.to_excel('coveredsummary.xlsx')



            




