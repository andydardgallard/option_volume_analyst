import os
from tkinter import messagebox
import pandas as pd
import parcer_quik, spec
import datetime as dt

def cleaner(dir_path):
    if dir_path == 'none' or dir_path == '':
            messagebox.showerror(title="Error", message="Choose files!")
    else:
        file_list = os.listdir(f'{dir_path}/data')
        for file in file_list:
            if file[0].isdigit():
                with open(f'{dir_path}/data/{file}', 'r') as fin:
                    data = pd.read_csv(fin, sep=';', header=None)
                data.columns = ["sec_code", "deal_num", "date", "price", "qty", "OI"]
                data["exp_date"] = ""
                for i in range(len(data["sec_code"])):
                    type = data["sec_code"][i].find('B') + 1
                    if ord(data["sec_code"][i][type]) < 77:
                        if data["sec_code"][i][-1].isnumeric():
                            data["exp_date"][i] = "202" + str(data["sec_code"][i][type + 1]) + '-' + \
                                                str(spec.call[data["sec_code"][i][type]]) + '-' + \
                                                str(parcer_quik.find_date("202" + str(data["sec_code"][i][type + 1]), \
                                                spec.call[data["sec_code"][i][type]], 'C'))
                        else:
                            data["exp_date"][i] = "202" + str(data["sec_code"][i][type + 1]) + '-' + \
                                                str(spec.call[data["sec_code"][i][type]]) + '-' + \
                                                str(parcer_quik.find_date("202" + str(data["sec_code"][i][type + 1]), \
                                                str(spec.call[data["sec_code"][i][type]]), data["sec_code"][i][-1]))
                    else:
                            if data["sec_code"][i][-1].isnumeric():
                                data["exp_date"][i] = "202" + str(data["sec_code"][i][type + 1]) + '-' + \
                                                    str(spec.put[data["sec_code"][i][type]]) + '-' + \
                                                    str(parcer_quik.find_date("202" + str(data["sec_code"][i][type + 1]), \
                                                    spec.put[data["sec_code"][i][type]], 'C'))                      
                            else:
                                data["exp_date"][i] = "202" + str(data["sec_code"][i][type + 1]) + '-' + \
                                                    str(spec.put[data["sec_code"][i][type]]) + '-' + \
                                                    str(parcer_quik.find_date("202" + str(data["sec_code"][i][type + 1]), \
                                                    str(spec.put[data["sec_code"][i][type]]), data["sec_code"][i][-1]))
                data["exp_date"] = pd.to_datetime(data["exp_date"])
                if os.path.exists(f'{dir_path}/data/{file}'):
                    print(f'{dir_path}/data/{file}')
                    os.remove(f'{dir_path}/data/{file}')
                for i in range(len(data["exp_date"])):
                    if  data["exp_date"][i] < dt.datetime.now():
                        data.drop(index=i, axis=0, inplace=True)
                    else:
                        lineToPrint = data["sec_code"][i] + ';' + \
                            str(data["deal_num"][i]) + ';' + \
                            str(data["date"][i]) + ';' + \
                            str(data["price"][i]) + ';' + \
                            str(data["qty"][i]) + ';' + \
                            str(data["OI"][i]) + '\n'
                        with open(f'{dir_path}/data/{file}', 'a') as fout:
                            fout.write(lineToPrint)
    messagebox.showerror(title="Error", message="Cleaning is over!")
