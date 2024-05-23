from tkinter import Toplevel,Frame,Label, IntVar, OptionMenu, Button, StringVar, Entry, messagebox, ttk
from tkinter.constants import DISABLED
from enums import MENOR_QUE
import input
class Max:
    def __init__(self):
        self.gui_sum_menu_dim = Toplevel()
        self.input=input.ProblemInput(1,self.gui_sum_menu_dim, DISABLED, 1)
        self.foot_frame=Frame(self.gui_sum_menu_dim)
        self.foot_frame.pack()
        self.fo_aumentada=None
        Button(self.foot_frame, text="Resolver",command=self.collect_data ).grid(row=1, column=1)
    def collect_data(self):
        self.funcion_objetivo = self.input.get_fo_value()
        self.restricciones = self.input.get_restriction_values()
        self.parse_restricciones_data()
        self.parse_fo_data()
        print(self.funcion_objetivo)
        print(self.fo_aumentada)
        print(self.restricciones)
    def parse_restricciones_data(self):
        numero_restricciones=len(self.restricciones)
        lista_ordenada=[]
        for i in range(numero_restricciones):#recorre filas
           if(self.restricciones[i][-2]==MENOR_QUE):#Se seleccionara un algoritmo en base al signo
              ultimo_elemento_row=self.restricciones[i][-1]
              lista_ordenada.append([ultimo_elemento_row]+self.restricciones[i][:-2]+ self.get_variable_holgura(i, numero_restricciones))
        self.restricciones=lista_ordenada

    def parse_fo_data(self):
        
        self.fo_aumentada=self.funcion_objetivo + [0 for _ in range(len(self.restricciones))]
        
        
        
    def get_variable_holgura(self, row_number, numero_restricciones):
        fila=[]
        for i in range(numero_restricciones):
            if(row_number==i):
                fila.append(1.00)
            else:
                fila.append(0.00)
        return fila

