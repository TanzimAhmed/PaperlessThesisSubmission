const question_tag = document.querySelector('#question_tag');
const option_tag = document.querySelector('#options_tag');
const points_tag = document.querySelector('#points_tag');
const timer_tag = document.querySelector('#timer_tag');
const form = document.querySelector('form');
let ques_no = 1;
let timer = null;

function set_question() {
    if (timer) {
        clearInterval(timer);
        console.log('Interval Cleared');
    }
    timer_tag.style.color = 'black';

    let question = questions.shift();
    question_tag.innerHTML = `${ques_no}. ${question.fields.text}`;
    points_tag.innerHTML = question.fields.points;
    timer_tag.innerHTML = question.fields.time;
    option_tag.innerHTML = '';
    ques_no++;

    let option_no = 'A';
    question.fields.options.split('<p>//</p>').forEach(option => {
        const option_node = document.createElement('input');
        const label_node = document.createElement('label');
        const line_break = document.createElement('br');
        option_node.type = 'radio';
        option_node.name = 'options';
        option_node.value = option_no;
        label_node.innerHTML = `${option_no}. ${option}`;
        option_tag.appendChild(option_node);
        option_tag.appendChild(label_node);
        option_tag.appendChild(line_break);
        option_no = String.fromCharCode(option_no.charCodeAt(0) + 1);
    });

    let time_left = question.fields.time;
    timer = setInterval(() => {
        if (time_left != 0){
            time_left--;
            timer_tag.innerHTML = time_left;
            if (time_left < 20)
                timer_tag.style.color = 'red';
        } else {
            next_question();
        }
    }, 1000);
}

form.onsubmit = function(event){
    if (form.options.value.length == 0)
        form.answers.value += 'NONE, ';
    else
        form.answers.value += `${form.options.value}, `;
    console.log(form.answers.value);
    console.log(questions.length);

    if (questions.length != 0) {
        event.preventDefault();
        set_question();
        load_math();
    }
};

function next_question() {
    if (form.options.value.length == 0)
        form.answers.value += 'NONE, ';
    else
        form.answers.value += `${form.options.value}, `;
    console.log(form.answers.value);
    console.log(questions.length);

    if (questions.length == 0)
        form.submit();
    set_question();
    load_math();
}

function load_math() {
    let node = document.querySelector('#question_area');
    MathJax.texReset();
    MathJax.typesetClear();
    MathJax.typesetPromise([node]).catch(function (err) {
        node.innerHTML = '';
        node.appendChild(document.createTextNode(err.message));
        console.error(err);
    }).then(function () {
    });
}

set_question();