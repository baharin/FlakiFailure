import pandas as pd
import ast
import re

def extract_arguments(input_array):

    input_array = input_array.replace('pass_throughfloat','')
    input_array = input_array.replace('pass_throughstr','')
    input_array = input_array.replace('pass_throughbool','')
    input_array = input_array.replace('pass_throughtuple','')
    input_array = input_array.replace('pass_through','')
    input_array = input_array.replace('sub_and','')

    pattern = r'(greater_than_func|less_than_func|equal_to)\(*?(ARG[0-7])\)*?, \(*?(-?\d+)\)*?\)'
    matches = re.findall(pattern, input_array)

    return matches



ts = ['Tarantula', 'Ochiai', 'Naish']
sub = ['AP-SNG', 'Dave2', 'R1', 'R2', 'R3', 'R4']
results = pd.DataFrame(columns = ['Run'+str(i) for i in range(1, 21)])

for ind1, s in enumerate(sub):
  for ind2, t in enumerate(ts):
    for kk in range(1, 10):

      data = pd.read_excel('GPresults_failclass'+s+'_'+t+'_'+str(k)+'.xlsx')  #change accordingly for pass class

      for i in range(len(data.index)):

        assertions = data.loc[i, 'BestIndividualFormula']

        assertions = ast.literal_eval(assertions)

        asrts = []

        for j in range(len(assertions)):

          asrt = extract_arguments(assertions[j])

          asrts.append(asrt)


        asrts = [str(item) for item in asrts]

        asrts = list(set(asrts))

        asrts = [ast.literal_eval(item) for item in asrts]

        for j in range(len(asrts)):

          results.loc[results.shape[0], :] = str(asrts[j])

        
      with pd.ExcelWriter('pure fail class rules - GP2.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer: #change accordingly for pass class
        results.to_excel(writer, sheet_name='dataset'+str(kk), index=False)
