$(document).ready(function() {
    const joinIconUrl = "/assets/vulero_dialer/images/joining-queue.png";
    const leaveIconUrl = "/assets/vulero_dialer/images/leaving-queue.png";

    window.addEventListener('queueEvent', function(e) {
      if(e.detail == 'join_queue') {
        $('#queueIcon').attr('src', leaveIconUrl);
       // $('#queueButton').css('border-color', 'red');
        frappe.msgprint('Joined the queue');
      } else if (e.detail == 'leave_queue') {
        $('#queueIcon').attr('src', joinIconUrl);
        //$('#queueButton').css('border-color', 'green');
        frappe.msgprint('Left the queue');
      }
    });
	
    frappe.call({
    	method: 'vulero_dialer.config.queue.get_queue_status',
    	args: {},
    	callback: function(response) {
            if (response.message && response.message.status === "success") {
                // Get the icon element
                let icon = $('#queueIcon');
            
                // If the user is a member, set the icon to the 'leave' icon
                if (response.message.is_member) {
                    icon.attr('src', leaveIconUrl);
                } else {
                    // If not a member, set the icon to the 'join' icon
                    icon.attr('src', joinIconUrl);
                }
            } else {
                console.log("Error:", response.message ? response.message : "Unknown error");
            }
        },
        error: function(err) {
            console.log("Error calling the method:", err);
        }
    });

    function appendQueueButton() {
        let queueButton = $(`
            <li class="nav-item">
                <button class="btn" id="queueButton" style="border: none; background-color: transparent;">
                    <img src="${joinIconUrl}" id="queueIcon" width="24" height="24" alt="joining-queue"/>
                </button>
            </li>
        `);


        let bellIcon = $('ul.navbar-nav > li.nav-item.dropdown-notifications');
        if (bellIcon.length === 0) {
            console.error("Bell icon not found");
            // Retry after a delay
            setTimeout(appendQueueButton, 500); // Retry after 500 milliseconds
            return;
        }

        bellIcon.after(queueButton);

	$('#queueButton').on('click', function () {
          let button = $(this);
          let icon = $('#queueIcon');
    
          if (icon.attr('src') === joinIconUrl) {
            frappe.call({
              method: "vulero_dialer.config.queue.add_to_queue", // Add to queue method
              callback: function (response) {
                if (response.message.message === "added") {
                  //$('#queueIcon').attr('src', leaveIconUrl);
                    console.log("Successfully joined the queue.");
                    icon.attr('src', leaveIconUrl); // Change icon to leave
                } else {
                    console.error("Failed to join the queue:", response.message.message);
                }
              }
            });
            frappe.call({
              method: "vulero_dialer.config.call_log.fetch_and_process_missed_call_logs", 
              callback: function (response) {
	        console.log("Fetched Missed Calls");
              }
            });
          } else {
            frappe.call({
              method: "vulero_dialer.config.queue.remove_from_queue", // Remove from queue method
              callback: function (response) {
                if (response.message.message === "removed") {
                  $('#queueIcon').attr('src', joinIconUrl);
                    console.log("Successfully left the queue.");
                    icon.attr('src', joinIconUrl); // Change icon to join
                } else {
                    console.error("Failed to leave the queue:", response.message);
                }
              }
            });
          }
         });

        $('head').append(`
            <style>
                #queueButton {
                    display: inline-block;
                    margin-left: 10px;
                    background-color: transparent;
                    border: none;
                    padding: 0;
                }
                #queueButton:hover {
                    background-color: rgba(0, 0, 0, 0.1);
                }
            </style>
        `);

    }

    appendQueueButton();
});

