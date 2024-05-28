from tkinter import Toplevel,Frame,Label, IntVar, Canvas, Button, StringVar, Entry, messagebox, ttk,Scrollbar
from tkinter.constants import DISABLED,NORMAL,VERTICAL,BOTH,RIGHT,Y,LEFT,NONE
from enums import MAYOR_QUE,MENOR_QUE,IGUAL
import input
class Min:
    def __init__(self):
        self.gui_sum_menu_dim = Toplevel()
        self.gui_sum_menu_dim.title("Ingreso Problemas")
        frame = Frame(self.gui_sum_menu_dim)
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
        self.inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.input=input.ProblemInput(2,self.inner_frame,NORMAL,MAYOR_QUE)
        self.foot_frame=Frame(self.gui_sum_menu_dim)
        self.foot_frame.pack()
        self.num_fase=1
        self.c_add=0
        self.c_artificial=0
        self.cabecera=[]
        Button(self.foot_frame, text="Resolver",command=self.collect_data ).grid(row=1, column=1)
    def collect_data(self):
        self.funcion_objetivo = self.input.get_fo_value()
        self.restricciones = self.input.get_restriction_values()
        self.set_default_cabecera()
        self.parse_fo_data_cabecera()
        self.matriz_xi,self.matriz_aumentada=self.parse_restriccion()
        self.salida_resultado()
        
    def parse_restriccion(self):
        numero_restricciones=len(self.restricciones)
        restricciones_extendidas=[]
        c_add=0
        c_artifical=0
        matriz_xi=[]
        for i in range(numero_restricciones):
            ultimo_elemento_row=self.restricciones[i][-1]
            if(self.restricciones[i][-2]==MENOR_QUE):
                c_add+=1
                columna_buscar =f"S{c_add}"
                matriz_xi.append([0 ,columna_buscar])
                restricciones_extendidas.append([ultimo_elemento_row]+self.restricciones[i][:-2]+ self.row_get_values( [columna_buscar]))
            elif(self.restricciones[i][-2]==MAYOR_QUE):
                c_add+=1
                c_artifical+=1
                columna_buscar1 =f"S{c_add}"
                columa_buscar2=f"A{c_artifical}"
                matriz_xi.append([1 ,columa_buscar2])
                restricciones_extendidas.append([ultimo_elemento_row]+self.restricciones[i][:-2]+ self.row_get_values( [columna_buscar1, columa_buscar2]))
            elif(self.restricciones[i][-2]==IGUAL):
                c_artifical+=1
                columna_buscar=f"A{c_artifical}"
                matriz_xi.append([1 ,columna_buscar])
                restricciones_extendidas.append([ultimo_elemento_row]+self.restricciones[i][:-2]+ self.row_get_values( [columna_buscar]))
        self.c_add=c_add
        self.c_artificial=c_artifical
        return matriz_xi,restricciones_extendidas
    def row_get_values(self,array_busqueda):#calcula el aumento a las restricciones originales
        longitu_fo_original=len(self.funcion_objetivo)
        longitud_fo_aumentada=len(self.cabecera)-longitu_fo_original
        row_extra_value=[0 for _ in range(longitud_fo_aumentada)]
        parte_aumenta=self.cabecera[longitu_fo_original:]
        #se podria validar 
        for item in array_busqueda:
            for i in range(longitud_fo_aumentada):
                if(parte_aumenta[i][1]==item):
                    if(len(array_busqueda)==2):
                        if item[0]=="S":
                            row_extra_value[i]=-1
                        else:#caso artificial
                            row_extra_value[i]=1
                    else:
                        row_extra_value[i]=1
        return row_extra_value
        
        
    def set_default_cabecera(self):
        for i in range(len(self.funcion_objetivo)):
            self.cabecera.append([0, f"X{i+1}"])
    def set_segunda_fase_cabecera(self):
        segunda_cabecera=[]
        for i in range(len(self.funcion_objetivo)):
            segunda_cabecera.append([self.funcion_objetivo[i], f"X{i+1}"])
        for i in range(self.c_add):
            segunda_cabecera.append([0,f"S{i+1}"])
        return segunda_cabecera
    def parse_fo_data_cabecera(self):#genera la cabecera
        c_olgura=0
        c_artificial=0
        for i in range(len(self.restricciones)):
            if(self.restricciones[i][-2]==MENOR_QUE):
                 c_olgura+=1
                 self.cabecera.append([0,f"S{c_olgura}"])
            elif(self.restricciones[i][-2] == MAYOR_QUE):
                c_olgura+=1
                self.cabecera.append([0,f"S{c_olgura}"])
                c_artificial+=1
            else:
                c_artificial+=1
        for i in range(c_artificial):
            self.cabecera.append([1,f"A{i+1}"])
        print(self.cabecera)
    def salida_resultado(self):
        self.salida_raw=Toplevel()
        self.salida_raw.title("Ventana Toplevel")
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
        self.simplex_operation(self.salida,self.cabecera,self.matriz_aumentada,self.matriz_xi)

    def formatear_numero(self,numero) -> str:
        if isinstance(numero, float):
            return "{:.2f}".format(numero)
        elif isinstance(numero, int):
            return str(numero)
        elif isinstance(numero, str):
            return numero
        else:
            return str(numero) 
        
    def simplex_operation(self,wind,cabecera, cuerpo_restricciones, matriz_xi):
        while True:
            fila_z=[]
            fila_c_z=[]
            columna_bj_xi=[]
            fila_pivote=None
            columna_pivote=None
            num_columns = len(cuerpo_restricciones[0])
            num_filas = len(cuerpo_restricciones)
            column_sums = [0] * num_columns
            for i in range(num_filas): #se multiplica para hallar z
                for j in range(num_columns):
                    column_sums[j]+=cuerpo_restricciones[i][j]*matriz_xi[i][0]
            fila_z=column_sums
            fila_c_z= [c[0] - z for c, z in zip(cabecera, fila_z[1:])]
            
            min_c_z=min(fila_c_z)
            if(min_c_z>=0):
                #imprime ultima tabla
                self.write_table(wind, cabecera, cuerpo_restricciones,matriz_xi, fila_z,fila_c_z,[ [item] for item in columna_bj_xi if item is not None],fila_pivote,columna_pivote)
                self.num_fase+=1
                if self.num_fase == 2:
                    self.segunda_fase(cuerpo_restricciones, matriz_xi)
                break
            columna_pivote=fila_c_z.index(min_c_z)+1
            
            for row in cuerpo_restricciones:
                if(row[columna_pivote]==0):#para evitar la divicion entre cero
                    row[columna_pivote]=-1
                columna_bj_xi.append(row[0]/row[columna_pivote])
            positive_numbers_bj_xi = [num for num in columna_bj_xi if num >= 0]
            if(positive_numbers_bj_xi==[]):
                #imprimir solucion no acotada
                messagebox.showinfo(message="Solucion no acotada", title="Sin solucion")
                wind.destroy()
                break
            menor_bj_xi = min(positive_numbers_bj_xi)
            
            fila_pivote = columna_bj_xi.index(menor_bj_xi) 
            pivote_multiplo=1/cuerpo_restricciones[fila_pivote][columna_pivote]

            self.write_table(wind, cabecera, cuerpo_restricciones,matriz_xi, fila_z,fila_c_z,[ [item] for item in columna_bj_xi],fila_pivote,columna_pivote)

            for i in range(len(cuerpo_restricciones[fila_pivote])):#esto se puede separar a una funcion/vuelve uni al pivote
                cuerpo_restricciones[fila_pivote][i]*=pivote_multiplo
            columna_pivote_temporal=[row[columna_pivote] for row in cuerpo_restricciones]#alamacenamos ya que se volvera 0 en nuestra matriz
            for i in range(num_filas):
                if(i is not fila_pivote):
                    for j in range(num_columns):#vuelve 0 las los elementos de la columan que no son pivote
                        cuerpo_restricciones[i][j]-=columna_pivote_temporal[i]*cuerpo_restricciones[fila_pivote][j]
            
            #matriz_xi[fila_pivote]=[c_fo_cabecera[columna_pivote-1],f'x{columna_pivote}']
            matriz_xi[fila_pivote]=cabecera[columna_pivote-1]

    def write_table(self,wind,cabecera,cuerpo_restricciones,matriz_xi, fila_z,fila_c_z,columna_bj_xi,fila_pivote,columna_pivote):
        frame_salida = Frame(wind)
        ancho=7
        frame_salida.pack(fill='both', expand=True, padx=5, pady=5)
        c_columnas=0
        if(columna_bj_xi ==[]):
            union_xi_cuerpo=[sub_a + sub_b  for sub_a, sub_b in zip(matriz_xi, cuerpo_restricciones)]
        else:
            union_xi_cuerpo=[sub_a + sub_b + sub_c for sub_a, sub_b, sub_c in zip(matriz_xi, cuerpo_restricciones,columna_bj_xi)]
        for i in range(3):
            Label(frame_salida, width=ancho).grid(row=1, column=i)
            Label(frame_salida, width=ancho).grid(row=2, column=i)
            c_columnas+=1
        for i,item in enumerate(cabecera):
            Label(frame_salida,text=item[0],highlightbackground='black',highlightthickness=1, width=ancho).grid(row=1, column=c_columnas+i)
            Label(frame_salida,text=item[1],highlightbackground='black',highlightthickness=1, width=ancho).grid(row=2, column=c_columnas+i)
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
    def segunda_fase(self,cuerpo_restricciones, matriz_xi):
        cabecera_fase_2=self.set_segunda_fase_cabecera();      
        cuerpo_segunda_fase=[]
        new_matriz_xi=[]
        for row in cuerpo_restricciones:
            cuerpo_segunda_fase.append(row[:-self.c_artificial]) 
        for row in matriz_xi:
            variable = row[1]
            for item in cabecera_fase_2:
                if(item[1]==variable):
                    new_matriz_xi.append([item[0],variable])
        self.simplex_operation(self.salida,cabecera_fase_2,cuerpo_segunda_fase,new_matriz_xi)