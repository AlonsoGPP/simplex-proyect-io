from tkinter import Tk, Frame,Label,Button,Menu,messagebox
from tkinter.constants import BOTH
from PIL import ImageTk, Image
import max, min
gui_menu = Tk() 
gui_menu.geometry("500x500")
gui_menu.iconbitmap("assets/LP.ico")
gui_menu.resizable(False,False)
gui_menu.title("Simplex Solver")
def acerca_de():
    messagebox.showinfo("Acerca de", "Creado por: David Garcia Pariona\nCurso: Investigacion de Operaciones I")

#menu
barra_menu = Menu(gui_menu)
menu_archivo = Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Acerca de", command=acerca_de)

menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=gui_menu.quit)

barra_menu.add_cascade(label="Info", menu=menu_archivo)
gui_menu.config(menu=barra_menu)
main_image_path="assets/LP.png"
img = Image.open(main_image_path)
img = img.resize((100, 100), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)  
#frame_main.pack()

frame_title = Frame(gui_menu)
frame_title.pack(padx=5, pady=30)
label_img = Label(frame_title, image=img)
text_label = Label(frame_title, text="LINEAR PROGRAMMING SOLVER", pady=10)
label_img.image = img
label_img.pack()
text_label.pack()

frame_menu = Frame(gui_menu, highlightbackground='black', highlightthickness=1)
frame_menu.pack(fill=BOTH, expand=True, padx=5, pady=5 )
frame_buttons=Frame(frame_menu)
frame_title_btns=Frame(frame_menu)
frame_title_btns.pack()
frame_buttons.pack()
class Menu:
    def __init__(self):
        self.label = Label(frame_title_btns, text="Menu de Operaciones").pack()
        self.btn_max=Button(frame_buttons, text="Simplex Maximizacion",command=max.Max)
        self.btn_min=Button(frame_buttons, text="Dos Fases Minimizacion", command=min.Min)
        
        self._packing()
        gui_menu.mainloop()
    def _packing(self):
        padx_g=15
        pady_g=5
        self.btn_max.grid(row=2, column=2, padx=padx_g, pady=pady_g)
        self.btn_min.grid(row=2, column=3, padx=padx_g, pady=pady_g)
        
