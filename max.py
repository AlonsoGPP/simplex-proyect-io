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
        matriz_xi=self.get_matriz_xi() 
        self.simplex_operation(self.fo_aumentada,self.restricciones,matriz_xi)
        # print(self.funcion_objetivo)
        # print(self.fo_aumentada)
        # print(self.restricciones)
        # print(self.get_matriz_xi())

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
    def get_matriz_xi(self):
        matriz_valores_xi=[]
        numero_varibles_fo = len(self.funcion_objetivo)
        fo_parte_aumentada=self.fo_aumentada[numero_varibles_fo:]
        longitud_parte_aumentada= len(fo_parte_aumentada)
        for i in range(longitud_parte_aumentada):
            matriz_valores_xi.append([fo_parte_aumentada[i], f"x{numero_varibles_fo+(i+1)}"])
        return matriz_valores_xi
    def simplex_operation(self,c_fo_extendida, cuerpo_restricciones, matriz_xi):
        
        
        while True:
            fila_z=[]
            fila_c_z=[]
            num_columns = len(cuerpo_restricciones[0])
            num_filas = len(cuerpo_restricciones)
            column_sums = [0] * num_columns
            for i in range(num_filas):
                for j in range(num_columns):
                    column_sums[j]+=cuerpo_restricciones[i][j]*matriz_xi[i][0]
            fila_z=column_sums
            fila_c_z= [c - z for c, z in zip(c_fo_extendida, fila_z[1:])]
            mayor_c_z=max(fila_c_z)
            if(mayor_c_z<=0):
                #imprime ultima tabla
                break
            columna_pivote=fila_c_z.index(mayor_c_z)+1
            columna_bj_xi=[]
            for row in cuerpo_restricciones:
                columna_bj_xi.append(row[0]/row[columna_pivote])
            positive_numbers_bj_xi = [num for num in columna_bj_xi if num > 0]
            if(positive_numbers_bj_xi==[]):
                #imprimir solucion no acotada
                break
            menor_bj_xi = min(positive_numbers_bj_xi)
            
            fila_pivote = columna_bj_xi.index(menor_bj_xi) 
            pivote_multiplo=1/cuerpo_restricciones[fila_pivote][columna_pivote]
            
            for i in range(len(cuerpo_restricciones[fila_pivote])):#esto se puede separar a una funcion
                cuerpo_restricciones[fila_pivote][i]*=pivote_multiplo
            columna_pivote_temporal=[row[columna_pivote] for row in cuerpo_restricciones]#alamacenamos ya que se volvera 0 en nuestra matriz
            for i in range(num_filas):
                if(i is not fila_pivote):
                    for j in range(num_columns):
                         cuerpo_restricciones[i][j]-=columna_pivote_temporal[i]*cuerpo_restricciones[fila_pivote][j]
            matriz_xi[fila_pivote]=[c_fo_extendida[columna_pivote-1],f'x{columna_pivote}']
        print(c_fo_extendida)
        print(cuerpo_restricciones)
        print(fila_z)
        print(matriz_xi)



        



