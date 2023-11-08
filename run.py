import pysftp
import sys

# Obtener los argumentos pasados al script
# argumento1 Nombre del ambiente (web1, web2, web3, etc)
# argumento2 Nombre del modulo (core, account, checkout)
# argumento3 Muestra los archivos 'module' del repositorio
argumentos = sys.argv
if len(argumentos) >= 3:
    ambiente = argumentos[1]
    nombre_modulo = argumentos[2]
    show_modules = False
    
    if len(argumentos) == 4:
        show_modules = argumentos[3]
else:
    print("Faltan argumentos para continuar")
    sys.exit()

# Conectarse al servidor SFTP
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  # Para evitar la verificación de la clave del host (no se recomienda en un entorno de producción)
sftp_host = 'host'
sftp_username = 'username'
sftp_password = 'password'

remote_directory = f'../usr/share/nginx/html/{ambiente}/tienda/resources/js/{nombre_modulo}'
git_dir = f'--git-dir={remote_directory}/.git'
sop_number = ""
nombre_del_arreglo = ""

def decode(output_array):
    return [line.decode('utf-8').rstrip('\n') for line in output_array]

def git_branch():
    branch = decode(sftp.execute(f'git {git_dir} branch'))
    
    print(branch)
    if any('*' in elemento and "master" in elemento for elemento in branch):
        print("Actualmente en master")
    else:
        # TODO: manejar casos donde falle checkout, como branch behind 'origin/master' o 
        # local changes to the following files would be overwritten
        sftp.execute(f'git {git_dir} checkout master')
        print("Ahora: " + str(decode(sftp.execute(f'git {git_dir} branch'))))
        
def gitAdd():
    # Especifica la ruta completa al directorio .git
    git_status_output = sftp.execute(f'git --git-dir={remote_directory}/.git status --porcelain')
    git_status_output = decode(git_status_output)
    
    # Crea una lista para almacenar los archivos con cambios
    files_to_add = []

    # Recorre las líneas de la salida y muestra los archivos con un índice
    for index, line in enumerate(git_status_output):
        if line.startswith(" M "):
            if (show_modules == False) and ("modules" in line):
                break
            else:
                files_to_add.append((index, line))
                print(f"[{index}] {line}")           

    if len(files_to_add) > 0:
        # Pide al usuario que ingrese los índices de los archivos que desea agregar con git add
        indices = input("Ingrese los índices de los archivos que desea agregar (separados por espacios, 'A' para agregarlos todos): ")
        if indices == "A" or indices == "a":
            # Si el usuario ingresa 'A', agregar todos los archivos
            for file_line in files_to_add:
                file_path = file_line[1].split()[1]
                git_add = sftp.execute(f'git --git-dir={remote_directory}/.git add {file_path}')
                print(f" - Se ha agregado '{file_path}' con éxito al repositorio.")
        else:
            # Divide los índices ingresados por el usuario y los convierte a una lista de números
            indices = [int(i) for i in indices.split()]

            # Ejecuta el comando 'git add' para los archivos seleccionados
            for index in indices:
                if 0 <= index < len(files_to_add):
                    file_line = files_to_add[index]
                    file_path = file_line[1].split()[1]
                    git_add = sftp.execute(f'git --git-dir={remote_directory}/.git add {file_path}')
                    print(f"- Se ha agregado '{file_path}' con éxito al repositorio.")
    else:
        print("No se encontraron cambios en el repositorio")
        
def reemplazar_espacios_con_guiones(cadena):
    # Utiliza el método replace para reemplazar espacios con guiones
    cadena_con_guiones = cadena.replace(' ', '-')
    return cadena_con_guiones

def git_checkout_new_branch():
    global sop_number
    global nombre_del_arreglo
    sop_number = input("SOP: ")
    nombre_del_arreglo = input(f'Nombre de rama: feature/SOP-{sop_number}/[nombre del arreglo] ')
    nombre_del_arreglo = reemplazar_espacios_con_guiones(nombre_del_arreglo)
    sftp.execute(f'git {git_dir} checkout -b \'feature/SOP-{sop_number}/{nombre_del_arreglo}\'')
    print(decode(sftp.execute(f'git {git_dir} fetch --all')))
    print(decode(sftp.execute(f'git {git_dir} pull origin master')))

def git_commit():
    global sop_number
    commit_message = input("Escribe el mensaje del commit: ")
    print(decode(sftp.execute(f'git {git_dir} commit -m \'feature/SOP-{sop_number}/{commit_message}\'')))

def git_push():
    global sop_number
    global nombre_del_arreglo
    print(decode(sftp.execute(f'git {git_dir} push origin feature/SOP-{sop_number}/{nombre_del_arreglo}')))

# TODO: Manejar excepciones
with pysftp.Connection(sftp_host, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
    print("Conectado\n")
    git_branch()
    git_checkout_new_branch()
    gitAdd()
    git_commit()
    git_push()
    print("\nProceso finalizado.")
    