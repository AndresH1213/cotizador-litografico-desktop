from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.tix import *
from PIL import ImageTk, Image

from datetime import date
import sqlite3

bg_color="#B5C2D5"
font_min = ('Helvetica', 10)
font_med = ('Helvetica', 11)
font_max = ('Helvetica', 12)

root=Tk()
root.title("Cotizador Medios Litográficos Disgrafic")
root.state(newstate = 'normal')
root.iconbitmap("Icono_Cotizador.ico")
root.geometry ("630x700+5+5")
root.config (bg = "#B5C2D5")

frame_cot = Frame(root, bg = bg_color, width = 600, heigh = 700)


""" ------------------- SET INPUTS VARIABLES ---------------------"""

nombre=StringVar()
direccion=StringVar()
cel=StringVar()
correo=StringVar()
clase_trabajo=StringVar()
unidades_trabajo=IntVar()
unidades_trabajo.set("")

precio_diseño = IntVar()
precio_diseño.set("")
precio_planchas = IntVar()
paper_price = IntVar()
precio_maquina = IntVar()
precio_tinta = IntVar()
precio_numerada = IntVar()
precio_numerada.set("")
precio_perforada = IntVar()
precio_perforada.set("")
precio_troquelada = IntVar()
precio_troquelada.set("")
precio_troquel = IntVar()
precio_troquel.set("")
precio_encuadernacion = IntVar()
precio_encuadernacion.set("")
precio_plastificiacion = IntVar()
precio_plastificiacion.set("")
precio_reservaUV = IntVar()
precio_reservaUV.set("")
precio_empaqueEnvio = IntVar()
precio_empaqueEnvio.set("")
calculo_papel=IntVar()
porcentaje_ganancia=IntVar()

cantidad_planchas = IntVar()
cantidad_planchas.set("")
cantidad_papel = IntVar()
cantidad_papel.set("")
cantidad_maquina = IntVar()
cantidad_maquina.set("")

var_planchas = StringVar()
var_clase_papel = StringVar()
var_tamaño = StringVar()
var_maquina = StringVar()
var_porcentaje = StringVar()

precio_total = ""


#-------------------------FETCH DATA  SET PRODUCTS ARRAYS----------------------------------------------

miConexion = sqlite3.connect('BaseDatos')
miCursor = miConexion.cursor()
miCursor.execute("SELECT Name FROM PRODUCTOS WHERE Category = 'Plancha'")
fetchPlanchas = miCursor.fetchall()

miCursor.execute("SELECT Name FROM PRODUCTOS WHERE Category = 'Papel'")
fetchPapel = miCursor.fetchall()

miCursor.execute("SELECT Name FROM PRODUCTOS WHERE Category = 'Maquina'")
fetchMaquinas = miCursor.fetchall()

miCursor.execute("SELECT Name FROM PRODUCTOS WHERE Category = 'Tamaños'")
fetchTamaños = miCursor.fetchall()

miConexion.commit()

miConexion.close()

list_planchas = []
list_papel = []
list_maquinas = []
list_tamaños = []

for element in range(0,len(fetchPlanchas)):
	list_planchas.append(fetchPlanchas[element][0])

for element in range(0,len(fetchPapel)):
	list_papel.append(fetchPapel[element][0])

for element in range(0,len(fetchMaquinas)):
	list_maquinas.append(fetchMaquinas[element][0])

for element in range(0,len(fetchTamaños)):
	list_tamaños.append(fetchTamaños[element][0])

list_porcentajes = [
		"20%",
		"30%",
		"40%",
		"50%",
		"60%",
		"70%",
		"80%",
		"90%",
		"100%"
]

#---------------------- DATA BASE FUNCTIONS -----------------------------------

"""THIS FUNCTION INIT THE CONNECTION TO THE DATABE AND TRY TO CREATE THE USER TABLE AND
THE ORDERS TABLE"""
def connect_db():

    miConexion=sqlite3.connect("BaseDatos")
    miCursor=miConexion.cursor()

    try:
    	miCursor.execute("CREATE TABLE USUARIOS (USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
			NOMBRE VARCHAR(35), DIRECCION VARCHAR(15),\
			CELULAR VARCHAR(12), EMAIL VARCHAR(20))")

    	miCursor.execute("CREATE TABLE PEDIDOS (ORDEN_ID INTEGER PRIMARY KEY AUTOINCREMENT, CLIENTE INTEGER, \
	    	 FECHA VARCHAR(10), 'CLASE DE TRABAJO' VARCHAR(50),'UNIDADES' INTEGER, DISEÑO INTEGER, PLANCHA VARCHAR(25),\
			'PLANCHA CANT' INTEGER,'PLANCHA PRECIO' INTEGER, PAPEL VARCHAR(15),'TAMAÑO PAPEL' VARCHAR(20),\
			'PAPEL CANT' INTEGER, 'PRECIO PAPEL UND' INTEGER,'PRECIO TOTAL PAPEL' INTEGER, MAQUINA VARCHAR(20),TINTAS INTEGER,\
			'PRECIO MAQUINA' INTEGER, NUMERADA INTEGER, PERFORADA INTEGER, TROQUELADA INTEGER,\
			TROQUEL INTEGER, ENCUADERNACION INTEGER, PLASTIFICADO INTEGER, RESERVAUV INTEGER,\
			'EMPAQUE ENVIO' INTEGER, 'PORCENTAJE GANANCIA' VARCHAR(10), 'PRECIO FABRICA' INTEGER, 'PRECIO TOTAL' INTEGER, FOREIGN KEY(CLIENTE)\
			REFERENCES USUARIOS(USER_ID))")
    	messagebox.showwarning("Base de Datos","Se ha conectado a la base de datos con exito")
    except:
    	messagebox.showwarning("Base de Datos","La base de datos ya ha sido creada")


