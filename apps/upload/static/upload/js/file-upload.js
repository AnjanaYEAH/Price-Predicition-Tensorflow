/******* FILE UPLOAD HANDLING *******/

// get request's csrf_token for secure AJAX requests
var csrftoken = getCookie('csrftoken');
var jqXHR; // ajax request object


// Add uploaded file with parsed upload date to table
function addToTable(file) {
    var date = parseDate(file.date);

    $("#file-explorer tbody").prepend(
        "<tr><td class='ellipsis'><a class='filename' href='" + file.url + "'>" + formatFilename(file.name) + "</a></td><td>" + date + "</td><td class='tight'><button class='upload-file btn-standard'>Upload</button></td><td class='tight'><button class='remove-file btn-standard' onclick=\"location.href='" + file.id + "/delete/';\">Remove</button></td></tr>"
    )
    $('.upload-file').attr('disabled', 'disabled');
    $('.remove-file').attr('disabled', 'disabled');
}

// Show 'upload' button
function canUpload() {
    $(".upload-progress").hide();
    $("#manual-upload-link").show();
    $("#cancel-upload").hide();
}

// Show 'cancel upload' button
function canCancelUpload() {
    $(".upload-progress").show();
    $("#manual-upload-link").hide();
    $("#cancel-upload").show();
}

function disableUploads() {
    $('#fileupload').fileupload({
        dropZone: null
    });
    $("#manual-upload-link").hide();
    $("#cancel-upload").hide();
    $('.upload-file').attr('disabled', 'disabled');
    $('.remove-file').attr('disabled', 'disabled');
    $(".upload-progress").hide();
}

// Extract CSV file name from longer path
function formatFilename(name) {
    return name.split('/')[1];
}

// Stop 'generating images' animations
function generatingImagesOff() {
    $("#generating-images-text").hide();
    $("#dropzone").removeClass("progress-orange");
    $(".loading-icon").hide();
}

// Start 'generating images' animations
function generatingImagesOn() {
    $("#generating-images-text").show();
    $("#dropzone").addClass("progress-orange");
    $(".loading-icon").show();
}

function getPercentage(x, total) {
    return parseInt(x / total * 100, 10) + "%";
}

// Converts datetime object into dd/mm/yyyy string
function parseDate(date) {
    var options = {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    };
    return new Date(date).toLocaleDateString('en-us', options);
}

function showErrorMessage(message) {
    $("#error-list").html("<p class='container'>" + message + "</p>");
    $("#error-list").show().delay(5000).fadeOut();
    generatingImagesOff();
}

// Show button linking to results page
function showGraphURL(fileName) {
    var graphURL = fileName.substring(fileName.indexOf('/') + 1, fileName.indexOf('.')) + '/graph/';
    $("#graph-link").html("<a class='btn-standard graph-link-a' href='" + graphURL + "'>View results</a>");
    fileAccepted();
    setTimeout(function() {
        $("#dropzone").addClass("results-bg");
        $(".graph-link-a").addClass("rotate-center");
    }, 500);
}

function updateProgressBar(percent) {
    $(".upload-progress-bar").css({
        "width": percent
    });
    $(".upload-progress-text").text(percent);
    if (percent == "100%") {
        $(".upload-progress").hide();
        $("#cancel-upload").hide();
        generatingImagesOn();
    }
}

// Events triggered when upload is cancelled
$("#cancel-upload").click(function() {
    jqXHR.abort(); // abort upload
    jqXHR = null;
    canUpload();
    fileRejected();
});

// Open file explorer to select file to upload
$("#manual-upload-link").click(function() {
    $("#fileupload").click();
});

// Drop zone upload handling
$('#fileupload').fileupload({
        dataType: 'json',
        dropZone: $('#dropzone'),
        singleFileUploads: false, // All files dropped at once so we can count them
        add: function(e, data) {
            var extension = data.originalFiles[0].name.substr(
                (data.originalFiles[0].name.lastIndexOf('.') + 1));
            // Only one upload at a time
            if (data.files.length > 1) {
                fileRejected();
                showErrorMessage("Only one file can be uploaded at once.");
            } else if (extension != 'csv') {
                fileRejected();
                showErrorMessage("File type must be .csv only.");
            } else if (data.originalFiles[0]['size'] > 10000000) {
                fileRejected();
                showErrorMessage("File size is too big. Maximum 10MB.");
            } else if (data.originalFiles[0]['size'] < 10000) {
                fileRejected();
                showErrorMessage("File size is too small. Minimum 10kB.");
            } else {
                jqXHR = data.submit();
            }
        },
        start: function(e) {
            canCancelUpload();
        },
        stop: function(e) {
            // Stop functionality
        },
        progressall: function(e, data) {
            updateProgressBar(getPercentage(data.loaded, data.total));
        },
        done: function(e, data) {
            if (data.result.is_valid) {
                generatingImagesOff();
                disableUploads();
                showGraphURL(data.result.name);
                addToTable(data.result);
            } else {
                if (data.result.file_error) {
                    // File error
                    showErrorMessage(data.result.file_error);
                } else {
                    // Form error
                    var a = JSON.parse(data.result.form_error);
                    showErrorMessage(a.__all__[0].message);
                }
                canUpload();
                fileRejected();
            }
        }
    })
    .on('fileuploadprocessalways', function(e, data) {
        if (data.files.error) {
            fileRejected();
        } else {
            xhr = data.submit(); // Submit ajax post
        }
    })
    .on("fileuploadprocessfail", function(e, data) {
        fileRejected();
        var file = data.files[data.index];
        alert(file.error);
    });


// Uploading a file from the database
$(document).on('click', '.upload-file', function(e, data) {
    // Get file name from table
    var fileURL = "csv-files/" + $('td:first', $(this).parents('tr')).text();
    disableUploads();
    generatingImagesOn();

    // AJAX POST request sending filename to be uploaded
    $.ajax({
        url: "",
        type: "post",
        dataType: 'json',
        data: JSON.stringify({
            fileName: fileURL
        }),
        success: function(data) {
            if (data.error) {
                showErrorMessage(data.error);
                canUpload();
            } else {
                disableUploads()
                showGraphURL(data.name);
            }
            generatingImagesOff();
        },
        error: function(xhr, errmsg, err) {
            alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
        }
    });
});
