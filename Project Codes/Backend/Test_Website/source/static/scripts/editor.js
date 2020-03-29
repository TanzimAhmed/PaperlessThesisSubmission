
// CK Editor initialization
CKEDITOR.plugins.addExternal('ckeditor_wiris', 'https://www.wiris.net/demo/plugins/ckeditor/', 'plugin.js');

let editor = CKEDITOR.replace('input', {
    // For now, MathType is incompatible with CKEditor file upload plugins.
    extraPlugins: 'image2,mathjax,embed,autoembed,ckeditor_wiris',
    removePlugins: 'image,uploadimage,uploadwidget,uploadfile,filetools,filebrowser',
    height: 400,
    mathJaxLib: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML',

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
    // Load the default contents.css file plus customizations for this sample.
    contentsCss: [
        'http://cdn.ckeditor.com/4.13.1/full-all/contents.css',
        'https://ckeditor.com/docs/vendors/4.13.1/ckeditor/assets/css/widgetstyles.css'
    ],
    // Setup content provider. See https://ckeditor.com/docs/ckeditor4/latest/features/media_embed
    embed_provider: '//ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}'

    // Update the ACF configuration with MathML syntax.
    //extraAllowedContent: mathElements.join(' ') + '(*)[*]{*};img[data-mathml,data-custom-editor,role](Wirisformula)'
});


// DOM Modifications
let output = document.querySelector('#output');
let form = document.querySelector('#image_upload_form');

form.onsubmit = function(event) {
    event.preventDefault();
    let form_data = new FormData(form);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', form.getAttribute('action'), true);
    console.log(form_data.get('upload_file'));
    xhr.onload = function() {
        if (this.status == 200) {
            let item_node = document.createElement('li');
            item_node.innerHTML = this.responseText;
            document.querySelector('#resources').appendChild(item_node);
        }
    };
    xhr.send(form_data);
    console.log('File Uploaded');
};

editor.on( 'change', function(event) {
    // getData() returns CKEditor's HTML content.
    load_math(event);
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

