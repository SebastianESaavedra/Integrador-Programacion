TP Integrador Técnicas de Programación

Trabajo práctico integrador desarrollado en Python y Mariadb en marco a la tecnicatura de Ciencia de Datos e Inteleigencia artificial.

Objetivos:

Gestion de Videoclub:
Cuenta con siguientes tablas:
- clientes : con los siguientes campos: DNI, Nombre Completo, Telefono, direccion, estado.
- peliculas (para el videoclub): campos: código de barra, titulo, genero, estado.
- prestamo: id, DNI cliente, código de barra, estado.

Cuenta con un menú con las siguientes opciones:
- Consulta de disponibilidad (de una pelicula, solo debe responder "Disponible" o "En préstamo al cliente ..Pepe..")
- Préstamo de Libro / Película : puede tener un sub-Menú que tenga las opciones:
        A - Consultar todos los títulos/películas disponible (verificando el campo estado)
        B - Registrar préstamo (deberá buscar el libro o película y cambiar el campo de estado a "P" de prestado y en el cliente con "O" de ocupado)
        C - Registrar Devolución (pedir datos necesarios para buscar el cliente y libro o pelicula y cambiar el campo de estado dejándolo con "D" de disponible)
- Gestión del cliente: tendrá un sub-menú:
        A - Alta de cliente
        C - Consulta estado del cliente
        M - Modificar teléfono o direccion del cliente
        E - Eliminar cliente (puede ser una baja lógica, es decir, cambiar su estado por ejemplo a Inahibilitado o Baja en lugar de eliminar al cliente).
- Gestión de Libro / Película: tendrá un sub-menu:
        A - Alta de Libro / película
        C - Consultar un libro/película (mostrando todos sus datos)
        M - Modificar Libro
        E - Eliminar Libro
