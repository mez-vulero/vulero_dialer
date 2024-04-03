document.addEventListener("DOMContentLoaded", function() {
      // HTML structure for the dialer UI
    const dialerHTML = `
        <div id="dialer-ui" style="display:none; position: fixed; bottom: 100px; right: 20px; background: white; border: 1px solid #ccc; border-radius: 8px; padding: 10px; z-index: 1000;">
            <div id="dialer-display" style="border-bottom: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">0</div>
            <div id="dialer-buttons" style="display: flex; flex-wrap: wrap; justify-content: space-between;">
                <button class="dialer-btn" style="flex: 1 1 30%; margin: 5px;">1</button>
                <button class="dialer-btn" style="flex: 1 1 30%; margin: 5px;">2</button>
                <button class="dialer-btn" style="flex: 1 1 30%; margin: 5px;">3</button>
                <button class="dialer-btn" style="flex: 1 1 30%; margin: 5px;">4</button>
                <button class="dialer-btn" style="flex: 1 1 30%; margin: 5px;">5</button>
                <button class="dialer-btn" style="flex: 1 1 30%; margin: 5px;">6</button>

                <!-- Add more buttons as needed -->
            </div>
        </div>
    `;

    // Append the dialer UI to the body
    $('body').append(dialerHTML);

    // Create and append the floating button
    const floatingBtn = $('<button/>', {
        text: 'Open Dialer',
        id: 'floating-btn',
    }).css({
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 999,
    }).appendTo('body');

    // Function to toggle dialer visibility
    function toggleDialer() {
        $('#dialer-ui').toggle();
    }

    // Attach click event to the floating button to open the dialer
    floatingBtn.click(toggleDialer);

    // Handle dialer button clicks
    $(document).on('click', '.dialer-btn', function() {
        const number = $(this).text();
        const currentDisplay = $('#dialer-display').text();
        $('#dialer-display').text(currentDisplay === '0' ? number : currentDisplay + number);
    });
});
