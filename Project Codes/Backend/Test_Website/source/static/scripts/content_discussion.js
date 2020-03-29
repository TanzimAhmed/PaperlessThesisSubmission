
// CK Editor Initializations
CKEDITOR.plugins.addExternal('ckeditor_wiris', 'https://www.wiris.net/demo/plugins/ckeditor/', 'plugin.js');
function load_editor(id) {
    const editor = CKEDITOR.replace(id, {
        // For now, MathType is incompatible with CKEditor file upload plugins.
        extraPlugins: 'image2,mathjax,embed,autoembed,ckeditor_wiris',
        removePlugins: 'image,uploadimage,uploadwidget,uploadfile,filetools,filebrowser',
        height: 200,
        mathJaxLib: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML',
        allowedContent: true
    });
    return editor;
}
// MathJax initialization
MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']]
    },
    svg: {
        fontCache: 'global'
    },
    loader: {load: ['input/asciimath', 'output/chtml']},
};

// DOM Objects
const reply_buttons = document.querySelectorAll('.reply_buttons');
const comments = document.querySelector('#comments');
const reply_form = document.querySelector('#replies_form');
const discussion_form = document.querySelector('#comment_form');
const discussion_editor = load_editor('comment_input');
let reply_editor = null;
let target_node = null;

// Websocket Actions
const end_point = 'ws://' + window.location.host + window.location.pathname;
const web_socket = new WebSocket(end_point);

web_socket.onopen = function(event) {
    console.log('Websocket Connection established');
};

web_socket.onclose = function(event) {
    console.log('Websocket closed');
};

web_socket.onerror = function(event) {
    console.log('Websocket Error', event);
};

web_socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(data);
    if (data['request_type'] == 'new_discussion') {
        comments.append(load_comment(
            data['node_id'],
            data['user_name'],
            data['date'],
            data['text']
        ), comment_reply_area(
            data['node_id']
        ));
    } else if (data['request_type'] == 'new_reply') {
        target_node = document.querySelector(`#${data['target_id']}`);
        target_node.childNodes[1].appendChild(load_reply(
            data['user_name'],
            data['date'],
            data['text']
        ));
    }
};

// DOM Modifications
reply_buttons.forEach(reply_button => {
    reply_button.addEventListener('click', (event) => {
        load_reply_form(event);
    });
});

discussion_form.onsubmit = function (event) {
    event.preventDefault();
    const text = discussion_editor.getData();
    if (text.length == 0)
        return;
    web_socket.send(JSON.stringify({
        'request_type': 'new_discussion',
        'text': text
    }));
    discussion_editor.setData('');
};

reply_form.onsubmit = function (event) {
    event.preventDefault();
    const text = reply_editor.getData();
    if (text.length == 0)
        return;
    web_socket.send(JSON.stringify({
        'request_type': 'new_reply',
        'target_id': target_node.id,
        'text': text
    }));
    reply_editor.setData('');
};


function load_reply_form(event) {
    event.preventDefault();
    const reply_area = document.querySelector('#reply_area');
    if (reply_area) {
        console.log(reply_area);
        reply_area.remove();
    }
    target_node = document.querySelector(`#replies_${event.target.id}`);
    target_node.appendChild(load_reply_area());
    reply_editor = load_editor('reply_input');
}

function load_reply_area() {
    const card_node = document.createElement('div');
    card_node.className = 'comment_card comment_form';
    card_node.id = 'reply_area';
    const info_node = document.createElement('div');
    info_node.className = 'comment_info';
    const text_node = document.createElement('h5');
    text_node.innerHTML = 'Write your reply';
    const body_node = document.createElement('div');
    body_node.className = 'comment_body';
    const input_node = document.createElement('textarea');
    input_node.name = 'text';
    input_node.id = 'reply_input';
    input_node.rows = 10;
    const actions_node = document.createElement('div');
    actions_node.className = 'actions text-right';
    const action_node = document.createElement('button');
    action_node.className = 'btn btn-outline-light';
    action_node.type = 'submit';
    action_node.innerHTML = 'Reply';

    info_node.appendChild(text_node);
    body_node.appendChild(input_node);
    actions_node.appendChild(action_node);
    card_node.append(info_node, body_node, actions_node);
    return card_node;
}

function load_comment(node_id, user_name, date, text) {
    const card_node = document.createElement('div');
    card_node.className = 'comment_card';
    const info_node = document.createElement('div');
    info_node.className = 'comment_info';
    const text_node = document.createElement('h5');
    text_node.innerHTML = user_name;
    const date_node = document.createElement('div');
    date_node.className = 'text-right';
    date_node.innerHTML = date;
    const body_node = document.createElement('div');
    body_node.className = 'comment_body';
    body_node.innerHTML = text;
    const actions_node = document.createElement('div');
    actions_node.className = 'actions text-right';
    const action_node = document.createElement('a');
    action_node.className = 'reply_buttons';
    action_node.id = `card_${node_id}`;
    action_node.href = '';
    action_node.innerHTML = 'Reply';

    info_node.append(text_node, date_node);
    actions_node.appendChild(action_node);
    card_node.append(info_node, body_node, actions_node);

    action_node.addEventListener('click', (event) => {
        load_reply_form(event);
    });
    return card_node;
}

function comment_reply_area(node_id) {
    const card_node = document.createElement('div');
    card_node.id = `replies_card_${node_id}`;
    const replies_node = document.createElement('div');
    replies_node.className = 'replies';

    card_node.appendChild(replies_node);
    return card_node;
}

function load_reply(user_name, date, text) {
    const card_node = document.createElement('div');
    card_node.className = 'comment_card comment_replies';
    const info_node = document.createElement('div');
    info_node.className = 'comment_info';
    const text_node = document.createElement('h5');
    text_node.innerHTML = user_name;
    const date_node = document.createElement('div');
    date_node.className = 'text-right';
    date_node.innerHTML = date;
    const body_node = document.createElement('div');
    body_node.className = 'comment_body';
    body_node.innerHTML = text;

    info_node.append(text_node, date_node);
    card_node.append(info_node, body_node);
    return card_node;
}

// MathJax Clean Load
window.onload = function() {
    document.querySelector('#content').style.display = 'block';
}