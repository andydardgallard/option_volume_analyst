import pandas as pd
import os

def parcer_fut(futName, dir_path):
    file_list = os.listdir(f'{dir_path}/data')
    for file in file_list:
        if file[0] == 'f':
            with open(f'data/{file}', 'r') as inf:
                data = pd.read_csv(inf, sep=';', header=None)
                return list(data[data[0] == futName].values)[0][1]