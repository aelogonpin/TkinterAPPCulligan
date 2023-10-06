import tkinter as tk
from tkinter import Toplevel, ttk
import sqlite3
from tkinter import messagebox
import tkinter.simpledialog
from tkinter.tix import NoteBook
import webbrowser
from tkinter.simpledialog import askstring

# Definir los rangos de ID para cada zona
rango_ids = {
    "Canarias": range(6001, 6100),
    "Murcia/Alicante": range(6101, 6200),
    "Sevilla/Huelva/Jerez/Cordoba": range(6201, 6300),
    "Malaga/Almeria/Granada": range(6301, 6400),
    "Badajoz": range(6401, 6500),
    "Madrid/Valladolid": range(6501, 6600),
    "Barcelona": range(6601, 6700),
    "Asturias/Galicia/Bilbao/San Sebastian": range(6701, 6800),
    "Zaragoza": range(6801, 6900),
    "Valencia/Mallorca": range(6901, 7000)
}





lista = None
entry_busqueda = None 


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de codigos Actiwhere BY IPnotics💻 ")
ventana.iconbitmap("icono.ico")
ventana.geometry("1366x768")

# Frame principal para la interfaz
frame_principal = tk.Frame(ventana)
frame_principal.pack(fill="both", expand=True)

# Frame para la tabla y scrollbar
frame_tabla = tk.Frame(frame_principal)
frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)



# Frame para la tabla
frame_tabla = tk.Frame(frame_tabla)
frame_tabla.pack(side=tk.LEFT, fill="both", expand=False)




def editar_campo(event):
    item_seleccionado = tabla.selection()
    if item_seleccionado:
        # Obtener la columna seleccionada mediante la ventana de selección
        columnas_seleccionadas = seleccionar_columnas()

        # Si no se selecciona ninguna o se seleccionan más de una columna, mostrar mensaje de reintentar
        if not columnas_seleccionadas or len(columnas_seleccionadas) != 1:
            respuesta = tkinter.messagebox.askretrycancel("Error", "Por favor, seleccione una columna para editar.")
            if not respuesta:
                return  # Si se elige "Cancelar", salir
        
        columna_seleccionada = columnas_seleccionadas[0]

        # Obtener el índice de la columna seleccionada
        indice_columna = tabla["columns"].index(columna_seleccionada)

        # Obtener el valor actual en la columna seleccionada
        valor_actual = tabla.item(item_seleccionado, "values")[indice_columna]

        # Crear una ventana de diálogo para editar el campo
        dialog = tkinter.Toplevel()
        dialog.title(f"Editar {columna_seleccionada}")

        # Entrada de texto para el nuevo valor
        nuevo_valor_var = tkinter.StringVar(value=valor_actual)
        nuevo_valor_entry = tkinter.Entry(dialog, textvariable=nuevo_valor_var)
        nuevo_valor_entry.pack()

        # Función para aplicar los cambios
        def aplicar_cambios():
            nuevo_valor_texto = nuevo_valor_var.get()
            
            # Actualizar los valores en la tabla
            nuevos_valores = list(tabla.item(item_seleccionado, "values"))
            nuevos_valores[indice_columna] = nuevo_valor_texto
            tabla.item(item_seleccionado, values=tuple(nuevos_valores))

            # Cerrar la ventana de diálogo
            dialog.destroy()

        # Botón para aplicar los cambios
        aplicar_button = tkinter.Button(dialog, text="Aplicar Cambios", command=aplicar_cambios)
        aplicar_button.pack()

        # Entrar en modo edición al abrir la ventana de diálogo
        nuevo_valor_entry.focus_set()
    else:
        tkinter.messagebox.showinfo("Información", "Por favor, seleccione un usuario para editar el campo.")

def seleccionar_columnas():
    # Crear una ventana de selección de columna
    ventana_seleccion = tkinter.Toplevel()
    ventana_seleccion.title("Seleccionar Columnas")

    # Variables para almacenar las columnas seleccionadas
    columnas_seleccionadas = []

    # Función para aplicar la selección
    def aplicar_seleccion():
        for columna, var in checkboxes.items():
            if var.get():
                columnas_seleccionadas.append(columna)
        ventana_seleccion.destroy()

    # Crear checkboxes para cada columna posible
    checkboxes = {}
    columnas_posibles = ["Nombre", "Zona", "ID", "Descripción"]

    for columna in columnas_posibles:
        var = tkinter.IntVar()
        checkbox = tkinter.Checkbutton(ventana_seleccion, text=columna, variable=var)
        checkbox.pack()
        checkboxes[columna] = var

    # Botón para aplicar la selección
    boton_aplicar = tkinter.Button(ventana_seleccion, text="Aplicar Selección", command=aplicar_seleccion)
    boton_aplicar.pack()

    ventana_seleccion.wait_window()

    return columnas_seleccionadas