"""THIS FUNCTION INIT THE CONNECTION TO THE DATABASE AND TRY TO CREATE THE USER TABLE AND
THE ORDERS TABLE"""
def continue_func(e):
	miConexion=sqlite3.connect("BaseDatos")
	miCursor=miConexion.cursor()
	user = []
	try:
		user = miCursor.execute('SELECT USER_ID FROM USUARIOS WHERE USER_ID =' + ID_cliente.get())
		user = miCursor.fetchone()[0]
		miConexion.commit()
		miConexion.close()

	except:
		messagebox.showinfo("Cliente", "Este cliente aun no existe en la base de datos")

	if not str(user).isdigit():
		try:
			user_values = [
						nombre.get(),
						direccion.get(),
						cel.get(),
						correo.get(),
						]

			miCursor.execute("INSERT INTO USUARIOS VALUES (NULL,?,?,?,?)", user_values)

			miCursor.execute("SELECT USER_ID FROM USUARIOS WHERE NOMBRE=" + "'" + nombre.get() + "'")
			
			user = miCursor.fetchone()[0]

			miConexion.commit()
			miConexion.close()

			messagebox.showinfo("informacion","El registro ha sido ingresado con exito")
		except:
			messagebox.showwarning("Algo anda mal!:(","Ocurrió un error con el registro de datos,\
		 	o puede que la tabla no se encuentre creada")

	ID_cliente.set(user)
	root.geometry ("1300x700+5+5")
	root.minsize(1210,650)
	frame_cot.place(relx = 0.5, rely = 0.05 )
	root.update_idletasks()

"""SAVING RECORDS RETRIEVE FROM THE GUI INPUTS"""
def save_record(e):
	try:

		if precio_total == "":
			raise ValueError('Te falta hacer el calculo con el boton')
		miConexion=sqlite3.connect("BaseDatos")
		miCursor=miConexion.cursor()

		pedidos_values = [
					ID_cliente.get(),
					fecha.get(),
					clase_trabajo.get(),
					unidades_trabajo.get(),
					precio_diseño.get(),
					var_planchas.get(),
					cantidad_planchas.get(),
					precio_planchas,
					var_clase_papel.get(),
					var_tamaño.get(),
					cantidad_papel.get(),
					paper_price,
					calculo_papel,
					var_maquina.get(),
					cantidad_maquina.get(),
					precio_maquina, 
					precio_numerada.get(),
					precio_perforada.get(),
					precio_troquelada.get(),
					precio_troquel.get(),
					precio_encuadernacion.get(),
					precio_plastificiacion.get(),
					precio_reservaUV.get(),
					precio_empaqueEnvio.get(),
					var_porcentaje.get(),
					precio_fabrica,
					precio_total
			]
		
		miCursor.execute("INSERT INTO PEDIDOS VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", pedidos_values)

		miConexion.commit()
		miConexion.close()

		messagebox.showinfo("informacion","El registro ha sido ingresado con exito")

	except ValueError as ce:

		messagebox.showwarning("Algo anda mal!:(","Se te olvidó utilizar el botón de calcular")

	except:
		messagebox.showwarning("Algo anda mal!:(","Ocurrió un error con el registro de datos,\
		 puede que la tabla no se encuentre creada")


"""THIS RETRIEVE THE RECORD OF AN ORDEN THAT THE USER SET IN THE INPUT ORDER ID"""       
def searchRecord(e):

	miConexion = sqlite3.connect("BaseDatos")
	miCursor = miConexion.cursor()

	try:
		miCursor.execute("SELECT * FROM USUARIOS LEFT JOIN PEDIDOS ON USER_ID = CLIENTE WHERE ORDEN_ID =" + str(orden_trabajo.get()))
		user_data = miCursor.fetchone()
		miConexion.commit()
		miConexion.close()

		root.geometry ("1300x700+5+5")
		root.minsize(1210,650)
		frame_cot.place(relx = 0.5, rely = 0.05 )
		root.update_idletasks()

		nombre.set(user_data[1])
		direccion.set(user_data[2])
		cel.set(user_data[3])
		correo.set(user_data[4])	
		ID_cliente.set(user_data[6])
		fecha.set(user_data[7])		
		clase_trabajo.set(user_data[8])
		unidades_trabajo.set(user_data[9])
		precio_diseño.set(user_data[10])
		var_planchas.set(user_data[11])
		cantidad_planchas.set(user_data[12])
		planchas_precio_label.config(text="$ {}".format('{:,}'.format(user_data[13]).replace(',','.')))
		precio_planchas = user_data[13]
		var_clase_papel.set(user_data[14])
		var_tamaño.set(user_data[15])
		cantidad_papel.set(user_data[16])
		papel_precio_label.config(text="$ {}".format('{:,}'.format(user_data[17]).replace(',','.')))
		paper_price = user_data[17]
		papel_precio_calculo_label.config(text="$ {}".format('{:,}'.format(user_data[18]).replace(',','.')))
		calculo_papel = user_data[18]
		var_maquina.set(user_data[19])
		cantidad_maquina.set(user_data[20])
		maquina_precio_label.config(text="$ {}".format('{:,}'.format(user_data[21]).replace(',','.')))
		precio_maquina = user_data[21]
		precio_numerada.set(user_data[22])
		precio_perforada.set(user_data[23])
		precio_troquelada.set(user_data[24])
		precio_troquel.set(user_data[25])
		precio_encuadernacion.set(user_data[26])
		precio_plastificiacion.set(user_data[27])
		precio_reservaUV.set(user_data[28])
		precio_empaqueEnvio.set(user_data[29])
		var_porcentaje.set(user_data[30])
		precio_fabrica_label.config(text = "El costo de fabrica del trabajo es: $ {}".format('{:,}'.format(round(user_data[31])).replace(',','.')))
		precio_total_label.config(text = "El costo total del trabajo es: $ {}".format('{:,}'.format(round(user_data[32])).replace(',','.')))

	except:

		messagebox.showwarning("Valor faltante","Por favor revise que el número ingresado en la orden esté correctamente")

	
"""THIS RETRIEVE THE USER INFO AFTER THE USER SET A VALID ID_CLIENT INPUT"""
def retrieve_user_info():
	
	miConexion=sqlite3.connect("BaseDatos")
	miCursor=miConexion.cursor()

	try:
		miCursor.execute("SELECT NOMBRE,DIRECCION,CELULAR,EMAIL FROM USUARIOS WHERE USER_ID =" + "'" + str(ID_cliente.get()) + "'" )
		Datos_personales=miCursor.fetchone()

		nombre.set(Datos_personales[0])
		direccion.set(Datos_personales[1])
		cel.set(Datos_personales[2])
		correo.set(Datos_personales[3])

	except:
		messagebox.showwarning("Lo siento","Verifique que el ID del cliente se encuentre correctamente")


""" ------------- BLOQUE DE FUNCIONES PARA ACTUALIZAR DATOS DLE USUARIO ------------- """

