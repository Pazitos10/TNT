$(document).ready(function(){

    //Definicion de funciones
    function add_thumbnail_to_form(canvas) {
        $('input[name=thumbnail]').val(canvas.toDataURL());
    }

    function get_thumbnail(contenido, alto, ancho){
        html2canvas( contenido, {
            height: alto,
            width: ancho,
            onrendered: function(canvas) {
                add_thumbnail_to_form(canvas);
                $('#form-plantilla').submit();
            }
        });
    }

    function add_placeholders_to_form(){
        var placeholders = {};
        var code_blocks = $('iframe').contents().find('body').find('code');
        for (var i=0; i < code_blocks.length ; i++) {
            content = String(code_blocks[i].innerHTML);
            placeholders[content] = content;
        }
        $('input[name=placeholders]').val(JSON.stringify(placeholders));
    }

    function prepare_form(){
        var contenido = $('iframe').contents().find('body');
        var alto = 150;
        var ancho = 250;
        get_thumbnail(contenido, alto, ancho);
        add_placeholders_to_form();
    }

    function confirmar_eliminacion() {
        console.log('hola');
        return confirm("Estás seguro de eliminar la Plantilla?");
    }

    $('#btn-guardar').click(function(e){
        e.preventDefault();
        prepare_form();
    });
});
