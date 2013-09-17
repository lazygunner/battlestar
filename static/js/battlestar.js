window.onload = function(){
    var opt = {
        basePath: '/static'
    }
    var editor = new EpicEditor(opt).load(function(){
        previewer = this.getElement('previewer');

            // Prettify JS
        var scriptTag = previewer.createElement('script');
        scriptTag.src = 'google-code-prettify/prettify.js';

            // Prettify CSS
        var cssTag = previewer.createElement('link');
        cssTag.rel = 'stylesheet';
        cssTag.type = 'text/css';
        cssTag.href = 'google-code-prettify/prettify.css';
           // Add JS / CSS
        previewer.body.appendChild(scriptTag);
        previewer.head.appendChild(cssTag);
    
    });
    editor.on('preview', function() {
        // Add necessary classes to <code> elements
        var previewerBody = previewer.body;
        var codeBlocks = previewerBody.getElementsByTagName('code');

        for (var i = 0; i < codeBlocks.length; i++)
            codeBlocks[i].className += ' prettyprint';

        prettyPrint(null, previewerBody);
    });

}


