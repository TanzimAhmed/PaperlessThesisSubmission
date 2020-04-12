// DOM Elements
const overlays = document.querySelectorAll('.overlays');
const statistics_image = document.querySelector('#statistics_image');
const close_icon = document.querySelector('#close_icon');
const statistics_form = document.querySelector('#quiz_stats_form');
const statistics_button = document.querySelector('#quiz_stats');

// Event Listeners
close_icon.onclick = function(event) {
    event.preventDefault();
    overlays.forEach((overlay) => {
        overlay.style.display = 'none';
    });
};

statistics_button.onclick = function (event) {
    event.preventDefault();
    const xhr = new XMLHttpRequest();
    const form_data = new FormData(statistics_form);

    xhr.open('POST', statistics_form.getAttribute('action'), true);
    xhr.onload = function () {
        if (this.status == 200) {
            const data = JSON.parse(this.responseText);
            console.log(data['url']);
            statistics_image.src = data['url'];
            overlays.forEach((overlay) => {
                overlay.style.display = 'block';
            });
        } else {
            alert(this.status + ' ' + this.responseText);
        }
    }
    xhr.send(form_data);
};