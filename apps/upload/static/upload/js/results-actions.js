/********* TAB BUTTON HANDLING *********/
$("#chartButton").click(function() {
    $("#chart-container").css('display', 'flex');
    $("#results-container").hide();
    $("#visualise-container").hide();
    activeButtonController();
});

$("#visualiseButton").click(function() {
    $("#visualise-container").css('display', 'flex');
    $("#chart-container").hide();
    $("#results-container").hide();
    activeButtonController();
});

$("#resultsButton").click(function() {
    $("#results-container").css('display', 'flex');
    $("#chart-container").hide();
    $("#visualise-container").hide();
    activeButtonController();
});

// Highlight button of active container
function activeButtonController() {
    activeButton('#chart-container');
    activeButton('#visualise-container');
    activeButton('#results-container');
}

// Identify container that is active and highlight it's associated button
function activeButton(tag) {
    var btnName = tag.substring(0,
        tag.lastIndexOf("-")
    ) + "Button";
    if (!$(tag).is(":hidden")) {
        $(btnName).addClass('activeButton');
    } else {
        $(btnName).removeClass('activeButton');
    }
}
