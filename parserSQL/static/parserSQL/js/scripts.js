document.addEventListener('DOMContentLoaded', function() {
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.28.0/min/vs' }});
    require(['vs/editor/editor.main'], function() {
        var editor = monaco.editor.create(document.getElementById('editor'), {
            language: 'sql',
            theme: 'vs-dark'
        });

        document.getElementById('my-file').addEventListener('change', function() {
            var file = this.files[0];
            var reader = new FileReader();

            reader.onload = function(e) {
                var contents = e.target.result;
                editor.setValue(contents);
            };

            reader.readAsText(file);
        });
    });
});