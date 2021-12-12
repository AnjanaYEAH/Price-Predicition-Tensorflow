/******* DRAG-DROP EFFECTS FOR UPLOAD FIELD *******/

// Allow for custom event handling
$(document).bind('drop dragover', function(e) {
    e.preventDefault();
});

// Add event handling for when the drag object leaves the dropzone
document.addEventListener("dragleave", function(e) {
    $('#dropzone').removeClass('over');
});

// Drag and drop handling
$('#fileupload')
    .bind('fileuploaddragover', function(e, data) {
        $('#dropzone').addClass('over');
    })
    .bind('fileuploaddrop', function(e, data) {
        $('#dropzone').removeClass('over');
    });

function fileRejected() {
    $('#dropzone').addClass('rejected').delay(1000).queue(function() {
        $(this).removeClass('rejected').dequeue();
    });
}

function fileAccepted() {
    $('#dropzone').addClass('uploaded').delay(1000).queue(function() {
        $(this).removeClass('uploaded').dequeue();
    });
}
