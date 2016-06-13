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
        $.each($('.card[data-materia='+materia+']'), function() {
            $(this).find('.nombre-materia')[0].innerHTML = nombre_materia;
            $(this).find('.meta')[0].innerHTML = anio + '° Año - ' + cuatrimestre + ' cuatrimestre';
        });
    });


    $.each($('input[name=evento]'), function() {
        var materia = $(this).data('materia'); //obtenemos el id materia
        var card_parent = $(this).parent();
        var evento = JSON.parse($(this).val()); //obtenemos sus eventos
        // Armamos la vista
        var titulo = evento.titulo;
        var fecha_comienzo = new Date(evento.comienzo);
        var fecha_fin = new Date(evento.fin);

        if(titulo === 'Mesa de Exámen'){
            card_parent.find('.labels').append('<br><label class="label label-primary">'+titulo+'</label>');
        }else{
            card_parent.find('.labels').append('<br><label class="label label-info">'+titulo+'</label>');
        }
        if(evento_en_curso(fecha_comienzo, evento.se_repite)){
            card_parent.find('.labels').append('<label class="label label-success" style="margin-left:5px">En curso<label>')
        }
        
        //llenamos la parte de atras
        set_description_back(card_parent, evento);
    });

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

    function get_direccion(descripcion_evento, con_profesores) {
        //Separados por coma: aula, lugar, profesores
        var datos = descripcion_evento.split('\n');
        var aula = datos[0];
        var lugar = datos[1].split(':')[1];
        var profesores = datos[2].split(':')[1];
        var salida = lugar+'<br> ('+aula+') ';
        if (con_profesores){
            return salida +'con:'+profesores;
        }else
            return salida;
    }

    /**
    *   Retorna true si la fecha y hora del evento indicado es igual a 
    *   la fecha/hora actual.
    */
    function evento_en_curso(fecha_evento, es_evento_recurrente){
        var fecha_actual = new Date();
        if (es_evento_recurrente){
            if (fecha_evento.getDay() === fecha_actual.getDay()) //Dia de la semana -> l, m, x...
                return en_curso_ahora(fecha_evento, fecha_actual);
        }else{
            if (fecha_evento.getDate() === fecha_actual.getDate()) //Dia del mes -> 1...30
                return en_curso_ahora(fecha_evento, fecha_actual);
        }
        return false;
    }

    function en_curso_ahora(fecha_evento, fecha_actual){
        //para probar lo siguiente, usar: new Date('mm/dd/aaaa hh:MM') en evento_en_curso
        if(get_hora(fecha_evento) === get_hora(fecha_actual))
            return true;
        else
            return false;
    }

    function set_description_back(card, evento) {
        var figure_parent = card.find('figure.materia-back');
        var materia = card.data('materia');
        var titulo = evento.titulo;
        var fecha_comienzo = new Date(evento.comienzo);
        var fecha_fin = new Date(evento.fin);
        var en_curso = evento_en_curso(fecha_comienzo, evento.se_repite);
        var fecha_dma = get_fecha(fecha_comienzo);
        var tiempo_hm = get_hora(fecha_comienzo); 
        var aula = get_direccion(evento.descrip, false);

        var markup_descripcion_back = '';
        if (titulo === 'Mesa de Exámen'){
            markup_descripcion_back =   '<div class="descripcion descripcion-back">'+
                                            '<p class="meta">'+fecha_dma+'-'+tiempo_hm+'<br> '+ aula +'</p>'+
                                        '</div>'+
                                        '<div class="asistencias asistencias-offline">'+
                                            '<span class="glyphicon glyphicon-info-sign info-mesa" data-materia="'+materia+'"></span>'+
                                        '</div>';
            figure_parent.removeClass('materia-online').addClass('materia-offline materia-examen');
            figure_parent.append(markup_descripcion_back);
        }else{
            markup_descripcion_back =   '<div class="descripcion descripcion-back">'+
                                            '<p>'+get_dia(fecha_comienzo)+'<br>'+get_hora(fecha_comienzo)+' - '+get_hora(fecha_fin)+'<br>'+ aula +'</p>'+
                                        '</div>';
            if (en_curso){
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
            figure_parent.append(markup_descripcion_back);
        }
        //descripcion_back.append(markup_descripcion_back);
    }

    // Manejo de botones en item materia
    $('.flip-card-btn-back, .flip-card-btn-front').click(function () {
        var card = $(this).parent().parent()[0];
        $(card).toggleClass('flipped');
    });
})

function initialize() {
    var mapProp = {
        center:new google.maps.LatLng(-43.2493016,-65.3076351),
        zoom:13,
        mapTypeId:google.maps.MapTypeId.ROADMAP
    };
    var map=new google.maps.Map($('.mapa-container')[0],mapProp);
}
google.maps.event.addDomListener(window, 'load', initialize);

'<label class="label label-success">En Curso</label><label class="label label-info">Práctica</label>'