"""DELETING AN ORDER AFTER SET AN ORDER_ID IN THE GUI INPUT RESPECTIVE"""
def delete_order():

	miConexion = sqlite3.connect("BaseDatos")
	miCursor = miConexion.cursor()

	borrar = messagebox.askyesno("Eliminación de registro","¿Seguro que desea eliminar el registro?")

	if borrar == True:
		try:
			miCursor.execute("DELETE FROM PEDIDOS WHERE ORDEN_ID = " + str(orden_trabajo.get()))
			miConexion.commit()
			miConexion.close()
			messagebox.showinfo("Informacion","Esta orden ha sido borrada con exito")
			
		except:
			messagebox.showinfo("Error","Ocurrió un error tratanto de eliminar el registro")

"""UPLOADING IN THE DATABASE USER TABLE WITH THEIR ID, THIS IS RETRIEVE FROM A TREEVIEW IN A TOPLEVEL WINDOW"""
def upload_clients_function(id):
# PICK THE INPUTS THAT ARE FILLED IN THE UPLOAD TOPLEVEL WINDOW AN UPLOAD THE DATABASE IN THEIR RESPECTIVE FIELD
	def upload_client(id):

		miConexion = sqlite3.connect("BaseDatos")
		miCursor = miConexion.cursor()

		if var_nombre_upload.get() != "":
			miCursor.execute('UPDATE USUARIOS SET NOMBRE = ? WHERE USER_ID = ?', (var_nombre_upload.get(), id))
		if var_direccion_upload.get() != "":
			miCursor.execute('UPDATE USUARIOS SET DIRECCION = ? WHERE USER_ID = ?', (var_direccion_upload.get(), id))
		if var_celular_upload.get() != "":
			miCursor.execute('UPDATE USUARIOS SET CELULAR = ? WHERE USER_ID = ?', (var_celular_upload.get(), id))
		if var_email_upload.get() != "":
			miCursor.execute('UPDATE USUARIOS SET EMAIL = ? WHERE USER_ID = ?', (var_email_upload.get(), id))
		miConexion.commit()
		miConexion.close()

		messagebox.showinfo("Informacion","Cliente modificado con exito")

	window_upload = Toplevel(root)
	window_upload.title ("Actualizar")
	window_upload.geometry("220x310+550+480")
	window_upload.iconbitmap("Icono_Cotizador.ico")
	window_upload.config(bg='#0A4A76')

	label_nombre=Label(window_upload, text = "Nuevo Nombre", bg = '#0A4A76', fg = "#C3C3C3", font = font_med)
	label_nombre.grid(row=0, column=0,padx=(50,2),pady=4)
	label_direccion=Label(window_upload, text = "Nueva Dirección", bg = '#0A4A76', fg = "#C3C3C3", font = font_med)
	label_direccion.grid(row=2, column=0,padx=(50,2),pady=4)
	label_celular=Label(window_upload, text = "Nuevo Celular", bg = '#0A4A76', fg = "#C3C3C3", font = font_med)
	label_celular.grid(row=4, column=0,padx=(50,2),pady=4)
	label_email=Label(window_upload, text = "Nuevo Email", bg = '#0A4A76', fg = "#C3C3C3", font = font_med)
	label_email.grid(row=6, column=0,padx=(50,2),pady=4)

	var_nombre_upload = StringVar()
	var_nombre_upload.set("")
	var_direccion_upload = StringVar()
	var_direccion_upload.set("")
	var_celular_upload = StringVar()
	var_celular_upload.set("")
	var_email_upload = StringVar()
	var_email_upload.set("")

	entry_nombre_upload = Entry(window_upload, textvariable=var_nombre_upload, font= font_med, highlightcolor = '#D49A41', width = 20)
	entry_nombre_upload.grid(row=1, column=0,padx=(25,2),pady=2)
	entry_direccion_upload = Entry(window_upload, textvariable=var_direccion_upload, font= font_med, highlightcolor = '#D49A41', width = 20)
	entry_direccion_upload.grid(row=3, column=0,padx=(25,2),pady=2)
	entry_celular_upload = Entry(window_upload, textvariable=var_celular_upload, font= font_med, highlightcolor = '#D49A41', width = 20)
	entry_celular_upload.grid(row=5, column=0,padx=(25,2),pady=2)
	entry_email_upload = Entry(window_upload, textvariable=var_email_upload, font= font_med, highlightcolor = '#D49A41', width = 20)
	entry_email_upload.grid(row=7, column=0,padx=(25,2),pady=2)

	btn_ok_modificar= Button(window_upload, text = "Modificar", font = font_med, bg = "#C3C3C3", fg = '#0A4A76',cursor = "hand2",\
			 command = lambda: [upload_client(id), window_upload.destroy()])
	btn_ok_modificar.grid(row=9, column=0,padx=(25,2),pady=(20,0))

	window_upload.mainloop()

"""THIS FUNCTION UPLOAD IN THE DATABASE USER TABLE WITH THEIR ID, THIS IS RETRIEVED FROM A TREEVIEW IN A TOPLEVEL WINDOW"""
def delete_client(_id):

	borrar = messagebox.askyesno("Eliminación de registro","¿Seguro que desea eliminar el registro?")

	try:
		if borrar:
			miConexion = sqlite3.connect("BaseDatos")
			miCursor = miConexion.cursor()
			miCursor.execute("DELETE FROM USUARIOS WHERE USER_ID = " + str(_id))
			miCursor.execute("DELETE FROM PEDIDOS WHERE CLIENTE = " + str(_id))
			miConexion.commit()
			miConexion.close()

			messagebox.showinfo("Informacion","Este cliente ha sido borrada con exito")
	except:
		messagebox.showwarning("Atención!","Ocurre un error, puede que este cliente no exista.")

