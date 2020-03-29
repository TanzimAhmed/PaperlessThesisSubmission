CKEDITOR.plugins.addExternal('ckeditor_wiris', 'https://www.wiris.net/demo/plugins/ckeditor/', 'plugin.js');
CKEDITOR.replace('question', {
    // For now, MathType is incompatible with CKEditor file upload plugins.
    extraPlugins: 'image2,mathjax,embed,autoembed,ckeditor_wiris',
    removePlugins: 'image,uploadimage,uploadwidget,uploadfile,filetools,filebrowser',
    height: 200,
    mathJaxLib: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML',
    allowedContent: true
});

CKEDITOR.replace('options', {
    // For now, MathType is incompatible with CKEditor file upload plugins.
    extraPlugins: 'image2,mathjax,embed,autoembed,ckeditor_wiris',
    removePlugins: 'image,uploadimage,uploadwidget,uploadfile,filetools,filebrowser',
    height: 200,
    mathJaxLib: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML',
    allowedContent: true
});