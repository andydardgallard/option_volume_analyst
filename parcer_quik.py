import pandas as pd
import os
import spec
import datetime as dt
from tkinter import messagebox

def find_date(year, month, symbol):
    weekday = dt.date(int(year), int(month), 1).isoweekday()
    # 1:1 + 3 = 4   4-1  4-weekday
    # 2:1 + 2 = 3   4-2
    # 3:1 + 1 = 2   4-3
    # 4:1 + 0 = 1   4-4
    # 5:1 + 6 = 7   4-5+7
    # 6:1 + 5 = 6   4-6+7
    # 7:1 + 4 = 5   4-7+7
    date = int()
    if weekday <= 4:
        date = 1 + 4 - weekday
    else:
        date = 1 + 4 - weekday + 7
    if symbol == 'A':
        return date
    elif symbol == 'B':
        return date + 7
    elif symbol == 'C':
        return date + 14
    elif symbol == 'D':
        return date + 21
    elif symbol == 'E':
        return date + 28

def preparcer_quik(optName, file, dir_path, flag):
    ticker_date = dt.datetime(int(str("20" + optName[6:8])), \
                        int(optName[4:6]), int(optName[2:4]))
    if file[0] != '.' and file[0] != 'f':
        if flag == 0:
            with open(f'{dir_path}/data/{file}', 'r') as inf:
                data = pd.read_csv(inf, sep=';', header=None)
        elif flag == 1:
            with open(f'{dir_path}/exp/{file}', 'r') as inf:
                data = pd.read_csv(inf, sep=';', header=None)
        data.columns = ["sec_code", "deal_num", "date", "price", "qty", "OI"]
        data["date"] = pd.to_datetime(data["date"], dayfirst=True)
        data.drop_duplicates(keep="first", inplace=True)
        data.sort_values(by="deal_num", ascending=True, inplace=True)
        data.reset_index(inplace=True)
    
        data["symbol"] = ""
        data["exp_date"] = ""
        data["opt_type"] = ""
        data["strike"] = ""

        for i in range(len(data["sec_code"])):
            data["symbol"][i] = data["sec_code"][i][:2]
            type = data["sec_code"][i].find('B') + 1
            data["strike"][i] = data["sec_code"][i][2:type - 1]
            if ord(data["sec_code"][i][type]) < 77:
                data["opt_type"][i] = "CA"
                if data["sec_code"][i][-1].isnumeric():
                    data["exp_date"][i] = str(find_date("202" + str(data["sec_code"][i][type + 1]), \
                                        spec.call[data["sec_code"][i][type]], 'C')) + '.' + \
                                        str(spec.call[data["sec_code"][i][type]]) + '.' + \
                                        "202" + str(data["sec_code"][i][type + 1])
                else:
                    data["exp_date"][i] = str(find_date("202" + str(data["sec_code"][i][type + 1]), \
                                        str(spec.call[data["sec_code"][i][type]]), data["sec_code"][i][-1])) \
                                        + '.' + str(spec.call[data["sec_code"][i][type]]) + '.' + \
                                        "202" + str(data["sec_code"][i][type + 1])
            else:
                data["opt_type"][i] = "PA"
                if data["sec_code"][i][-1].isnumeric():
                    data["exp_date"][i] = str(find_date("202" + str(data["sec_code"][i][type + 1]), \
                                        spec.put[data["sec_code"][i][type]], 'C')) + '.' + \
                                        str(spec.put[data["sec_code"][i][type]]) + '.' + \
                                        "202" + str(data["sec_code"][i][type + 1])
                else:
                    data["exp_date"][i] = str(find_date("202" + str(data["sec_code"][i][type + 1]), \
                                        str(spec.put[data["sec_code"][i][type]]), data["sec_code"][i][-1])) \
                                        + '.' + str(spec.put[data["sec_code"][i][type]]) + '.' + \
                                        "202" + str(data["sec_code"][i][type + 1])
        data["exp_date"] = pd.to_datetime(data["exp_date"])
        data["strike"] = data["strike"].astype(float)

        slice = data[(data["symbol"] == optName[:2]) & (data["exp_date"] == ticker_date)]
        slice["index"] = range(len(slice))
        header = "sec_code;deal_num;date;price;qty;OI;symbol;exp_date;opt_type;strike\n"
        if not os.path.exists(f'{dir_path}/instruments/{optName}.txt'):
            with open(f'{dir_path}/instruments/{optName}.txt', 'w') as fout:
                fout.write(header)
        with open(f'{dir_path}/instruments/{optName}.txt', 'a') as fout:
            for i in slice["index"]:
                lineToPrint = slice["sec_code"][slice["index"] == i].values[0] + ';' + \
                                str(slice["deal_num"][slice["index"] == i].values[0]) + ';' + \
                                str(slice["date"][slice["index"] == i].values[0]) + ';' + \
                                str(slice["price"][slice["index"] == i].values[0]) + ';' + \
                                str(slice["qty"][slice["index"] == i].values[0]) + ';' + \
                                str(slice["OI"][slice["index"] == i].values[0]) + ';' + \
                                slice["symbol"][slice["index"] == i].values[0] + ';' + \
                                str(slice["exp_date"][slice["index"] == i].values[0]) + ';' + \
                                slice["opt_type"][slice["index"] == i].values[0] + ';' + \
                                str(slice["strike"][slice["index"] == i].values[0]) + '\n'
                fout.write(lineToPrint)
            
