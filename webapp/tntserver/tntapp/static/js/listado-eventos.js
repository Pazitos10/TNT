$(document).ready(function(){
    $(document).delegate("#update-btn", 'click', function(event){
        $.ajax({
            url : "materias/update_events",
            type : "GET",
            success : function(html) {
                $('.scroll-list').empty().append(html);
                localStorage.setItem("notifications", 0);
                window.process_events();
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log('Ups, something went wrong.'+
                            ' Cannot get events updates from server');
            }
        });
    });

});
