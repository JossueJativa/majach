# Proyecto para empresa Majach
El principal objetivo de esta tienda es vender objetos que traen de Estados Unidos hacia Ecuador, donde quieren una forma más eficiente de llegar a las personas, dando más oportunidades de ver todo su catálogo de compras.

### Objetivo de Majach
Para Majach su objetivo es traer distintos tipos de catálogos para todo tipo de personas que se interesen en comprar cosas de alta calidad en menor precio, entonces al realizar una aplicación de compra de artículos, con sus vendedores atentos a los nuevos compradores, se realiza de forma rápida la compra y de manera segura.

### Que tecnologías se usó
Para este proyecto se utilizó un framework llamado Django, en donde se trata de hacer un back-end seguro para cualquier cambio con respecto a las bases de datos se haga de manera segura y sin necesidad de andar tocando las mismas

### Dificultades y expectativas para implementar
En este proyecto se presentó dificultades para enviar información desde el back-end hasta el front-end para dar información gráfica de todos los productos que se presenta en Majach.

#### Features
* Se utiliza una forma gráfica de presentar estadística con respecto a una librería llamada Apache EChart donde enviando un JSON con la información necesaria, nos genera un gráfico representativo de como van las ventas y como se ha realizado la calificación de los productos para ver como mejorar y saber que es lo que se puede comprar para mejorar la calidad de venta.

* Se realiza una forma de ver que comprador a realizado la mayor cantidad de compras en general y poder actuar en accion con respecto a lo que hacen.

