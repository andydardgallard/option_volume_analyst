import tkinter as tk
import datetime as dt

def visual_pnl(prices_CA, prices_PA, root, optName, FutPrice):
    root.title(f'PnL {optName} - {dt.datetime.now().date()}')
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
    
    for i in prices_CA:
        if i < FutPrice and prices_CA[i][0][0] != 0:
            prices_CA[i].append(i - FutPrice + prices_CA[i][0][0])
            prices_CA[i].append((i - FutPrice + prices_CA[i][0][0]) * prices_CA[i][0][1])
        elif i >= FutPrice and prices_CA[i][0][0] != 0:
            prices_CA[i].append(prices_CA[i][0][0])
            prices_CA[i].append(prices_CA[i][0][0] * prices_CA[i][0][1])
        else:
            prices_CA[i].append(0)
            prices_CA[i].append(0)

    for i in prices_PA:
        if i > FutPrice and prices_PA[i][0][0] != 0:
            prices_PA[i].append(FutPrice - i + prices_PA[i][0][0])
            prices_PA[i].append((FutPrice - i + prices_PA[i][0][0]) * prices_PA[i][0][1])
        elif i <= FutPrice and prices_PA[i][0][0] != 0:
            prices_PA[i].append(prices_PA[i][0][0])
            prices_PA[i].append(prices_PA[i][0][0] * prices_PA[i][0][1])
        else:
            prices_PA[i].append(0)
            prices_PA[i].append(0)
    
    for i in prices_PA:
        prices_PA[i].append(prices_CA[i][2] + prices_PA[i][2])
    
    max_call_Pnl = max(prices_CA[i][2] for i in prices_CA)
    min_call_Pnl = min(prices_CA[i][2] for i in prices_CA)
    max_put_Pnl = max(prices_PA[i][2] for i in prices_PA)
    min_put_Pnl = min(prices_PA[i][2] for i in prices_PA)
    max_Pnl = max(prices_PA[i][3] for i in prices_PA)
    min_Pnl = min(prices_PA[i][3] for i in prices_PA)
    
    rng_pos = max(max_call_Pnl, max_put_Pnl, max_Pnl) / \
        (max(max_call_Pnl, max_put_Pnl, max_Pnl) - min(min_call_Pnl, min_put_Pnl, min_Pnl))
    y_grid_med = y_grid_start + (y_grid_end - y_grid_start) * rng_pos
    scale_y = (y_grid_end - y_grid_start) * rng_pos / max(max_call_Pnl, max_put_Pnl, max_Pnl)

    x = x_grid_start
    canv.create_line(x, y_grid_med, x + scale_x, y_grid_med - scale_y * list(prices_CA.values())[0][2], \
                    fill="green", width=3)
    canv.create_line(x, y_grid_med, x + scale_x, y_grid_med - scale_y * list(prices_PA.values())[0][2], \
                    fill="red", width=3)

    for i in range(1, len(prices_CA)):
        x += scale_x
        canv.create_line(x, y_grid_med - scale_y * list(prices_CA.values())[i - 1][2], \
                        x + scale_x, y_grid_med - scale_y * list(prices_CA.values())[i][2], fill="green", width=3)
        
        canv.create_line(x, y_grid_med - scale_y * list(prices_PA.values())[i - 1][2], \
                        x + scale_x, y_grid_med - scale_y * list(prices_PA.values())[i][2], fill="red", width=3)  
    
    x += scale_x
    if len(prices_PA) != 1:
        canv.create_line(x, y_grid_med - scale_y * list(prices_CA.values())[i][2], \
                            x + scale_x, y_grid_med, fill="green", width=3)
        canv.create_line(x, y_grid_med - scale_y * list(prices_PA.values())[i][2], \
                            x + scale_x, y_grid_med, fill="red", width=3)
    else:
        canv.create_line(x, y_grid_med - scale_y * list(prices_CA.values())[0][2], x + scale_x, y_grid_med, \
                    fill="green", width=3)
        canv.create_line(x, y_grid_med - scale_y * list(prices_PA.values())[0][2], x + scale_x, y_grid_med, \
                    fill="red", width=3)

    x = x_grid_start
    canv.create_line(x, y_grid_med, x + scale_x, y_grid_med - scale_y * list(prices_PA.values())[0][3], \
                    fill="blue", width=3)

    for i in range(1, len(prices_PA)):
        x += scale_x
        canv.create_line(x, y_grid_med - scale_y * list(prices_PA.values())[i - 1][3], \
                        x + scale_x, y_grid_med - scale_y * list(prices_PA.values())[i][3], fill="blue", width=3)
        lbl_call = tk.Label(root, text="total_" +  str(int(list(prices_PA.values())[i - 1][3])), font=("Arial", 10))
        if list(prices_PA.values())[i - 1][3] != 0:
            lbl_call.place(x=x, y=y_grid_med - scale_y * list(prices_PA.values())[i - 1][3])
    
    x += scale_x
    if len(prices_PA) != 1:
        canv.create_line(x, y_grid_med - scale_y * list(prices_PA.values())[i][3], \
                            x + scale_x, y_grid_med, fill="blue", width=3)
    else:
        canv.create_line(x, y_grid_med - scale_y * list(prices_PA.values())[0][3], x + scale_x, y_grid_med, \
                    fill="blue", width=3)
    
    lbl = tk.Label(root, text="grand_total = " + str(int(sum(prices_PA[i][3] for i in prices_PA))), font=("Arial", 12))
    lbl.place(x=10, y=10)

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


        