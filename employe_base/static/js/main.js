$(document).ready(function() {
    
    var url = window.location.href;

    var workers = url.split('?').pop().split('&')[0].split('=')[1]
    var departments = decodeURI(url.split('&').pop().split('=')[1]);

    if (workers != null){
        $('option[value="'+workers+'"]').attr('selected', true);
    } 

    if (departments != null){
        $('option[value="'+departments+'"]').attr('selected', true);
    } 

});