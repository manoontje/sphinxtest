

/**
 * This is the file which handles the socketIO connection for the god view,
 * requesting a redraw of the grid when a socketIO update has been received.
 */

 var doVisualUpdates = true;
 var isFirstCall=true;
 var pause = false;

/**
 * Check if the current tab is in focus or not
 */
document.addEventListener('visibilitychange', function(){
  doVisualUpdates = !document.hidden;
});

$(document).ready(function(){
    // specify a namespace, so that we only listen to messages from the server for the god view
    var namespace = "/god"

    // make connection with python server via socket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    $(".pause").click(function() {
        pause = true;
    });

    $(".play").click(function() {
        pause = false;
    });

    /**
     * Event handler for new connections.
     */

    socket.on('connect', function() {
        console.log("Connected");

    });

    socket.on('error', function (err) {
    console.log(err);
    });



    /**
     * receive an update from the python server
     */
    socket.on('update', function(data){
         console.log("Received an update from the server:", data);

        var rangeslider = document.getElementById("sliderRange");
        var slider_output = document.getElementById("tickspeed");
        slider_output.innerHTML = rangeslider.value;

        rangeslider.oninput = function() {
            slider_output.innerHTML = this.value;
            console.log("PRINT", JSON.stringify(slider_output.innerHTML));
            }

        $.ajax({
          type: "GET",
          contentType: "application/json",
          url: "/god/tick_speed",
          traditional: "true",
          data: slider_output.innerHTML,
          dataType: "json"
          });

        // Only perform the GUI update if it is in the foreground, as the
        // background tabs are often throttled after which the browser cannot
        // keepup
        if (!doVisualUpdates) {
            console.log("Chrome in background, skipping");
            return;
        }

        // unpack received data
        grid_size = data.params.grid_size;
        state = data.state;
        tick = data.params.tick;
        tick_speed = data.params.tick_speed;
        vis_bg_clr = data.params.vis_bg_clr;
        vis_bg_img = data.params.vis_bg_img;
        agent_info = data.agent_info;
        //draw the menu if it is the first call
        if(isFirstCall){
            isFirstCall=false;
            populateMenu(state);
            parseGifs(state);}
        // draw the grid again
        requestAnimationFrame(function() {
            if(pause){

            }
            else{
                data.params.tick_speed = slider_output.innerHTML;
                tick_speed = data.params.tick_speed;
                doTick(grid_size, state, tick, tick_speed, vis_bg_clr,vis_bg_img, parsedGifs, agent_info);}
                console.log("Tick speed is ", tick_speed);
        });
    });
});
