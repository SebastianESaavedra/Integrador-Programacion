import mariadb 
#os.system("cls")  para limpiar la pantalla
# import os
# def limpioPantalla():
# 	sisOper = os.name
# 	if sisOper == "posix":   # si fuera UNIX, mac para Apple, java para maquina virtual Java
# 		os.system("clear")
# 	elif sisOper == "ce" or sisOper == "nt" or sisOper == "dos":  # windows
# 		os.system("cls")


def y_o_n ():
    MENU=""
    while True:
        try:
            MENU=input("¿Intentamos otra vez? ingrese Y o N ").upper()
        except ValueError:
            print("Ingresa Y o N ")
        else:
            if MENU!="Y" and MENU!="N":
                print("Debe ingresar Y o N : ")
            else:
                return MENU

#FUNCIONES DE SALIR Y VOLVER
def salir(mydb):
    menu="S"
    return menu


def volver(mydb):
    print("Usted va a Volver al Menu Inicial") #Anto
    menu2="S"
    return menu2

#DISPONIBILIDAD MENU 0
def disponibilidad(mydb): 
    pass

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
                mycursor.execute(sqlcli)   
                mycliente= mycursor.fetchall()
                for  nombre,dni,estado in mycliente:
                    if estado == "P":
                        print(f"El cliente {nombre}, DNI numero = {dni}, tiene videos tomados en prestamo")
                        Sino=input("¿Quiere consultar sobre otro cliente? Si/No : ").upper()
                        if Sino=="NO":
                            Flag=False
                    else:
                        print(f"El cliente {nombre}, DNI numero = {dni}, NO tiene videos tomados en prestamo. Puede tomar prestado")
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
        #DNI, nombre_completo,Direccion, Estado, Telefono
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
                print(f"Nombre:{nom},DNI:{dni},Telefono:{tel},Direccion:{direc},Estado:{estado}")
                bien=input("Si lo datos son correctos escriba Si, sino escriba No:")
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
                    if tel>10:
                        print("Por favor ingrese el telefono sin codigo de area")
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
                bien=input("Si lo datos son correctos escriba Si, para seguir modificando escriba No:")
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
    #Muestra las peliculas y el codigo

    #Seleccion del DNI
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
    flag="Y"
    while True:
        flag=input((f"Usted va a Eliminar al cliente {mycliente}. ¿Desea continuar? Y/N").upper())
        if flag == "Y":
            sqldeletecli="DELETE FROM clientes WHERE DNI="+cliente+""
            mycursor.execute(sqldeletecli)
            print(f"Se ha eliminado de la base de datos el cliente {mycliente}")
            mydb.commit()
            break
        elif flag == "N":
            break
        else:
            print("Ingrese Y para continuar o N para Cancelar")
    


#GESTION DE PELIS/VIDEOS

#Alta de pelis
    #Ingreso datos
def ingreso_pelis():
        nom=input("Por favor ingrese el nombre de la pelicula:")
        nom=nom.title()
        gen=input("Ingrese el género:")
        gen=gen.title()       #Hay que hacer tabla aparte para genero
        while True:
            try:
                estado=input("Ingrese el estado de la pelicula (Disponible o No Disponible):")
                estado=estado.title()
                d="Disponible"
                n="No Disponible"
            except ValueError:
                print("Por favoe ingrese lo pedido")
            else:
                if estado!=d and estado!=n:
                    print("Por favor ingrese: Disponible o No disponible")
                else:
                    break
        return nom,gen,estado
    #chequear que todo este bien
def check_pelis_alta(nom,gen,estado):
        while True:
            try:
                print(f"Nombre:{nom},genero:{gen}, estado:{estado}")
                bien=input("Si lo datos son correctos escriba Si, sino escriba No:")
                bien=bien.upper()
            except ValueError:
                print("Por favor ingrese Si o No")
            if bien!="SI" and bien!="NO":
                print("Por favor ingrese Si o No")
            else:
                break
        return bien
    #Funcion menu alta
def alta_peli(mydb):
    bien="NO"
    while bien=="NO":
        nom,gen,estado=ingreso_pelis()
        bien=check_pelis_alta(nom,gen,estado)
    mycursor = mydb.cursor()
    sql= "INSERT INTO peliculas (Titulo, Genero, Estado)  VALUES (%s,%s,%s)"
    val=[
        (nom,gen,estado),
    ]
    mycursor.executemany(sql,val)
    mydb.commit()
    print(mycursor.rowcount, " registro insertado.")


#Modificacion peliculas    
    #Funcion para seleccionar la modificacion
def selec_modif_pelis():
    while True:
        try:
            print("1:Titulo   2:Genero   3:Estado")
            num=int(input("Ingrese el numero de lo que desee modificar: "))
        except ValueError:
            print("Por favor ingrese un numero")
        else:
            if num!=1 and num!=2 and num!=3:
                print("Por favor ingrese un numero válido")
            else:
                break
    return num
    #Funcion para modificar en si
