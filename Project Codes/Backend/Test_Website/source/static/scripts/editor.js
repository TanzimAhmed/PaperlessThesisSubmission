
// CK Editor initialization
CKEDITOR.plugins.addExternal('ckeditor_wiris', 'https://www.wiris.net/demo/plugins/ckeditor/', 'plugin.js');

// CK Editor configurations
let editor = CKEDITOR.replace('input', {
    // For now, MathType is incompatible with CKEditor file upload plugins.
    extraPlugins: 'image2,mathjax,codesnippet,embed,autoembed,ckeditor_wiris',
    removePlugins: 'image,uploadimage,uploadwidget,uploadfile,filetools,filebrowser',
    height: 700,
    mathJaxLib: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=TeX-MML-AM_CHTML',

    //filebrowserBrowseUrl: '/apps/ckfinder/3.4.5/ckfinder.html',
    //filebrowserImageBrowseUrl: '/apps/ckfinder/3.4.5/ckfinder.html?type=Images',
    //filebrowserUploadUrl: '/content/upload/',
    //filebrowserImageUploadUrl: '/content/upload/',

    allowedContent: true,

    toolbarGroups: [
        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
        '/',
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
        { name: 'links', groups: [ 'links' ] },
        '/',
        { name: 'styles', groups: [ 'styles' ] },
        { name: 'colors', groups: [ 'colors' ] },
        { name: 'tools', groups: [ 'tools' ] },
        { name: 'others', groups: [ 'others' ] },
        { name: 'about', groups: [ 'about' ] },
        '/',
        { name: 'insert', groups: [ 'insert' ] }
    ],
    removeButtons: 'Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,CreateDiv',
    codeSnippet_theme: 'dark',
    // Load the default contents.css file plus customizations for this sample.
    contentsCss: [
        'http://cdn.ckeditor.com/4.13.1/full-all/contents.css',
        'https://ckeditor.com/docs/vendors/4.13.1/ckeditor/assets/css/widgetstyles.css'
    ],
    // Embed Content provider (Iframely API)
    // Setup content provider. See https://ckeditor.com/docs/ckeditor4/latest/features/media_embed
    embed_provider: '//ckeditor.iframe.ly/api/oembed?url={url}&_horizontal=true&_height=300&callback={callback}'

    // Update the ACF configuration with MathML syntax.
    //extraAllowedContent: mathElements.join(' ') + '(*)[*]{*};img[data-mathml,data-custom-editor,role](Wirisformula)'
});


// DOM Modifications
const output = document.querySelector('#output');
const asset_display = document.querySelector('#asset_display_button');
const overlays = document.querySelectorAll('.overlays');
const close_icon = document.querySelector('#close_icon');
const asset_form_container = document.querySelector('#asset_form_container');
const asset_form = document.querySelector('#asset_form');
const asset_delete_form = document.querySelector('#asset_delete_form');
const asset_delete_buttons = document.querySelectorAll('.asset_delete_buttons');
const asset_area = document.querySelector('#asset_area');

// Event Listeners
asset_delete_buttons.forEach((delete_button) => {
   delete_button.addEventListener('click', delete_asset);
});

asset_display.onclick = function(event) {
    event.preventDefault();
    overlays.forEach((overlay) => {
        overlay.style.display = 'block';
    });

};

close_icon.onclick = function(event) {
    event.preventDefault();
    overlays.forEach((overlay) => {
        overlay.style.display = 'none';
    });
};

// Asset Upload form submit
asset_form.onsubmit = function(event) {
    event.preventDefault();
    const xhr = new XMLHttpRequest();
    const form_data = new FormData(asset_form);

    xhr.open('POST', asset_form.getAttribute('action'), true);
    console.log(form_data.get('upload_file'));
    xhr.onload = function() {
        if (this.status == 200) {
            const data = JSON.parse(this.responseText)

            const card_node = create_node('div', 'asset_card');
            const delete_node = create_node(
                'a',
                'btn btn-danger asset_delete_buttons',
                data.id
            );
            delete_node.href = '';
            delete_node.innerHTML = 'Delete';
            const resource_node = create_node('a');
            resource_node.href = data.url;
            const image_node = create_node('img', 'rounded');
            image_node.src = data.url;
            const info_node = create_node('p', 'resource_url');
            info_node.title = 'Copy this URL';
            info_node.setAttribute('data-toggle', 'tooltip');
            const helper_text = create_node('strong');
            helper_text.innerHTML = 'URL';
            const line_break = create_node('br');
            const url_node = create_node('span');
            url_node.innerHTML = data.url;

            resource_node.appendChild(image_node);
            info_node.append(helper_text, line_break, url_node);
            card_node.append(delete_node, resource_node, info_node);

            delete_node.addEventListener('click', delete_asset);

            asset_area.insertBefore(card_node, asset_form_container);
            asset_form.reset();
        } else {
            alert(this.status + ' ' + this.responseText);
        }
    };
    xhr.send(form_data);
    console.log('File Uploaded');
};

function delete_asset(event) {
    event.preventDefault();
    const xhr = new XMLHttpRequest();
    const form_data = new FormData(asset_delete_form);
    const target_node = event.target;

    form_data.set('resource_id', target_node.id);

    xhr.open('POST', asset_delete_form.getAttribute('action'), true);
    xhr.onload = function() {
        if (this.status == 200) {
            target_node.parentElement.remove();
        } else {
            alert(this.status + ' ' + this.responseText);
        }
    };
    xhr.send(form_data);
}

function create_node(node_tag, class_name=null, id=null) {
    const node = document.createElement(node_tag);
    if (class_name)
        node.className = class_name;
    if (id)
        node.id = id;
    return node;
}

// Editor Change Listeners
editor.on( 'change', (event) => {
    // getData() returns CKEditor's HTML content.
    load_math(event);
    load_code();
});

editor.on('dialogHide', (event) => {
    load_math(event);
    load_code();
});

function load_math(event) {
    output.innerHTML = event.editor.getData();
    MathJax.texReset();
    MathJax.typesetClear();
    MathJax.typesetPromise([output]).catch(function (err) {
        latex_output.innerHTML = '';
        latex_output.appendChild(document.createTextNode(err.message));
        console.error(err);
    }).then(function () {
    });
    document.querySelector('#right').style.borderLeft = '1px solid grey';
}

function load_code() {
    document.querySelectorAll('pre code').forEach((code) => {
        hljs.highlightBlock(code);
    });
}

// MathJax initialization
MathJax = {
    loader: {load: ['input/asciimath', 'output/chtml']},
};

/*
document.querySelector('#insert_text').addEventListener('click', insert_text);

function insert_text() {
  alert("Insert Text");
  CKEDITOR.instances.input.insertHtml('<div> some text here </div>');
}
*/

