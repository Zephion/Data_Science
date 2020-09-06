import pandas as pd
import getting_started

def test_duplicated():
    data_patient, data_pcr = getting_started.execute_qwery()
    x = getting_started.detect_duplicates(data_patient)

    # Count number of NaN in the column 'patient_id' of table patient
    assert sum(pd.isnull(x['patient_id'])) == 0
    # Count number of NaN in the column 'age' of table patient
    assert sum(pd.isnull(x['age'])) == 0
    # Count number of NaN in the column 'state' of table patient
    assert sum(pd.isnull(x['state'])) == 0
    # Count number of the table patient rows after the deduplicate process, it should be more than 0 row
    assert x.patient_id.count() > 0
    # If even after the deduplicated process, there are any deleted rows. When we should have 20000 rows max
    assert x.patient_id.count() <= 20000
