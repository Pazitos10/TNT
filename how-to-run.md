### Para hacer correr la aplicación:
*AVISO: El presente tutorial asume que el sistema operativo utilizado es Ubuntu o derivado, el nombre de los paquetes puede variar dependiendo de la distribución elegida.*

Deben tenerse instalados los paquetes virtualenv y virtualenvwrapper para python 2.7.

Si no se dispone de pip:

    $ sudo apt-get install python-pip
Luego:

    $ sudo pip install virtualenv virtualenvwrapper

#### Paso 1:  Crear un virtualenv y comenzar a usarlo

    $ mkvirtualenv --python='python2' <nombre_entorno>
    $ workon ditenv

#### Paso 2: Instalar las dependencias

**Para Python**: Las dependencias se encuentran en el archivo requirements.txt, ubicado en la raíz de este repositorio. Para instalarlas procedemos a utilizar pip como sigue:

    (ditenv)$ pip install -r requirements.txt

*Observación*: el prefijo (ditenv) en el interprete bash indica que se está utilizando el virtualenv creado con anterioridad. Verifiquelo antes de intentar instalar los paquetes. De otro modo, el procedimento podría fallar.

**Para el sistema operativo**: Es necesario instalar [RabbitMQ](https://www.rabbitmq.com/), para hacer funcionar las tareas asincrónicas de [Celery](http://docs.celeryproject.org/en/latest/) (Paquete instalado como dependencia de python).

    $ sudo apt-get install rabbitmq-server

#### Paso 3: Correr el servidor

Si es la primera vez que ejecuta el servidor, lo mejor es aplicar las migraciones para tener la última versión del esquema de la base de datos.

    (ditenv)$ python manage.py migrate

A continuación, inicializamos la base de datos con la información de las materias:

    (ditenv)$ python manage.py initdb

Luego levantamos el servidor de desarrollo:

    (ditenv)carpeta_de_proyecto$ python manage.py runserver
    Performing system checks...

    System check identified no issues (0 silenced).
    July 04, 2016 - 21:34:12
    Django version 1.9.6, using settings 'tntserver.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Donde carpeta_de_proyecto es equivalente al directorio en el cual puede visualizarse el archivo manage.py

Si las migraciones ya han sido ejecutadas con anterioridad y la base de datos ya tiene el esquema actualizado y los datos cargados, solo ejecutamos el servidor:

    (ditenv)$ python manage.py runserver

#### Paso 4: Ejecutar Celery

Utilizando otra terminal, situarse en el mismo directorio que en el paso 3 y ejecutar:

    (ditenv)carpeta_de_proyecto$ celery -A tntserver worker -B -l info

| Opción | Utitlidad |
|-------|-----------|
|  -A, --app   | Instancia de aplicación (celery) a invocar. Fue definida en [celery.py](https://github.com/Pazitos10/TNT/blob/master/webapp/tntserver/tntserver/celery.py#L9)           |
| worker | Indica a Celery que ejecute un worker dedicado para la/s tarea/s definidas en nuestra instancia de aplicacion celery. |
|  -B   | Activa el scheduler de celery llamado Beat. Configurado en [settings.py](https://github.com/Pazitos10/TNT/blob/master/webapp/tntserver/tntserver/settings.py#L8)  |
|  -l, --loglevel   | Logging level, se debe elegir entre : DEBUG, INFO, WARNING, ERROR, CRITICAL, o FATAL. |

[Más información](http://docs.celeryproject.org/en/latest/genindex.html) sobre las opciones disponibles.

La salida a ese comando, mostrará entre otras cosas:

    ...
    [tasks]
    . tntapp.tasks.watch_calendars_task
    . tntserver.celery.debug_task

    [2016-07-04 21:39:35,590: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
    [2016-07-04 21:39:35,704: INFO/MainProcess] mingle: searching for neighbors
    [2016-07-04 21:39:36,726: INFO/MainProcess] mingle: all alone
    ...

Lo cual indica que todo funciona correctamente.

Opcionalmente, puede ejecutarse el ultimo comando y dejar a Celery correr en background como sigue:

    (ditenv)carpeta_de_proyecto$ celery -A tntserver worker -B &

Para detener a los workers, podremos hacer uso del comando kill. Podemos consultar el pid de los mismos y utilizar dicha informacion para eliminarlos como se muestra a continuación:

    ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill

De este modo permitimos que los workers completen sus tareas antes de terminar su ejecución.

Si se deseara eliminar a todos los workers sin esperar a que terminen sus tareas, podremos ejecutar:

    ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9

#### Paso 5: Utilizar la aplicación normalmente

Celery corre automáticamente una tarea cada 5 minutos que se encargará de verificar que los datos locales son consistentes con los datos de Google Calendar, y en caso contrario, actualiza los datos locales. Dado que dicha tarea es asincrónica no detiene el funcionamiento normal de la aplicación.

En un browser, nos dirigimos a la direccion:

    http://localhost:8000/

Donde veremos lo siguiente:

![](https://k60.kn3.net/A/E/1/4/9/D/16E.png)

A la izquierda un listado de todos los eventos registrados en los diferentes calendarios de la cuenta horarios.dit@gmail.com y a la derecha un mapa que indicará la posición de los diferentes lugares de dictado para los eventos mencionados anteriormente.
