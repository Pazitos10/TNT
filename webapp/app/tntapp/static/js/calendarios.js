$('#options, #no-results').hide();
$(document).ready(function () {
    var map = {};
    var markers = [];
    set_filter_options();
    subscribe_to_updates();
    buscar_eventos($("#search-term-input").val());

    window.process_events = function (){
        localStorage.setItem("notifications", localStorage.getItem("notifications") || 0);
        var notifications = Number(localStorage.getItem("notifications"));
        if (!notifications)
            $('#alert-updates').fadeOut();
        $.each($('input[name=evento]'), function() {
            process_event_data(this);
        });
    }

    window.process_events();

    // Manejo de botones en item materia
    $(document).delegate('.flip-card-btn-back, .flip-card-btn-front','click',function (e) {
        var card = $(this).parent().parent()[0];
        $(card).toggleClass('flipped');
        set_marker(card);
    });

    $(document).delegate('#search-filter-button.glyphicon-chevron-down','click',function () {
        show_options();
    });

    $(document).delegate('#search-filter-button.glyphicon-chevron-up','click',function () {
        hide_options();
    });

    $('#update-btn').click(function () {
        $.ajax({
            url : "materias/update_events",
            type : "get",
            data: get_filter_options(),
            success : function(html) {
                $('.scroll-list').empty().append(html);
                localStorage.setItem("notifications", 0);
                window.process_events();
            },
            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log('Ups, something went wrong.'+
                            ' Cannot get events updates from server');
            }
        });
        $('#alert-updates').fadeOut();
    })

    // Dispara el modal
    $('#modal-info-mesa').on('show.bs.modal', function(e) {
        set_modal_data(e, this);
    });

    $('#btn-guardar-options').click(function(e) {
        set_filter_options({
            'es_hoy': $('#eventos-hoy:checked').attr('name') ? true : false ,
            'en_curso': $('#eventos-en-curso:checked').attr('name') ? true : false,
            'tipo_evento': $('#tipo-evento').val()
        });
        hide_options();
        buscar_eventos($("#search-term-input").val());
    });

    $('#btn-cancelar-options').click(function(e) {
        set_filter_options(null);
        reset_form();
        hide_options();
    });

    $("#search-term-input").keypress(function( event ) {
        if ( event.which == 13 ) {
            buscar_eventos($(this).val());
        }
    });

    $("#search-term-button").click(function () {
        buscar_eventos($("#search-term-input").val());
    });

    //Inicializa el mapa en pantalla
    function initialize() {
        var mapProp = {
            center:new google.maps.LatLng(-43.2493016,-65.3076351),
            zoom:13,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
        map=new google.maps.Map($('.mapa-container')[0],mapProp);
    }
    google.maps.event.addDomListener(window, 'load', initialize);

    function subscribe_to_updates(){
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var port = ws_scheme === "wss" ? ":8443" : "";
        var path = ws_scheme+ '://'+window.location.host + port+'/sync';
        var ws = new WebSocket(path);
        ws.onmessage = function(message) {
            var notifications = JSON.parse(message.data)['user_need_refresh'];
            if (notifications){
                localStorage.setItem("notifications", Number(notifications));
                if (localStorage.getItem("notifications")){
                    $('#alert-updates').fadeIn();
                }
            } else {
                console.log('Websocket response has wrong format. Expected JSON');
                localStorage.setItem("notifications", 0);
                $('#alert-updates').fadeOut();
            }
        }
        ws.onopen = function() {
            //console.log('WS Connecting to receive updates!');
            this.send('WS Connecting to receive updates!');
        }
    }

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
            fecha_dma : get_fecha(fecha_comienzo),
            coordenadas: {lat: -43.249763, lng: -65.3084728} //Edificio Aulas
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
            if (datos['lugar']){
              if (datos['lugar'].toLowerCase().includes("cc")
                  || datos['lugar'].toLowerCase().includes("dit"))
                datos['coordenadas'] = {lat: -43.2576106, lng: -65.3077018}; //DIT
            }
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

    function set_marker(card) {
      empty_markers();
      var evento = $(card).find('input[name=evento]')[0];
      var datos = get_datos_evento(JSON.parse($(evento).val()));
      if (datos.coordenadas){
        var marker = new google.maps.Marker({
         position: datos.coordenadas,
         map: map
        });
        map.setCenter(datos.coordenadas);
        map.setZoom(18);
        markers.push(marker);
        google.maps.event.addListener(marker , 'click', function(){
          var infowindow = new google.maps.InfoWindow({
            content: datos["titulo"],
            position: datos.coordenadas,
          });
          infowindow.open(map);
        });
      } else
        console.log('no tenia coordenadas');
    }

    function empty_markers() {
      for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
      }
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


    function set_filter_options(options) {
        if (!options){
            var filter_options = {
                'es_hoy' : false,
                'en_curso': false,
                'tipo_evento': 'Todos'
            };
            localStorage.setItem("filter_options", JSON.stringify(filter_options));
        } else {
            localStorage.setItem("filter_options", JSON.stringify(options));
        }
    }

    function get_filter_options(){
        return JSON.parse(localStorage.getItem("filter_options"));
    }

    function show_options() {
        $('#options').show();
        $('#results').hide();
        $('#search-filter-button').removeClass('glyphicon-chevron-down')
                                    .addClass('glyphicon-chevron-up');
    }

    function hide_options() {
        $('#options').hide();
        $('#results').show();
        $('#search-filter-button').removeClass('glyphicon-chevron-up')
                                    .addClass('glyphicon-chevron-down');
    }

    function reset_form() {
        document.getElementById('form-filter-options').reset();
    }

    function buscar_eventos(termino) {
        var filter_options = localStorage.getItem('filter_options');
        filter_options = $.extend({}, JSON.parse(filter_options), {'termino': termino});
        $.ajax({
            url: './buscar',
            type: 'get',
            data: filter_options
        }).done(function(html){
            if (html.length === 0){
                $('#no-results').show();
                $('.scroll-list').hide();
            } else{
                $('#no-results').hide();
                $('.scroll-list').show();
                // para filtrar segun tipo evento, obtenemos los elementos
                // (cambiar .en-curso por lo que corresponda)
                var panels = ﻿$('.panel').not($('.en-curso').parents('.panel'));
                // ocultamos los otros elem
                panels.map(function(i, panel){$(panel).hide()});
            }
            $('.scroll-list').empty().append(html);
            window.process_events();
        }).error(function(error){
            console.log('error',error);
        })
    }

})
