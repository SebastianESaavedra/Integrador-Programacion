from funcionespropias import *
import mariadb 

menu="Y"
menu2="Y"

menu1={0:"Consulta de Disponibilidad",1:"Prestamo de Videos",2:"Gestion del Cliente", 3:"Gestion de Peliculas",4:"Salir"}

submenus={1:[(0,"Consultar pelis disponibles"),(1,"Registrar prestamo"),(3,"Registrar devolución"),(4,"Volver")],2:[(0,"Alta Cliente"),(1,"Consultar estado del cliente"),(2,"Modificar teléfono o direccion del cliente"),(3,"Eliminar cliente"),(4,"Volver")],3:[(0,"Alta de Peli"),(1,"Consultar Pelicula"),(2, "Modificar Pelicula"),(3, "Eliminar Pelicula"),(4,"Volver")]}

menus_sql={"0":disponibilidad,"1.0":consultar_peli_disponibles,"1.1":registro_prestamo,"1.2":registro_devolucion,"1.4":volver,"2.0":alta_cliente,"2.1":estado_cliente,"2.2":mod_cliente,"2.3":eliminar_cliente,"2.4":volver,"3.0":alta_peli,"3.1":consultar_pelis,"3.2":modificar_peli,"3.3":eliminar_peli,"3.4":volver,"4":salir}

mydb = mariadb.connect(
            host="127.0.0.1",
            user="root",
            autocommit=True
        )

mydb = mariadb.connect(
            host="127.0.0.1",
            user="root",
            database= "VIDEOCLUB"
        )

#eliminar_peli(mydb)


while menu == "Y":
    menu2="Y"
    print("----- MENU VIDEOCLUB ------")
    print("----- Ingrese una de estas opciones ------")
    for i in range(len(menu1)):
        print("{}.{}".format(i,menu1[i]))
    opcion1=int(input("Ingrese un numero según la opcion que desea elegir: "))
    while menu2=="Y":
        if opcion1 in submenus.keys():
            print("----- MENU :{} ------".format(menu1[opcion1]))
            for i in range(len(submenus[opcion1])):
                (a,b)=(submenus[opcion1][i])
                print("{}...{}".format(a,b))
            opcion2=int(input("Ingrese un numero según la opcion que desea elegir: "))
            print("Usted ha elegido {}".format(submenus[opcion1][opcion2]))
            if opcion2==4:
                print("-------------------------------------\n")
                menu2=menus_sql["{}.{}".format(opcion1,opcion2)](mydb)
                print("-------------------------------------\n")
                break
            else:
                menus_sql["{}.{}".format(opcion1,opcion2)](mydb)

        elif opcion1==4:
            print("---------------------------------------------\n")
            print("Usted selecciono SALIR. Muchas gracias. ¡Adios!\n")
            print("---------------------------------------------\n")
            menu2=menus_sql["{}".format(opcion1)](mydb)
            menu=menus_sql["{}".format(opcion1)](mydb)
            
        elif opcion1 in menu1.keys():
            print("Usted ha elegido {}".format(menu1[opcion1]))
            menus_sql["{}".format(opcion1)](mydb)

        else:
            print("Ingrese un numero valido por favor")

mydb.close()



