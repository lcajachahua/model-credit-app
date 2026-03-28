import pandas as pd
from src.make_dataset import read_file_csv, data_preparation, data_exporting

# Realizar el test del proceso

def test_make_dataset():
    df1 = read_file_csv('defaultcc.csv')
    print("Tests de Carga")
    assert df1.shape == (30000, 24), "El archivo está vacío"
    assert df1.LIMIT_BAL.isnull().sum() == 0 , "El archivo tiene otros datos"
    assert df1.DEFAULT.gt(0).sum() == 6636, "El archivo está incompleto"
    print("Tests de Preparación")
    tdf1 = data_preparation(df1)
    assert tdf1.SEX.gt(0).sum() == 18112
    assert tdf1.AGE.max() == 79
    assert tdf1.AGE.min() == 21
    print("Tests de Exportado")
    data_exporting(tdf1, ['LIMIT_BAL', 'DEFAULT'],'test_train.csv')
    dff = pd.read_csv("./data/processed/test_train.csv").set_index('ID')
    assert dff.shape == (30000, 2)
    assert dff.LIMIT_BAL.isnull().sum() == 0
    assert dff.DEFAULT.gt(0).sum() == 6636
    print("Todas las pruebas terminaron satisfactoriamente")

test_make_dataset()
