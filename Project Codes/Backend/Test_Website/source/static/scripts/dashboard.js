// DOM Elements
const view_document = document.querySelector('#view_document');
const view_button = document.querySelector('#view_button');

view_button.onclick = function (event) {
    event.preventDefault();

    view_document['group_id'].value = view_button.getAttribute('group');
    view_document['document_id'].value = view_button.getAttribute('document');
    console.log(view_document);
    view_document.submit();
}