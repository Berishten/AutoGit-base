
# AutoGit-Samurai

Automatiza la creación y subida de cambios al repositorio.

## Configuración del Entorno Virtual (venv)

Para ejecutar este proyecto, se recomienda configurar un entorno virtual de Python. Siga estos pasos para configurar su entorno virtual:

### 1. Instalar Python

Si no tiene Python instalado, descargue e instale Python desde [el sitio web oficial de Python](https://www.python.org/downloads/).

### 2. Instalar `virtualenv`

Si no tiene `virtualenv` instalado, puede hacerlo ejecutando el siguiente comando en git bash o windows (solo con el python en el path)

``` bash
pip install virtualenv
```

***Si no funciona, verifica que agregaste python en el path***

### 3. Crear el Entorno Virtual

Abra un terminal en la carpeta del proyecto y ejecute el siguiente comando para crear un entorno virtual en el directorio de su proyecto (reemplace myenv con el nombre que desee para su entorno virtual):

``` bash
# En Unix
python3 -m venv nombre_del_entorno
# En windows
python -m venv nombre_del_entorno
```

### 4. Activando el venv

``` bash
# En unix
source nombre_del_entorno/bin/activate
# En windows
nombre_del_entorno\Scripts\activate
```

### 5. Instalar Dependencias

Una vez que el entorno virtual esté activado, instale las dependencias de este proyecto desde el archivo requirements.txt proporcionado con el siguiente comando:

``` py
pip install -r requirements.txt
```

# 6. Ejecutando el script

``` py
# Ambiente (web1, web2, etc)
# Modulo (core o checkout o account)
# True para mostrar archivos "modules" del repositorio (opcional)
python run.py ambiente modulo opcional
```
