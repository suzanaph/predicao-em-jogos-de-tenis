import numpy as np

def saveDFtoCSV(dataframe, filename):
    print('Writing CSV')
    np.savetxt(filename+".csv", dataframe, delimiter=";", fmt='%s', encoding='utf-8')
    print('CSV writed')
    