def modif_pelis(num,mydb,peli):
    if num==1:
        nom=str(input("Ingrese el nombre:"))
        mycursor = mydb.cursor()
        sql = "UPDATE peliculas SET Titulo = '"+nom+"' WHERE Cod_Barra LIKE '%"+peli+"%'"
        mycursor.execute(sql)
        mydb.commit()
    elif num==2:
        gen=str(input("Ingrese el genero"))
        mycursor = mydb.cursor()
        sql = "UPDATE peliculas SET Genero = '"+gen+"' WHERE Cod_Barra LIKE '%"+peli+"%'"
        mycursor.execute(sql)
        mydb.commit()
    else:
        while True:
            try:
                estado=input("Ingrese el estado de la pelicula (Disponible o No Disponible):")
                estado=estado.title()
                d="Disponible"
                n="No Disponible"
            except ValueError:
                print("Por favoe ingrese lo pedido")
            else:
                if estado!=d and estado!=n:
                    print("Por favor ingrese: Disponible o No disponible")
                else:
                    break
        mycursor = mydb.cursor()
        sql = "UPDATE peliculas SET Estado = '"+estado+"' WHERE Cod_Barra LIKE '%"+peli+"%'"
        mycursor.execute(sql)
        mydb.commit()
    #loop´para modificar
def check_peli_modif(peli,mydb):
    while True:
        try:
            mycursor = mydb.cursor()
            sql = "SELECT * FROM peliculas WHERE Cod_Barra LIKE '%"+peli+"%'"
            mycursor.execute(sql)
            myresultado = mycursor.fetchone()
            print(myresultado)
            bien=input("Si lo datos son correctos escriba Si, para seguir modificando escriba No:")
            bien=bien.upper()
        except ValueError:
            print("Por favor ingrese Si o No")
        if bien!="SI" and bien!="NO":
            print("Por favor ingrese Si o No")
        else:
            break
    return bien    
#Funcion menu modificacion
def modificar_peli(mydb):
    #Muestra las peliculas y el codigo
    mycursor = mydb.cursor()
    sql = "SELECT Cod_Barra, Titulo FROM peliculas "
    mycursor.execute(sql)
    myresultado = mycursor.fetchall()
    listadoind=[]

    for pelicula, ind in myresultado:
        print("{} - {}".format(pelicula,ind))
        listadoind.append(pelicula)

    #Seleccionar la pelicula
    while True:
        try:
            peli=int(input("Ingrese el codigo de la pelicula a modificar:"))
        except ValueError:
            print("Por favor ingrese un número")
        else:
            if peli not in listadoind:
                print("Por favor ingrese un número de la lista mostrada")
            else:
                break
    peli=str(peli)
    #loop que hace todo
    bien="NO"
    while bien=="NO":
        num=selec_modif_pelis()
        modificacion=modif_pelis(num,mydb,peli)
        bien=check_peli_modif(peli,mydb)

#Eliminacion peliculas

def eliminar_peli(mydb):
    mycursor = mydb.cursor()
    sql = "SELECT Titulo, Cod_Barra FROM peliculas "
    mycursor.execute(sql)
    myresultado = mycursor.fetchall()
    listadoind=[]
    print(type(myresultado))
    for pelicula, ind in myresultado:
        print("{} - {}".format(pelicula,ind))
        listadoind.append(ind)
    print(listadoind)
    while True:
        try:
            peli=int(input("Ingrese el codigo de la pelicula a eliminar:"))
        except ValueError:
            print("Por favor ingrese un número")
        else:
            if peli not in listadoind:
                print("Por favor ingrese un número de la lista mostrada")
            else:
                break
    peli=str(peli)         
    sql2="DELETE FROM peliculas WHERE Cod_Barra LIKE '%"+peli+"%'"
    mycursor.execute(sql2)
    print(f"Se ha eliminado el registro de la pelicula numero {peli}")
    mydb.commit()

 #Consulta peliculas 

def consultar_pelis(mydb): 
    mycursor = mydb.cursor()
    sql = "SELECT Titulo, Cod_Barra FROM peliculas "
    mycursor.execute(sql)
    myresultado = mycursor.fetchall()
    listadoind=[]
    for pelicula, ind in myresultado:
        print("{} - {}".format(pelicula,ind))
        listadoind.append(ind)
    while True:
        try:
            peli=int(input("Ingrese el codigo de la pelicula a consultar: "))
        except ValueError:
            print("Por favor ingrese un numero")
        else:
            if peli not in listadoind:
                print("Por favor ingrese un numero de la lista mostrada")
            else:
                break
            
    peli=str(peli)
    mycursor2 = mydb.cursor()      
    sql2="SELECT Titulo, Cod_Barra, Genero, Estado FROM peliculas WHERE Cod_Barra = '"+peli+"' "
    mycursor2.execute(sql2)
    myresultado2 = mycursor2.fetchall()
    for pelicula, ind, gen, est in myresultado2:
	    print("{} - {} - {} - {}".format(pelicula,ind,gen, est))
    


#PRESTAMO VIDEOS

def consultar_peli_disponibles():
    pass

def registro_prestamo():
    pass

def registro_devolucion():
    pass

