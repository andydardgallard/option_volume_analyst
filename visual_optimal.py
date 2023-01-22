import tkinter as tk
import datetime as dt

def visual_opt(prices_CA, prices_PA, root, optName, FutPrice):
    root.title(f'Optimal Fitires Price {optName} - {dt.datetime.now().date()}')
    win_h = root.winfo_screenheight() * 0.8
    win_w = root.winfo_screenwidth()
    root.geometry(f'{win_w}x{int(win_h)}')
    root.resizable(False, False)

    # Create canvas frame
    x_cnvs_start = 0
    y_cnvs_start = win_h * 0.05
    cnvs_width = win_w
    cnvs_height = win_h * 0.89
    canv = tk.Canvas(root, width=cnvs_width, height=cnvs_height)
    canv.place(x=x_cnvs_start, y=y_cnvs_start)

    x_grid_start = cnvs_width * 0.05
    x_grid_end = cnvs_width * 0.95
    y_grid_start = y_cnvs_start * 0.2 + y_cnvs_start
    y_grid_end = cnvs_height * 0.9 + y_cnvs_start
    scale_x = (x_grid_end - x_grid_start) / (len(prices_CA.keys()) + 1)
    
    FutRzlts = opt_price_finder(prices_CA, prices_PA)
    maxVar_strike = max(FutRzlts, key=FutRzlts.get)
    maxVar = FutRzlts[maxVar_strike]
    minVar = -maxVar / 2

    coord_y = {i : [] for i in FutRzlts}
    for i in FutRzlts:
        if FutRzlts[i] < minVar:
            coord_y[i].append(minVar)
        else:
            coord_y[i].append(FutRzlts[i])
    
    rng_pos = maxVar / (maxVar - minVar)
    y_grid_med = y_grid_start + (y_grid_end - y_grid_start) * rng_pos
    scale_y = (y_grid_end - y_grid_start) * rng_pos / maxVar

    x = x_grid_start
    canv.create_line(x, y_grid_med - scale_y * minVar, x + scale_x, y_grid_med - scale_y * list(coord_y.values())[0][0], \
                    fill="blue", width=3)

    for i in range(1, len(coord_y)):
        x += scale_x
        canv.create_line(x, y_grid_med - scale_y * list(coord_y.values())[i - 1][0], \
                        x + scale_x, y_grid_med - scale_y * list(coord_y.values())[i][0], fill="blue", width=3)
        lbl_call = tk.Label(root, text=str(int(list(coord_y.values())[i - 1][0])), font=("Arial", 10))
        if list(coord_y.values())[i - 1][0] > 0:
            lbl_call.place(x=x, y=y_grid_med - scale_y * list(coord_y.values())[i - 1][0])
    
    x += scale_x
    if len(prices_PA) != 1:
        canv.create_line(x, y_grid_med - scale_y * list(coord_y.values())[i][0], \
                            x + scale_x, y_grid_med - scale_y * minVar, fill="blue", width=3)
    else:
        canv.create_line(x, y_grid_med - scale_y * list(coord_y.values())[0][0], x + scale_x, y_grid_med - scale_y * minVar, \
                    fill="blue", width=3)
    
    ba_range = (FutPrice - list(prices_CA.keys())[0]) / \
                (list(prices_CA.keys())[len(prices_CA) - 1] - list(prices_CA.keys())[0])
    scale_ba = (x_grid_end - x_grid_start - scale_x * 2) * ba_range
    canv.create_line(x_grid_start + scale_ba + scale_x, y_grid_start, \
                    x_grid_start + scale_ba + scale_x, y_grid_end, width=3)
    lbl_ba = tk.Label(root, text=str(float(FutPrice)), font=("Arial", 12))
    lbl_ba.place(x=x_grid_start + scale_ba + scale_x - 15, y=y_grid_end + y_cnvs_start + 25)

    canv.create_line(x_grid_start, y_grid_med, x_grid_end, y_grid_med)
    x = x_grid_start
    for i in prices_CA:
        x += scale_x
        canv.create_line(x, y_grid_end, x, y_grid_start)
        lbl = tk.Label(root, text=str(i), font=("Arial", 12))
        lbl.place(x=x - 15, y=y_grid_end + y_cnvs_start + 5)

def opt_price_finder(prices_CA, prices_PA):
    futRzlts = {i : [] for i in list(prices_PA.keys())}    
    
    for j in futRzlts:
        pnl_CA = {k: [] for k in prices_CA}
        pnl_PA = {k: [] for k in prices_CA}

        for i in prices_CA: 
            if i < j and prices_CA[i][0][0] != 0:
                pnl_CA[i].append(i - j + prices_CA[i][0][0])
                pnl_CA[i].append((i - j + prices_CA[i][0][0]) * prices_CA[i][0][1])
            elif i >= j and prices_CA[i][0][0] != 0:
                pnl_CA[i].append(prices_CA[i][0][0])
                pnl_CA[i].append(prices_CA[i][0][0] * prices_CA[i][0][1])
            else:
                pnl_CA[i].append(0)
                pnl_CA[i].append(0)

        for i in prices_PA:
            if i > j and prices_PA[i][0][0] != 0:
                pnl_PA[i].append(j - i + prices_PA[i][0][0])
                pnl_PA[i].append((j - i + prices_PA[i][0][0]) * prices_PA[i][0][1])
            elif i <= j and prices_PA[i][0][0] != 0:
                pnl_PA[i].append(prices_PA[i][0][0])
                pnl_PA[i].append(prices_PA[i][0][0] * prices_PA[i][0][1])
            else:
                pnl_PA[i].append(0)
                pnl_PA[i].append(0)
    
        for i in pnl_PA:
            pnl_PA[i].append(pnl_CA[i][1] + pnl_PA[i][1])
        
        futRzlts[j] = int(sum(pnl_PA[i][2] for i in pnl_PA))
    return futRzlts
        
def opt_price_finder(prices_CA, prices_PA):
    futRzlts = {i : [] for i in list(prices_PA.keys())}    
    
    for j in futRzlts:
        pnl_CA = {k: [] for k in prices_CA}
        pnl_PA = {k: [] for k in prices_CA}

        for i in prices_CA: 
            if i < j and prices_CA[i][0][0] != 0:
                pnl_CA[i].append(i - j + prices_CA[i][0][0])
                pnl_CA[i].append((i - j + prices_CA[i][0][0]) * prices_CA[i][0][1])
            elif i >= j and prices_CA[i][0][0] != 0:
                pnl_CA[i].append(prices_CA[i][0][0])
                pnl_CA[i].append(prices_CA[i][0][0] * prices_CA[i][0][1])
            else:
                pnl_CA[i].append(0)
                pnl_CA[i].append(0)

        for i in prices_PA:
            if i > j and prices_PA[i][0][0] != 0:
                pnl_PA[i].append(j - i + prices_PA[i][0][0])
                pnl_PA[i].append((j - i + prices_PA[i][0][0]) * prices_PA[i][0][1])
            elif i <= j and prices_PA[i][0][0] != 0:
                pnl_PA[i].append(prices_PA[i][0][0])
                pnl_PA[i].append(prices_PA[i][0][0] * prices_PA[i][0][1])
            else:
                pnl_PA[i].append(0)
                pnl_PA[i].append(0)
    
        for i in pnl_PA:
            pnl_PA[i].append(pnl_CA[i][1] + pnl_PA[i][1])
        
        futRzlts[j] = int(sum(pnl_PA[i][2] for i in pnl_PA))
    return futRzlts