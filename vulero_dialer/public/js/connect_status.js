$(document).ready(function() {
    // Function to update the connection status dot color
    window.addEventListener('statusEvent', function(e) {
      switch (e.detail) {
        case 'connected':
          $('#connectionStatusDot').css('background-color', 'green');
          break;
        case 'disconnected':
          $('#connectionStatusDot').css('background-color', 'red');
          break;
        case 'reconnecting':
          $('#connectionStatusDot').css('background-color', 'orange');
          break;
        default:
          console.log('Unknown status:', e.detail);
          $('#connectionStatusDot').css('background-color', 'grey');
          break;
      }
    });

    function appendConnectionStatusDot() {
        let bellIcon = $('ul.navbar-nav > li.nav-item.dropdown-notifications');
        if (bellIcon.length === 0) {
            console.error("Bell icon not found");
            // Retry after a delay
            setTimeout(appendConnectionStatusDot, 500); // Retry after 500 milliseconds
            return;
        }

        // Add the connection status dot to the navbar
        let connectionStatusDot = $(`<li class="nav-item"><span id="connectionStatusDot"></span></li>`);
        bellIcon.after(connectionStatusDot);

        // Add CSS styles for the connection status dot
        $('head').append(`
            <style>
                #connectionStatusDot {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background-color: red;
                    display: inline-block;
                    margin-left: 10px;
                    vertical-align: middle;
                }
            </style>
        `);
    }

    appendConnectionStatusDot();
});