# Crear una tabla para mostrar los datos de la zona seleccionada
tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Zona", "Descripción"))
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Descripción", text="Descripción")
tabla.heading("Zona", text="Zona")
tabla.bind("<<TreeviewDoubleClick>>", editar_campo)
tabla.bind("<Double-1>", editar_campo)
tabla.pack(fill="both", expand=True)


tabla.column("#0", width=0, stretch=tk.NO ) 
tabla.column("#1", width=100, stretch=tk.NO) 
tabla.column("#2", width=250, stretch=tk.YES) 
tabla.column("#3", width=200, stretch=tk.NO) 
tabla.column("#4", width=200, stretch=tk.NO) 




# Frame para los botones
frame_botones = tk.Frame(frame_principal)
frame_botones.pack(side=tk.RIGHT, fill=tk.Y, expand=True)













# Botón para mostrar información del usuario
def mostrar_informacion_usuario():
    # Código para mostrar información del usuario

 # Obtener la selección actual en la tabla
    seleccion = tabla.selection()

    # Verificar si se ha seleccionado una fila
    if seleccion:
        # Obtener el ID y el nombre del usuario seleccionado
        id_seleccionada = tabla.item(seleccion)['values'][0]
        nombre_seleccionado = tabla.item(seleccion)['values'][1]

        # Crear la cadena de información
        informacion = f"{id_seleccionada}-{nombre_seleccionado}"

        # Crear una nueva ventana para mostrar la información
        ventana_info = tk.Toplevel(ventana)
        ventana_info.title("Información del Usuario")
        ventana_info.iconbitmap("icono.ico")

        # Crear un widget Text para mostrar la información
        texto_info = tk.Text(ventana_info, wrap=tk.WORD, height=3, width=80)
        texto_info.insert(tk.END, informacion)
        texto_info.pack(padx=10, pady=10)

        # Función para copiar el texto al portapapeles
        def copiar_texto():
            ventana.clipboard_clear()
            ventana.clipboard_append(informacion)
            ventana.update()

      

    else:
        tkinter.messagebox.showinfo("Información", "Por favor, seleccione un usuario para ver la información.")



# Botón para editar un usuario
def editar_usuario():
  
    # Obtener la selección actual en la tabla
    seleccion = tabla.selection()

    # Verificar si se ha seleccionado una fila
    if seleccion:
        # Obtener el ID del usuario seleccionado
        id_seleccionada = tabla.item(seleccion)['values'][0]

        # Obtener la zona seleccionada
        zona_seleccionada = zona_combo.get()

        # Conectar a la base de datos (o crearla si no existe)
        conexion = sqlite3.connect('basededatos.db')
        cursor = conexion.cursor()

        # Obtener los datos del usuario seleccionado
        cursor.execute('SELECT nombre FROM personas WHERE zona = ? AND id = ?', (zona_seleccionada, id_seleccionada))
        nombre_actual = cursor.fetchone()[0]

        # Mostrar un cuadro de diálogo para editar el nombre y/o la ID
        nuevo_nombre = tkinter.simpledialog.askstring("Editar Usuario", "Nuevo Nombre:", initialvalue=nombre_actual)
        if nuevo_nombre is None:
            # Cancelar la edición si se presiona "Cancelar" en el cuadro de diálogo
            conexion.close()
            return

        nuevo_id = tkinter.simpledialog.askinteger("Editar Usuario", "Nueva ID:", initialvalue=id_seleccionada)
        if nuevo_id is None:
            # Cancelar la edición si se presiona "Cancelar" en el cuadro de diálogo
            conexion.close()
            return

        # Actualizar el nombre y/o la ID en la base de datos
        cursor.execute('UPDATE personas SET nombre = ?, id = ? WHERE zona = ? AND id = ?',
                       (nuevo_nombre, nuevo_id, zona_seleccionada, id_seleccionada))
        conexion.commit()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Llamar a cargar_datos() para actualizar la tabla y el Combobox de IDs
        cargar_datos()
    else:
        tkinter.messagebox.showinfo("Información", "Por favor, seleccione un usuario para editar.")