"""THIS FUNCTION DISPLAY THE TREEVIEW WITH THE USER DATA AND STABLISH TWO OPTION UPLOAD OR DELETE A CLIENT"""
def client_managment():
# RELOAD THE INFO THAT TREEVIEW SHOWS
	def actualizar_db_clientes(e):

		miConexion = sqlite3.connect("BaseDatos")
		miCursor = miConexion.cursor()

		miCursor.execute("SELECT * FROM USUARIOS")
		clientes_data = miCursor.fetchall()

		for record in my_tree.get_children():
			my_tree.delete(record)

		for element in range(0,len(clientes_data)):			
			my_tree.insert(parent='', index='end', iid=clientes_data[element][0], text="", values=clientes_data[element])

		miConexion.commit()
		miConexion.close()

	window_cliente = Toplevel(root)
	window_cliente.title ("Actualizar un cliente")
	window_cliente.iconbitmap("Icono_Cotizador.ico")
	window_cliente.geometry("730x320+250+25")
	window_cliente.config(bg='#CDC3BC')


	miConexion = sqlite3.connect("BaseDatos")
	miCursor = miConexion.cursor()
	miCursor.execute("SELECT * FROM USUARIOS")
	clientes_data = miCursor.fetchall()
	miConexion.commit()
	miConexion.close()

# -- SET THE TREVIEW THAT DISPLAYS THE DATA
	my_tree = ttk.Treeview(window_cliente)
	my_tree['columns'] = ('CLIENTE_ID', 'NOMBRE', 'DIRECCION', 'CELULAR', 'EMAIL')
	

	my_tree.column("#0", width=0)
	my_tree.column("CLIENTE_ID", anchor=CENTER, width=60)
	my_tree.column("NOMBRE", anchor=CENTER, width=200)
	my_tree.column("DIRECCION", anchor=CENTER, width=150)
	my_tree.column("CELULAR", anchor=W ,width=120)
	my_tree.column("EMAIL", anchor=W ,width=200)

	my_tree.heading("#0", text="", anchor=W)
	my_tree.heading("CLIENTE_ID", text="Cliente id", anchor=CENTER)
	my_tree.heading("NOMBRE", text="Nombre", anchor=CENTER)
	my_tree.heading("DIRECCION", text="Dirección", anchor=CENTER)
	my_tree.heading("CELULAR", text="Celular", anchor=CENTER)
	my_tree.heading("EMAIL", text="E-mail", anchor=CENTER)
	my_tree.pack()

	# ADD DATA TO THE TREEVIEW
	for element in range(0,len(clientes_data)):			
		my_tree.insert(parent='', index='end', iid=clientes_data[element][0], text="", values=clientes_data[element])

	# BTNS

	btn_actualizar= Button(window_cliente, text = "Actualizar", font = font_med, bg = "#CDC3BC", fg = "#0D3A75",cursor = "hand2",\
			 command = lambda: upload_clients_function(my_tree.selection()[0]))
	btn_actualizar.place(relx = 0.4, rely = 0.88)

	btn_eliminar = Button(window_cliente, text = "Eliminar", font = font_med, bg ="#CDC3BC", fg = "#0D3A75",cursor = "hand2",\
			 command = lambda: delete_client(my_tree.selection()[0]))
	btn_eliminar.place(relx = 0.55, rely = 0.88)

	# set the message ballon

	tags = Balloon(window_cliente)

	imagen_relaod = ImageTk.PhotoImage(Image.open("./images/reload.png"))
	btn_reload=Label(window_cliente, image=imagen_relaod, bg= '#CDC3BC', cursor = 'hand2')
	btn_reload.place(relx=0.3,rely=0.88)

	btn_reload.bind("<Button-1>", actualizar_db_clientes)
	tags.bind_widget(btn_reload, balloonmsg = "Recargar base de datos")

	window_cliente.mainloop()

""" ------------------- UTIL FUNCTIONS ---------------------- """
""" CLEAN THE INPUTS OF THE WORK CALCULATION"""
def clean_work_data():
	
	precio_diseño.set("")
	unidades_trabajo.set("")
	cantidad_planchas.set("")
	cantidad_papel.set("")
	cantidad_maquina.set("")
	precio_numerada.set("")
	precio_perforada.set("")	
	precio_troquelada.set("")
	precio_troquel.set("")
	precio_encuadernacion.set("")
	precio_plastificiacion.set("")
	precio_reservaUV.set("")
	precio_empaqueEnvio.set("")

	var_planchas.set("Elija una opción")
	var_tamaño.set("Escoja tipo papel")
	var_maquina.set("Elija una opción")
	var_clase_papel.set("Elija una opción")
	var_porcentaje.set("Elija una opción")
	planchas_precio_label.config(text="")
	papel_precio_label.config(text="")
	papel_precio_calculo_label.config(text="")
	maquina_precio_label.config(text="")

	precio_fabrica_label.config(text = "")
	precio_total_label.config(text="")

""" CLEAN THE INPUTS OF THE USER DATA"""
def clean_inputuser_data():

	ID_cliente.set("")
	orden_trabajo.set("")
	nombre.set("")
	direccion.set("")
	cel.set("")
	correo.set("")
	clase_trabajo.set("")
	unidades_trabajo.set("")
	fecha.set(date.today())

""" FORGET THE FRAME FOR THE CALCULATION AN SET THE WINDOW SIZE SMALL AGAIN"""
def back_main_form(e):

	frame_cot.place_forget()
	root.update_idletasks()
	root.minsize(610,710)
	root.geometry("630x710")
	clean_work_data()

def licencia():
    messagebox.showinfo("Licencia", "Este programa es de uso exclusivo de Litografia Disgrafic.")

def Acerca_de():
    messagebox.showinfo("Acerca de...", "El objetivo del sofware es calcular el valor del servicio que la empresa ofrece.")

def salir():

    Cerrar=messagebox.askokcancel("salir","¿Deseas salir de la aplicación?")
    if Cerrar==True:
        root.destroy()

#---------------- CALCULATE FUNCTIONS TO STABLISH THE PRICE OF THE JOB -------------------
""" DOING THE CALCULOUS OF THE WORK'S PRICE DEPARTING FROM THE INPUT DATA AND OTHER CALCULATIONS
	THE PRICE OF THE MATERIAL ARE RETRIEVE FROM THE DATABASE """

def f_cotizar(e):
	global porcentaje_ganancia
	global precio_total
	global precio_fabrica

	try:
		
		precio_fabrica = precio_diseño.get() + (precio_planchas*cantidad_planchas.get())\
		+ calculo_papel + (precio_maquina*cantidad_maquina.get())\
		+ precio_numerada.get() + precio_perforada.get() + precio_troquelada.get()\
		+ precio_troquel.get() + precio_encuadernacion.get() + precio_plastificiacion.get()	+ precio_reservaUV.get() + precio_empaqueEnvio.get()

		precio_total = precio_fabrica*porcentaje_ganancia 

	# OUTPUT THE PRICE IN A LABEL
		precio_fabrica_label.config(text = "El costo de fabrica del trabajo es: $ {}".format('{:,}'.format(round(precio_fabrica)).replace(',','.')))
		precio_total_label.config(text = "El costo total del trabajo es: $ {}".format('{:,}'.format(round(precio_total)).replace(',','.')))

	except:

		messagebox.showwarning("Ops!","Por favor ingrese todos los datos")

