import pandas as pd

def FlakinessRate(dataset, rep, label):

  datasets = []

  for hh in range(10):

    data = pd.read_excel('..\\path_to_file\\'+dataset+str(h)+'.xlsx')

    datasets.append(data)

  labels = pd.DataFrame()

  for i, df in enumerate(datasets):
      labels[f'label_{i}'] = df[label]
  
  f_mask = labels.nunique(axis=1) > 1
  
  dtotal_rows = len(datasets[0])
  
  fcount = f_mask.sum()
  
  frate = fcount / total_rows

  return frate  


a = input('Select dataset from AP-SNG, Dave2, R1, R2, R3, R4, Router...')

if a == 'AP-SNG':

  label = 'TestOutcome'
  dataset = 'AP-SNG'
  
elif a == 'R1':

  label = 'Label'
  dataset = 'AP-TWN - R1 - '

elif a == 'R2':

  label = 'Label(Damage)'
  dataset = 'AP-TWN - R2 to R4 - '

elif a == 'R3':

  label = 'Label(Ultra)'
  dataset = 'AP-TWN - R2 to R4 - '

elif a == 'R4':

  label = 'Label(Distance)'
  dataset = 'AP-TWN - R2 to R4 - '

elif a == 'Router':

  label = 'Label'
  dataset = 'Router'

rep = 10

fr = FlakinessRate(dataset, rep, label)
