from tkinter import Toplevel,Frame,Label, IntVar, OptionMenu, Button, StringVar, Entry, messagebox, ttk
import input
class Min:
    def __init__(self):
        self.gui_sum_menu_dim = Toplevel()
        self.input=input.ProblemInput(2,self.gui_sum_menu_dim)
