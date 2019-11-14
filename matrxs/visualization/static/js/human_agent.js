/**
 * This is the file which handles the socketIO connection for the human agent view,
 * requesting a redraw of the grid when a socketIO update has been received.
 * Specific to the human agent, key inputs are also handled and sent back to the server.
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

    var id = document.getElementById('id').innerHTML;

    // specify a namespace, so that we only listen to messages from the server for this specific human agent
    var namespace = "/humanagent";

    // make connection with python server via socket to get messages only for the human agent
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

        var room = "/humanagent/" + id;

        // request to be added to room so the server can send messages specific to this human agent
        console.log("Requesting to be added to room:", room)
        socket.emit('join', {room: room});
    });

    /**
     * receive an update from the python server
     */
    socket.on('update', function(data){
        var rangeslider = document.getElementById("sliderRange");
        var slider_output = document.getElementById("tickspeed");
        slider_output.innerHTML = rangeslider.value;

        rangeslider.oninput = function() {
            slider_output.innerHTML = this.value;
            console.log("PRINT", JSON.stringify(slider_output.innerHTML));
            }

        $.ajax({
          type: "POST",
          contentType: "application/json",
          url: "/god/tick_speed",
          traditional: "true",
          data: JSON.stringify(slider_output.innerHTML),
          dataType: "json",
          success: function(data){
            console.log("Your tick speed is " + data);
            },
          error: function(data) {
            console.log("ERROR, data is: " + data.text);
            }
          });

          
        if (!doVisualUpdates) {
            console.log("Chrome in background, skipping");
            return;
        }



        // unpack received data
        grid_size = data.params.grid_size;
        state = data.state;
        tick = data.params.tick;
        vis_bg_clr = data.params.vis_bg_clr;
        vis_bg_img = data.params.vis_bg_img;
        agent_info = data.agent_info;
        if(isFirstCall){
            isFirstCall=false;
            populateMenu(state, id);
            parseGifs(state);
            }
        // draw the grid again
        requestAnimationFrame(function() {
            console.log("h_agent: ", String(agent_info))
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


    var id = -1;


    // bind key listener
    document.onkeydown = checkArrowKey;

    // get the ID of the current human_agent from the html
    id = document.getElementById('id').innerHTML;


    /**
     * Catch userinput with arrow keys
     *
     * Arrows keys: up=1, right=2, down=3, left=4
     */
    function checkArrowKey(e) {
        e = e || window.event;

        // send an update for every key pressed
        socket.emit("userinput", {"key": e.key, 'id': id});
    }
});
