$(document).ready(function () {

    //completamos la parte delantera de cada item materia
    $.each($('input[name=meta]'), function () {
        var materia = $(this).data('materia'); //obtenemos el id materia
        var meta = JSON.parse($(this).val());
        var nombre_materia = meta[materia].split(/:|\n/)[1];
        var anio = meta[materia].split(/:|\n/)[3];
        var cuatrimestre = Number(meta[materia].split(/:|\n/)[5]);
        if (cuatrimestre === 1)
            cuatrimestre += '<sup>er</sup>';
        else
            cuatrimestre += '<sup>do</sup>';
        /*$.each($('.card[data-materia='+materia+']'), function() {
            $(this).find('.nombre-materia')[0].innerHTML = nombre_materia;
            $(this).find('.meta')[0].innerHTML = anio + '° Año - ' + cuatrimestre + ' cuatrimestre';
        });*/
    });


    $.each($('input[name=evento]'), function() {
        var materia = $(this).data('materia'); //obtenemos el id materia
        var card_parent = $(this).parent();
        var evento = JSON.parse($(this).val()); //obtenemos sus eventos
        // Armamos la vista
        var datos_evento = get_datos_evento(evento);
        var titulo = datos_evento['titulo'];
        var etiquetas = '';
        var tipo_clase = '';
        if(titulo.includes('(P)'))
          tipo_clase = 'Clase Práctica';
        if(titulo.includes('(T)'))
            tipo_clase = 'Clase Teórica';
        if(titulo.includes('(TyP)'))
            tipo_clase = 'Teoría y Práctica';
        etiquetas = '<br><label class="label label-info">'+tipo_clase+'</label>';

        if(datos_evento['en_curso'])
            etiquetas += '<label class="label label-success en-curso">En curso<label>';

        card_parent.find('.nombre-materia').append(titulo);
        card_parent.find('.labels').append(etiquetas);
        //llenamos la parte de atras
        set_description_back(card_parent, evento);
    });


    function get_datos_evento (evento) {
        console.log(evento);
        var fecha_comienzo = new Date(evento.comienzo);
        var fecha_fin = new Date(evento.fin);
        var descripcion = evento.descrip.split('\n');
        if (descripcion.length > 2) {
          var aula = '('+descripcion[0]+')';
          var lugar = descripcion[1].split(':')[1] || "" ;
          var profesores = descripcion[2].split(':')[1] || "";
        }
        var datos = {
            titulo : evento.titulo,
            fecha_comienzo : fecha_comienzo,
            fecha_fin : fecha_fin,
            dia: get_dia(fecha_comienzo),
            hora_inicio: get_hora(fecha_comienzo),
            hora_fin: get_hora(fecha_fin),
            se_repite : evento.se_repite,
            en_curso : evento_en_curso(fecha_comienzo, evento.se_repite),
            fecha_dma : get_fecha(fecha_comienzo),
            aula : aula || "",
            lugar: lugar || "",
            profesores: profesores || ""
        }
        return datos;
    }


    function get_hora(fecha){
        var hora = fecha.getHours();
        var mins = fecha.getMinutes();
        if (mins === 0) mins = '00';
        return hora + ":" + mins + "hs";
    }

    function get_fecha(fecha){
        var dia = fecha.getDate();
        var mes = fecha.getMonth()+1;
        var anio = fecha.getFullYear();
        return dia + '/' + mes + '/' + anio;
    }

    function get_dia(fecha_completa) {
        var dias = ['Lunes', 'Martes', 'Miércoles',
                'Jueves', 'Viernes','Sábado', 'Domingo'];
        return dias[fecha_completa.getDay() - 1 ];
    }

    /**
    *   Retorna true si la fecha y hora del evento indicado es igual a
    *   la fecha/hora actual.
    */
    function evento_en_curso(fecha_evento, es_evento_recurrente){
        var fecha_actual = new Date(); //to test -> '6/13/2016 16:00'
        if (es_evento_recurrente){
            if (fecha_evento.getDay() === fecha_actual.getDay()){
                console.log('es el mismo dia'); //Dia de la semana -> l, m, x...
                return en_curso_ahora(fecha_evento, fecha_actual);
            }
        }else{
            if (fecha_evento.getDate() === fecha_actual.getDate()) //Dia del mes -> 1...30
                return en_curso_ahora(fecha_evento, fecha_actual);
        }
        return false;
    }

    function en_curso_ahora(fecha_evento, fecha_actual){
        //para probar lo siguiente, usar: new Date('mm/dd/aaaa hh:MM') en evento_en_curso
        if(fecha_evento.getHours() === fecha_actual.getHours())
            return true;
            //si la hora es mayor o igual que la fecha de inicio y menor o igual que la fecha de fin (duracion)
        else
            return false;
    }

    function set_description_back(card, evento) {
        var figure_parent = card.find('figure.materia-back');
        var materia = card.data('materia');
        var datos = get_datos_evento(evento);

        var markup_descripcion_back = '';
        if (datos['titulo'] === 'Mesa de Exámen'){
            markup_descripcion_back =   '<div class="descripcion descripcion-back">'+
                                            '<p class="meta">'+datos['fecha_dma']+' - '+datos['hora_inicio']+'<br> '+
                                            datos['lugar'] +' '+ datos['aula'] +'</p>'+
                                        '</div>'+
                                        '<div class="asistencias asistencias-offline">'+
                                            '<span class="glyphicon glyphicon-info-sign info-mesa" data-toggle="modal" data-target="#modal-info-mesa">'+
                                            '</span>'+
                                        '</div>';
            figure_parent.removeClass('materia-online').addClass('materia-offline materia-examen');
        }else{
            markup_descripcion_back =   '<div class="descripcion descripcion-back">'+
                                            '<p>'+datos['dia']+'<br>'+datos['hora_inicio']+' - '+datos['hora_fin']+'<br>'+
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

    // Manejo de botones en item materia
    $('.flip-card-btn-back, .flip-card-btn-front').click(function () {
        var card = $(this).parent().parent()[0];
        $(card).toggleClass('flipped');
    });

    $('#modal-info-mesa').on('show.bs.modal', function(e) {
        var card_parent = $(e.relatedTarget).parents().get(2); //obtenemos el elemento card relacionado
        var materia = $(card_parent).data('materia');
        var meta = JSON.parse($(card_parent).find('input[name=meta]').val());
        var nombre_materia = meta[materia].split(/:|\n/)[1];
        var evento = $(card_parent).find('input[name=evento]')[0];
        var datos = get_datos_evento(JSON.parse($(evento).val()));
        var titulo_modal = $(this).find('.modal-title')[0];
        var cuerpo_modal = $(this).find('.modal-body')[0];
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
        console.log(cuerpo_modal);
    });

    function initialize() {
        var mapProp = {
            center:new google.maps.LatLng(-43.2493016,-65.3076351),
            zoom:13,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
        var map=new google.maps.Map($('.mapa-container')[0],mapProp);
    }
    google.maps.event.addDomListener(window, 'load', initialize);
})
