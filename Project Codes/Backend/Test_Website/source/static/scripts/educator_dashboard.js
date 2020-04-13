// DOM Elements
const accept_buttons = document.querySelectorAll('.accept_request_buttons');
const reject_buttons = document.querySelectorAll('.reject_request_buttons');
const process_request = document.querySelector('#process_request');

// Event listeners
function accept_paper(event) {
    event.preventDefault();

    process_request['group_id'].value = this.getAttribute('group');
    process_request['request_type'].value = 'accept';
    process_request.submit();
}

function reject_paper(event) {
    event.preventDefault();

    process_request['group_id'].value = this.getAttribute('group');
    process_request['request_type'].value = 'reject';
    process_request.submit();
}

accept_buttons.forEach((accept_button) => {
    accept_button.addEventListener('click', accept_paper);
});

reject_buttons.forEach((reject_button) => {
    reject_button.addEventListener('click', reject_paper);
});