def parcer_quik(optName, dir_path):
    if os.path.exists(f'{dir_path}/instruments/pr_{optName}.txt'):
        os.remove(f'{dir_path}/instruments/pr_{optName}.txt')
    with open(f'{dir_path}/instruments/{optName}.txt', 'r') as inf:
        data = pd.read_csv(inf, sep=';')
        if len(data) == 0:
            messagebox.showerror(title="Error", message="File is Empty! Choose another date")
            if os.path.exists(f'{dir_path}/instruments/{optName}.txt'):
                os.remove(f'{dir_path}/instruments/{optName}.txt')
            return 0, 0
        data["date"] = pd.to_datetime(data["date"])
        data["exp_date"] = pd.to_datetime(data["exp_date"])
        data.drop_duplicates(keep="first", inplace=True)
        data.sort_values(by="deal_num", ascending=True, inplace=True)
        data.reset_index(inplace=True)

        strikes_tmp = data["strike"].unique()
        strikes_tmp.sort()
        strikes_step = list()
        if len(strikes_tmp) != 1:
            for i in range(1, len(strikes_tmp)):
                strikes_step.append(strikes_tmp[i] - strikes_tmp[i - 1])
            strikes = []
            k = strikes_tmp[0]
            while(k <= strikes_tmp[len(strikes_tmp) - 1]):
                strikes.append(k)
                k = k + min(strikes_step)
        else:
            strikes = []
            strikes.append(strikes_tmp[0])

        deals_CA = {i : [] for i in strikes}
        deals_PA = {i : [] for i in strikes}
        # группируем сделки по страйку и типу опциона
        for i in strikes:
            for j in range(len(data)):
                if data["strike"][j] == i and data["opt_type"][j] == "CA":
                    deals_CA[i].append([data["opt_type"][j], data["price"][j], data["qty"][j], data["OI"][j]])
                if data["strike"][j] == i and data["opt_type"][j] == "PA":
                    deals_PA[i].append([data["opt_type"][j], data["price"][j], data["qty"][j], data["OI"][j]])

        prices_CA = {i : [] for i in strikes}
        prices_PA = {i : [] for i in strikes}

    for i in deals_CA:
        if len(deals_CA[i]) != 0:
            if len(prices_CA[i]) == 0 and deals_CA[i][0][2] * 2 == deals_CA[i][0][3]:
                prices_CA[i].append([deals_CA[i][0][1], deals_CA[i][0][3]])
            elif len(prices_CA[i]) == 0 and deals_CA[i][0][2] * 2 != deals_CA[i][0][3]:
                out = [i, "CA"]
                with open("errors_strikes.txt", 'a+') as errout:
                    errout.write("%s\n" % str(out))
            for j in range(1, len(deals_CA[i])):
                if len(prices_CA[i]) != 0:
                    if prices_CA[i][0][1] + deals_CA[i][j][2] * 2 == deals_CA[i][j][3]:
                        prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) + deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                            / ((prices_CA[i][0][1] / 2) + deals_CA[i][j][2])  
                    elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                        prices_CA[i][0][1] - deals_CA[i][j][2] * 2 != 0:
                        prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) - deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                            / ((prices_CA[i][0][1] / 2) - deals_CA[i][j][2])
                    elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                        prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == 0:
                        prices_CA[i][0][0] = 0
                    prices_CA[i][0][1] = deals_CA[i][j][3]
        else:
            prices_CA[i].append([0, 0])

    for i in deals_PA:
        if len(deals_PA[i]) != 0:
            if len(prices_PA[i]) == 0 and deals_PA[i][0][2] * 2 == deals_PA[i][0][3]:
                prices_PA[i].append([deals_PA[i][0][1], deals_PA[i][0][3]])
            elif len(prices_PA[i]) == 0 and deals_PA[i][0][2] * 2 != deals_PA[i][0][3]:
                out = [i, "PA"]
                with open("errors_strikes.txt", 'a+') as errout:
                    errout.write("%s\n" % str(out))
            for j in range(1, len(deals_PA[i])):
                if len(prices_PA[i]) != 0:
                    if prices_PA[i][0][1] + deals_PA[i][j][2] * 2 == deals_PA[i][j][3]:
                        prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) + deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                            / ((prices_PA[i][0][1] / 2) + deals_PA[i][j][2])   
                    elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                        prices_PA[i][0][1] - deals_PA[i][j][2] * 2 != 0:
                        prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) - deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                            / ((prices_PA[i][0][1] / 2) - deals_PA[i][j][2])
                    elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                        prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == 0:
                        prices_PA[i][0][0] = 0
                    prices_PA[i][0][1] = deals_PA[i][j][3]
        else:
            prices_PA[i].append([0, 0])
        # print(i, prices_PA[i], deals_PA[i])

    header = "opt_type;strike;price;OI\n"
    if not os.path.exists(f'{dir_path}/instruments/pr_{optName}.txt'):
        with open(f'{dir_path}/instruments/pr_{optName}.txt', 'w') as fout:
            fout.write(header)
    with open(f'{dir_path}/instruments/pr_{optName}.txt', 'a') as fout:
        for i in prices_CA:
            lineToPrint = "CA" + ';' + str(i) + ';' + str(prices_CA[i][0][0]) + ';' + str(prices_CA[i][0][1]) + '\n'
            fout.write(lineToPrint)
        for i in prices_PA:
            lineToPrint = "PA" + ';' + str(i) + ';' + str(prices_PA[i][0][0]) + ';' + str(prices_PA[i][0][1]) + '\n'
            fout.write(lineToPrint)   
    # for i in prices_CA:
    #     print(i, "CA -", prices_CA[i], "PA -", prices_PA[i])
    # # print(len(prices_CA))
    return prices_CA, prices_PA
            