# Its the same function but not receiving the event that its passing by de click on de label 'button', this is called by the menu
def f_cotizar_menu():
	global porcentaje_ganancia
	global precio_total
	global precio_fabrica

	try:
		
		precio_fabrica = precio_diseño.get() + (precio_planchas*cantidad_planchas.get())\
		+ calculo_papel + (precio_maquina*cantidad_maquina.get())\
		+ precio_numerada.get() + precio_perforada.get() + precio_troquelada.get()\
		+ precio_troquel.get() + precio_encuadernacion.get() + precio_plastificiacion.get()	+ precio_reservaUV.get() + precio_empaqueEnvio.get()

		precio_total = precio_fabrica*porcentaje_ganancia 

	# OUTPUT THE PRICE IN A LABEL
		precio_fabrica_label.config(text = "El costo de fabrica del trabajo es: $ {}".format('{:,}'.format(round(precio_fabrica)).replace(',','.')))
		precio_total_label.config(text = "El costo total del trabajo es: $ {}".format('{:,}'.format(round(precio_total)).replace(',','.')))

	except:

		messagebox.showwarning("Ops!","Por favor ingrese todos los datos")

def f_precio_planchas(event):
	global precio_planchas

	miConexion = sqlite3.connect('BaseDatos')
	miCursor = miConexion.cursor()
	miCursor.execute("SELECT Price FROM PRODUCTOS WHERE Category = 'Plancha'")
	fetchPrice_planchas = miCursor.fetchall()
	miConexion.commit()
	miConexion.close()

	for i in range(0,len(list_planchas)):
		if var_planchas.get() == list_planchas[i]:
			precio_planchas = fetchPrice_planchas[i][0]
	

	planchas_precio_label.config(text = "$ {}".format('{:,}'.format(precio_planchas).replace(',','.')))

def f_paper_price(event):
	global paper_price
	global list_papel

	miConexion = sqlite3.connect('BaseDatos')
	miCursor = miConexion.cursor()
	miCursor.execute("SELECT Price FROM PRODUCTOS WHERE Category = 'Papel'")
	fetchPrice_papel = miCursor.fetchall()
	miConexion.commit()
	miConexion.close()

	for i in range(0,len(list_papel)):
		if var_clase_papel.get() == list_papel[i]:
			if list_papel[i] == 'Resmilla-Carta':
				try:
					paper_price = fetchPrice_papel[i][0]
					cantidad_papel.set(unidades_trabajo.get()/500)
				except:
					messagebox.showwarning("Cantidad Trabajo", "Asegurarse que la cantidad del trabajo este llena")
			elif list_papel[i] == 'Resmilla-Oficio':
				try:
					paper_price = fetchPrice_papel[i][0]
					cantidad_papel.set(unidades_trabajo.get()/500)
				except:
					messagebox.showwarning("Cantidad Trabajo", "Asegurarse que la cantidad del trabajo este llena")
			else:
				paper_price = fetchPrice_papel[i][0]
		
	papel_precio_label.config(text = "$ {}".format('{:,}'.format(paper_price).replace(',','.')))

def f_calculo_papel(event):
	global calculo_papel

	miConexion = sqlite3.connect('BaseDatos')
	miCursor = miConexion.cursor()
	miCursor.execute("SELECT Price FROM PRODUCTOS WHERE Category = 'Tamaños'")
	fetchTamaños = miCursor.fetchall()
	miConexion.commit()
	miConexion.close()

	try:
		for i in range(0,len(list_tamaños)):
			if var_tamaño.get() == list_tamaños[i]:
				if list_tamaños[i] == 'No aplica':
					division_papel = cantidad_papel.get()
				else:
					division_papel = unidades_trabajo.get()/fetchTamaños[i][0]

		calculo_papel=round(division_papel*paper_price)
			
		papel_precio_calculo_label.config(text = "$ {}".format('{:,}'.format(calculo_papel).replace(',','.')))
		cantidad_papel.set('{:,}'.format(round(division_papel)).replace(',','.'))
	except:
		messagebox.showwarning("Revisar","Revisar si la cantidad del trabajo es númerica o si el papel del trabajo ya fue escojido")

def f_precio_maquina(event):
	global precio_maquina

	miConexion = sqlite3.connect('BaseDatos')
	miCursor = miConexion.cursor()
	miCursor.execute("SELECT Price FROM PRODUCTOS WHERE Category = 'Maquina'")
	fetchPrice_maquinas = miCursor.fetchall()
	miConexion.commit()
	miConexion.close()

	for i in range(0,len(list_maquinas)):
		if var_maquina.get() == list_maquinas[i]:
			precio_maquina = fetchPrice_maquinas[i][0]
	
	maquina_precio_label.config(text = "$ {}".format('{:,}'.format(precio_maquina).replace(',','.')))

def f_porcentaje(event):
	global porcentaje_ganancia

	for i in range(0,len(list_porcentajes)):
		if var_porcentaje.get() == list_porcentajes[i]:
			porcentaje_ganancia = 1.2 + i*(0.1)

#-------------- GRAPHIC USER INTERFACE BLOCK -----------------------

"""----------- MAIN FORM USER INFO -----------------------------"""

frame1=Frame(root, heigh=300, bg="#157EA5")
frame1.grid(row=0,column=0, sticky=N, padx=10,pady=10)

frame2=Frame(root, heigh=300,  bg="#B5C2D5")
frame2.grid(row=0,column=1, sticky=N ,padx=5,pady=5)

frame3 = Frame(root,  bg= "#B5C2D5" )
frame3.grid(row=1,column=0, columnspan=2)

#Button to set the info user automatically in the GUI

btn_oldClient=Button(frame2, text = "Cliente Antiguo", font = font_min, bg="#CDC3BC", fg= "#0D3A75",
 command = retrieve_user_info, cursor="hand2")
btn_oldClient.grid(row= 1, column = 1, padx=0,pady=(25,5), sticky='s')

