
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
const comment_edit_buttons = document.querySelectorAll('.comments_edit');
const comment_delete_buttons = document.querySelectorAll('.comments_delete');
const reply_edit_buttons = document.querySelectorAll('.replies_edit');
const reply_delete_buttons = document.querySelectorAll('.replies_delete');
const comments = document.querySelector('#comments');
const reply_form = document.querySelector('#replies_form');
const discussion_form = document.querySelector('#comment_form');
const discussion_editor = load_editor('comment_input');
const comment_form_header = document.querySelector('#comment_form_header');
const comment_button = document.querySelector('#comment_button');
const exit_comment_button = document.querySelector('#exit_comment_button');
let reply_editor = null;
let target_node = null;
let edit_node = null;

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
    if (data['request_type'] == 'new_discussion') {
        comments.append(load_comment(
            data['node_id'],
            data['user_name'],
            data['date'],
            data['text']
        ));
    } else if (data['request_type'] == 'new_reply') {
        document.querySelector(`#${data['target_id']} .replies`).appendChild(load_reply(
            data['target_id'].split('_')[2],
            data['node_id'],
            data['user_name'],
            data['date'],
            data['text']
        ));
    } else if (data['request_type'] == 'edit_discussion') {
        const node = document.querySelector(`#comment_time_${data['node_id']}`);
        node.innerHTML = data['date'];
        document.querySelector(`#comment_${data['node_id']}`).innerHTML = data['text'];
        node.scrollIntoView(true);
    } else if (data['request_type'] == 'edit_reply') {
        const node = document.querySelector(`#reply_time_${data['node_id']}`);
        node.innerHTML = data['date'];
        document.querySelector(`#reply_${data['node_id']}`).innerHTML = data['text'];
        node.scrollIntoView(true);
    } else if (data['request_type'] == 'delete_discussion') {
        document.querySelector(`#comment_card_${data['node_id']}`).remove();
    } else if (data['request_type'] == 'delete_reply') {
        document.querySelector(`#reply_card_${data['node_id']}`).remove();
    }
    load_math();
};

// DOM Modifications
if (reply_buttons) {
    reply_buttons.forEach(reply_button => {
        reply_button.addEventListener('click', (event) => {
            edit_node = null;
            load_reply_form(event);
        });
    });
}

if (comment_edit_buttons) {
    comment_edit_buttons.forEach(edit_button => {
        edit_button.addEventListener('click', (event) => {
            edit_thread(event, 'comment');
        });
    });
}

if (comment_delete_buttons) {
    comment_delete_buttons.forEach(delete_button => {
        delete_button.addEventListener('click', (event) => {
            delete_thread(event, 'comment');
        });
    });
}

if (reply_edit_buttons) {
    reply_edit_buttons.forEach(edit_button => {
        edit_button.addEventListener('click', (event) => {
            edit_thread(event, 'reply');
        });
    });
}

if (reply_delete_buttons) {
    reply_delete_buttons.forEach(delete_button => {
        delete_button.addEventListener('click', (event) => {
            delete_thread(event, 'reply');
        });
    });
}

discussion_form.onsubmit = function (event) {
    event.preventDefault();
    console.log(event.target.id, edit_node);
    const text = discussion_editor.getData();
    if (text.length == 0)
        return;
    if (edit_node) {
        web_socket.send(JSON.stringify({
            'request_type': 'edit_discussion',
            'node_id': edit_node,
            'text': text
        }));
        edit_node = null;
        comment_form_header.innerHTML = 'Write your query';
        comment_button.innerHTML = 'Post';
        exit_comment_button.style.display = 'none';
    } else {
        web_socket.send(JSON.stringify({
            'request_type': 'new_discussion',
            'text': text
        }));
    }
    discussion_editor.setData('');
};

reply_form.onsubmit = function (event) {
    event.preventDefault();
    console.log(event.target.id, edit_node);
    const text = reply_editor.getData();
    if (text.length == 0)
        return;
    if (edit_node) {
        web_socket.send(JSON.stringify({
            'request_type': 'edit_reply',
            'node_id': edit_node,
            'text': text
        }));
        edit_node = null;
        document.querySelector('#reply_form_header').innerHTML = 'Write your reply';
        document.querySelector('#reply_button').innerHTML = 'Reply';
    } else {
        web_socket.send(JSON.stringify({
            'request_type': 'new_reply',
            'target_id': target_node.id,
            'text': text
        }));
    }
    reply_editor.setData('');
};

exit_comment_button.onclick = function (event) {
    if (edit_node != null) {
        comment_form_header.innerHTML = 'Write your query';
        comment_button.innerHTML = 'Post';
        exit_comment_button.style.display = 'none';
        discussion_editor.setData('');
        edit_node = null;
    }
};

function delete_thread(event, type) {
    event.preventDefault();
    console.log(type, event.target.id);
    if (type == 'comment') {
        web_socket.send(JSON.stringify({
            'request_type': 'delete_discussion',
            'node_id': event.target.id,
        }));
    } else if (type == 'reply') {
        web_socket.send(JSON.stringify({
            'request_type': 'delete_reply',
            'node_id': event.target.id
        }));
    }
}

