// DOM Elements
const view_document = document.querySelector('#view_document');
const view_buttons = document.querySelectorAll('.view_buttons');

// Event listeners
function view_paper(event) {
    event.preventDefault();

    view_document['group_id'].value = this.getAttribute('group');
    view_document['document_id'].value = this.getAttribute('document');
    console.log(view_document);
    view_document.submit();
}

view_buttons.forEach((view_button) => {
    view_button.addEventListener('click', view_paper);
});