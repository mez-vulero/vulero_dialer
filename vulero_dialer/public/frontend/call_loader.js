(function() {
  // Create a new script element
  function createAndAppendDiv(id) {
    const div = document.createElement('div');
    div.id = id;

    // Apply special styles and classes to the 'app' div
    if (id === 'app') {
        div.classList.add('sticky-top');
        div.style.zIndex = '2000';
    }

    var mainSection = document.querySelector('.main-section');
    if (mainSection) {
        mainSection.prepend(div);
    } else {
        document.body.prepend(div);
    }
  }

  // Create the required div elements
  createAndAppendDiv('app');
  createAndAppendDiv('modals');
  createAndAppendDiv('popovers');

  var script = document.createElement('script');
  
  // Create a new link element for the stylesheet
  var link = document.createElement('link');

  // Set the script's source (src) to the URL of the module you want to load
  link.rel = 'stylesheet'; // Correct relationship attribute for stylesheets
  link.href = '/assets/vulero_dialer/frontend/assets/index-DhGVavMg.css';
  
  script.src = '/assets/vulero_dialer/frontend/assets/index-DYGwVt-t.js';

  // IMPORTANT: Set the script type to "module"
  script.type = 'module';

  // Append the script and link elements to the head of the document
  // to load and execute the module script and apply the stylesheet
  document.head.appendChild(script);
  document.head.appendChild(link);
})();


