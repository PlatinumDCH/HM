document.addEventListener('DOMContentLoaded', function() {
    // Найти элементы на странице
    var toggleButton = document.getElementById('toggle-author-input');
    var selectField = document.getElementById('author-select');
    var inputField = document.getElementById('author-input');

    // Добавить обработчик события для клика по кнопке
    toggleButton.addEventListener('click', function() {
        // Переключение видимости полей выбора и ввода автора
        if (selectField.style.display === 'none') {
            selectField.style.display = 'block';
            inputField.style.display = 'none';
        } else {
            selectField.style.display = 'none';
            inputField.style.display = 'block';
        }
    });
});