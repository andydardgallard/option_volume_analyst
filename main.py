import os
import form
import tkinter as tk

if __name__ == "__main__":
    if os.path.exists("errors_strikes.txt"):
        os.remove("errors_strikes.txt")
    root_form = tk.Tk()    
    menu = form.Form(root_form)
    root_form.mainloop()
