from tkinter import Toplevel,Frame,Label, IntVar, Scrollbar,Canvas, Button, StringVar, Entry, messagebox, ttk
from tkinter.constants import DISABLED,NORMAL,VERTICAL,BOTH,RIGHT,Y,LEFT,NONE
from enums import MAYOR_QUE,MENOR_QUE,IGUAL
import input
class Max:
    def __init__(self):
        self.gui_sum_menu_dim = Toplevel()
        self.input=input.ProblemInput(1,self.gui_sum_menu_dim, DISABLED, MENOR_QUE)
        self.foot_frame=Frame(self.gui_sum_menu_dim)
        self.foot_frame.pack()
        self.fo_aumentada=None
        Button(self.foot_frame, text="Resolver",command=self.collect_data ).grid(row=1, column=1)
    def collect_data(self):
        self.funcion_objetivo = self.input.get_fo_value()
        self.restricciones = self.input.get_restriction_values()
        self.parse_restricciones_data()
        self.parse_fo_data()
        self.matriz_xi=self.get_matriz_xi() 
        self.salida_resultado()

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
    def salida_resultado(self):
        self.salida_raw=Toplevel()

        self.salida_raw.title("Ventana Resultado")
        self.salida_raw.geometry("1000x700")
        frame = Frame(self.salida_raw)
        frame.pack(fill=BOTH, expand=True)
        
         # Crear el Canvas
        canvas = Canvas(frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
         # Crear la scrollbar vertical
        scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configurar el Canvas para que use la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.salida = Frame(canvas)
        canvas.create_window((0, 0), window=self.salida, anchor="nw")



        self.frame_menu_sum = Frame(self.salida, highlightbackground='red', highlightthickness=1)
        self.frame_menu_sum.pack(fill='both', expand=True, padx=5, pady=5)
        Label(self.frame_menu_sum, text="Resultado :", font=('arial', 10, 'bold')).pack()
        self.simplex_operation(self.salida,self.fo_aumentada, self.restricciones,self.matriz_xi)
        #self.write_table(self.salida,self.fo_aumentada, self.restricciones,self.matriz_xi)

    def write_table(self,wind, c_fo_extendida,cuerpo_restricciones,matriz_xi, fila_z,fila_c_z,columna_bj_xi,fila_pivote,columna_pivote,c_iteration):
        frame_salida = Frame(wind)
        ancho=7
        frame_salida.pack(fill='both', expand=True, padx=5, pady=5)
        c_columnas=0
        if(columna_bj_xi ==[]):
            union_xi_cuerpo=[sub_a + sub_b  for sub_a, sub_b in zip(matriz_xi, cuerpo_restricciones)]
        else:
            union_xi_cuerpo=[sub_a + sub_b + sub_c for sub_a, sub_b, sub_c in zip(matriz_xi, cuerpo_restricciones,columna_bj_xi)]
 
        Label(frame_salida,text="Iteracion", width=ancho).grid(row=1, column=0)
        Label(frame_salida,text="Xi",highlightbackground='black',highlightthickness=1, width=ancho).grid(row=2, column=1)
        Label(frame_salida,text=f"{c_iteration}", width=ancho).grid(row=1, column=1)
        Label(frame_salida,text="C",highlightbackground='black',highlightthickness=1, width=ancho).grid(row=1, column=2)
        Label(frame_salida,text="", width=ancho).grid(row=2, column=2)
        c_columnas+=3
        for i in range(len(c_fo_extendida)):
            Label(frame_salida,text=c_fo_extendida[i],highlightbackground='black',highlightthickness=1, width=ancho).grid(row=1, column=c_columnas+i)
            Label(frame_salida,text=f"x{i+1}",highlightbackground='black',highlightthickness=1, width=ancho).grid(row=2, column=c_columnas+i)
        row_count=3
        for i in range(len(union_xi_cuerpo)):
            for j in range(len(union_xi_cuerpo[0])):
                if(i==fila_pivote and j == columna_pivote+2):
                    color="red"
                else:
                    color="white"
                Label(frame_salida,text=self.formatear_numero(union_xi_cuerpo[i][j]),highlightbackground='black',highlightthickness=1,background=color, width=ancho).grid(row=3+i, column=j)
            row_count+=1
        for i in range(len(fila_z)):
            Label(frame_salida,text=self.formatear_numero(fila_z[i]),highlightbackground='black',highlightthickness=1, width=ancho).grid(row=row_count, column=i+2)
        row_count+=1
        for i in range(len(fila_c_z)):
            Label(frame_salida,text=self.formatear_numero(fila_c_z[i]),highlightbackground='black',highlightthickness=1, width=ancho).grid(row=row_count, column=i+3)

    def formatear_numero(self,numero) -> str:
        if isinstance(numero, float):
            return "{:.2f}".format(numero)
        elif isinstance(numero, int):
            return str(numero)
        elif isinstance(numero, str):
            return numero
        else:
            return str(numero) 
    def simplex_operation(self,wind,c_fo_extendida, cuerpo_restricciones, matriz_xi):
        c_iteration=0
        while True:
            fila_pivote=None
            columna_pivote=None
            fila_z=[]
            fila_c_z=[]
            columna_bj_xi=[]
            c_iteration+=1
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
                self.write_table(wind,c_fo_extendida, cuerpo_restricciones,matriz_xi, fila_z,fila_c_z,[ [item] for item in columna_bj_xi if item is not None],fila_pivote,columna_pivote,c_iteration)
                break
            columna_pivote=fila_c_z.index(mayor_c_z)+1
            
            for row in cuerpo_restricciones:
                if(row[columna_pivote]==0):
                    row[columna_pivote]=-1
                columna_bj_xi.append(row[0]/row[columna_pivote])
            positive_numbers_bj_xi = [num for num in columna_bj_xi if num > 0]
            if(positive_numbers_bj_xi==[]):
                #imprimir solucion no acotada
                messagebox.showinfo(message="Solucion no acotada", title="Sin solucion")
                wind.destroy()
                break
            menor_bj_xi = min(positive_numbers_bj_xi)
            
            fila_pivote = columna_bj_xi.index(menor_bj_xi) 
            pivote_multiplo=1/cuerpo_restricciones[fila_pivote][columna_pivote]

            self.write_table(wind,c_fo_extendida, cuerpo_restricciones,matriz_xi, fila_z,fila_c_z,[ [item] for item in columna_bj_xi],fila_pivote,columna_pivote,c_iteration)

            for i in range(len(cuerpo_restricciones[fila_pivote])):#esto se puede separar a una funcion
                cuerpo_restricciones[fila_pivote][i]*=pivote_multiplo
            columna_pivote_temporal=[row[columna_pivote] for row in cuerpo_restricciones]#alamacenamos ya que se volvera 0 en nuestra matriz
            for i in range(num_filas):
                if(i is not fila_pivote):
                    for j in range(num_columns):
                         cuerpo_restricciones[i][j]-=columna_pivote_temporal[i]*cuerpo_restricciones[fila_pivote][j]
            
            matriz_xi[fila_pivote]=[c_fo_extendida[columna_pivote-1],f'x{columna_pivote}']
 