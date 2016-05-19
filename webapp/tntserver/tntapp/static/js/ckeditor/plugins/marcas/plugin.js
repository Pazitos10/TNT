CKEDITOR.plugins.add( 'marcas', {
    icons: 'tag',
    init: function( editor ) {
        editor.addCommand( 'crearMarca', {
            exec: function( editor ) {
                var placeholder_style = "background-color: #18BC9C;" +
                                "color: white;" +
                                "font-weight: bold;" +
                                "padding: 5px 10px;"

                var texto_seleccionado = editor.getSelection().getSelectedText();
                var code_tag = new CKEDITOR.dom.element("code");
                code_tag.setAttributes({style: placeholder_style})
                code_tag.setText(texto_seleccionado);
                editor.insertElement(code_tag);
            }
        });
        editor.ui.addButton( 'tag', {
            label: 'Crear Marca',
            command: 'crearMarca',
            toolbar: 'basicstyles'
        });
    }
});