# Como instalar dependencias
Como tratamos con Django, necesitamos tener algunas instalaciones, se necesita si o si tener instalado Python en sus dispositivos, y el link de instalación de Python puede sacarse de Google como en estos links:
* Python en web: [Python Web](https://www.python.org/downloads/)
* Python en Microsoft Store: [Python Microsoft](https://apps.microsoft.com/detail/9pjpw5ldxlz5?hl=en-US&gl=US)

Después de tener las dependencias listas, lo que necesitaremos un entorno virtual **Esto es recomendado para hacer aplicaciones con Django**, al ya tener instalado Python, pondremos el siguiente comando para crear una instancia de variable de entorno
> python -m venv <nombreDeEntorno>

Un ejemplo sería poner 

> python -m venv env

Después dependiendo de en donde se esté trabajando, como en MAC, LINUX y WINDOWS, se realizaran distintas formas de activar el entorno virtual, estos siendo así
* WINDOWS
> env\Scripts\activate
* LINUX y MAC
> source env\bin\activate

Al tener listo el entorno, te aparecerá en la consola de comandos `(env)` o `<NombreDeEntorno>` delante de toda la ruta de tus comandos y ahí sabremos que estamos dentro de la variable de entorno.

Por último vamos a realizar las instalaciones dentro de nuestra variable de entorno, llegando a ser estos dos comandos:
```
> pip install django
> pip install pillow
```

> [!NOTE]
> Con respecto a lo que es el proyecto, muchas funciones no van a compilar, ya que hará falta un archivo de configuración, llamado config.py que esta omitiéndose en él .gitignore

Después de ver esta nota, sabrán que se necesitara si o si un archivo de config.py para correr el proyecto de forma correcta, donde se necesitara dentro del mismo una configuración así:
```
EMAIL_HOST = Tipo de host como 'smtp.mail.yahoo.com', 'smtp.gmail.com', 'smtp.office365.com', 'smtp.mail.me.com', etc
EMAIL_PORT = Puerto del correo de la persona auspíciente
EMAIL_HOST_USER = Correo de la persona auspíciente
EMAIL_HOST_PASSWORD = contraseña de aplicación del email
EMAIL_USE_TLS = Booleano, True o False
```
Al terminar nuestro archivo de configuración podremos ejecutar nuestro proyecto con los comandos siguientes, los cuales tendremos su explicación de que hace cada uno
```
> python manage.py makemigrations // Este llega a comprobar si las migraciones a las bases de datos pueden dar error
> python manage.py migrate // Este hace que las migraciones se lleguen a hacer en la base de datos
> python manage.py runserver // Este hace que el proyecto ya se encuentre listo para ingresar como página web
```
Al ejecutar el `runserver` nos va a aparecer el siguiente mensaje por debajo de nuestro comando ejecutado
```
System check identified no issues (0 silenced).
May 08, 2024 - 18:48:08
Django version 5.0.4, using settings 'majachi.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
Y para ingresar a nuestra página web, tendremos que entrar al siguiente link: `http://127.0.0.1:8000/` yo siempre recomendaré entrar en modo incógnito, ya que Django guarda muchas cookies, entonces si se llega a hacer un cambio, y no quieras borrar las cookies cada que abras el proyecto, recomiendo entrar en modo incógnito de tu navegador web.

# Como usar el proyecto
El proyecto primero necesitaremos un superusuario para crear un usuario administrador, entonces para crear un superusuario se llega a ingresar el siguiente comando
```
> python manage.py createsuperuser
```
Y con ese comando te llega a pedir `Usuario`, `Correo`, `Contraseña`, `Confirmar Contraseña`, si esta contraseña llega a ser muy simple, Django te pedirá una confirmación, pero de ahí se genere con total normalidad, y para ingresar a loguearte como un superusuario necesitas entrar al siguiente enlace: `http://127.0.0.1:8000/admin` y aquí te pedirá que te ingreses con las credenciales de superusuario donde te aparecerá esta pantalla:
<img src="./img_readme/Screenshot 2024-05-09 115023.png" alt="Imagen de logueo de superusuario">
Esta es donde pondrás el usuario y la contraseña que creaste con el superusuario, después de ingresar aparecerá esta pantalla: 
<img src="./img_readme/Screenshot 2024-05-09 114929.png" alt="Imagen de superusuario">
Aquí es donde ingresaremos a `Users` y haremos clic en `ADD USER +` y cuando nos salga toda esta información:
<img src="./img_readme/Screenshot 2024-05-09 115251.png" alt="Imagen de creacion de usuario">
Bajaremos hasta que encontremos unos botones que diga `Is admin` y ahí le daremos clic para crear un usuario administrador
> [!NOTE]
> Se deben completar todos los campos requeridos, eso quiere decir todos los que están en negrilla para crear el usuario correctamente

De ahí nos podemos hacer `LOG OUT` e ingresar al link `http://127.0.0.1:8000/` para ya hacer login como administrador, y realizar las acciones que hace un admin, donde nos aparecerá estos tres botones: 
<img src="./img_readme/Screenshot 2024-05-09 115606.png" alt="Imagenes de Administracion" width="100%">
Y de aquí los importantes son el primer y segundo icono, el tercero es para ver información sobre el administrador.

# Diseño de ingenieria

### Administrador
Al mostrar el segundo icono, es donde nosotros llegamos a administrar los productos que se quiera vender

> [!NOTE]
> Aquí se necesitará primero ingresar al superusuario para crear las categorías que pondremos para nuestros objetos

Y también se podrá ingresar los vendedores que van a estar de responsables para la función de realizar la venta de forma exitosa
<img src="./img_readme/Screenshot 2024-05-09 120038.png" alt="Imagen de administrador tuerca">

Por último en la parte de las estadísticas donde al inicio nos aparecerá un formulario para filtrar información por fechas:
<img src="./img_readme/Screenshot 2024-05-09 121204.png" alt="Imagen de estadísticas">
Al poner alguna fecha se llenarán los campos con respecto a lo que necesitaremos comparar entre productos más vendidos entre esas fechas, y productos con más estrellas entre esas fechas

> [!IMPORTANT]
> Las filtraciones de información por fecha en la parte de productos con más estrellas, se realiza por medio de los comentarios que hace las personas que tiene cuenta y quieren dar su opinión con estrellas en los comentarios de la aplicación

Al finalizar y poner las fechas con respecto a lo que queremos filtrar, se verán los gráficos respectivos de que tiene más estrellas y productos vendidos en esas etapas
<img src="./img_readme/Screenshot 2024-05-09 121605.png" alt="Imagen con filtro de fechas">

### Como funciona el administrador
El administrador se centra en ver y categorizar cada producto, viendo nuestra tabla de datos en Entidad-Relación vemos como se categoriza cada información y como se une cada una de ellas, esta relación hará referencia siempre a como se venden las cosas, la relación entre clientes y vendedores, el carrito de compras que se tiene, y toda la información que se mostrara en forma gráfica para el administrador tiene relación con nuestras tablas
<img src="./img_readme/Imagen1.png" width="100%" style="background-color:white" alt="Diagrama entidad relación">

El administrador al tener la capacidad de ingresar de forma sencilla y simple los productos y realizar de manera sencilla el contrato de personal, se llega a ver como realiza acciones de ingreso de data para nuestro CORE de aplicación, y como este mismo puede eliminar comentarios o hacer acciones como comentar en los mismos artículos, podrá modificar las estadísticas a su gusto, **pero esto no llega a ser ético del todo** entonces esto es más para comprobar y manipular datos de forma sencilla

De aqui podremos ver como se puede ingresar a la aplicacion por medio del diagrama de flujo, aqui se puede ver como se ingresa el administrador, el vendedor y el comprador mediante una verificacion de roles.
<img src="./img_readme/Imagen2.png" width="100%" style="background-color:white" alt="Diagrama de flujo">

# Principios SOLID y Patrones de Dieño
## Principios SOLID
### SRP (Single Responsability Principle): 
Este principio solid hace referencia a que cada clase debe tener únicamente una sola responsabilidad. En este caso las clases como tal únicamente tienen la responsabilidad de crear una instancia en la base de datos. 

### Open Closed Principle: 
Este principio hace referencia a cuando se pretenda introducir un comportamiento ya existente en el sistema, se deberán crear nuevas clases, pero usando herencia de una clase padre o inyectando dependencias para poder dar la funcionalidad que se quiere, en este caso podemos ver que la clase usuarios hereda de otra clase llamada AbstractUser, y a esta se le agregan todas las funcionalidades que se requieran 

### Interface Segregation: 
Este principio tiene como objetivo desacoplar el código en dependencias directas, haciendo que no se dependa de cales superarlos o inferiores, pero de su abstracción. Esto da origen a inyección de dependencias donde una clase inyecta objetos a otra en vez de tener que instanciar los objetos. Esto lo podemos ver cuando vemos un Foreign Key en las clases ya que se esta haciendo referencia a otros datos, sin tener que instanciarlos. 

## Patrones de Diseño
### Builder: 
Builder es un factor el cual ayuda en la construcción de las clases en la base de datos, para realizarlo de mejor manera y con menos lineas de código, para eso se ayuda de la clase normal que se instancia en la base de datos y el buider se encarga de construir y guardar los datos correctamente en la clase para que se agreden en la base de datos con la clase 
### Factory Method: 
Es el cual se realiza al crear una clase, y de ella pueden salir mas de un objeto, como en este ejemplo se hace para que se puedan crear distintos tipos de usuarios con la clase de factory method