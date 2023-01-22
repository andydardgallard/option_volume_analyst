import tkinter as tk
import datetime as dt

def visualization(prices_CA, prices_PA, root, optName, FutPrice):
    root.title(f'Open Interest {optName} - {dt.datetime.now().date()}')
    win_h = root.winfo_screenheight() * 0.75
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

    #Create grid
    max_callOI = max(prices_CA[key][0][1] for key in prices_CA)
    max_putOI = max(prices_PA[key][0][1] for key in prices_PA)
    maxOI = max(max_callOI, max_putOI)
    scale_y = (y_grid_end - y_grid_start)/maxOI
    x = x_grid_start
    canv.create_line(x, y_grid_end, x + scale_x, y_grid_end - scale_y * list(prices_CA.values())[0][0][1], fill="lightgreen", width=2)
    canv.create_line(x, y_grid_end, x + scale_x, y_grid_end - scale_y * list(prices_PA.values())[0][0][1], fill="#FF8D8D", width=2)

    for i in range(1, len(prices_CA)):
        x += scale_x
        canv.create_line(x, y_grid_end - scale_y * list(prices_CA.values())[i - 1][0][1], \
                        x + scale_x, y_grid_end - scale_y * list(prices_CA.values())[i][0][1], fill="lightgreen", width=2)
        
        canv.create_line(x, y_grid_end - scale_y * list(prices_PA.values())[i - 1][0][1], \
                        x + scale_x, y_grid_end - scale_y * list(prices_PA.values())[i][0][1], fill="#FF8D8D", width=2)  
    x += scale_x
    if len(prices_PA) != 1:
        canv.create_line(x, y_grid_end - scale_y * list(prices_CA.values())[i][0][1], \
                            x + scale_x, y_grid_end, fill="lightgreen", width=2)

        canv.create_line(x, y_grid_end - scale_y * list(prices_PA.values())[i][0][1], \
                            x + scale_x, y_grid_end, fill="#FF8D8D", width=2)
    else:
        canv.create_line(x, y_grid_end - scale_y * list(prices_CA.values())[0][0][1], x + scale_x, y_grid_end, fill="lightgreen", width=2)
        canv.create_line(x, y_grid_end - scale_y * list(prices_PA.values())[0][0][1], x + scale_x, y_grid_end, fill="#FF8D8D", width=2)

    vol_CA = [(prices_CA[key][0][0] * prices_CA[key][0][1]) for key in prices_CA]
    vol_PA = [(prices_PA[key][0][0] * prices_PA[key][0][1]) for key in prices_PA]

    max_callOI = max(vol_CA)
    max_putOI = max(vol_PA)
    maxOI = max(max_callOI, max_putOI)
    scale_y = (y_grid_end - y_grid_start)/maxOI
    x = x_grid_start
    canv.create_line(x, y_grid_end, x + scale_x, y_grid_end - scale_y * vol_CA[0], fill="green", width=3)
    canv.create_line(x, y_grid_end, x + scale_x, y_grid_end - scale_y * vol_PA[0], fill="red", width=3)

    for i in range(1, len(vol_CA)):
        x += scale_x
        canv.create_line(x, y_grid_end - scale_y * vol_CA[i - 1], \
                        x + scale_x, y_grid_end - scale_y * vol_CA[i], fill="green", width=3)
        lbl_call = tk.Label(root, text="mca_" +  str(int(vol_CA[i - 1])), font=("Arial", 10))
        if vol_CA[i - 1] > 0:
            lbl_call.place(x=x, y=y_grid_end - scale_y * vol_CA[i - 1])
        
        canv.create_line(x, y_grid_end - scale_y * vol_PA[i - 1], \
                        x + scale_x, y_grid_end - scale_y * vol_PA[i], fill="red", width=3)  
        lbl_put = tk.Label(root, text="mpa_" +  str(int(vol_PA[i - 1])), font=("Arial", 10))
        if vol_PA[i - 1] > 0:
            lbl_put.place(x=x, y=y_grid_end - scale_y * vol_PA[i - 1])
    
    x += scale_x
    if len(prices_PA) != 1:
        canv.create_line(x, y_grid_end - scale_y * vol_CA[i], x + scale_x, y_grid_end, fill="green", width=3)
        lbl_call = tk.Label(root, text="mca_" +  str(int(vol_CA[i])), font=("Arial", 10))
        if vol_CA[i] > 0:
            lbl_call.place(x=x, y=y_grid_end - scale_y * vol_CA[i])
        canv.create_line(x, y_grid_end - scale_y * vol_PA[i], x + scale_x, y_grid_end, fill="red", width=3)
        lbl_put = tk.Label(root, text="mpa_" +  str(int(vol_PA[i])), font=("Arial", 10))
        if vol_PA[i] > 0:
            lbl_put.place(x=x, y=y_grid_end - scale_y * vol_PA[i])
    else:
        canv.create_line(x, y_grid_end - scale_y * vol_CA[0], x + scale_x, y_grid_end, fill="green", width=3)
        canv.create_line(x, y_grid_end - scale_y * vol_PA[0], x + scale_x, y_grid_end, fill="red", width=3)

    
    ba_range = (FutPrice - list(prices_CA.keys())[0]) / \
                (list(prices_CA.keys())[len(prices_CA) - 1] - list(prices_CA.keys())[0])
    scale_ba = (x_grid_end - x_grid_start - scale_x * 2) * ba_range
    canv.create_line(x_grid_start + scale_ba + scale_x, y_grid_start, \
                    x_grid_start + scale_ba + scale_x, y_grid_end, width=3)
    lbl_ba = tk.Label(root, text=str(float(FutPrice)), font=("Arial", 12))
    lbl_ba.place(x=x_grid_start + scale_ba + scale_x - 15, y=y_grid_end + y_cnvs_start + 25)

    canv.create_line(x_grid_start,y_grid_end,x_grid_end,y_grid_end)
    x = x_grid_start
    for i in prices_CA:
        x += scale_x
        canv.create_line(x, y_grid_end, x, y_grid_start)
        lbl = tk.Label(root, text=str(i), font=("Arial", 12))
        lbl.place(x=x - 15, y=y_grid_end + y_cnvs_start + 5)
