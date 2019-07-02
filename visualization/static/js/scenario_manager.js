/**
 * Check if the current tab is in focus or not
 */
document.addEventListener('visibilitychange', function(){
  doVisualUpdates = !document.hidden;
});

$(document).ready(function(){
    // specify a namespace, so that we only listen to messages from the server for the god view
    var namespace = "/scenario_manager"

    // make connection with python server via socket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    /**
     * Event handler for new connections.
     */
    socket.on('connect', function() {
        console.log("Connected");
    });

    /**
     * receive an update from the python server
     */
    socket.on('update', function(data){
        console.log("Received data:", data);
    });
});

$( ".scenario-1" ).click(start_scenario);


function start_scenario() {
    var data = ['god', 'agent-1', 'agent-2', 'hu_ag-1'];


    console.log("Starting scenario: " + $(this).attr('class'));

    // change button colour
    $(this).addClass("running");
    $(this).text("Running.. Press to stop.")

    console.log($(this));

    // unblock buttons
    var i;
    for (i = 0; i < data.length; i++) {
        $( "." + data[i] + " #button" ).removeClass("btn-blocked");
        console.log("unblocking button");
    }

    // block after timeout
    setTimeout(function () {
        end_scenario();
    }, 1000);

}

function end_scenario() {
    var data = ['god', 'agent-1', 'agent-2', 'hu_ag-1']

    // remove the "scenairo-running" layout
    var scen_but = $( ".running" );
    scen_but.removeClass("running");

    // get the scenario which is stopping
    var sc_running = scen_but.attr('class');
    console.log("Ending scenario " + sc_running);

    // add back the start layout
    scen_but.addClass("blocked-btn").text("Start");



    // revert the agent buttons back to blocked
    var i;
    for (i = 0; i < data.length; i++) {
        $( "#overview-agents #button" ).addClass("btn-blocked");
        console.log("blocking button");
    }
}
