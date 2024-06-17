'use strict';

// Скрипт для перенаправления на url для удаления при удалении товара

function modalShown(event) {
    let button = event.relatedTarget;
    let bookId = button.dataset.bookId;
    let newUrl = `/books/${bookId}/delete`;
    let form = document.getElementById('deleteModalForm');
    form.action = newUrl;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);