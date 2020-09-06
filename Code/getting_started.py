import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

def detect_duplicates(List_patient):
    # Total row of List_patient:
    tot_row_patient = List_patient.patient_id.count()
    print("Total of row on table patient: ", tot_row_patient)

    # If there many similar rows, when the function drop_duplicates will keep only one row and delete others
    List_patient = List_patient.drop_duplicates()
    List_patient2 = List_patient.dropna(subset=['state', 'age'])

    # delete all rows when age == 0.00
    age_zero = List_patient2[List_patient2['age'] == 0.00].index
    List_patient2.drop(age_zero, inplace=True)
    #I am deleting column, which are not usefull
    List_patient2 = List_patient2.drop(columns=['given_name', 'surname',
                                               'street_number', 'address_1', 'suburb', 'phone_number',
                                                'address_2'])

    tot_row_patient2 = List_patient2.patient_id.count()
    print("Total of row on table patient after the de duplication: ", tot_row_patient2)

    # How many deleted data's ?
    delete_row = ((tot_row_patient - tot_row_patient2) / tot_row_patient) * 100
    print("To deduplicated, there is: ", delete_row, " % of row, which are deleted")

    return List_patient2

def execute_qwery():
    engine = create_engine('sqlite:///data.db', echo=False)
    con = engine.connect()
    df_patient = pd.read_sql('select * from patient', con=con)
    df_pcr = pd.read_sql('select * from test', con=con)
    con.close()
    return df_patient, df_pcr

patient, pcr = execute_qwery()

dedublicated_patient = detect_duplicates(patient)
#print(dedublicated_patient.describe(include="all"))

#Below, this a merge between patient and pcr
df_inner = pd.merge(dedublicated_patient, pcr, on='patient_id', how='inner')

#Number of posive people in the database
positive_people = df_inner.query('pcr == "Positive" | pcr == "P"').patient_id.count()
print("Number of positif case: ", positive_people)

#Pourcentage of people who are positive
perc_positive = (int(positive_people)/20000)*100
print("Total of positive people is: ", perc_positive, "%")

perc_positive_dedub = (int(positive_people)/14393)*100
print("Total of positive people in deduplicated data is: ", perc_positive_dedub, "%")

# EDA exploratory data analysis
#boxplot = df_inner.boxplot(column=['age'])

#plt.hist(df_inner.age, range = (0, 100), bins = 10, color = 'yellow', edgecolor = 'red')
#plt.xlabel('age')
#plt.ylabel('nombres de personne')
#plt.title('Ratio age et nombre de personne')

#Below indicated the ratio between age et pcr
#df_inner.plot(kind='bar',x='pcr',y='age')
#df_inner.groupby('pcr')['pcr'].nunique().plot(kind='bar', figsize=(20,10))
#plt.show()


#Below indicated the ratio between age et pcr, with more information about age
#df_inner.plot(kind='scatter',x='age',y='pcr',color='red', figsize=(20,10))
#plt.show()

#List_positive_case will take only positive people to the virus
List_positive_case = df_inner
no_positive = List_positive_case[(List_positive_case['pcr'] == 'Negative') | (List_positive_case['pcr'] == 'N')].index
List_positive_case.drop(no_positive, inplace=True)

#Below, we can make a graph avec List_positive_case data's
#Thz graph will help us to understand in with state are more concerned by the virus
#List_positive_case.plot(kind='bar', x='state', y='age')
#List_positive_case.groupby('state')['state'].nunique().plot(kind='bar', figsize=(20, 10))
#plt.show()

#It will show us, how many people are positive in each state of Australia
print(List_positive_case.groupby('state').patient_id.count())