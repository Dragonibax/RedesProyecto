Antes de correr el proyecto hay que borrar la database.db si es que tiene alguna,
porque las tablas fueron modificadas ligeramente.

Conexión SSH:
    - 1. Hay que insertar el router que tienes en tu topología,
         los datos de ese router los pasas al objeto Router que se encuentra en 
         apps.protocols.routes -> insert, eso registra el router en la base de datos.

         El router en  gns3 debe estar configurado con los siguientes comandos después de su creación
            configure terminal
            #aqui se levantan las interfaces que tengas, una vez terminado, seguir a la línea de abajo
            enable secret unsecreto
            line vty 0 4 
            password unacontraseña
            login
            username unusuario
        
        Con los comandos anteriores habilitamos telnet, al registrar el router en la base de datos,
        unsecreto, unacontraseña y unusuario deben ser los valores que se guardan en la tabla del router.
        Recomiendo que todo sea "admin".

    - 2. Una vez realizado el paso anterior, deberás hacer click en el apartado "Usuarios" del nav,
         esto hará que se desplieguen los routers registrados en la bd e indicará si disponen o no de 
         ssh. Si ssh está inhabilitado entonces dar click al botón y esto habilitará ssh con un usuario por
         defecto llamado root con contraseña root. 
    
    - 3. Cuando se habilita ssh por primera vez, es necesario generar las llaves para ese router,
         de otra forma netmiko manda un error que no es detectado por el sistema y el usuario se registra   
         en la bd sin estar registrado en el router.

    - 4. Una vez habilitado ssh en un router y generado las llaves en la terminal de linux, es posible
         enviar comandos tanto de configuración como tipo show, utilizando las funciones definidas en 
         security.sshconnection

Posibles fallas en linux:
    Cuando corres el proyecto en linux puede salir un error relacionado a werkzeug.safe_str_cmp
    si este es el caso entonces ejecutar los siguientes comandos la terminal.

    pip uninstall werkzeug (o pip3 si es que pip no es reconocido)
    pip install werkzeug==2.0.0

    Con eso debería funcionar todo.

    MODULOS PARA SNMP
    pip install cairosvg
    pip install pysnmp-mibs
    pip install pysnmp
    pip install pygal