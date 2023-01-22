import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
import spec, parcer_fut, parcer_quik, visual, visual_pnl, visual_optimal, cleaner, screenshot

class Form:
    dir_path = "none"
    rb_var = int()
    fut_var = str()
    exp_date = str()
    scr_chck = int()
    sim_chck = int()
    txt_futPrice = "none"

    def __init__(self, root) -> None:
        root.title("Option Stratagy")
        win_h = root.winfo_screenheight() * 0.25
        win_w = root.winfo_screenwidth() * 0.25
        root.geometry(f'{int(win_w)}x{int(win_h)}')
        root.resizable(False, False)
        root.config(bg="gray")

        browse_button = tk.Button(root, text="Choose opt folder", command=lambda: self.browse_files(root))
        browse_button.place(x=10, y=10)

        self.fut_var = tk.StringVar()
        fut_name = ttk.Combobox(root, textvariable=self.fut_var, width=14)
        fut_name['values'] = ("RTS", "Si", "SBER", "CNY")
        fut_name["state"] = 'readonly'
        fut_name.place(x=10, y=45)
        fut_name.current(0)

        self.exp_date = DateEntry(root, width=14, foreground="black")
        self.exp_date.place(x=160, y=45)

        self.rb_var = tk.IntVar()
        rb_antcs = tk.Radiobutton(root, text="Analitics mode", value=0, variable=self.rb_var, bg="gray")
        rb_antcs.place(x=10, y=110)
        rb_exprtn = tk.Radiobutton(root, text="Expiration mode", value=1, variable=self.rb_var, bg="gray")
        rb_exprtn.place(x=10, y=140)
        
        start_button = tk.Button(root, text="START", command=self.start_visual)
        start_button.place(x=10, y=200)

        stop_button = tk.Button(root, text="UPD for Exp mode", command=self.upd_exp_mode)
        stop_button.place(x=100, y=200)

        cleaner_button = tk.Button(root, text="Cleaner", command=lambda: cleaner.cleaner(self.dir_path))
        cleaner_button.place(x=260, y=200)

        self.scr_chck = tk.IntVar()
        self.scr_chck.set(0)
        scr_checkbtn = tk.Checkbutton(root, variable=self.scr_chck, text="Screenshot", \
                    onvalue=1, offvalue=0, bg="gray")
        scr_checkbtn.place(x=200, y=110)

        self.sim_chck = tk.IntVar()
        self.sim_chck.set(0)
        sim_checkbtn = tk.Checkbutton(root, variable=self.sim_chck, text="Simulation", \
            onvalue=1, offvalue=0, bg="gray")
        sim_checkbtn.place(x=10, y=165)

        self.txt_futPrice = tk.StringVar()
        futPrice_textbox = tk.Entry(root, width=14, textvariable=self.txt_futPrice)
        futPrice_textbox.place(x=10, y=78)

    def upd_exp_mode(self):
        if self.dir_path == 'none' or self.dir_path == '':
            messagebox.showerror(title="Error", message="Choose files!")
        else:
            if self.rb_var.get() == 1 :
                futName = spec.symbol[self.fut_var.get()]
                optName = self.date_define(futName)
                if os.path.exists(f'{self.dir_path}/instruments/{optName}.txt'):
                    os.remove(f'{self.dir_path}/instruments/{optName}.txt')
                file_list = os.listdir(f'{self.dir_path}/exp')
                if self.sim_chck.get() == 0:
                    futPrice = parcer_fut.parcer_fut(futName, self.dir_path)
                else:
                    try:
                        futPrice = float(self.txt_futPrice.get())
                    except:
                        messagebox.showerror(title="Error", message="Insert numeric value fo Future price!")
                        return
                if len(file_list) == 1:
                        parcer_quik.preparcer_quik(optName, file_list[0], self.dir_path, self.rb_var.get())
                else:
                    messagebox.showerror(title="Error", message="Too mach or no files in exp folder!")
                    return
                prices_CA, prices_PA = parcer_quik.parcer_prices(optName, self.dir_path, file_list[0])
                if prices_CA != 0 and prices_PA != 0:
                    root_oi = tk.Tk()
                    visual.visualization(prices_CA, prices_PA, root_oi, optName, futPrice)
                    root_pnl = tk.Tk()
                    visual_pnl.visual_pnl(prices_CA, prices_PA, root_pnl, optName, futPrice)
                    root_opt = tk.Tk()
                    visual_optimal.visual_opt(prices_CA, prices_PA, root_opt, optName, futPrice)
                    # root_pnl.mainloop()
                    # root_oi.mainloop()
            else:
                messagebox.showerror(title="Error", message="Start button!")

    def browse_files(self, root):
        self.dir_path = filedialog.askdirectory()
        path_label = tk.Label(root, text=self.dir_path, font=("Arial", 12), bg="gray")
        path_label.place(x=160, y=15)
    
    def date_define(self, futName):
        name = futName
        if len(str(self.exp_date.get_date().day)) == 1:
            name = name + '0' + str(self.exp_date.get_date().day)
        else:
            name = name + str(self.exp_date.get_date().day)

        if len(str(self.exp_date.get_date().month)) == 1:
            name = name + '0' + str(self.exp_date.get_date().month)
        else:
            name = name + str(self.exp_date.get_date().month)
        
        name = name + str(self.exp_date.get_date().year)[2:]
        return(name)

    def start_visual(self):
        if self.dir_path == 'none' or self.dir_path == '':
            messagebox.showerror(title="Error", message="Choose files!")
        elif self.sim_chck.get() == 1:
            messagebox.showerror(title="Error", message="Use only in Expiration mode!")
        else:
            if self.rb_var.get() == 0:
                futName = spec.symbol[self.fut_var.get()]
                optName = self.date_define(futName)
                if os.path.exists(f'{self.dir_path}/instruments/{optName}.txt'):
                    os.remove(f'{self.dir_path}/instruments/{optName}.txt')
                file_list = os.listdir(f'{self.dir_path}/data')
                futPrice = parcer_fut.parcer_fut(futName, self.dir_path)
                for file in file_list:
                    parcer_quik.preparcer_quik(optName, file, self.dir_path, self.rb_var.get())
                prices_CA, prices_PA = parcer_quik.parcer_quik(optName, self.dir_path)
                if prices_CA != 0 and prices_PA != 0:
                    root_oi = tk.Tk()
                    visual.visualization(prices_CA, prices_PA, root_oi, optName, futPrice)
                    root_pnl = tk.Tk()
                    visual_pnl.visual_pnl(prices_CA, prices_PA, root_pnl, optName, futPrice)
                    root_opt = tk.Tk()
                    visual_optimal.visual_opt(prices_CA, prices_PA, root_opt, optName, futPrice)
                    # root_pnl.mainloop()
                    # root_oi.mainloop()
            else:
                messagebox.showerror(title="Error", message="Use UPD button!")  
              

