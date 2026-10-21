import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from cliente import Cliente
from cliente_dao import ClienteDAO


class App(tk.Tk):
    COLOR_VENTANA = '#1d2d44'
    def __init__(self):
        super().__init__()
        self.id_cliente = None
        self.configurar_ventana()
        self.configurar_grid()
        self.mostrar_titulo()
        self.mostrar_formulario()
        self.cargar_tabla()
        self.mostrar_botones()

    def configurar_ventana(self):
        self.geometry('900x600')
        self.title('Zona Fit App')
        self.configure(background=App.COLOR_VENTANA)
        #aplicamos el estilo
        self.estilos = ttk.Style()
        self.estilos.theme_use('clam')
        self.estilos.configure(self, background=App.COLOR_VENTANA, foreground= 'white'
                               ,fieldbackground = 'black')

    def configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def mostrar_titulo(self):
        etiqueta = ttk.Label(self, text='Zona Fit GYM', font=('Arial', 20),
                             background=App.COLOR_VENTANA, foreground='white')
        etiqueta.grid(row=0, column=0, columnspan=2, pady=30)

    def mostrar_formulario(self):
        self.frame_forma = tk.Frame(self, background=App.COLOR_VENTANA)

        #Nombre
        nombre_l = ttk.Label(self.frame_forma, text='Nombre: ')
        nombre_l.grid(row=0, column=0, sticky=tk.W, pady=30, padx=30)
        self.nombre_t = ttk.Entry(self.frame_forma)
        self.nombre_t.grid(row=0, column=1)

        #Apellido
        apellido_l = ttk.Label(self.frame_forma, text='Apellido: ')
        apellido_l.grid(row=1, column=0, sticky=tk.W, pady=30, padx=30)
        self.apellido_t = ttk.Entry(self.frame_forma)
        self.apellido_t.grid(row=1, column=1)

        #Membresia
        membresia_l = ttk.Label(self.frame_forma, text='Membresia: ')
        membresia_l.grid(row=2, column=0, sticky=tk.W, pady=30, padx=30)
        self.membresia_t = ttk.Entry(self.frame_forma)
        self.membresia_t.grid(row=2, column=1)


        #publicar el frame del formulario
        self.frame_forma.grid(row=1, column=0)

    def cargar_tabla(self):
        #crear un frame para mostrar la tabla
        self.frame_tabla = ttk.Frame(self)
        #Definimos los estilos de la tabla
        self.estilos.configure('Treeview', background='black', foreground='white',
                               fielbackground='black', rowheight = 20)
        #DEFINIMOS LAS COLUMNAS
        columnas = ('Id', 'Nombre', 'Apellido', 'Membresia')
        #creamos el objeto tabla
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show='headings')

        #agregamos los cabeceros
        self.tabla.heading('Id', text='Id', anchor=tk.CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tabla.heading('Apellido', text='Apellido', anchor=tk.W)
        self.tabla.heading('Membresia', text='Membresia', anchor=tk.W)

        #Definir las columans
        self.tabla.column('Id', anchor=tk.CENTER, width=50)
        self.tabla.column('Nombre', anchor=tk.W, width=100)
        self.tabla.column('Apellido', anchor=tk.W, width=100)
        self.tabla.column('Membresia', anchor=tk.W, width=100)

        #Cargamos los datos de ña BD
        clientes = ClienteDAO.seleccionar()
        for cliente in clientes:
            self.tabla.insert(parent='', index=tk.END,
                              values=(cliente.id, cliente.nombre,
                                      cliente.apellido, cliente.membresia))

        #Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL,
                                  command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        #asociar el evento select
        self.tabla.bind('<<TreeviewSelect>>', self.cargar_cliente)
        #capturamos el valor de la tabla que se seleccione

        #publicamos la tabla
        self.tabla.grid(row=0, column=0)

        #mostramos el frame de tabla
        self.frame_tabla.grid(row=1, column=1, padx=20)

    def mostrar_botones(self):
        self.frame_botones = ttk.Frame()
        #crear los botones
        #boton de agregar
        agregar_boton = ttk.Button(self.frame_botones, text='Guardar',
                                   command= self.validar_cliente)
        agregar_boton.grid(row=0, column=0, padx=30)

        #boton de eliminar
        eliminar_boton = ttk.Button(self.frame_botones, text='Eliminar',
                                    command = self.eliminar_cliente)
        eliminar_boton.grid(row=0, column=1, padx=30)

        #boton de limpiar
        limpar_boton = ttk.Button(self.frame_botones, text='Limpar',
                                  command = self.limpiar_datos)
        limpar_boton.grid(row=0, column=2, padx=30)

        #aplicar estilos a los botones
        self.estilos.configure('TButton', background='#005f73')
        self.estilos.map('TButton', background=[('active', '#0a9396')])

        #Publicamos el frame de botones
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=20)

    def validar_cliente(self):
        #validar cliente
        if(self.nombre_t.get() and self.apellido_t.get() and self.membresia_t.get()):
            if self.validar_membresia():
                self.guardar_cliente()
            else:
                showerror(title='ATENCION', message='El valor de membresia NO es numerico ')
                self.membresia_t.delete(0, tk.END) #se limpia desde el caracter 0 hasta el ultimo
                self.membresia_t.focus_set() #poner el cursor en el campo de membresia

        else:
            showerror(title='ATENCION', message='Debe llenar el formulario')
            self.membresia_t.focus_set()

    def validar_membresia(self):
        try:
            int(self.membresia_t.get())
            return True
        except:
            return False

    def guardar_cliente(self):
        #recuperar los valores de las cajad de texto
        nombre= self.nombre_t.get()
        apellido= self.apellido_t.get()
        membresia= self.membresia_t.get()
        #Validamos el valor del self.id_cliente
        if self.id_cliente is None:
            cliente = Cliente(nombre= nombre, apellido=apellido, membresia=membresia)
            ClienteDAO.insertar(cliente)
            showinfo(title='Agregar', message='Cliente guardado correctamente')
        else: #Actualizar
            cliente = Cliente(self.id_cliente, nombre, apellido, membresia)
            ClienteDAO.actualizar(cliente)
            showinfo(title='Actualizar', message='Cliente actualizado correctamente')
        #Volvemos a mostrar los datos y limpiamos el formulario
        self.recargar_datos()

    def cargar_cliente(self, event):
        elemento_seleccionado = self.tabla.selection()[0]
        elemento = self.tabla.item(elemento_seleccionado)
        cliente_t = elemento['values']
        #recueprar cada valor del cliente
        self.id_cliente =cliente_t[0]
        nombre= cliente_t[1]
        apellido= cliente_t[2]
        membresia= cliente_t[3]
        #antes de cargar limpiamos el formulario
        self.limpiar_formulario()
        #ahora cargamos los valores
        self.nombre_t.insert(0, nombre)
        self.apellido_t.insert(0, apellido)
        self.membresia_t.insert(0, membresia)

    def recargar_datos(self):
        #volver a cargar los datos de la tabla
        self.cargar_tabla()
        #Limpiar los datos
        self.limpiar_datos()

    def eliminar_cliente(self):
        if self.id_cliente is None:
            showerror(title='ATENCION', message='Debe seleccionar el cliente a eliminar')
        else:
            cliente = Cliente(id=self.id_cliente)
            ClienteDAO.eliminar(cliente)
            showinfo(title='Eliminado', message='Cliente eliminado correctamente')
            self.recargar_datos()

    def limpiar_datos(self):
        self.limpiar_formulario()
        self.id_cliente = None

    def limpiar_formulario(self):
        self.nombre_t.delete(0, tk.END)
        self.apellido_t.delete(0, tk.END)
        self.membresia_t.delete(0, tk.END)

if __name__ == '__main__':
    app = App()
    app.mainloop()