@REM Creacion del Proyecto

@echo off

@REM Nombre del entorno virtual
set "nombre_entorno=env"

@REM Creacion del entorno virtual
python -m venv %nombre_entorno%

@REM Activar el entorno virtual
call %nombre_entorno%\Scripts\activate.bat

@REM Instalacion de la libreria de django
pip install -r requirements.txt

@REM Creacion de las carpetas migrations
mkdir .\apps\pais\migrations
mkdir .\apps\productos\migrations
mkdir .\apps\sucursales\migrations
mkdir .\apps\usuarios\migrations
mkdir .\apps\ventas\migrations
mkdir .\apps\pedidos\migrations

@REM Asignacion de las rutas de las carpetas
set "pais=.\apps\pais\migrations"
set "productos=.\apps\productos\migrations"
set "sucursales=.\apps\sucursales\migrations"
set "usuarios=.\apps\usuarios\migrations"
set "ventas=.\apps\ventas\migrations"
set "pedidos=.\apps\pedidos\migrations"

set "init_pais=%pais%\__init__.py"
set "init_productos=%productos%\__init__.py"
set "init_sucursales=%sucursales%\__init__.py"
set "init_usuarios=%usuarios%\__init__.py"
set "init_ventas=%ventas%\__init__.py"
set "init_pedidos=%pedidos%\__init__.py"

@REM Creacion de los archivos __init__.py dentro de las carpetas migrations
echo. > "%init_pais%"
echo. > "%init_productos%"
echo. > "%init_sucursales%"
echo. > "%init_usuarios%"
echo. > "%init_ventas%"
echo. > "%init_pedidos%"

@REM Creacion de las variavles de entorno
set "archivoenv=.\farmacia\.env"

@REM Ingresar informacion para las variables de entorno
set /p "name_database=Ingrese el nombre de la base de datos: "
set /p "password_database=Ingrese la contrsena de la base de datos: "

echo NAME_DATABASE='%name_database%'> "%archivoenv%"
echo USER_DATABASE=root>> "%archivoenv%"
echo PASSWORD_DATABASE='%password_database%'>> "%archivoenv%"
echo HOST_DATABASE=localhost>> "%archivoenv%"
echo PORT_DATABASE=3306>> "%archivoenv%"

@REM Creacion de los archivos con los modelos
python manage.py makemigrations

@REM Creacion de las tablas de la base de datos
python manage.py migrate

@REM Creacion del super usuario

echo \n "Creacion del superusuario"
echo \n "Ingrese una contrasena"
python manage.py createsuperuser --username admin --nombre nombreadmin --apellido apellidoadmin --correo admin@gmail.com

@REM Ejecucion del proyecto
python manage.py runserver
