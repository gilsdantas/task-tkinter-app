import sqlite3
from tkinter import ttk
from tkinter import *
import sqlite3
from tkinter.ttk import Combobox


class Producto:
    db = 'database/productos.db'

    # Constructor da classe Producto
    def __init__(self, root):
        # Creacion de la ventana principal
        self.ventana = root
        self.ventana.title("App Gestor de Produtos")  # Titulo de la ventana
        self.ventana.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        # Creacion del contenedor Frame principal
        frame = LabelFrame(
            self.ventana,
            text="Registrar un nuevo Producto",
            font=('Calibri', 16, 'bold')
        )
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(
            frame,
            text="Nombre: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre.grid(row=1, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre (caja de texto que recibira el nombre)
        self.nombre = Entry(frame, font=('Calibri', 13))  # Caja de texto (input de texto) ubicada en el frame
        self.nombre.focus()  # Para que el foco del raton vaya a este Entry al inicio
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(
            frame,
            text="Precio: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio.grid(row=2, column=0)

        # Entry Precio (caja de texto que recibira el precio)
        self.precio = Entry(frame, font=('Calibri', 13))  # Caja de texto (input de texto) ubicada en el frame
        self.precio.grid(row=2, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(
            frame,
            text="Categoria: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria.grid(row=3, column=0)

        # Combo Categoria (caja de verificación de opciones para la categoria)
        self.categoria = Combobox(
            frame,
            state='readonly',
            values=['Sin Categoria', 'Alimentación', 'Limpieza', 'Papelería', 'Otros'],
            width=18,
            font=('Calibri', 13)
        )
        self.categoria.current(0)
        self.categoria.grid(row=3, column=1)

        # Label Estoque
        self.etiqueta_estoque = Label(
            frame,
            text="Stock: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_estoque.grid(row=4, column=0)

        # Entry Estoque (caja de texto que recibira el estoque)
        self.estoque = Entry(frame, font=('Calibri', 13))  # Caja de texto (input de texto) ubicada en el frame
        self.estoque.grid(row=4, column=1)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=5, column=0, columnspan=2, sticky=W + E)

        # Boton Añadir Producto
        s = ttk.Style()
        s.configure(
            'my.TButton',
            font=('Calibri', 14, 'bold')
        )
        self.boton_aniadir = ttk.Button(
            frame,
            text="Guardar Producto",
            command=self.add_producto,
            style='my.TButton'
        )
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure(
            "mystyle.Treeview",
            highlightthickness=0,
            bd=0,
            font=('Calibri', 11)
        )  # Se modifica la fuente de la tabla
        style.configure(
            "mystyle.Treeview.Heading",
            font=('Calibri', 13, 'bold')
        )  # Se modifica la fuente de las cabeceras
        style.layout(
            "mystyle.Treeview",
            [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]
        )  # Eliminamos los bordes

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        boton_eliminar = ttk.Button(
            text='ELIMINAR',
            command=self.del_producto,
            style='my.TButton'
        )
        boton_eliminar.grid(row=7, column=0, sticky=W + E)

        boton_editar = ttk.Button(
            text='EDITAR',
            command=self.edit_producto,
            style='my.TButton'
        )
        boton_editar.grid(row=7, column=1, sticky=W + E)

        # Estructura de la tabla
        self.tabla = ttk.Treeview(
            height=20,
            style="mystyle.Treeview"
        )
        self.tabla.grid(row=6, column=0, columnspan=2)
        self.tabla['columns'] = ('nombre', 'precio', 'categoria', 'estoque')
        self.tabla.column("#0", width=0, stretch=NO)
        self.tabla.column("nombre", anchor=CENTER, width=280)
        self.tabla.column("precio", anchor=CENTER, width=80)
        self.tabla.column("categoria", anchor=CENTER, width=180)
        self.tabla.column("estoque", anchor=CENTER, width=80)
        self.tabla.heading('nombre', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('precio', text='Precio', anchor=CENTER)  # Encabezado 1
        self.tabla.heading('categoria', text='Categoria', anchor=CENTER)  # Encabezado 2
        self.tabla.heading('estoque', text='Stock', anchor=CENTER)  # Encabezado 3

        # Llamada al metodo get_productos() para obtener el listado de productos al inicio de la app
        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:  # Iniciamos una conexion con la base de datos (alias con)
            cursor = con.cursor()  # Generamos un cursor de la conexion para poder operar en la base de datos
            resultado = cursor.execute(consulta, parametros)  # Preparar la consulta SQL (con parametros si los hay)
            con.commit()  # Ejecutar la consulta SQL preparada anteriormente
        return resultado  # Retornar el resultado de la consulta SQL

    def get_productos(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children()  # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)  # Consulta SQL

        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)  # Se hace la llamada al metodo db_consultas
        # Escribir los datos en pantalla
        self.tabla.tag_configure('even_row', background='gray', foreground='white')
        self.tabla.tag_configure('odd_row', background='white', foreground='black')
        even_row = 0
        for fila in registros_db:
            print(f"Fila: {fila}")  # print para verificar por consola los datos
            self.tabla.insert(
                parent='',
                id=fila[0],
                index='end',
                text='',
                values=(fila[1], fila[2], fila[4], fila[3]),
                tags=('even_row',) if even_row % 2 == 0 else ('odd_row',)
            )
            even_row += 1

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0 and precio_introducido_por_usuario.isnumeric()

    def validacion_categoria(self):
        categoria_introducida_por_usuario = self.categoria.get()
        return len(categoria_introducida_por_usuario) != 0

    def validacion_estoque(self):
        estoque_introducido_por_usuario = self.estoque.get()
        return len(estoque_introducido_por_usuario) != 0 and estoque_introducido_por_usuario.isnumeric()

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_estoque():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)'  # Consulta SQL (sin los datos)

            # Parametros de la consulta SQL
            parametros = (
                self.nombre.get(),
                self.precio.get(),
                self.estoque.get(),
                self.categoria.get(),
            )
            self.db_consulta(query, parametros)
            # Label ubicado entre el boton y la tabla
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END)  # Borrar el campo precio del formulario
            self.categoria.delete(0, END)  # Borrar el campo categoria del formulario
            self.estoque.delete(0, END)  # Borrar el campo estoque del formulario
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_estoque() == False:
            self.mensaje['text'] = 'El estoque es obligatorio y necesita ser un numero'
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() == False and self.validacion_estoque():
            self.mensaje['text'] = 'La categoria es obligatoria'
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() == False and self.validacion_estoque() == False:
            self.mensaje['text'] = 'La categoria y estoque son obligatorios y estoque necesita ser un numero'
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() and self.validacion_estoque():
            self.mensaje['text'] = 'El precio es obligatorio y necesita ser un numero'
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() and self.validacion_estoque() == False:
            self.mensaje['text'] = 'El precio y estoque son obligatorios y necesitan ser un numero'
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() == False and self.validacion_estoque():
            self.mensaje['text'] = 'La categoria y precio son obligatorios y precio necesita ser un numero'
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() == False and self.validacion_estoque() == False:
            self.mensaje['text'] = 'La categoria y estoque y precio son obligatorios. Estoque y precio necesitan ser un numero'
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria() and self.validacion_estoque():
            self.mensaje['text'] = 'El nombre es obligatorio'
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria() and self.validacion_estoque() == False:
            self.mensaje['text'] = 'El nombre y estoque son obligatorios y estoque necesita ser un numero'
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria() == False and self.validacion_estoque():
            self.mensaje['text'] = 'La categoria y nombre son obligatorios'
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria() == False and self.validacion_estoque() == False:
            self.mensaje['text'] = 'La categoria y estoque y nombre son obligatorios. Estoque necesita ser un numero'
        elif self.validacion_nombre() == False and self.validacion_precio() == False and self.validacion_categoria() and self.validacion_estoque():
            self.mensaje['text'] = 'El nombre y precio son obligatorios y precio necesita ser un numero'
        elif self.validacion_nombre() == False and self.validacion_precio() == False and self.validacion_categoria() and self.validacion_estoque() == False:
            self.mensaje['text'] = 'El nombre y precio y estoque son obligatorios. Precio y estoque necesitan ser un numero'
        elif self.validacion_nombre() == False and self.validacion_precio() == False and self.validacion_categoria() == False and self.validacion_estoque():
            self.mensaje['text'] = 'El nombre y precio y categoria son obligatorios. Precio necesita ser un numero'
        else:
            self.mensaje['text'] = 'Todos los campos son son obligatorios. Precio y estoque necesitan ser un numero'

        # Cuando se finalice la insercion de datos volvemos a invocar a este
        # metodo para actualizar el contenido y ver los cambios
        self.get_productos()

    def del_producto(self):
        print(self.tabla.item(self.tabla.selection()))
        # Mensaje inicialmente vacio # Comprobacion de que se seleccione un producto para poder eliminarlo
        self.mensaje['text'] = ''

        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['values'][0]
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        producto_id = self.tabla.selection()[0]
        old_nombre = self.tabla.item(self.tabla.selection())['values'][0]
        old_precio = self.tabla.item(self.tabla.selection())['values'][1]
        old_estoque = self.tabla.item(self.tabla.selection())['values'][3]
        old_categoria = self.tabla.item(self.tabla.selection())['values'][2]

        # Ventana nueva (editar producto)
        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')  # Icono de la ventana

        titulo = Label(
            self.ventana_editar,
            text='Edición de Productos',
            font=('Calibri', 40, 'bold')
        )
        titulo.grid(column=0, row=0)
        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(
            self.ventana_editar,
            text="Editar el siguiente Producto",
            font=('Calibri', 16, 'bold')
        )  # frame_ep: Frame Editar Producto
        frame_ep.grid(
            row=1,
            column=0,
            columnspan=20,
            pady=20
        )

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(
            frame_ep,
            text="Nombre antiguo: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(
            frame_ep,
            textvariable=StringVar(self.ventana_editar, value=old_nombre),
            state='readonly',
            font=('Calibri', 13)
        )
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(
            frame_ep,
            text="Nombre nuevo: ",
            font=('Calibri', 13)
        )
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(
            frame_ep,
            text="Precio antiguo: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid

        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(
            frame_ep,
            textvariable=StringVar(self.ventana_editar, value=old_precio),
            state='readonly',
            font=('Calibri', 13)
        )
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(
            frame_ep,
            text="Precio nuevo: ",
            font=('Calibri', 13)
        )
        self.etiqueta_precio_nuevo.grid(row=5, column=0)

        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(
            frame_ep,
            font=('Calibri', 13)
        )
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoria antigua
        self.etiqueta_categoria_antigua = Label(
            frame_ep,
            text="Categoria antiguo: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria_antigua.grid(row=6, column=0)  # Posicionamiento a traves de grid

        # Combo Categoria antiguo (texto que no se podra modificar)
        self.input_categoria_antiguo = Entry(
            frame_ep,
            textvariable=StringVar(self.ventana_editar, value=old_categoria),
            state='readonly',
            font=('Calibri', 13)
        )
        self.input_categoria_antiguo.grid(row=6, column=1)

        # Label Categoria nuevo
        self.etiqueta_categoria_nuevo = Label(
            frame_ep,
            text="Categoria nueva: ",
            font=('Calibri', 13)
        )
        self.etiqueta_categoria_nuevo.grid(row=7, column=0)

        # Entry Categoria nuevo (texto que si se podra modificar)
        self.input_categoria_nuevo = Combobox(
            frame_ep,
            state='readonly',
            values=['Sin Categoria', 'Alimentación', 'Limpieza', 'Papelería', 'Otros'],
            width=18,
            font=('Calibri', 13)
        )
        self.input_categoria_nuevo.grid(row=7, column=1)

        # Label Estoque antiguo
        self.etiqueta_estoque_antiguo = Label(
            frame_ep,
            text="Estoque antiguo: ",
            font=('Calibri', 13)
        )  # Etiqueta de texto ubicada en el frame
        self.etiqueta_estoque_antiguo.grid(row=8, column=0)  # Posicionamiento a traves de grid

        # Entry Estoque antiguo (texto que no se podra modificar)
        self.input_estoque_antiguo = Entry(
            frame_ep,
            textvariable=StringVar(self.ventana_editar, value=old_estoque),
            state='readonly',
            font=('Calibri', 13)
        )
        self.input_estoque_antiguo.grid(row=8, column=1)

        # Label Estoque nuevo
        self.etiqueta_estoque_nuevo = Label(
            frame_ep,
            text="Estoque nuevo: ",
            font=('Calibri', 13)
        )
        self.etiqueta_estoque_nuevo.grid(row=9, column=0)

        # Entry Estoque nuevo (texto que si se podra modificar)
        self.input_estoque_nuevo = Entry(
            frame_ep,
            font=('Calibri', 13)
        )
        self.input_estoque_nuevo.grid(row=9, column=1)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(
            frame_ep,
            text="Actualizar Producto",
            style='my.TButton',
            command=lambda: self.actualizar_productos(
                producto_id,
                self.input_nombre_nuevo.get(),
                self.input_nombre_antiguo.get(),
                self.input_precio_nuevo.get(),
                self.input_precio_antiguo.get(),
                self.input_categoria_nuevo.get(),
                self.input_categoria_antiguo.get(),
                self.input_estoque_nuevo.get(),
                self.input_estoque_antiguo.get()
            )
        )

        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(
            self,
            producto_id,
            nuevo_nombre, antiguo_nombre,
            nuevo_precio, antiguo_precio,
            nueva_categoria, antigua_categoria,
            nuevo_estoque, antiguo_estoque
    ):
        producto_modificado = False
        parametros = ()
        query = f"UPDATE producto SET nombre = ?, precio = ?, estoque = ?, categoria = ? WHERE id = {producto_id}"

        # Validando todas las posibilidades de cambio
        if nuevo_nombre != '' and nuevo_precio != '' and nuevo_estoque != '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (nuevo_nombre, nuevo_precio, nuevo_estoque, nueva_categoria)
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_estoque != '' and nueva_categoria == '':
            producto_modificado = True
            parametros = (nuevo_nombre, nuevo_precio, nuevo_estoque, antigua_categoria)
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_estoque == '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (nuevo_nombre, nuevo_precio, antiguo_estoque, nueva_categoria)
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_estoque == '' and nueva_categoria == '':
            producto_modificado = True
            parametros = (nuevo_nombre, nuevo_precio, antiguo_estoque, antigua_categoria)
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_estoque != '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, nuevo_estoque, nueva_categoria)
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_estoque != '' and nueva_categoria == '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, nuevo_estoque, antigua_categoria)
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_estoque == '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, antiguo_estoque, nueva_categoria)
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_estoque == '' and nueva_categoria == '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, antiguo_estoque, antigua_categoria)
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_estoque != '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (antiguo_nombre, nuevo_precio, nuevo_estoque, nueva_categoria)
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_estoque != '' and nueva_categoria == '':
            producto_modificado = True
            parametros = (antiguo_nombre, nuevo_precio, nuevo_estoque, antigua_categoria)
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_estoque == '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (antiguo_nombre, nuevo_precio, antiguo_estoque, nueva_categoria)
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_estoque == '' and nueva_categoria == '':
            producto_modificado = True
            parametros = (antiguo_nombre, nuevo_precio, antiguo_estoque, antigua_categoria)
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_estoque != '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, nuevo_estoque, nueva_categoria)
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_estoque != '' and nueva_categoria == '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, nuevo_estoque, antigua_categoria)
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_estoque == '' and nueva_categoria != '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, antiguo_estoque, nueva_categoria)

        if producto_modificado:
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de producto
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(
                antiguo_nombre)  # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)  # Mostrar mensaje para el usuario


if __name__ == '__main__':
    root = Tk()  # Instancia de la ventana principal
    app = Producto(root)  # Se envia a la clase Producto el control sobre la ventana root
    root.mainloop()  # Comenzamos el bucle de aplicacion, es como un while True
