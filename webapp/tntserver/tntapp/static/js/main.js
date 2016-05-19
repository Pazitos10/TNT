function mostrar_tabla() {
    $('#btn-listado').removeClass('active');
    $('#btn-tabla').addClass('active');
    $('#content-listado').hide();
    $('#content-tabla').show();
}

function mostrar_listado() {
    $('#btn-listado').addClass('active');
    $('#btn-tabla').removeClass('active');
    $('#content-listado').show();
    $('#content-tabla').hide();
}

$(document).ready(function(){
    mostrar_tabla();

    //Event handling
    $('#btn-listado').click(function() {
        mostrar_listado();
    });

    $('#btn-tabla').click(function() {
        mostrar_tabla();
    });
});