# Botón para agregar un usuario
def agregar_usuario():
    # Código para agregar un usuario
    # Obtener los valores seleccionados
    nombre = nombre_entry.get()
    zona = zona_combo.get()
    id_seleccionada = id_combo.get()
    descripcion = descripcion_entry.get()  # Obtener la descripción

    # Verificar si la ID seleccionada está dentro del rango de la zona seleccionada
    rango = rango_ids[zona]
    if int(id_seleccionada) not in rango:
        tkinter.messagebox.showerror("Error", "La ID seleccionada no está dentro del rango para la zona seleccionada.")
        return

    # Conectar a la base de datos (o crearla si no existe)
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Verificar si la ID seleccionada ya está en uso
    cursor.execute('SELECT id FROM personas WHERE zona = ? AND id = ?', (zona, id_seleccionada))
    resultado = cursor.fetchone()

    if resultado:
        mensaje_error = f"La ID {id_seleccionada} ya está en uso para la zona seleccionada."
        tkinter.messagebox.showerror("Error", mensaje_error)
        conexion.close()
        return

    try:
        # Insertar el nuevo usuario en la base de datos, incluyendo la descripción
        cursor.execute('INSERT INTO personas (nombre, zona, id, descripcion) VALUES (?, ?, ?, ?)',
                       (nombre, zona, id_seleccionada, descripcion))
        conexion.commit()

        # Mostrar un mensaje de éxito
        tkinter.messagebox.showinfo("Éxito", "Usuario creado.")

        # Llamar a la función cargar_datos para actualizar la tabla
        cargar_datos()

    except Exception as e:
        # En caso de error, mostrar un mensaje de error
        tkinter.messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}")

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Limpiar los campos después de agregar el usuario
    nombre_entry.delete(0, tk.END)
    id_combo.set('')
    descripcion_entry.delete(0, tk.END)  # Limpiar la entrada de descripción


# Botón para eliminar un usuario
def eliminar_usuario():
    # Código para eliminar un usuario
    # Obtener la selección actual en la tabla
    seleccion = tabla.selection()

    # Verificar si se ha seleccionado una fila
    if seleccion:
        # Obtener el ID del usuario seleccionado
        id_seleccionada = tabla.item(seleccion)['values'][0]

        # Obtener la zona seleccionada
        zona_seleccionada = zona_combo.get()

        # Conectar a la base de datos (o crearla si no existe)
        conexion = sqlite3.connect('basededatos.db')
        cursor = conexion.cursor()

        # Eliminar el usuario de la base de datos
        cursor.execute('DELETE FROM personas WHERE zona = ? AND id = ?', (zona_seleccionada, id_seleccionada))
        conexion.commit()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Llamar a cargar_datos() para actualizar la tabla y el Combobox de IDs
        cargar_datos()
    else:
        tkinter.messagebox.showinfo("Información", "Por favor, seleccione un usuario para eliminar.")





# Frame para otros elementos (etiquetas, campos de entrada, Combobox, etc.)
frame_elementos = tk.Frame(frame_principal)
frame_elementos.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

# Crear un Combobox para seleccionar la zona
nombre_combo = tk.Label(frame_elementos, text="Zonas")
nombre_combo.pack(padx=5, pady=10)

zonas = ["Canarias", "Murcia/Alicante", "Sevilla/Huelva/Jerez/Cordoba", "Malaga/Almeria/Granada", "Badajoz",
         "Madrid/Valladolid", "Barcelona", "Asturias/Galicia/Bilbao/San Sebastian", "Zaragoza", "Valencia/Mallorca"]
zona_combo = ttk.Combobox(frame_elementos, values=zonas)
zona_combo.pack(padx=5, pady=5)

# Etiqueta para el campo de IDs
id_label = tk.Label(frame_elementos, text="Identificador:")
id_label.pack(padx=(10, 0), pady=5)

# Combobox para seleccionar la ID dentro del rango correspondiente a la zona seleccionada
id_combo = ttk.Combobox(frame_elementos)
id_combo.pack(padx=(0, 10), pady=5)

# Etiqueta para el campo de Nombre
nombre_label = tk.Label(frame_elementos, text="Nombre:")
nombre_label.pack(padx=(10, 0), pady=5)

# Campo de entrada para el Nombre
nombre_entry = tk.Entry(frame_elementos)
nombre_entry.pack(padx=(0, 10), pady=5)

# Etiqueta para el campo de Descripción
descripcion_label = tk.Label(frame_elementos, text="Descripción:")
descripcion_label.pack(padx=(10, 0), pady=5)

# Campo de entrada para la descripción
descripcion_entry = tk.Entry(frame_elementos)
descripcion_entry.pack(padx=(0, 10), pady=5)

# Espaciador para separar los campos de entrada y los botones
espaciador = tk.Label(frame_elementos, text="")
espaciador.pack(pady=10)


# Botón para copiar informacion de nomreb + ID
boton_agregar = tk.Button(frame_elementos, text="Copiar informacion fusionada", command=mostrar_informacion_usuario)
boton_agregar.pack(pady=5)
# Botón para agregar un usuario
boton_agregar = tk.Button(frame_elementos, text="Agregar Usuario", command=agregar_usuario)
boton_agregar.pack(pady=5)

# Botón para editar un usuario
boton_editar = tk.Button(frame_elementos, text="Editar Usuario", command=editar_usuario)
boton_editar.pack(pady=5)

