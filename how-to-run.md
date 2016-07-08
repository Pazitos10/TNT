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

**Para el sistema operativo**: Es necesario instalar [RabbitMQ](https://www.rabbitmq.com/), para hacer funcionar las tareas asincrónicas de [Celery](http://docs.celeryproject.org/en/latest/) (Paquete instalado como dependencia de python) y [Redis](http://redis.io/) para la comunicacion asincrónica de Django con el cliente a través de [channels](http://channels.readthedocs.io/en/latest/) y [websockets](https://developer.mozilla.org/es/docs/WebSockets-840092-dup).

    $ sudo apt-get install rabbitmq-server

[Guía de instalación de Redis](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis)

**Observación**: Llevar a cabo sólo lo detallado en el  apartado "Installing Redis" para instalar y comprobar la correcta ejecución

#### Paso 3: Correr el servidor

Si es la primera vez que ejecuta el servidor, lo mejor es aplicar las migraciones para tener la última versión del esquema de la base de datos.

    (ditenv)carpeta_de_proyecto$
    (ditenv)carpeta_de_proyecto$ python manage.py migrate

A continuación, inicializamos la base de datos con la información de las materias:

    (ditenv)carpeta_de_proyecto$ python manage.py initdb

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

| Opción | Utilidad |
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

Celery corre automáticamente una tarea cada 1 minuto que se encargará de verificar que los datos locales son consistentes con los datos de Google Calendar, y en caso contrario, actualiza los datos locales y notifica a los usuarios conectados para que estos actualicen su lista si así lo desean.
Dado que dicha tarea es asincrónica no detiene el funcionamiento normal de la aplicación.

En un browser, nos dirigimos a la direccion:

    http://localhost:8000/

Donde veremos lo siguiente:

![](https://k60.kn3.net/A/E/1/4/9/D/16E.png)

A la izquierda un listado de todos los eventos registrados en los diferentes calendarios de la cuenta horarios.dit@gmail.com y a la derecha un mapa que indicará la posición de los diferentes lugares de dictado para los eventos mencionados anteriormente.

Si en Google Calendar se agrega, modifica o elimina un evento, el usuario recibe una notificación para actualizar la lista.

Por ejemplo, en la siguiente imagen se muestra la lista de eventos locales y los cargados en google calendar (en este último, crearemos un evento)
![preevento](https://k61.kn3.net/D/1/F/8/A/A/9CE.png)

Aquí vemos el evento ya creado.
![postevento](https://k61.kn3.net/B/3/3/5/E/D/D2A.png)

En la terminal se puede ver como Celery toma la nueva tarea para ejecutarla (terminal de la derecha: "Received Task...")
![terminal](https://k61.kn3.net/7/8/0/9/0/F/00A.png)

Como resultado de la ejecución, en la pantalla de los usuarios se muestra la notificación correspondiente. Sólo se mostrarán las actualizaciones cuando el usuario haga clic en el símbolo de recarga de la misma.
![notificacion](https://k60.kn3.net/2/4/C/6/7/0/B5D.png)

Podemos observar como resultado, el evento que creamos en Google Calendar, ya esta presente en los datos locales y disponibles para todos los usuarios.
![resultado](https://k61.kn3.net/F/0/8/7/C/7/1BC.png)