ID_cliente=StringVar()
ID_cliente.set("")
entry_oldClient=Entry(frame2, textvariable=ID_cliente, font = font_min, width=6)
entry_oldClient.grid(row=2,column=1,padx=5 )

imagen= ImageTk.PhotoImage(Image.open("./images/Disgrafic.jpg"))
label_imagen=Label(frame1, image=imagen, bg=bg_color)
label_imagen.grid(row=0, column=0,padx=10,pady=10)

label_date=Label(frame2, text="Año / Mes / Día", font= font_max, bg=bg_color)
label_date.grid(row=1,column=0, sticky=N)

fecha = StringVar()
fecha.set(date.today())
orden_trabajo= IntVar()

entry_date=Entry(frame2, textvariable=fecha, font= font_med, width=10, justify="left")
entry_date.grid(row=0,column=0,padx=5, pady=2)

entry_orden=Entry(frame2, textvariable=orden_trabajo, font= font_med, width=6, justify="center")
entry_orden.grid(row=0,column=1, padx=8)

nombre_label=Label(frame3, text="NOMBRE: ", font= font_min, bg=bg_color)
nombre_label.grid(row=0,column=0)

direccion_label=Label(frame3, text="DIRECCION: ", font= font_min, bg=bg_color)
direccion_label.grid(row=1,column=0)

cel_label=Label(frame3, text="CEL ", font= font_min, bg=bg_color)
cel_label.grid(row=1,column=2, padx=0)

correo_label=Label(frame3, text="E-MAIL: ", font= font_min, bg=bg_color)
correo_label.grid(row=2,column=0)

clase_trabajo_label=Label(frame3, text="CLASE DE TRABAJO: ", font= font_min, bg=bg_color)
clase_trabajo_label.grid(row=3,column=0)

unidades_trabajo_label=Label(frame3, text="UNIDADES: ", font= font_min, bg=bg_color)
unidades_trabajo_label.grid(row=4,column=0)

# ----------------- INPUTS USER FORM ------------------------------------------------

entry_nombre=Entry(frame3, textvariable=nombre, font= font_med, width=45)
entry_nombre.grid(row=0,column=1, columnspan=3, pady=3)

entry_direccion=Entry(frame3, textvariable=direccion, font= font_med)
entry_direccion.grid(row=1,column=1,pady=3)

entry_cel=Entry(frame3, textvariable=cel, font= font_med,width=19)
entry_cel.grid(row=1,column=3,pady=3)

entry_correo=Entry(frame3, textvariable=correo, font= font_med, width=45)
entry_correo.grid(row=2,column=1, columnspan=3,pady=3)

entry_clase=Entry(frame3, textvariable=clase_trabajo, font= font_med, width=45)
entry_clase.grid(row=3,column=1, columnspan=3,pady=(3))

entry_unidades_trabajo=Entry(frame3, textvariable=unidades_trabajo, font= font_med, width=15)
entry_unidades_trabajo.grid(row=4,column=1, columnspan=3,pady=(3,10), sticky=W)

# set the message ballon

tags = Balloon(root)

imagen_continue = ImageTk.PhotoImage(Image.open("./images/continue.png"))
btn_continue = Label(root, image=imagen_continue, bg= bg_color, cursor = 'hand2')
btn_continue .place(relx=0.15,rely=0.4)

btn_continue.bind("<Button-1>", continue_func)
tags.bind_widget(btn_continue, balloonmsg = "Continuar y guardar")

imagen_search = ImageTk.PhotoImage(Image.open("./images/search.png"))
btn_search = Label(root, image=imagen_search, bg= bg_color, cursor = 'hand2', borderwidth = 0.5, height = 40)
btn_search.place(x=480, y=5)

btn_search.bind("<Button-1>", searchRecord)
tags.bind_widget(btn_search, balloonmsg = "Buscar registro")

#-------------BLOQUE PARA DESPLEGAR LA INFORMACION DE LOS USUARIOS---------------------------------------

def actualizar_db(e):
	miConexion = sqlite3.connect("BaseDatos")
	miCursor = miConexion.cursor()

	miCursor.execute("SELECT * FROM USUARIOS")
	info_user_db = miCursor.fetchall()

	miCursor.execute("SELECT ORDEN_ID, CLIENTE, FECHA, `CLASE DE TRABAJO`, UNIDADES, `PRECIO TOTAL` FROM PEDIDOS")
	info_pedidos_db = miCursor.fetchall()

	for record in my_tree_db.get_children():
		my_tree_db.delete(record)

	for user in range(0,len(info_user_db)):

		my_tree_db.insert(parent='', index='end', iid=info_user_db[user][0], text="", values=info_user_db[user])

	my_tree_db.tag_configure('child', background = '#E3C85D')

	for pedido in range(0,len(info_pedidos_db)):
		values = [
					'orden: ' + str(info_pedidos_db[pedido][0]),
					info_pedidos_db[pedido][3],
					info_pedidos_db[pedido][2],
					'uds: ' + str(info_pedidos_db[pedido][4]),
					'total: $ ' + str('{:,}'.format(round(info_pedidos_db[pedido][5])).replace(',','.'))
				 ]
		my_tree_db.insert(parent=info_pedidos_db[pedido][1], index='end', iid=f"{info_pedidos_db[pedido][1]}-{info_pedidos_db[pedido][0]}", text="", values=values, tags = ('child'))

	miConexion.commit()
	miConexion.close()

miConexion = sqlite3.connect("BaseDatos")
miCursor = miConexion.cursor()

miCursor.execute("SELECT * FROM USUARIOS")
info_user_db = miCursor.fetchall()


miCursor.execute("SELECT ORDEN_ID, CLIENTE, FECHA, `CLASE DE TRABAJO`, UNIDADES, `PRECIO TOTAL` FROM PEDIDOS")
info_pedidos_db = miCursor.fetchall()

miConexion.commit()
miConexion.close()

#-- ADD SOME STYLE --

style = ttk.Style()

# Pick a theme
style.theme_use('default')
style.configure("Treeview", 
	background = "#EAE9DE",
	foreground = "black",
	rowheight = 25,
	fieldbackground ="#EAE9DE"
	)

# Change Selected Color
style.map('Treeview',
	background = [('selected', '#0A4A76')])

my_tree_db = ttk.Treeview(root)
my_tree_db['columns'] = ('CLIENTE_ID', 'NOMBRE', 'DIRECCION', 'CELULAR', 'EMAIL')

