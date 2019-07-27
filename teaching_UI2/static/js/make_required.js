$( document ).ready(function() {
    console.log( "ready!" );

    // add html5 required field, because Flask sucks
    $( "input" ).each(function( index ) {
        console.log("radio input");
        $( this ).attr('required',true);
    });

});