# Botón para eliminar un usuario
boton_eliminar = tk.Button(frame_elementos, text="Eliminar Usuario", command=eliminar_usuario)
boton_eliminar.pack(pady=5)











# Función para cargar datos
def cargar_datos(event=None):
    # Código para cargar datos en la tabla
     # Obtener la zona seleccionada
    zona_seleccionada = zona_combo.get()

    # Verificar si la zona seleccionada está en rango_ids
    if zona_seleccionada in rango_ids:
        # Conectar a la base de datos (o crearla si no existe)
        conexion = sqlite3.connect('basededatos.db')
        cursor = conexion.cursor()

        # Verificar si la tabla personas existe, si no, crearla
        cursor.execute('''CREATE TABLE IF NOT EXISTS personas (
                          id INTEGER PRIMARY KEY,
                          nombre TEXT,
                          zona TEXT,
                          descripcion TEXT)''')

        # Consultar los datos de la zona seleccionada
        cursor.execute('SELECT id, nombre, descripcion FROM personas WHERE zona = ?', (zona_seleccionada,))
        datos = cursor.fetchall()

        # Crear una lista de todas las IDs dentro del rango para la zona
        todas_las_ids = list(rango_ids[zona_seleccionada])

        # Crear una lista de las IDs que ya están en uso
        ids_en_uso = [dato[0] for dato in datos]

        # Filtrar las IDs disponibles eliminando las IDs en uso
        ids_disponibles = [id_ for id_ in todas_las_ids if id_ not in ids_en_uso]

        # Actualizar los valores en el desplegable de IDs
        id_combo['values'] = ids_disponibles

        # Limpiar la tabla antes de mostrar los datos
        for fila in tabla.get_children():
            tabla.delete(fila)

        # Consultar los datos nuevamente para la tabla
        cursor.execute('SELECT * FROM personas WHERE zona = ?', (zona_seleccionada,))
        datos = cursor.fetchall()

        # Mostrar los datos en la tabla
        for dato in datos:
            tabla.insert('', 'end', values=dato)

        # Cerrar la conexión a la base de datos después de todas las operaciones
        conexion.close()
    else:
        # Si la zona no está en rango_ids, borra los valores de id_combo
        id_combo['values'] = []



# Asociar la función de carga de datos al evento <<ComboboxSelected>> del ComboBox de zona
zona_combo.bind("<<ComboboxSelected>>", cargar_datos)

# Botón para buscar usuarios
def buscar_usuarios():
    # Código para buscar usuarios
    global entry_busqueda
    busqueda = entry_busqueda.get()
    conexion = sqlite3.connect("basededatos.db")
    cursor = conexion.cursor()
    
    # Consulta para buscar por nombre o ID
    cursor.execute("SELECT * FROM personas WHERE nombre LIKE ? OR id LIKE ?", ('%' + busqueda + '%', '%' + busqueda + '%'))
    resultados = cursor.fetchall()
    
    conexion.close()
    
    actualizar_lista(resultados)


# Función para actualizar la lista de resultados
def actualizar_lista(resultados):
    global lista  # Declarar lista como una variable global
    lista.delete(*lista.get_children())
    for row in resultados:
        lista.insert("", "end", values=row)






# Función para abrir la ventana de búsqueda
def abrir_ventana_busqueda():
    global entry_busqueda, lista  # Declarar entry_busqueda y lista como variables globales
    ventana_busqueda = tk.Toplevel(ventana)
    ventana_busqueda.title("Búsqueda de Usuarios")
    
    frame_busqueda = ttk.Frame(ventana_busqueda)
    frame_busqueda.pack(padx=10, pady=10, fill="x")

    label_busqueda = ttk.Label(frame_busqueda, text="Buscar:")
    label_busqueda.pack(side="left")

    entry_busqueda = ttk.Entry(frame_busqueda)
    entry_busqueda.pack(side="left", fill="x", expand=True)
    entry_busqueda.bind('<KeyRelease>', lambda event: buscar_usuarios())

    frame_resultados = ttk.Frame(ventana_busqueda)
    frame_resultados.pack(padx=10, pady=10, fill="both", expand=True)

    # Inicializar lista como Treeview
    lista = ttk.Treeview(frame_resultados, columns=("ID", "Nombre", "Zona", "Descripción"))
    lista.heading("#1", text="ID")
    lista.heading("#2", text="Nombre")
    lista.heading("#3", text="Zona")
    lista.heading("#4", text="Descripción")
    lista.pack(fill="both", expand=True)

    buscar_usuarios()



# Botón para buscar usuarios

boton_buscar = tk.Button(frame_elementos, text="Buscar Usuarios", command=abrir_ventana_busqueda)
boton_buscar.pack(pady=5)


# Llamar a la función cargar_datos para cargar los datos iniciales
cargar_datos()

# Ejecutar la aplicación
ventana.mainloop()
