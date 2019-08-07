$( document ).ready(function() {

    // add html5 required field, because doing so with Flask sucks
    $( "input" ).each(function( index ) {
        $( this ).attr('required',true);
    });

});
