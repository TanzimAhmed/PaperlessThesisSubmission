const quiz_statistics_form = document.querySelector('#quiz_stats_form');
const quiz_statistics_button = document.querySelector('#quiz_stats');

quiz_statistics_button.onclick = function (event) {
    event.preventDefault();
    quiz_statistics_form.submit();
};