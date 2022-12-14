import mariadb 
import os



def limpioPantalla():
	sisOper = os.name
	if sisOper == "posix":   # si fuera UNIX, mac para Apple, java para maquina virtual Java
		os.system("clear")
	elif sisOper == "ce" or sisOper == "nt" or sisOper == "dos":  # windows
		os.system("cls")


def y_o_n ():
	MENU=""
	while True:
		try:
			MENU=input("¿Intentamos otra vez? Si/No : ").upper()
		except ValueError:
			print("Ingresar Si o No ")
		else:
			if MENU!="SI" and MENU!="NO":
				print("Debe ingresar Si o No  ")
			else:
				return MENU

#FUNCIONES DE SALIR Y VOLVER
def salir(mydb):
	menu="S"
	return menu


def volver(mydb):
	print("Usted va a Volver al Menu Inicial")
	menu2="S"
	return menu2

#DISPONIBILIDAD MENU 0
def disponibilidad(mydb): 
	Flag=True
	mycursor = mydb.cursor()
	while Flag:
		continuo=True
		limpioPantalla()
		print("---------Consultar Pelicula----------")
		print("1.por titulo")
		print("2.por Codigo")
		try:
			opcion=int(input("Ingrese su opción elegida: "))
		except ValueError:
			print("Por favor ingrese un número del listado")
		else:
			if opcion != 1 and opcion != 2:
				print("Por favor, vuelva a ingresar un numero. Esta vez del listado ( 1 o 2)")
			else:
				if opcion ==1:
					titulo=input("Ingrese el titulo que busca: ")
					sqltitulo = "SELECT peliculas.Titulo,peliculas.Estado,GROUP_CONCAT(DISTINCT clientes.nombre_completo  ORDER BY prestamo.pk_prestamos DESC LIMIT 1) FROM peliculas LEFT JOIN prestamo ON prestamo.cod_barra=peliculas.Cod_barra LEFT JOIN clientes ON prestamo.cliente=clientes.pk_Cliente WHERE peliculas.Titulo LIKE '%"+titulo+"%' GROUP BY peliculas.titulo"
					mycursor.execute(sqltitulo)   
					titulosobtenidos= mycursor.fetchall()
					if not titulosobtenidos:
						print("Ese titulo no se encuentra en nuestra base.")
					else:
						for i in range(len(titulosobtenidos)):
							if titulosobtenidos[i][1]=="Disponible":
								print(titulosobtenidos[i][0]+" : "+titulosobtenidos[i][1]+"\n")
							else:
								print(titulosobtenidos[i][0]+" : "+titulosobtenidos[i][1]+" prestado a :"+titulosobtenidos[i][2]+"\n")
								i=len(titulosobtenidos)+1
					Sino=input("¿Quiere consultar sobre otra Pelicula? Si/No : ").upper()
					if Sino!="SI":
						Flag=False
						break
				else:
					Flag2=True
					while Flag2:
						try:
							codigo=int(input("Ingrese el codigo que busca: "))
						except ValueError:
							print("Ingrese el codigo de barras de la pelicula. Es numerico.")
						else:
							sqlcodigo="SELECT peliculas.Titulo,peliculas.Estado,GROUP_CONCAT(DISTINCT clientes.nombre_completo  ORDER BY prestamo.pk_prestamos DESC LIMIT 1) FROM peliculas LEFT JOIN prestamo ON prestamo.cod_barra=peliculas.Cod_barra LEFT JOIN clientes ON prestamo.cliente=clientes.pk_Cliente WHERE peliculas.Cod_barra="+str(codigo)+""
							mycursor.execute(sqlcodigo)  
							codigoobtenido= mycursor.fetchone()
							if not codigoobtenido:
								print("Ese codigo no existe en nuestra base. Intente nuevamente.")
							else:
								tit,estado,cliente=codigoobtenido
								if estado=="Disponible":
									print("{} : {}\n".format(tit,estado))
								else:
									print("{} : {} prestado a {} .\n".format(tit,estado,cliente))
								break
					while continuo==True:
						try:
							Sino=input("¿Quiere consultar sobre otra Pelicula? Si/No : ").upper()
						except ValueError:
							print("Por favor, ingrese SI O NO" )
						else:
							if Sino!="SI" and Sino!="NO":
								print("Por favor, ingrese SI O NO" )
							elif Sino!="SI":
								Flag=False
								break
							else:
								continuo=False

#FUNCIONES CLIENTES

