import re
import pandas as pd


def extract_arguments(input_array):
    result = []


    input_array = input_array.replace('pass_throughfloat','')
    input_array = input_array.replace('pass_throughstr','')
    input_array = input_array.replace('pass_throughbool','')
    input_array = input_array.replace('pass_throughtuple','')
    input_array = input_array.replace('pass_through','')
    input_array = input_array.replace('sub_and','')

    pattern = r"\(\(*(\d+\.\d+)\)*\)"

    result = re.sub(pattern,r"\1", input_array)

    return input_array

import ast 

ts = ['Tarantula', 'Ochiai', 'Naish']
for ind1, t in enumerate(ts):
    for kk in range(0, 10):

        results = pd.read_excel('...\\path_to_file\\GP - FailClass Assertions.xlsx', sheet_name='dataset'+str(kk)) #change for pass class
        
        counter = 0

        for i in range(len(data.index) - 20, len(data.index)):

            assertions = data.loc[i, 'BestIndividualFormula']

            assertions = ast.literal_eval(assertions)

            asrts = []

            for j in range(len(assertions)):

                asrt = extract_arguments(assertions[j])

                asrts.append(asrt)

            asrts = [str(item) for item in asrts]

            asrts = list(set(asrts))


            for j in range(len(asrts)):

                results.loc[j + ind1*20 + 360 , 'Run'+str(counter+1)] = str(asrts[j])


            counter = counter + 1


        with pd.ExcelWriter('GP - FailClass Assertions.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer: #change for pass class
            results.to_excel(writer, sheet_name='dataset'+str(kk), index=False)
