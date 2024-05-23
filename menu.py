from tkinter import Tk, Frame,Label,Button
from tkinter.constants import BOTH
from PIL import ImageTk, Image
import max, min
#import suma, mult, trans, determinante, potencia, inversa, rango
gui_menu = Tk() 
gui_menu.geometry("500x500")
gui_menu.resizable(False,False)
gui_menu.title("Max and Min Solver")

# main_image_path="matrix-icon.jpg"
# img = Image.open(main_image_path)
# img = img.resize((100, 100), Image.Resampling.LANCZOS)
# img = ImageTk.PhotoImage(img)  
# # frame_main.pack()

frame_title = Frame(gui_menu)
frame_title.pack(padx=5, pady=30)
#label_img = Label(frame_title, image=img)
text_label = Label(frame_title, text="LINEAR PROGRAMMING SOLVER", pady=10)
#label_img.image = img
#label_img.pack()
text_label.pack()


frame_menu = Frame(gui_menu, highlightbackground='black', highlightthickness=1)
frame_menu.pack(fill=BOTH, expand=True, padx=5, pady=5 )
frame_buttons=Frame(frame_menu)
frame_buttons.pack()
class Menu:
    def __init__(self):
        self.label = Label(frame_buttons, text="Menu de Operaciones")
        self.sum_btn=Button(frame_buttons,text="Metodo Grafico", )
        self.mul_btn=Button(frame_buttons, text="Simplex Maximizacion",command=max.Max)
        self.trans_btn=Button(frame_buttons, text="Dos Fases Minimizacion", command=min.Min)
        
        self._packing()
        gui_menu.mainloop()
    def _packing(self):
        padx_g=15
        pady_g=5
        self.label.grid(row=1, column=2, padx=padx_g, pady=pady_g)
        self.sum_btn.grid(row=2, column=1, padx=padx_g, pady=pady_g)
        self.mul_btn.grid(row=2, column=2, padx=padx_g, pady=pady_g)
        self.trans_btn.grid(row=2, column=3, padx=padx_g, pady=pady_g)
        