$(document).ready(function() {
    const joinIconUrl = "https://img.icons8.com/ios/50/40C057/joining-queue.png";
    const leaveIconUrl = "https://img.icons8.com/ios/50/FA5252/leaving-queue.png";

    window.addEventListener('queueEvent', function(e) {
      if(e.detail == 'join_queue') {
        $('#queueIcon').attr('src', leaveIconUrl);
        $('#queueButton').css('border-color', 'red');
      } else if (e.detail == 'leave_queue') {
        $('#queueIcon').attr('src', joinIconUrl);
        $('#queueButton').css('border-color', 'green');
      }
    });

    function appendQueueButton() {
        let queueButton = $(`
            <li class="nav-item">
                <button class="btn" id="queueButton" style="border: 1px solid green; background-color: transparent;">
                    <img src="${joinIconUrl}" id="queueIcon" width="24" height="24" alt="joining-queue"/>
                </button>
            </li>
        `);

        console.log("Created Queue Button: ", queueButton);

        let bellIcon = $('ul.navbar-nav > li.nav-item.dropdown-notifications');
        if (bellIcon.length === 0) {
            console.error("Bell icon not found");
            // Retry after a delay
            setTimeout(appendQueueButton, 500); // Retry after 500 milliseconds
            return;
        }


        bellIcon.after(queueButton);

        // Add event listener for the button
        $('#queueButton').on('click', function() {
            let button = $(this);
            let icon = $('#queueIcon');
            if (icon.attr('src') === joinIconUrl) {
                window.dispatchEvent(new CustomEvent('callEvent', {
                  detail: { number: 'join_queue' }
                }));
            } else {
                window.dispatchEvent(new CustomEvent('callEvent', {
                  detail: { number: 'leave_queue' }
                }));
            }
        });

        $('head').append(`
            <style>
                #queueButton {
                    display: inline-block;
                    margin-left: 10px;
                    background-color: transparent;
                    border: 1px solid green;
                }
                #queueButton:hover {
                    background-color: rgba(0, 0, 0, 0.1);
                }
            </style>
        `);

        console.log("Queue Button appended to Navbar");
    }

    appendQueueButton();
});
