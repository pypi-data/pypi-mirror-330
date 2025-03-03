// post_preview
// previewTimer must live outside the functions.
var previewTimer = null;

function previewAjax(textarea, div, show_raw = false){
    // set div to raw textarea while waiting for remote Markdown rendering.
    if (show_raw) {
	// bust HTML tags like <script> to prevent running evil code.
        var busted_textarea = $('#'+textarea).val().replace(/&/g, '&amp;').replace(/</g,'&lt;');
        $('#' + div).html('<span class="preview-raw-markup">'+busted_textarea+'</span>');
    }
    if (previewTimer) {
        clearTimeout(previewTimer);
    }
    previewTimer = setTimeout(
        function() { sendPreview( textarea, div); },
	800
    );
}

function sendPreview(textarea, div){
    $.ajaxSetup ({
        cache: false
    });

    var url    = '/markup-editor-preview';
    var params = { 'data' : $('#'+textarea).val() };

    $( '#' + div ).load( url, params );
}