function edit_thread(event, type) {
    event.preventDefault();
    if (type == 'comment') {
        edit_node = event.target.id;
        const text_node = document.querySelector(`#comment_${edit_node}`);

        comment_form_header.innerHTML = 'Update your comment';
        comment_button.innerHTML = 'Update';
        exit_comment_button.style.display = 'inline-block';
        discussion_editor.setData(text_node.innerHTML);
        comment_form_header.scrollIntoView();
    } else if (type == 'reply') {
        edit_node = event.target.id;
        const node_id = edit_node.split('_');
        const text_node = document.querySelector(`#reply_${edit_node}`);
        load_reply_form(null, node_id[0]);

        const reply_form_header = document.querySelector('#reply_form_header');
        reply_form_header.innerHTML = 'Update your Reply';
        document.querySelector('#reply_button').innerHTML = 'Update';
        reply_editor.setData(text_node.innerHTML);
        reply_form_header.scrollIntoView();
    }
}

function load_reply_form(event=null, node_id=null) {
    if (event)
        event.preventDefault();
    const reply_area = document.querySelector('#reply_area');
    if (reply_area) {
        console.log(reply_area);
        reply_area.remove();
    }
    if (event)
        target_node = document.querySelector(`#replies_${event.target.id}`);
    else
        target_node = document.querySelector(`#replies_card_${node_id}`);
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
    text_node.id = 'reply_form_header';
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
    action_node.id = 'reply_button';
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
    card_node.id = `comment_card_${node_id}`;
    const info_node = document.createElement('div');
    info_node.className = 'comment_info';
    const text_node = document.createElement('h5');
    text_node.innerHTML = user_name;
    const date_node = document.createElement('div');
    date_node.className = 'text-right';
    date_node.id = `comment_time_${node_id}`;
    date_node.innerHTML = date;
    const body_node = document.createElement('div');
    body_node.className = 'comment_body';
    body_node.id = `comment_${node_id}`;
    body_node.innerHTML = text;
    const replies_card_node = document.createElement('div');
    replies_card_node.id = `replies_card_${node_id}`;
    const replies_node = document.createElement('div');
    replies_node.className = 'replies';
    const actions_node = document.createElement('div');
    actions_node.className = 'actions text-right';
    const reply_node = document.createElement('a');
    reply_node.className = 'reply_buttons';
    reply_node.id = `card_${node_id}`;
    reply_node.href = '';
    reply_node.innerHTML = 'Reply';
    const edit_node = document.createElement('a');
    edit_node.className = 'comments_edit';
    edit_node.id = node_id;
    edit_node.href = '';
    edit_node.innerHTML = 'Edit';
    const delete_node = document.createElement('a');
    delete_node.className = 'comments_delete';
    delete_node.id = node_id;
    delete_node.href = '';
    delete_node.innerHTML = 'Delete';

    info_node.append(text_node, date_node);
    replies_card_node.appendChild(replies_node);
    actions_node.append(delete_node, edit_node, reply_node);
    card_node.append(info_node, body_node, replies_card_node, actions_node);

    reply_node.addEventListener('click', (event) => {
        load_reply_form(event);
    });
    edit_node.addEventListener('click', (event) => {
        edit_thread(event, 'comment');
    });
    delete_node.addEventListener('click', (event) => {
        delete_thread(event, 'comment');
    });
    return card_node;
}

function load_reply(target_id, node_id, user_name, date, text) {
    const card_node = document.createElement('div');
    card_node.className = 'comment_card comment_replies';
    card_node.id = `reply_card_${target_id}_${node_id}`;
    const info_node = document.createElement('div');
    info_node.className = 'comment_info';
    const text_node = document.createElement('h5');
    text_node.innerHTML = user_name;
    const date_node = document.createElement('div');
    date_node.className = 'text-right';
    date_node.id = `reply_time_${target_id}_${node_id}`;
    date_node.innerHTML = date;
    const body_node = document.createElement('div');
    body_node.className = 'comment_body';
    body_node.id = `reply_${target_id}_${node_id}`;
    body_node.innerHTML = text;
    const actions_node = document.createElement('div');
    actions_node.className = 'actions text-right';
    const edit_node = document.createElement('a');
    edit_node.className = 'replies_edit';
    edit_node.id = `${target_id}_${node_id}`;
    edit_node.href = '';
    edit_node.innerHTML = 'Edit';
    const delete_node = document.createElement('a');
    delete_node.className = 'replies_delete';
    delete_node.id = `${target_id}_${node_id}`;
    delete_node.href = '';
    delete_node.innerHTML = 'Delete';

    info_node.append(text_node, date_node);
    actions_node.append(delete_node, edit_node);
    card_node.append(info_node, body_node, actions_node);

    edit_node.addEventListener('click', (event) => {
        edit_thread(event, 'reply');
    });
    delete_node.addEventListener('click', (event) => {
        delete_thread(event, 'reply');
    });
    return card_node;
}

function load_math() {
    let node = document.querySelector('#comments');
    MathJax.texReset();
    MathJax.typesetClear();
    MathJax.typesetPromise([node]).catch(function (err) {
        node.innerHTML = '';
        node.appendChild(document.createTextNode(err.message));
        console.error(err);
    }).then(function () {
    });
}

// MathJax Clean Load
window.onload = function() {
    document.querySelector('#content').style.display = 'block';
};