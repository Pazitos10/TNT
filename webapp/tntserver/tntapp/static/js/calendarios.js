$(document).ready(function () {

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
        /*var cuerpo = '<li>'+ titulo +
                    get_dia(fecha_comienzo, evento.se_repite)+
                    ' desde las: '+get_hora(fecha_comienzo)+
                    ' hasta las: '+get_hora(fecha_fin)+
                    ' en: '+ get_direccion(evento.descrip) +'</li>';
        console.log(cuerpo);*/
        if(titulo === 'Mesa de Exámen'){
            card_parent.find('.labels').append('<br><label class="label label-primary">'+titulo+'</label>');
        }else{
            card_parent.find('.labels').append('<br><label class="label label-info">'+titulo+'</label>');
        }
        if(evento_en_curso(fecha_comienzo, evento.se_repite)){
            card_parent.find('.labels').append('<label class="label label-success" style="margin-left:5px">En curso<label>')
        }
    });

    function get_hora(fecha){
        var hora = fecha.getHours();
        var mins = fecha.getMinutes();
        if (mins === 0) mins = '00';
        return hora + ":" + mins + "hs";
    }

    function get_dia(fecha_completa, se_repite) {
      var dias = ['lunes', 'martes', 'miércoles',
                'jueves', 'viernes','sábado', 'domingo'];
      if (se_repite)
        return ': todos los ' + dias[fecha_completa.getDay() - 1 ];
      else
        return ': el ' + fecha_completa.getDay() +
                '/' + fecha_completa.getMonth() +
                '/' + fecha_completa.getFullYear();
    }

    function get_direccion(descripcion_evento) {
        //Separados por coma: aula, lugar, profesores
        var datos = descripcion_evento.split('\n');
        var aula = datos[0];
        var lugar = datos[1].split(':')[1];
        var profesores = datos[2].split(':')[1];
        return lugar+' ('+aula+') '+'con:'+profesores;
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
