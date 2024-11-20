## Paso a paso para probar este proyecto en tu ordenador

# Guía de Instalación y Configuración

Esta guía te ayudará a configurar el entorno necesario para probar la aplicación en tu dispositivo. Sigue los pasos detallados a continuación.

## Tabla de Contenidos

1. [Prerequisitos](#prerequisitos)
2. [Creación del Entorno Virtual](#creación-del-entorno-virtual)
3. [Instalación de Dependencias](#instalación-de-dependencias)
4. [Obtención de las API Keys](#obtención-de-las-api-keys)
    - [OpenAI](#openai)
    - [Groq](#groq)
    - [Serper](#serper)
5. [Configuración del Archivo de Entorno](#configuración-del-archivo-de-entorno)
6. [Ejecución del Notebook](#ejecución-del-notebook)
7. [Resolución de Problemas](#resolución-de-problemas)

---

## Prerequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

- **Python 3.7 o superior**: Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- **Git** (opcional, pero recomendado para clonar el repositorio).
- **Acceso a internet** para descargar dependencias y obtener las API Keys.

## Creación del Entorno Virtual

Es recomendable utilizar un entorno virtual para aislar las dependencias de este proyecto de otros en tu sistema.

1. **Abre una terminal** en tu sistema operativo.
2. **Navega** al directorio donde deseas clonar o tener tu proyecto.
3. **Crea el entorno virtual** ejecutando el siguiente comando:

    ```bash
    python -m venv nombre_del_entorno
    ```

    Reemplaza `nombre_del_entorno` con el nombre que prefieras para tu entorno virtual.

4. **Activa el entorno virtual**:

    - **En Windows**:

        ```bash
        nombre_del_entorno\Scripts\activate
        ```

    - **En macOS/Linux**:

        ```bash
        source nombre_del_entorno/bin/activate
        ```

    Después de activar, tu terminal debería mostrar el nombre del entorno virtual al inicio de la línea de comandos.

## Instalación de Dependencias

Con el entorno virtual activado, instala las dependencias necesarias utilizando el archivo `requirements.txt`.

1. **Asegúrate** de estar en el directorio raíz del proyecto donde se encuentra `requirements.txt`.
2. **Ejecuta** el siguiente comando:

    ```bash
    pip install -r requirements.txt
    ```

    Este comando instalará todas las librerías y paquetes necesarios para ejecutar la aplicación.

## Obtención de las API Keys

La aplicación requiere claves de API para interactuar con los servicios de OpenAI, Groq y Serper. A continuación, se explica cómo obtener cada una de ellas.

### OpenAI

1. **Regístrate** o **inicia sesión** en [OpenAI](https://platform.openai.com/).
2. Navega a la sección de **API Keys** en tu cuenta.
3. **Genera una nueva clave** y cópiala. La necesitarás más adelante.

### Groq

1. **Visita** el sitio oficial de [Groq](https://www.groq.com/) para obtener más información sobre cómo obtener una API Key.
2. **Regístrate** y sigue las instrucciones para generar tu clave de API.

### Serper

1. **Accede** a [Serper](https://serper.dev/?gad_source=1&gclid=CjwKCAiArva5BhBiEiwA-oTnXTP0RDl86d5bR2bCJDOJ0HBjX4zu3tIHgt26s_KTYoh0ic16MzR9txoCrl4QAvD_BwE).
2. **Regístrate** para obtener acceso a la API.
3. **Genera** y **copia** tu clave de API una vez que se te proporcione.

## Configuración del Archivo de Entorno

Para que la aplicación funcione correctamente, debes configurar un archivo de entorno con tus claves de API.

1. **Crea** un archivo llamado `.env` en el directorio raíz del proyecto.
2. **Abre** el archivo `.env` con tu editor de texto preferido.
3. **Añade** las siguientes líneas, reemplazando cada valor con tu respectiva clave de API:

    ```env
    OPENAI_API_KEY=tu_clave_de_openai
    SERPER_API_KEY=tu_clave_de_serper
    GROQ_API_KEY=tu_clave_de_groq
    ```

    Asegúrate de **no dejar espacios** alrededor del signo `=` y **no incluir comillas**.

4. **Guarda** el archivo `.env`.

## Ejecución del Notebook

Ya deberia estar todo preparado para ejecutar las distintas celdas del notebook.

## Resolución de Problemas

Si encuentras algún problema durante la instalación o ejecución, considera lo siguiente:

- **Entorno Virtual No Activado**: Asegúrate de haber activado el entorno virtual antes de instalar dependencias o ejecutar el notebook.
- **Claves de API Incorrectas o Faltantes**: Verifica que todas las claves de API estén correctamente configuradas en el archivo `.env`.
- **Dependencias Faltantes**: Revisa que todas las dependencias se hayan instalado sin errores. Puedes intentar reinstalar ejecutando `pip install -r requirements.txt`.
- **Problemas con el Kernel de Jupyter**: Asegúrate de que el kernel seleccionado en Jupyter corresponde al entorno virtual donde instalaste las dependencias.

Para asistencia adicional, no dudes en hablarme directamente por linkedin www.linkedin.com/in/saul-gomez-jimenez-47b30328b


---