my_tree_db.column("#0", width=0)
my_tree_db.column("CLIENTE_ID", anchor=CENTER, width=60)
my_tree_db.column("NOMBRE", anchor=CENTER, width=150)
my_tree_db.column("DIRECCION", anchor=CENTER, width=110)
my_tree_db.column("CELULAR", anchor=W ,width=100)
my_tree_db.column("EMAIL", anchor=W ,width=150)

my_tree_db.heading("#0", text="", anchor=W)
my_tree_db.heading("CLIENTE_ID", text="Cliente id", anchor=CENTER)
my_tree_db.heading("NOMBRE", text="Nombre", anchor=CENTER)
my_tree_db.heading("DIRECCION", text="Dirección", anchor=CENTER)
my_tree_db.heading("CELULAR", text="Celular", anchor=CENTER)
my_tree_db.heading("EMAIL", text="E-mail", anchor=CENTER)
my_tree_db.place(rely=0.5, relx=0.03)

# IMAGES TO IMPROVE UX, BLIND IMAGES TO FUNCTION TO MADE THEM BTNS

imagen_db = ImageTk.PhotoImage(Image.open("./images/db.png"))
btn_db = Label(root, image=imagen_db, bg= bg_color, cursor = 'hand2', borderwidth = 0.5, height=40)
btn_db.place(relx=0.3,rely=0.41)

btn_db.bind("<Button-1>", actualizar_db)
tags.bind_widget(btn_db, balloonmsg = "Mostrar/actualizar base de datos")


#-------------BLOQUE INTERFAZ GRAFICA DE LOS DATOS PARA COTIZAR EL TRABAJO -------------------------------

frame4 = Frame(frame_cot,  bg= "#B5C2D5" )
frame4.pack()

titulo_calculo = Label(frame4, text="CARACTERISTICAS DEL TRABAJO", font = ("Helvetica", 10, "underline"), bg=bg_color)
titulo_calculo.grid(row=0, column=1, columnspan=2)

cantidad_label=Label(frame4, text="CANT ", font= font_min, bg=bg_color, fg="#000")
cantidad_label.grid(row=1,column=2, padx=5,pady=5)

precio_label=Label(frame4, text="PRECIO UNID", font= font_min, bg=bg_color, fg="#000")
precio_label.grid(row=1,column=3, padx=5,pady=5)

diseño_label=Label(frame4, text="DISEÑO: ", font= font_min, bg=bg_color)
diseño_label.grid(row=2,column=0, padx=5,pady=5, sticky=W)

unidades_trabajo_label=Label(frame4, text="CANTIDAD DE PLIEGOS: ", font= font_min, bg=bg_color)
unidades_trabajo_label.grid(row=3,column=0, sticky=W)

planchas_label=Label(frame4, text="PLANCHAS: ", font= font_min, bg=bg_color)
planchas_label.grid(row=4,column=0,  padx=5,pady=5, sticky=W)

planchas_precio_label=Label(frame4, font= font_med, bg=bg_color)
planchas_precio_label.grid(row=4, column=3, padx=5,pady=5)

clase_papel_label=Label(frame4, text="CLASE DE PAPEL: ", font= font_min, bg=bg_color)
clase_papel_label.grid(row=5,column=0,  padx=5,pady=5, sticky=W)

tamaño_label=Label(frame4, text="TAMAÑO: ", font= font_min, bg=bg_color)
tamaño_label.grid(row=6,column=0,  padx=5,pady=5, sticky=W)

papel_precio_label=Label(frame4, font= font_med, bg=bg_color)
papel_precio_label.grid(row=5, column=3, padx=5,pady=5)

papel_precio_calculo_label=Label(frame4, font= font_med, bg=bg_color)
papel_precio_calculo_label.grid(row=6, column=3, padx=5,pady=5)

tipo_maquina_label=Label(frame4, text="TIPO DE MAQUINA: ", font= font_min, bg=bg_color)
tipo_maquina_label.grid(row=7,column=0, padx=5,pady=5, sticky=W)

maquina_precio_label=Label(frame4, font= font_med, bg=bg_color)
maquina_precio_label.grid(row=7, column=3, padx=5,pady=3)

numerada_label=Label(frame4, text="NUMERADA: ", font= font_min, bg=bg_color)
numerada_label.grid(row=8,column=0, padx=5,pady=2, sticky=W)

perforado_label=Label(frame4, text="PERFORADA: ", font= font_min, bg=bg_color)
perforado_label.grid(row=9,column=0, padx=5,pady=2, sticky=W)

troquelada_label=Label(frame4, text="TROQUELADA: ", font= font_min, bg=bg_color)
troquelada_label.grid(row=10,column=0,  padx=5,pady=2, sticky=W)

troquel_label=Label(frame4, text="TROQUEL: ", font= font_min, bg=bg_color)
troquel_label.grid(row=11,column=0,  padx=5,pady=2, sticky=W)

encuadernacion_label=Label(frame4, text="ENCUADERNACION: ", font= font_min, bg=bg_color)
encuadernacion_label.grid(row=12,column=0,  padx=5,pady=2, sticky=W)

plastificado_label=Label(frame4, text="PLASTIFICADO: ", font= font_min, bg=bg_color)
plastificado_label.grid(row=13,column=0,  padx=5,pady=2, sticky=W)

reservaUV_label=Label(frame4, text="RESERVA UV: ", font= font_min, bg=bg_color)
reservaUV_label.grid(row=14,column=0,  padx=5,pady=2, sticky=W)

empaqueenvio_label=Label(frame4, text="EMPAQUE Y ENVIO: ", font= font_min, bg=bg_color)
empaqueenvio_label.grid(row=15,column=0,  padx=5,pady=2, sticky=W)

porcentaje_ganancia_label=Label(frame4, text="PORCENTAJE GANANCIA: ", font= font_min, bg=bg_color)
porcentaje_ganancia_label.grid(row=16,column=0,  padx=5,pady=2, sticky=W)

precio_fabrica_label=Label(root, font= font_max,  bg=bg_color)
precio_fabrica_label.place(rely=0.9, relx=0.6)

precio_total_label=Label(root, font= font_max,  bg=bg_color)
precio_total_label.place(rely=0.95, relx=0.6)


#----------- INPUTS PARA HACEER EL CALCULO DEL TRABAJO A COTIZAR------------------------

setOptions = 'Escoja una opción'

