# TNT
Documentación del Trabajo Práctico

## Calendarios de Materias
Cada materia utiliza un calendario propio. El mismo puede ser compartido a la dirección del profesor titular de la materia de manera que el profesor pueda administrar desde su cuenta de GMail el calendario de la materia, sin que esto repercuta en los calendarios del resto de las materias

### Creación de un Calendario
Para crear un calendario:

1. Acceder a [Google Calendar](http://calendar.google.com) con la cuenta de usuario del DIT.
2. Debajo del listado de *Mis Calendarios* en el frame de la izquierda, hacer clic en la opción *Crear calendario nuevo*.
![](https://k61.kn3.net/C/B/7/7/2/6/CB4.png)
3. Dar nombre al calendario siguiendo la forma **[codigo-materia] - [nombre-materia]** donde:
	* **[codigo-materia]** Es el código alfanumérico de la materia de acuerdo al [Plan de Estudios](http://www.ing.unp.edu.ar/info_lic_informatica_2010_c.htm).
	* **[nombre-materia]** Es el nombre de la materia de acuerdo al [Plan de Estudios](http://www.ing.unp.edu.ar/info_lic_informatica_2010_c.htm).
4. Ingresar si se desea una descripción y en Lugar indicar la Ciudad, en nuestro caso *Trelew*.
5. Seleccionar la opción *Hacer público este calendario*.
6. Finalmente hacer clic en el botón de *Crear calendario*.
![](https://k60.kn3.net/D/E/0/8/C/F/691.png)
7. Para obtener el **ID del calendario** asignado por Google, hacer clic en el menú contextual del menú y ahí en *Configuración del calendario*.
![](https://k60.kn3.net/B/7/3/2/F/0/2E3.png)
8. En la sección titulada *Dirección del calendario* aparece el **ID del calendario**.
![](https://k61.kn3.net/8/3/1/6/7/E/22C.png)

### Compartir un Calendario
Para compartir un calendario con un profesor, siga los siguientes pasos:

1. Desde la cuenta del DIT, ingresar en Google Calendar. Seleccionar la Opción *Compartir este calendario* desde el menú contextual de la materia.
![](https://k61.kn3.net/A/B/8/7/4/4/9C9.png)
2. Ingresar la dirección de correo electrónico del profesor y seleccionar la opción de *Realizar cambios en eventos* de manera que pueda administrar los eventos del calendario correspondiente a su materia.
![](https://k60.kn3.net/8/B/C/A/5/0/CC8.png)
3. Finalmente, hacer clic en el botón *Agregar usuario*.
4. El profesor recibirá en su casilla de correo electrónico un aviso de que se ha compartido un calendario con él y apartir de ahí ya podrá administrar el calendario correspondiente a su materia o bien ingresando a la página web de [Google Calendar](http://calendar.google.com) o bien, desde su dispositivo móvil, configurando su cuenta de [GMail](http://mail.google.com).

	![](https://k60.kn3.net/B/7/5/5/7/B/C48.png)

### Gestionar un Calendario
La aplicación desarrollada basará su funcionamiento en la consulta de los eventos creados en cada uno de los calendarios de las materiar. Para ello será de suma importancia la creación de eventos, siguiendo unas simples reclas. Los eventos serán principalmente de 2 tipos: *Clases* y *Examenes*

#### Creación de Evento de tipo Clase
El evento de tipo clase se corresponderá con el dictado de clases en un cuatrimestre. La siguiente guía utilizar un navegador web, anque hay que seguir prácticamente los mismos paoss para realizarlo desde un dispositivo móvil. Para crear el evento de tipo clase, siga los siguientes pasos:

1. Ingresar en [Calendar](http://calendar.google.com) y sitúese en el Calendario correspondiente ![](https://k61.kn3.net/5/9/F/A/D/9/F22.png)
2. Haga clic en el Botón *Crear*
3. Se abrirá una ventana donde ingresará los datos de la clase:
	* Como nombre del evento puede optar entre:
		* Clase Práctica.
		* Clase Teórica.
		* Clase de consulta.
		* Parcial.

			![](https://k61.kn3.net/B/9/8/E/2/F/1BB.png)
	* Como Fecha:
		* Si se trata de una Clase de consulta o un Parcial:
			* Ingrese la fecha de ocurrencia como fecha de inicio y fecha de fin.
			* Verifique que se encuentra desmarcada la opción repetir.
			* Complete la hora de inicio y la hora de fin del evento.
	 	* Si se trata de una Clase Pŕactica o Teórica:
			*	Ingrese la fecha de la primera clase correspondiente al cutrimestre *14/3/2016* corresponde a la primera clase del primer cuatrimestre de 2016 (día martes).
			* Ingrese horario de inicio y de finalización de la clase.
			* Seleccione la opción de *Repetir* para indicar que el evento Clase se repite todas las semanas. Se abrirá una ventana como la siguiente:

				![](https://k61.kn3.net/2/8/8/7/F/7/7BA.png)
			* En este caso hemos puesto que la clase se repite todos los días Martes.
			* Ingrese la fecha de Finalización del Cuatrimestre como fecha de finalización de la Repetición.
	* En Descripción del evento ingrese toda la metainformación que desee de la manera *{etiqueta: valor}* de cursado de la siguiente manera:
		* **lugar: XXXX** (donde XXXX será **CC** o **aulas**). Este dato es opcional.
		*  **aula: YY** (YY donde YY será el Nº de aula). Este dato es opcional.
	![](https://k61.kn3.net/0/0/7/6/7/1/50D.png)
	**Importante:**  La utilización de la etiqueta **lugar** con valores **CC** o **aulas** hará que el evento pueda visualizarse en un punto del mapa, ya que estos valores fijos estarán asociadas a las coordenadas del lugar. Puede utilizar cuantas etiquetas desee, una por línea de la Descripción del Evento

### Creación de Evento de tipo Mesa de Examen
Los examenes serán cargados todos en un Calendario aparte. Para agregar un aviso de examen, póngase en contacto con el administrador del [DIT](http://www.dit.ing.unp.edu.ar).
Los pasos a seguir son básicamente los mismos que los de un evento de tipo *Clase*, salvo que no cargará repetición. En a descripción del evento también puede utilizar las etiquetas **lugar: XXXX**, **aula: YY** o todas las etiquetas personalizadas que deseee


## Listado de Materias
A Junio de 2016, el listado de materias correspondiente a la carrera de [Licenciatura en Sistemas (Or. Planificación, Gestión y Control de Proyectos Informáticos](http://www.ing.unp.edu.ar/info_lic_informatica_2010_c.htm) con sus correspondientes **ID del Calendario** es el siguiente:

| Código | Asignatura                                          | anio | Cuatrimestre | Nombre Calendario                                           | ID del Calendario                                |
|--------|-----------------------------------------------------|-----|--------------|-------------------------------------------------------------|------------------------------------------------------|
| EXAME  | Mesas de Exámenes                            	   |     |              | EXAME - Mesas de Exámenes									  | nubkn5itvfi3n25bpv0mkgps84@group.calendar.google.com |
| IF001  | Elementos de informática                            | 1   | 1            | IF001 - Elementos de informática                            | aod40c9ls454d9jqsh7oetc910@group.calendar.google.com |
| MA045  | Algebra                                             | 1   | 1            | MA045 - Algebra                                             | 5cv4ur5p3enrbvjlt875us5qes@group.calendar.google.com |
| IF002  | Expresión de Problemas y algoritmos                 | 1   | 1            | IF002 - Expresión de Problemas y algoritmos                 | jrjdur8jrdkktb4b87ctfh9nt4@group.calendar.google.com |
| IF003  | Algorítmica y Programación I                        | 1   | 2            | IF003 - Algorítmica y Programación I                        | no563qhav0opleeksuljh2igvk@group.calendar.google.com |
| MA048  | Análisis Matemático - S                             | 1   | 2            | MA048 - Análisis Matemático - S                             | nnib87ebfm3jc3rf4q4vl6hvas@group.calendar.google.com |
| MA008  | Elementos de Lógica y Matemática Discreta           | 1   | 2            | MA008 - Elementos de Lógica y Matemática Discreta           | ulejanbq8o0vu0051uikgcrcts@group.calendar.google.com |
| IF004  | Sistemas y Organizaciones                           | 2   | 1            | IF004 - Sistemas y Organizaciones                           | u435g4290uurj04akttvu8oe8o@group.calendar.google.com |
| IF005  | Arquitectura de Computadoras                        | 2   | 1            | IF005 - Arquitectura de Computadoras                        | 0vv9158nrqj66m8382hu665p4c@group.calendar.google.com |
| IF006  | Algorítmica y Programación II                       | 2   | 1            | IF006 - Algorítmica y Programación II                       | oigrphjfmk8dbhble3ed7m897s@group.calendar.google.com |
| IF007  | Bases de Datos I                                    | 2   | 2            | IF007 - Bases de Datos I                                    | qf0f4fj3skov4kbm3nr3fnujkg@group.calendar.google.com |
| MA006  | Estadística                                         | 2   | 2            | MA006 - Estadística                                         | 5sq3en190kr31qv66c0n7592s8@group.calendar.google.com |
| IF008  | Programación Orientada a Objetos                    | 2   | 2            | IF008 - Programación Orientada a Objetos                    | d3v1k1v4lkme3b6bo8id57ksso@group.calendar.google.com |
| IF038  | Introducción a la Concurrencia                      | 2   | 2            | IF038 - Introducción a la Concurrencia                      | m3j2o5j14v3r58oh8do9tupt6c@group.calendar.google.com |
| IF009  | Laboratorio de Programación y Lenguajes             | 3   | 1            | IF009 - Laboratorio de Programación y Lenguajes             | 44n2egpv8jtf50gklttqtrb3b0@group.calendar.google.com |
| IF040  | Ingeniería de Software I - T                        | 3   | 1            | IF040 - Ingeniería de Software I - T                        | oifnjkdoarm4ccc1rqpej3fr20@group.calendar.google.com |
| IF037  | Sistemas Operativos - S                             | 3   | 1            | IF037 - Sistemas Operativos - S                             | ct35ivinohqe7hjos7v53h8chg@group.calendar.google.com |
| IF012  | Desarrollo de Software                              | 3   | 2            | IF012 - Desarrollo de Software                              | li7nr9tu7ckfrvb0ssqpcqjko0@group.calendar.google.com |
| IF013  | Fundamentos Teóricos de Informática                 | 3   | 2            | IF013 - Fundamentos Teóricos de Informática                 | sb12dshqfp74gvb5ku3fq74csk@group.calendar.google.com |
| IF043  | Ingeniería de Software II - T                       | 3   | 2            | IF043 - Ingeniería de Software II - T                       | k8dpu029kq3be4vobh1bh0trv8@group.calendar.google.com |
| IF019  | Redes y Transmisión de Datos                        | 4   | 1            | IF019 - Redes y Transmisión de Datos                        | 479kq0gffslu7jivobkgpu9aj4@group.calendar.google.com |
| IF044  | Base de Datos II - S                                | 4   | 1            | IF044 - Base de Datos II - S                                | 5nff8m8hobmj2ujls74059cdk4@group.calendar.google.com |
| IF020  | Paradigmas y Lenguajes de Programación - T          | 4   | 1            | IF020 - Paradigmas y Lenguajes de Programación - T          | 91rftv0gds25df85t7khasju00@group.calendar.google.com |
| IF046  | Administración de Redes y Seguridad                 | 4   | 2            | IF046 - Administración de Redes y Seguridad                 | 5vuope2lv20ecaphvtco546m80@group.calendar.google.com |
| IF047  | Ingeniería de Software III - T                      | 4   | 2            | IF047 - Ingeniería de Software III - T                      | 9cfuban51c8egirdi9s4c2rqgs@group.calendar.google.com |
| IF016  | Aspectos Legales y Profesionales                    | 4   | 2            | IF016 - Aspectos Legales y Profesionales                    | gmqdq5ebs0qk64f9ho5vm4rg1o@group.calendar.google.com |
| IF022  | Sistemas Distribuidos                               | 4   | 2            | IF022 - Sistemas Distribuidos                               | f333raq619gkck7296ef6j61lg@group.calendar.google.com |
| IF049  | Administración de Proyectos                         | 5   | 1            | IF049 - Administración de Proyectos                         | 1lkt8vhajum08gptuvol23ru9g@group.calendar.google.com |
| IF050  | Aplicaciones Web                                    | 5   | 1            | IF050 - Aplicaciones Web                                    | desntamfq0aevjn09lmv98dvrc@group.calendar.google.com |
| IF017  | Taller de Nuevas Tecnologias                        | 5   | 1            | IF017 - Taller de Nuevas Tecnologias                        | alibc0t7lt2fphpl0pgl270ago@group.calendar.google.com |
| IF027  | Modelos y Simulación                                | 5   | 1            | IF027 - Modelos y Simulación                                | eh20c0mot7q95ijetu7rhp3rr4@group.calendar.google.com |
| IF053  | Planificación y Gestión de Sistemas de Información  | 5   | 2            | IF053 - Planificación y Gestión de Sistemas de Información  | rq64o17me91gd3bnh21hebo0ho@group.calendar.google.com |
| IF054  | Sistemas de Soporte para la Toma de Decisiones      | 5   | 2            | IF054 - Sistemas de Soporte para la Toma de Decisiones      | fdaci27fn9ip704k1rtb32cuq0@group.calendar.google.com |
