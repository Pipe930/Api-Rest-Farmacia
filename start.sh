
# Creation of the virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Installation of project dependencies
pip3 install -r requirements.txt

# Creation of the migrations folders
pais="./apps/pais/migrations"
pedidos="./apps/pedidos/migrations"
productos="./apps/productos/migrations"
usuarios="./apps/usuarios/migrations"
ventas="./apps/ventas/migrations"
sucursales="./apps/sucursales/migrations"

# Condiciones si las carpetas existen
if [ ! -d "$pais" ]; then
    # Create the folder
    mkdir "$pais"
    paisfile="$pais/__init__.py"
    touch "$paisfile"
else
    echo "La carpeta $pais ya existe."
fi

if [ ! -d "$pedidos" ]; then
    # Create the folder
    mkdir "$pedidos"
    pedidosfile="$pedidos/__init__.py"
    touch "$pedidosfile"
else
    echo "La carpeta $pedidos ya existe."
fi

if [ ! -d "$productos" ]; then
    # Create the folder
    mkdir "$productos"
    productosfile="$productos/__init__.py"
    touch "$productosfile"
else
    echo "La carpeta $productos ya existe."
fi

if [ ! -d "$usuarios" ]; then
    # Create the folder
    mkdir "$usuarios"
    usuariosfile="$usuarios/__init__.py"
    touch "$usuariosfile"
else
    echo "La carpeta $usuarios ya existe."
fi

if [ ! -d "$ventas" ]; then
    # Create the folder
    mkdir "$ventas"
    ventasfile="$ventas/__init__.py"
    touch "$ventasfile"
else
    echo "La carpeta $ventas ya existe."
fi

if [ ! -d "$sucursales" ]; then
    # Create the folder
    mkdir "$sucursales"
    sucursalesfile="$sucursales/__init__.py"
    touch "$sucursalesfile"
else
    echo "La carpeta $sucursales ya existe."
fi

# Creating the environment variable file path
env="./core/.env"

# Creating the environment variables file
touch "$env"

# User assignment of some environment variables
read -p "Ingrese el nombre de la base de datos: " name_database
read -p "Ingrese la contrasena de la base de datos: " password_database
echo "Para conseguir una secret key para el proyecto ingresa en esta pagina web"
echo "https://djecrety.ir"
read -p "Ingrese una secret key para el proyecto: " secret_key

# Create environment variables in the .env file
echo "NAME_DATABASE=$name_database"> "$env"
echo "USER_DATABASE=root">> "$env"
echo "PASSWORD_DATABASE=$password_database">> "$env"
echo "HOST_DATABASE=localhost">> "$env"
echo "PORT_DATABASE=3306">> "$env"
echo "SECRET_KEY=$secret_key">> "$env"
echo "DEBUG=True">> "$env"

# Creation of the files with the models
python manage.py makemigrations

# Creation of database tables
python manage.py migrate

# Creation of the super user
echo \n "Creacion del superusuario"
echo \n "Ingrese una contrasena"

python manage.py createsuperuser --username admin --first_name adminnombre --last_name adminapellido --email admin@gmail.com

# Project execution
python manage.py runserver