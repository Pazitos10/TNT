$(document).ready(function () {

    $.each($('input[name=meta]'), function () {
        set_description_front(this);
    });

    $.each($('input[name=evento]'), function() {
        process_event_data(this);
    });

    // Manejo de botones en item materia
    $('.flip-card-btn-back, .flip-card-btn-front').click(function () {
        var card = $(this).parent().parent()[0];
        $(card).toggleClass('flipped');
    });

    // Dispara el modal
    $('#modal-info-mesa').on('show.bs.modal', function(e) {
        set_modal_data(e, this);
    });

    //Inicializa el mapa en pantalla
    function initialize() {
        var mapProp = {
            center:new google.maps.LatLng(-43.2493016,-65.3076351),
            zoom:13,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
        var map=new google.maps.Map($('.mapa-container')[0],mapProp);
    }
    google.maps.event.addDomListener(window, 'load', initialize);

    /**
    *   Coloca el nombre de la materia que toma mesa de examen
    *   como metadata del item materia de la interfaz.
    */
    function set_materia_mesa(card, materia_mesa) {
        card.find('.meta')[0].innerHTML = materia_mesa;
    }

    function process_event_data(target) {
        var card_parent = $(target).parent();
        var evento = JSON.parse($(target).val()); //obtenemos sus eventos
        var datos_evento = get_datos_evento(evento);
        if (datos_evento.materia.length > 0)
            set_materia_mesa(card_parent, datos_evento.materia);
        var labels = get_labels_front(datos_evento.titulo, datos_evento.en_curso);
        card_parent.find('.labels').append(labels);
        set_description_back(card_parent, evento);
    }

    /*
    *   Retorna un string con el markup para los labels de un item materia.
    */
    function get_labels_front(titulo, en_curso) {
        var labels = '<br><label class="label label-warning">'+titulo+'</label>';
        if (titulo === 'Exámen Final')
            labels = '<br><label class="label label-primary">'+titulo+'</label>';
        if(en_curso)
            labels += '<label class="label label-success en-curso">En curso<label>';
        return labels;
    }

    //completamos la parte delantera de cada item materia
    function set_description_front(target) {
        var materia = $(target).data('materia'); //obtenemos el id materia
        var meta = JSON.parse($(target).val());
        var nombre_materia = meta[materia].nombre;
        var anio = meta[materia].anio;
        var cuatrimestre = Number(meta[materia].cuatrimestre);
        cuatrimestre += (cuatrimestre === 1) ? '<sup>er</sup>' : '<sup>do</sup>';
        $.each($('.card[data-materia='+materia+']'), function() {
            $(this).find('.nombre-materia')[0].innerHTML = nombre_materia;
            var meta = anio + '° Año - ' + cuatrimestre + ' cuatrimestre';
            $(this).find('.meta')[0].innerHTML = meta;
        });
    }

    /*
    *   Retorna un objeto json con los datos del evento recibido como parametro
    */
    function get_datos_evento (evento) {
        var fecha_comienzo = new Date(evento.comienzo);
        var fecha_fin = new Date(evento.fin);
        var descripcion = evento.descrip;
        var datos = {
            titulo : evento.titulo,
            fecha_comienzo : fecha_comienzo,
            fecha_fin : fecha_fin,
            dia: get_dia(fecha_comienzo),
            hora_inicio: get_hora(fecha_comienzo),
            hora_fin: get_hora(fecha_fin),
            se_repite : evento.se_repite,
            en_curso : evento_en_curso(fecha_comienzo, fecha_fin, evento.se_repite),
            fecha_dma : get_fecha(fecha_comienzo)
        }
        var terminos = ['aula','lugar', 'profesores', 'materia'];
        var value = '';
        for (var i=0; i < terminos.length; i++){
            value = '';
            if (descripcion.includes(terminos[i])){
                value = descripcion.split(terminos[i]+':')[1];
                value = value.split('\n')[0];
                if (terminos[i] === 'aula')
                    value = '(aula: '+value+')';
                if (terminos[i] === 'profesores')
                    value = value.substr(0, 35)+'...';
            }
            datos[terminos[i]] = value;
        }
        return datos;
    }

    /*
    *   Retorna un string con la hora en formato hh:mm
    */
    function get_hora(fecha){
        var hora = fecha.getHours();
        var mins = fecha.getMinutes();
        if (mins === 0) mins = '00';
        return hora + ":" + mins + "hs";
    }

    /*
    *   Retorna un string con la fecha en formato dd/mm/aaaa
    */
    function get_fecha(fecha){
        var dia = fecha.getDate();
        var mes = fecha.getMonth()+1;
        var anio = fecha.getFullYear();
        return dia + '/' + mes + '/' + anio;
    }

    /**
    *   Retorna el nombre del día correspondiente a el numero de
    *   día de la fecha recibida. P. ej: 4/7/2016 -> Lunes
    */
    function get_dia(fecha_completa) {
        var dias = ['Lunes', 'Martes', 'Miércoles',
                'Jueves', 'Viernes','Sábado', 'Domingo'];
        return dias[fecha_completa.getDay() - 1 ];
    }

    /**
    *   Retorna true si la fecha y hora del evento indicado es igual a
    *   la fecha/hora actual.
    */
    function evento_en_curso(f_comienzo_evento, f_fin_evento, es_evento_recurrente){
        var fecha_actual = new Date(); //to test -> '6/13/2016 16:00'
        if (es_evento_recurrente){
            if (f_comienzo_evento.getDay() === fecha_actual.getDay()){
                return en_curso_ahora(f_comienzo_evento, f_fin_evento, fecha_actual);
            }
        }else{
            //Dia del mes -> 1...30
            if (f_comienzo_evento.getDate() === fecha_actual.getDate())
                return en_curso_ahora(f_comienzo_evento, f_fin_evento, fecha_actual);
        }
        return false;
    }

    /**
    *   Retorna true si el evento se encuentra en curso en el momento de
    *   invocacion a esta funcion, caso contrario, retorna false.
    */
    function en_curso_ahora(f_inicio_evento, f_fin_evento, fecha_actual){
        //to test -> new Date('mm/dd/aaaa hh:MM') en evento_en_curso()
        if(Date.parse(fecha_actual) >= Date.parse(f_inicio_evento) &&
            Date.parse(fecha_actual) <= Date.parse(f_fin_evento))
            return true;
        else
            return false;
    }

    //completamos la parte trasera de cada item materia
    function set_description_back(card, evento) {
        var figure_parent = card.find('figure.materia-back');
        var materia = card.data('materia');
        var datos = get_datos_evento(evento);
        var markup_descripcion_back = '';
        if (datos['titulo'] === 'Exámen Final'){
            markup_descripcion_back =   '<div class="descripcion descripcion-back">'+
                                            '<p class="meta">'+datos['fecha_dma'] +' - '+datos['hora_inicio']+'<br> '+
                                            datos['lugar'] +' '+ datos['aula'] +'<br>'+ datos['profesores']+'</p>'+
                                        '</div>'+
                                        '<div class="asistencias asistencias-offline">'+
                                            '<span class="glyphicon glyphicon-info-sign info-mesa" data-toggle="modal" data-target="#modal-info-mesa">'+
                                            '</span>'+
                                        '</div>';
            figure_parent.removeClass('materia-online').addClass('materia-offline materia-examen');
        }else{
            var dia = datos['dia'] || datos['fecha_dma'];
            var hora_inicio = datos['hora_inicio'] || '';
            var hora_fin = datos['hora_fin'] || '';
            markup_descripcion_back =   '<div class="descripcion descripcion-back">'+
                                            '<p>'+dia+'<br>'+hora_inicio+' - '+hora_fin+'<br>'+
                                            datos['lugar'] +' '+ datos['aula'] +'</p>'+
                                        '</div>';
            if (datos['en_curso']){
                markup_descripcion_back +=  '<div class="asistencias asistencias-online">'+
                                                '<p class="asistencias-value">7</p>'+
                                                '<span class="glyphicon glyphicon-user"></span>'+
                                            '</div>';
            }else{
                markup_descripcion_back +=  '<div class="asistencias asistencias-offline">'+
                                                '<span class="glyphicon glyphicon-map-marker"></span>'+
                                            '</div>';
                figure_parent.removeClass('materia-online').addClass('materia-offline');
            }
        }
        figure_parent.append(markup_descripcion_back);
    }

    //Completa los datos del modal para las mesas de examen.
    function set_modal_data(e, modal) {
        var card_parent = $(e.relatedTarget).parents().get(2); //obtenemos el elemento card relacionado
        var materia = $(card_parent).data('materia');
        var meta = JSON.parse($(card_parent).find('input[name=meta]').val());
        var evento = $(card_parent).find('input[name=evento]')[0];
        var datos = get_datos_evento(JSON.parse($(evento).val()));
        var nombre_materia = datos.materia;
        var titulo_modal = $(modal).find('.modal-title')[0];
        var cuerpo_modal = $(modal).find('.modal-body')[0];
        var lista_profesores = datos['profesores'].split(';');
        $(titulo_modal).addClass('text-center');
        titulo_modal.innerHTML = datos['titulo'];
        var tabla = '<div class="col-lg-8 col-lg-offset-2">'+
                    '<h6 class="text-center">'+ nombre_materia +'</h6>'+
                    '<table class="table table-striped">'+
                        '<thead><tr><th class="titulo-tabla-modal">Profesores</th></tr></thead>'+
                        '<tbody class="cuerpo-tabla-modal">';
        $.each(lista_profesores, function(i){
            tabla += '<tr><td><p>'+ lista_profesores[i].toLowerCase() +'</p></td></tr>';
        });
        tabla += '</tbody></table></div>';
        cuerpo_modal.innerHTML = tabla;
    }
})
