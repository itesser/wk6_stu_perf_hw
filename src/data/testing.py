import pandas as pd

cols = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
       'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime',
       'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3', 'subj']

new_cols = []

df = pd.read_csv(r'student-por.csv', delimiter=';')

for col in df.columns:
    if col == col.lower():
        new_cols.append(col)
    else:
        if col[0] == col[0].upper():
            new_cols.append(col[0].lower() + "_" + col[1:])
            
bool_cols = ['schoolsup',
 'famsup',
 'paid',
 'activities',
 'nursery',
 'higher',
 'internet',
 'romantic']

for col in bool_cols:
    df[col] = df[col].str.replace('yes','True')
    df[col] = df[col].str.replace('no', 'False')
    df[col].astype('bool', in_place = True)
    