entry_diseño = Entry (frame4, textvariable=precio_diseño, font= font_max, width= 12, justify="center")
entry_diseño.grid(row=2,column=3,padx=5)

entry_unidades_trabajo=Entry(frame4, textvariable=unidades_trabajo, font= font_max, width=10, justify="center")
entry_unidades_trabajo.grid(row=3,column=2,pady=(3,10),padx=5)

entry_numerada = Entry (frame4, textvariable=precio_numerada, font= font_max, width= 12, justify="center")
entry_numerada.grid(row=8,column=3,padx=5)

entry_perforada = Entry (frame4, textvariable=precio_perforada, font= font_max, width= 12, justify="center")
entry_perforada.grid(row=9,column=3,padx=5)

entry_troquelada = Entry (frame4, textvariable=precio_troquelada, font= font_max, width= 12, justify="center")
entry_troquelada.grid(row=10,column=3,padx=5)

entry_troquel = Entry (frame4, textvariable=precio_troquel, font= font_max, width= 12, justify="center")
entry_troquel.grid(row=11,column=3,padx=5)

entry_encuadernacion = Entry (frame4, textvariable=precio_encuadernacion, font= font_max, width= 12, justify="center")
entry_encuadernacion.grid(row=12,column=3,padx=5)

entry_plastificado = Entry (frame4, textvariable=precio_plastificiacion, font= font_max, width= 12, justify="center")
entry_plastificado.grid(row=13,column=3,padx=5)

entry_reservaUV = Entry (frame4, textvariable=precio_reservaUV, font= font_max, width= 12, justify="center")
entry_reservaUV.grid(row=14,column=3,padx=5)

entry_empaqueEnvio = Entry (frame4, textvariable=precio_empaqueEnvio, font= font_max, width= 12, justify="center")
entry_empaqueEnvio.grid(row=15,column=3,padx=5)

entry_cantidad_planchas = Entry (frame4, textvariable=cantidad_planchas, font= font_max, width= 10, justify="center")
entry_cantidad_planchas.grid(row=4,column=2,padx=5)

entry_cantidad_papel = Entry (frame4, textvariable=cantidad_papel, font= font_max, width= 10, justify="center")
entry_cantidad_papel.grid(row=6,column=2,padx=5)

entry_cant_maquina = Entry (frame4, textvariable=cantidad_maquina, font= font_max, width= 10, justify="center")
entry_cant_maquina.grid(row=7,column=2,padx=5)

option_planchas = ttk.OptionMenu(frame4, var_planchas, setOptions, *list_planchas, command=f_precio_planchas)
option_planchas.grid(row=4,column=1,padx=5,pady=3)

option_clase_papel = ttk.OptionMenu (frame4, var_clase_papel, setOptions, *list_papel, command=f_paper_price)
option_clase_papel.grid(row=5,column=1,padx=5,pady=3)

option_tamaño = ttk.OptionMenu(frame4, var_tamaño, setOptions, *list_tamaños, command=f_calculo_papel)
option_tamaño.grid(row=6,column=1,padx=5,pady=3)

option_maquina = ttk.OptionMenu(frame4, var_maquina, setOptions, *list_maquinas, command=f_precio_maquina )
option_maquina.grid(row=7,column=1,padx=5,pady=3)

option_porcentaje = ttk.OptionMenu(frame4, var_porcentaje, setOptions ,*list_porcentajes, command=f_porcentaje )
option_porcentaje.grid(row=16,column=1,padx=3,pady=3)

# IMAGES TO IMPROVE UX, BLIND IMAGES TO FUNCTION TO MADE THEM BTNS

imagen_back = ImageTk.PhotoImage(Image.open("./images/back.png"))
btn_back = Label(frame4, image=imagen_back, bg= bg_color, cursor = 'hand2')
btn_back.grid(row=17,column=0,pady=5)

btn_back.bind("<Button-1>", back_main_form)
tags.bind_widget(btn_back, balloonmsg = "Regresar a clientes")

imagen_cotizar = ImageTk.PhotoImage(Image.open("./images/cotizar.png"))
btn_cotizar = Label(frame4, image=imagen_cotizar, bg= bg_color, cursor = 'hand2')
btn_cotizar.grid(row=17,column=1,pady=5)

btn_cotizar.bind("<Button-1>", f_cotizar)
tags.bind_widget(btn_cotizar, balloonmsg = "Calcular valor del trabajo")

imagen_save = ImageTk.PhotoImage(Image.open("./images/save.png"))
btn_save = Label(frame4, image=imagen_save, bg= bg_color, cursor = 'hand2')
btn_save.grid(row=17,column=2,pady=5)

btn_save.bind("<Button-1>", save_record)
tags.bind_widget(btn_save, balloonmsg = "Guardar registro")


#---------------------------------- TOP MENU ---------------------------------------------------

barraMenu = Menu(root)
root.config(menu=barraMenu)

ArchivoMenu=Menu(barraMenu, tearoff=0)
ArchivoMenu.add_command(label="Conectar a BBDD", command=connect_db)
ArchivoMenu.add_command(label="Guardar Reqistro", command=save_record)
ArchivoMenu.add_command(label="Salir",command=salir)

EditarMenu=Menu(barraMenu, tearoff=0)
EditarMenu.add_command(label="Limpiar datos del usuario",command=clean_inputuser_data)
EditarMenu.add_command(label="Limpiar datos del trabajo",command=clean_work_data)
EditarMenu.add_command(label="Borrar Todo", command=lambda:[clean_inputuser_data(),clean_work_data()])

HerramientasMenu=Menu(barraMenu, tearoff=0)
HerramientasMenu.add_command(label="Cotizar", command= f_cotizar_menu)
HerramientasMenu.add_command(label="Actualizar Clientes", command=client_managment)
HerramientasMenu.add_command(label="Eliminar una Orden", command=delete_order)

AyudaMenu=Menu(barraMenu, tearoff=0)
AyudaMenu.add_command(label="Licencia",command=licencia)
AyudaMenu.add_command(label="Acerca de...", command=Acerca_de)

barraMenu.add_cascade(label="Archivo",menu=ArchivoMenu)
barraMenu.add_cascade(label="Editar",menu=EditarMenu)
barraMenu.add_cascade(label="Herramientas",menu=HerramientasMenu)
barraMenu.add_cascade(label="Ayuda",menu=AyudaMenu)

frame_cot.mainloop()
root.mainloop()