#Consulta clientes
def estado_cliente(mydb): 
	Flag=True
	mycursor = mydb.cursor()
	sql = "SELECT DNI,nombre_completo FROM clientes"
	mycursor.execute(sql)
	myresultado = mycursor.fetchall()
	listadocliente=[]
	for  dni,nombre in myresultado:
		listadocliente.append(dni)
		listadocliente.append(nombre)
	while Flag:
		try:
			cliente=int(input("Ingrese el DNI del cliente a a consultar estado:"))
		except ValueError:
			print("Por favor ingrese un número")
		else:
			if cliente not in listadocliente:
				print("Ese cliente no se encuentra en nuestra base de datos aún")
			else:
				cliente=str(cliente)
				sqlcli = "SELECT nombre_completo,DNI,Estado FROM clientes WHERE DNI="+cliente+""
				sqlpeli= "SELECT Cod_Barra, Titulo FROM prestamos INNER JOIN peliculas ON prestamos.FK_Cod_Barra = peliculas.Cod_Barra INNER JOIN clientes ON prestamos.FK_Cliente = clientes.pk_Cliente WHERE DNI="+cliente+" AND Estado_Prestamo ='P' "
				mycursor.execute(sqlcli)   
				mycliente= mycursor.fetchall()
				for  nombre,dni,estado in mycliente:
					if estado == "P":
						print(f"El cliente {nombre}, DNI numero = {dni}, tiene peliculas tomadas en prestamo")
						Sino=input("¿Quiere consultar sobre otro cliente? Si/No : ").upper()
						if Sino=="NO":
							Flag=False
					else:
						print(f"El cliente {nombre}, DNI numero = {dni}, NO tiene peliculas tomadas en prestamo. Puede tomar prestado")
						Sino=input("¿Quiere consultar sobre otro cliente? Si/No : ").upper()
						if Sino=="NO":
							Flag=False 

#Alta clientes
	#Ingreso datos cliente
def ingreso_cliente(mydb):
		mycursor = mydb.cursor()
		sql = "SELECT DNI FROM clientes"
		mycursor.execute(sql)
		myresultado = mycursor.fetchall()
		while True:
			try:
				dni=int(input("Por favor ingrese el DNI del cliente sin puntos:"))
			except ValueError:
				print("Por favor ingrese el DNI con numeros sin puntos")
			else:
				if dni in myresultado:
					print("El DNI ingresado ya existe, por favor ingrese uno válido o dirijase a modificar un cliente")
				else:
					break
		nom=input("Ingrese el nombre completo:")
		nom=nom.title()
		direc=input("Ingrese la direccion:")
		direc=direc.title()
		estado="L"
		while True:
			try:
				tel=int(input("Ingrese el telefono sin utilizar simbolos:")) 
			except ValueError:
				print("Por favor ingrese lo pedido")
			else:
				break
		return dni,nom,direc,estado,tel
	#Chequear que todo este bien
def check_clientes_alta(dni,nom,direc,estado,tel):
		while True:
			try:
				print(f"Nombre:{nom},DNI:{dni},Telefono:{tel},Direccion:{direc}")
				bien=input("¿Son correctos los datos? Si/No :")
				bien=bien.upper()
			except ValueError:
				print("Por favor ingrese Si o No")
			if bien!="SI" and bien!="NO":
				print("Por favor ingrese Si o No")
			else:
				break
		return bien
	#Funcion menu que da el alta
def alta_cliente(mydb):
	bien="NO"
	while bien=="NO":
		dni,nom,direc,estado,tel=ingreso_cliente(mydb)
		bien=check_clientes_alta(dni,nom,direc,estado,tel)
	mycursor = mydb.cursor()
	sql= "INSERT INTO clientes (DNI, nombre_completo,Direccion, Estado, Telefono)  VALUES (%s,%s,%s,%s,%s)"
	val=[
		(dni,nom,direc,estado,tel),
	]
	mycursor.executemany(sql,val)
	mydb.commit()
	print(mycursor.rowcount, " registro insertado.")
	continuo=True
	while continuo==True:
		try:
			Sino=input("Para volver escriba Si : ").upper()
		except ValueError:
			print("Por favor, ingrese SI" )
		else:
			if Sino!="SI" :
				print("Por favor, ingrese SI" )
			elif Sino!="SI":
				Flag=False
				break
			else:
				continuo=False


#Modificacion clientes
	#Selecion de que modificar
def selec_clientes_modif():
		while True:
			try:
				print("1:DNI   2:Nombre   3:Direccion   4:Telefono")
				num=int(input("Ingrese el numero de lo que desee modificar: "))
			except ValueError:
				print("Por favor ingrese un numero")
			else:
				if num!=1 and num!=2 and num!=3 and num!=4:
					print("Por favor ingrese un numero válido")
				else:
					break
		return num
	#Hace la modificaccion
