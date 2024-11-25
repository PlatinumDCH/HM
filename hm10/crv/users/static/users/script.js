document.addEventListener('DOMContentLoaded', function() {
    // find element on page
    var toggleButton = document.getElementById('toggle-author-input');
    var selectField = document.getElementById('author-select');
    var inputField = document.getElementById('author-input');

    // Added ivent for click bottom
    toggleButton.addEventListener('click', function() {
        // change process autihor-chose option
        if (selectField.style.display === 'none') {
            selectField.style.display = 'block';
            inputField.style.display = 'none';
        } else {
            selectField.style.display = 'none';
            inputField.style.display = 'block';
        }
    });
});