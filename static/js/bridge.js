window.onload = function(){
    document.getElementById('body').style.display='none';
    document.getElementById('slug').style.display='none';

    var labels = document.getElementsByTagName('label');
    for (var i=0; i < labels.length; i++)
        if(labels[i].htmlFor != 'title')
            labels[i].style.display='none';
   
    var opt = {
        basePath: '/static',
        textarea: 'body'
    }
    var editor = new EpicEditor(opt).load(function(){
        previewer = this.getElement('previewer');

            // Prettify JS
        var scriptTag = previewer.createElement('script');
        scriptTag.src = '/static/js/google-code-prettify/prettify.js';

            // Prettify CSS
        var cssTag = previewer.createElement('link');
        cssTag.rel = 'stylesheet';
        cssTag.type = 'text/css';
        cssTag.href = '/static/js/google-code-prettify/prettify.css';
           // Add JS / CSS
        previewer.body.appendChild(scriptTag);
        previewer.head.appendChild(cssTag);
    
    });

    editor.on('preview', function() {
        // Add necessary classes to <code> elements
        var previewerBody = previewer.body;
        var codeBlocks = previewerBody.getElementsByTagName('code');

        for (var i = 0; i < codeBlocks.length; i++)
            codeBlocks[i].className += ' prettyprint linenums';
            
        prettyPrint(null, previewerBody);	
        
        var li = previewerBody.getElementsByTagName('li');
        for (var i = 0; i < li.length; i++)
            li[i].className = 'list-style-type: decimal';
	
    });

}

function formSubmit()
{
    document.getElementById('slug').value = document.getElementById('title').value
    document.getElementById('form').submit();
}
