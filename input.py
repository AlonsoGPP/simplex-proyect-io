from tkinter import Frame,Label, Button, StringVar, Entry, messagebox, ttk

from enums import MAX, MAYOR_QUE, IGUAL, MENOR_QUE
class ProblemInput:
    """
    Tiene los datos de FO en array, restricciones en matriz
    """
    def __init__(self, type_op, wind, option_state, default_sign) -> None:
        #menu.gui_menu.withdraw()
        self.option_state=option_state
        self.gui_sum_menu_dim = wind
        self.default_sign=self.calcular_default_sign(default_sign) 
       
        #self.gui_sum_menu_dim.resizable(False, False)
        self.fo_values=[]#guarda datos
        self.fo_entries=[]#guarda entries
        self.frame_menu_sum = Frame(self.gui_sum_menu_dim, highlightbackground='red', highlightthickness=1)
        self.frame_menu_sum.pack(fill='both', expand=True, padx=5, pady=5)
        operacion = "Max =" if type_op == MAX else "Min ="
        Label(self.frame_menu_sum, text='Funcion Objetivo:', font=('arial', 10, 'bold'))\
            .grid(row=1, column=1, columnspan=1)
        self.fo_btn_add =Button(self.frame_menu_sum, text="Añadir", command=self.add_variable)
        self.fo_btn_add.grid(row=1, column=2)
        Label(self.frame_menu_sum, text=operacion).grid(row=3, column=2)
        self.agregar_campos_fo_defecto()
        self.add_panel_restricciones()
        
    def agregar_campos_fo_defecto(self):#x1 y x2
        self.fo_values.extend([StringVar(), StringVar()])
        self.fo_entries.extend([Entry(self.frame_menu_sum, textvariable=self.fo_values[0], width=6),\
                                Entry(self.frame_menu_sum, textvariable=self.fo_values[1], width=6)])
        self.columna=2
        for i in range(len(self.fo_entries)):
            
            self.columna += 1 
            self.fo_entries[i].grid(row=3, column=self.columna)
            self.columna += 1 
            Label(self.frame_menu_sum, text=f"x{i+1} + ").grid(row=3,column=self.columna)
    def add_variable(self):
        self.fo_values.append(StringVar())
        lastItem=len(self.fo_values)-1
        self.fo_entries.append(Entry(self.frame_menu_sum, textvariable=self.fo_values[lastItem], width=6))
        self.columna+=1
        self.fo_entries[lastItem].grid(row=3, column=self.columna)#imprime el ultimo elemento añadido
        self.columna+=1
        Label(self.frame_menu_sum, text=f"x{lastItem+1}+").grid(row=3,column=self.columna)
    def add_panel_restricciones(self):
        self.row_count=1
        self.restricciones_values=[]
        self.restricciones_entries=[]
        self.frame_restricciones = Frame(self.gui_sum_menu_dim, highlightbackground='red', highlightthickness=1)
        self.frame_restricciones.pack(fill='both', expand=True, padx=5, pady=5)
        title_frame = Frame(self.frame_restricciones)
        title_frame.pack()
        Label(title_frame, text="Sujeto a: ").pack()
        frame_ingreso_restriciones=Frame(self.frame_restricciones)
        frame_ingreso_restriciones.pack()
        Button(frame_ingreso_restriciones, text="Añadir", command=lambda:self.add_restriccion(frame_ingreso_restriciones)).grid(row=1, column=1)
    def add_restriccion(self, wind):
        self.fo_btn_add.config(state="disabled")
        numero_variables= len(self.fo_entries)
        
        fila_restriccion_values=[]
        fila_restriccion_entries=[]
        for i in range(numero_variables+2):#debido a que estamos agregando dos campos el combo y sa
            fila_restriccion_values.append(StringVar()) 
            if i ==numero_variables:
                fila_restriccion_values[i].set(self.default_sign)
                fila_restriccion_entries.append(ttk.Combobox(wind,textvariable=fila_restriccion_values[i], state=self.option_state,values=['<=','=','>='], width=3))
            else:
                fila_restriccion_entries.append(Entry(wind,textvariable=fila_restriccion_values[i], width=6))
            
        self.restricciones_values.append(fila_restriccion_values)#añade fila
        self.restricciones_entries.append(fila_restriccion_entries)
        self.imprimir_restriccion(wind)

    def imprimir_restriccion(self, wind):
        columna=0
        self.row_count+=1
        numero_variables= len(self.fo_entries)
        logitud_ultimo_elem=len(self.restricciones_entries[-1])
        for i in range(logitud_ultimo_elem):            
                columna+=1
                self.restricciones_entries[-1][i].grid(row=self.row_count, column=columna)
                if(i<numero_variables):
                    columna+=1
                    Label(wind, text=f"x{i+1}+").grid(row=self.row_count, column=columna)

    def get_fo_value(self):
        fo_values_parsed:list=[]
        for i in range (len(self.fo_values)):
            try:
                valor:float=float(self.fo_values[i].get())
            except Exception as e:
                messagebox.showerror(message=f"Error en ingreso de funcion Objetivo: {e}", title="Error")
                return None
            fo_values_parsed.append(valor)
        return fo_values_parsed
    def get_restriction_values(self):
        """
        Devuelve las restricciones en formato matriz
        """
        fo_restriccion_parsed=[]
        numero_restricciones = len(self.restricciones_values)
        for i in range(numero_restricciones):
            fila_value=[]
            for j in range(len(self.restricciones_values[0])):
               valor_item=self.restricciones_values[i][j].get()
               if valor_item == '<=':
                    fila_value.append(float(MENOR_QUE))
               elif valor_item == '=':
                   fila_value.append(float(IGUAL))
               elif valor_item=='>=':
                   fila_value.append(float(MAYOR_QUE))
               else:
                   try:
                       fila_value.append(float(valor_item))
                   except Exception as e:
                        messagebox.showerror(message=f"Error en conversion: {e}", title="Error")
                        return None
            fo_restriccion_parsed.append(fila_value)
        return fo_restriccion_parsed
    def calcular_default_sign(self,defaut_sign_value):
        if defaut_sign_value==MENOR_QUE:
            return "<="
        if defaut_sign_value==IGUAL:
            return "="
        if defaut_sign_value==MAYOR_QUE:
            return ">="
        return "<="
            