def parcer_prices(optName, dir_path, file):
    if not os.path.exists(f'{dir_path}/instruments/pr_{optName}.txt'):
        messagebox.showerror(title="Error", message="You haven't prices! Run analitics mode first.")
        return 0, 0
    else:
        with open(f'{dir_path}/instruments/pr_{optName}.txt', 'r') as fin:
            prices = pd.read_csv(fin, sep=';')
        with open(f'{dir_path}/instruments/{optName}.txt', 'r') as inf:
            data = pd.read_csv(inf, sep=';')
        strikes = list(set(list(prices["strike"].values)))
        strikes_tmptmp = list(set(list(data["strike"].values)))
        strikes_step = list()
        strikes.extend(strikes_tmptmp)
        strikes_tmp = list(set(strikes))
        strikes_tmp = sorted(strikes_tmp)
        
        if len(strikes_tmp) != 1:
            for i in range(1, len(strikes_tmp)):
                strikes_step.append(strikes_tmp[i] - strikes_tmp[i - 1])
            strikes = []
            k = strikes_tmp[0]
            while(k <= strikes_tmp[len(strikes_tmp) - 1]):
                strikes.append(k)
                k = k + min(strikes_step)
        else:
            strikes = []
            strikes.append(strikes_tmp[0])

        deals_CA = {i : [] for i in strikes}
        deals_PA = {i : [] for i in strikes}

        file_date = dt.datetime.strptime(file[:-4], '%d-%m-%Y').day + 1
        data["date"] = pd.to_datetime(data["date"])

        for i in strikes:
            for j in range(len(data)):
                if data["strike"][j] == i and data["opt_type"][j] == "CA" and data["date"][j].day == file_date:
                    deals_CA[i].append([data["opt_type"][j], data["price"][j], data["qty"][j], data["OI"][j]])
                if data["strike"][j] == i and data["opt_type"][j] == "PA" and data["date"][j].day == file_date:
                    deals_PA[i].append([data["opt_type"][j], data["price"][j], data["qty"][j], data["OI"][j]])

        prices_CA = {i : [] for i in strikes}
        prices_PA = {i : [] for i in strikes}

        for i in deals_CA:
            if len(deals_CA[i]) != 0:
                try:
                    if list(prices[(prices["strike"] == i) & (prices["opt_type"] == "CA")]["price"].values)[0] == 0:
                        if len(prices_CA[i]) == 0 and deals_CA[i][0][2] * 2 == deals_CA[i][0][3]:
                            prices_CA[i].append([deals_CA[i][0][1], deals_CA[i][0][3]])
                        elif len(prices_CA[i]) == 0 and deals_CA[i][0][2] * 2 != deals_CA[i][0][3]:
                            out = [i, "CA"]
                            with open("errors_strikes.txt", 'a+') as errout:
                                errout.write("%s\n" % str(out))
                        for j in range(1, len(deals_CA[i])):
                            if len(prices_CA[i]) != 0:
                                if prices_CA[i][0][1] + deals_CA[i][j][2] * 2 == deals_CA[i][j][3]:
                                    prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) + deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                                        / ((prices_CA[i][0][1] / 2) + deals_CA[i][j][2])  
                                elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                                    prices_CA[i][0][1] - deals_CA[i][j][2] * 2 != 0:
                                    prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) - deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                                        / ((prices_CA[i][0][1] / 2) - deals_CA[i][j][2])
                                elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                                    prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == 0:
                                    prices_CA[i][0][0] = 0
                                prices_CA[i][0][1] = deals_CA[i][j][3]
                    else:
                        if len(prices_CA[i]) == 0:
                            prices_CA[i].append([list(prices[(prices["strike"] == i) & (prices["opt_type"] == "CA")]["price"].values)[0], \
                                        list(prices[(prices["strike"] == i) & (prices["opt_type"] == "CA")]["OI"].values)[0]])  
                           
                except:
                    if len(deals_CA[i]) != 0:
                        if len(prices_CA[i]) == 0 and deals_CA[i][0][2] * 2 == deals_CA[i][0][3]:
                            prices_CA[i].append([deals_CA[i][0][1], deals_CA[i][0][3]])
                        elif len(prices_CA[i]) == 0 and deals_CA[i][0][2] * 2 != deals_CA[i][0][3]:
                            out = [i, "CA"]
                            with open("errors_strikes.txt", 'a+') as errout:
                                errout.write("%s\n" % str(out))
                        for j in range(1, len(deals_CA[i])):
                            if len(prices_CA[i]) != 0:
                                if prices_CA[i][0][1] + deals_CA[i][j][2] * 2 == deals_CA[i][j][3]:
                                    prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) + deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                                        / ((prices_CA[i][0][1] / 2) + deals_CA[i][j][2])   
                                elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                                    prices_CA[i][0][1] - deals_CA[i][j][2] * 2 != 0:
                                    prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) - deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                                        / ((prices_CA[i][0][1] / 2) - deals_CA[i][j][2])
                                elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                                    prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == 0:
                                    prices_CA[i][0][0] = 0
                                prices_CA[i][0][1] = deals_CA[i][j][3]
                    else:
                        prices_CA[i].append([0, 0])
            else:
                try:
                    prices_CA[i].append([list(prices[(prices["strike"] == i) & (prices["opt_type"] == "CA")]["price"].values)[0], \
                                        list(prices[(prices["strike"] == i) & (prices["opt_type"] == "CA")]["OI"].values)[0]])
                except:
                    prices_CA[i].append([0, 0])

        for i in deals_CA:
            if len(deals_CA[i]) != 0:
                for j in range(0, len(deals_CA[i])):   
                    if prices_CA[i][0][1] + deals_CA[i][j][2] * 2 == deals_CA[i][j][3]:
                        prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) + deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                            / ((prices_CA[i][0][1] / 2) + deals_CA[i][j][2])
                    elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                            prices_CA[i][0][1] - deals_CA[i][j][2] * 2 != 0:
                            prices_CA[i][0][0] = (prices_CA[i][0][0] * (prices_CA[i][0][1] / 2) - deals_CA[i][j][1] * deals_CA[i][j][2]) \
                                                / ((prices_CA[i][0][1] / 2) - deals_CA[i][j][2])
                    elif prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == deals_CA[i][j][3] and \
                        prices_CA[i][0][1] - deals_CA[i][j][2] * 2 == 0:
                        prices_CA[i][0][0] = 0
                    prices_CA[i][0][1] = deals_CA[i][j][3]

        for i in deals_PA:
            if len(deals_PA[i]) != 0:
                try:
                    if list(prices[(prices["strike"] == i) & (prices["opt_type"] == "PA")]["price"].values)[0] == 0:
                        if len(prices_PA[i]) == 0 and deals_PA[i][0][2] * 2 == deals_PA[i][0][3]:
                            prices_PA[i].append([deals_PA[i][0][1], deals_PA[i][0][3]])
                        elif len(prices_PA[i]) == 0 and deals_PA[i][0][2] * 2 != deals_PA[i][0][3]:
                            out = [i, "PA"]
                            with open("errors_strikes.txt", 'a+') as errout:
                                errout.write("%s\n" % str(out))
                        for j in range(1, len(deals_PA[i])):
                            if len(prices_PA[i]) != 0:
                                if prices_PA[i][0][1] + deals_PA[i][j][2] * 2 == deals_PA[i][j][3]:
                                    prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) + deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                                        / ((prices_PA[i][0][1] / 2) + deals_PA[i][j][2])  
                                elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                                    prices_PA[i][0][1] - deals_PA[i][j][2] * 2 != 0:
                                    prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) - deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                                        / ((prices_PA[i][0][1] / 2) - deals_PA[i][j][2])
                                elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                                    prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == 0:
                                    prices_PA[i][0][0] = 0
                                prices_PA[i][0][1] = deals_PA[i][j][3]
                    else:
                        if len(prices_PA[i]) == 0:
                            prices_PA[i].append([list(prices[(prices["strike"] == i) & (prices["opt_type"] == "PA")]["price"].values)[0], \
                                        list(prices[(prices["strike"] == i) & (prices["opt_type"] == "PA")]["OI"].values)[0]])
                except:
                    if len(deals_PA[i]) != 0:
                        if len(prices_PA[i]) == 0 and deals_PA[i][0][2] * 2 == deals_PA[i][0][3]:
                            prices_PA[i].append([deals_PA[i][0][1], deals_PA[i][0][3]])
                        elif len(prices_PA[i]) == 0 and deals_PA[i][0][2] * 2 != deals_PA[i][0][3]:
                            out = [i, "PA"]
                            with open("errors_strikes.txt", 'a+') as errout:
                                errout.write("%s\n" % str(out))
                        for j in range(1, len(deals_PA[i])):
                            if len(prices_PA[i]) != 0:
                                if prices_PA[i][0][1] + deals_PA[i][j][2] * 2 == deals_PA[i][j][3]:
                                    prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) + deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                                        / ((prices_PA[i][0][1] / 2) + deals_PA[i][j][2])   
                                elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                                    prices_PA[i][0][1] - deals_PA[i][j][2] * 2 != 0:
                                    prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) - deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                                        / ((prices_PA[i][0][1] / 2) - deals_PA[i][j][2])
                                elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                                    prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == 0:
                                    prices_PA[i][0][0] = 0
                                prices_PA[i][0][1] = deals_PA[i][j][3]
                    else:
                        prices_PA[i].append([0, 0])
            else:
                try:
                    prices_PA[i].append([list(prices[(prices["strike"] == i) & (prices["opt_type"] == "PA")]["price"].values)[0], \
                                        list(prices[(prices["strike"] == i) & (prices["opt_type"] == "PA")]["OI"].values)[0]])
                except:
                    prices_PA[i].append([0, 0])

        for i in deals_PA:
            if len(deals_PA[i]) > 0:
                for j in range(0, len(deals_PA[i])):
                    if prices_PA[i][0][1] + deals_PA[i][j][2] * 2 == deals_PA[i][j][3]:
                        prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) + deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                            / ((prices_PA[i][0][1] / 2) + deals_PA[i][j][2])
                    elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                            prices_PA[i][0][1] - deals_PA[i][j][2] * 2 != 0:
                            prices_PA[i][0][0] = (prices_PA[i][0][0] * (prices_PA[i][0][1] / 2) - deals_PA[i][j][1] * deals_PA[i][j][2]) \
                                                / ((prices_PA[i][0][1] / 2) - deals_PA[i][j][2])
                    elif prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == deals_PA[i][j][3] and \
                        prices_PA[i][0][1] - deals_PA[i][j][2] * 2 == 0:
                        prices_PA[i][0][0] = 0
                    prices_PA[i][0][1] = deals_PA[i][j][3]
    return prices_CA, prices_PA