def modif_clientes(num,mydb,dni):
		if num==1:
			while True:
				try:
					dni2=int(input("Ingrese el DNI modificado:"))
				except ValueError:
					print("Por favor ingrese un número sin puntos")
				else:
					break
			mycursor = mydb.cursor()
			dni2=str(dni2)
			sql = "UPDATE clientes SET DNI = '"+dni2+"' WHERE DNI LIKE '%"+dni+"%'"
			mycursor.execute(sql)
			mydb.commit()
			mycursor.close()
		elif num==2:
			nom=str(input("Ingrese el nombre completo:"))
			mycursor = mydb.cursor()
			sql = "UPDATE clientes SET nombre_completo = '"+nom+"' WHERE DNI LIKE '%"+dni+"%'"
			mycursor.execute(sql)
			mydb.commit()
			mycursor.close()
		elif num==3:
			direc=str(input("Ingrese la nueva direccion:"))
			mycursor = mydb.cursor()
			sql = "UPDATE clientes SET Direccion = '"+direc+"' WHERE DNI LIKE '%"+dni+"%'"
			mycursor.execute(sql)
			mydb.commit()
			mycursor.close()
		else:
			while True:
				try:
					tel=int(input("Ingrese el telefono sin utilizar simbolos:")) 
				except ValueError:
					print("Por favor ingrese lo pedido")
				else:
					break
			
			mycursor = mydb.cursor()
			tel=str(tel)
			sql = "UPDATE clientes SET Telefono = '"+tel+"' WHERE DNI LIKE '%"+dni+"%'"
			mycursor.execute(sql)
			mydb.commit()
			mycursor.close()
	#Check que todo este bien
def check_clientes_modif(mydb,dni):
		while True:
			try:
				mycursor = mydb.cursor()
				sql = "SELECT * FROM clientes WHERE DNI LIKE '%"+dni+"%'"
				mycursor.execute(sql)
				myresultado = mycursor.fetchone()
				print(myresultado)                
				bien=input("¿Son correctos los datos? Si/No :")
				bien=bien.upper()
				mycursor.close()
			except ValueError:
				print("Por favor ingrese Si o No")
			if bien!="SI" and bien!="NO":
				print("Por favor ingrese Si o No")
			else:
				break
		return bien    
	#Funcion menu que junta todo
def mod_cliente(mydb):
	mycursor = mydb.cursor()
	sql = "SELECT DNI FROM Clientes "
	mycursor.execute(sql)
	myresultado = mycursor.fetchall()
	listadoind=[]
	
	for cliente in myresultado:
		listadoind.append(cliente[0])
	
	mycursor.close()
	while True:
		try:
			dni=int(input("Ingrese el DNI del cliente a modificar:"))
		except ValueError:
			print("Por favor ingrese un número sin puntos")
		else:
			if dni not in listadoind:
				print("Por favor ingrese un DNI válido")
			else:
				break
	bien="NO"
	dni=str(dni)
	while bien=="NO":
		num=selec_clientes_modif()
		modificacion=modif_clientes(num,mydb,dni)
		bien=check_clientes_modif(mydb,dni)

#Eliminar Cliente
def eliminar_cliente(mydb):
	mycursor = mydb.cursor()
	sql = "SELECT DNI FROM clientes"
	mycursor.execute(sql)
	myresultado = mycursor.fetchall()
	listadodni=[]
	for  dni in myresultado:
		listadodni.append(dni[0])

	while True:
		try:
			cliente=int(input("Ingrese el DNI del cliente a eliminar:"))
		except ValueError:
			print("Por favor ingrese un número")
		else:
			if cliente not in listadodni:
				print("Ese cliente no se encuentra en nuestra base de datos aún")
			else:
				break
	
	cliente=str(cliente)
	sqlcli = "SELECT nombre_completo,DNI FROM clientes WHERE DNI="+cliente+""
	mycursor.execute(sqlcli)   
	mycliente= mycursor.fetchone()
	sqlest = "SELECT Estado FROM clientes WHERE DNI="+cliente+""
	mycursor.execute(sqlest)   
	myestado= mycursor.fetchone()
	
	if myestado[0]=="L":
		flag="SI"
		while True:
			flag=input((f"Usted va a Eliminar al cliente {mycliente}. ¿Desea continuar? Si/No :").upper())
			if flag == "SI":
				sqldeletecli="DELETE FROM clientes WHERE DNI="+cliente+""
				mycursor.execute(sqldeletecli)
				print(f"Se ha eliminado de la base de datos el cliente {mycliente}")
				mydb.commit()
				break
			elif flag == "NO":
				break
			else:
				print("Ingrese Si para continuar o No para Cancelar")
	else: 
		print("No se puede eliminar al cliente porque posee una pelicula alquilada")
	continuo=True
	while continuo==True:
		try:
			Sino=input("Para volver escriba Si : ").upper()
		except ValueError:
			print("Por favor, ingrese SI" )
		else:
			if Sino!="SI" :
				print("Por favor, ingrese SI" )
			elif Sino!="SI":
				Flag=False
				break
			else:
				continuo=False
		
