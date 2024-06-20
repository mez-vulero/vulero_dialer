(function() {
  // Function to create and append a div to the body
  function createAndAppendDiv(id) {
    const div = document.createElement('div');
    div.id = id;
    document.body.appendChild(div);
  }

  // Create the required div elements
  createAndAppendDiv('app');
  createAndAppendDiv('modals');
  createAndAppendDiv('popovers');

  // Create a new script element
  var script = document.createElement('script');
  
  // Create a new link element for the stylesheet
  var link = document.createElement('link');

  // Set the script's source (src) to the URL of the module you want to load
  link.rel = 'stylesheet'; // Correct relationship attribute for stylesheets
  link.href = '/assets/vulero_dialer/frontend/assets/index-0ac285a5.css';
  
  script.src = '/assets/vulero_dialer/frontend/assets/index-29895d2c.js';

  // IMPORTANT: Set the script type to "module"
  script.type = 'module';

  // Append the script and link elements to the head of the document
  // to load and execute the module script and apply the stylesheet
  document.head.appendChild(script);
  document.head.appendChild(link);
})();


