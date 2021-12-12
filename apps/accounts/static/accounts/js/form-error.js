// FORM REJECT
function shakeForm() {
    $(".form").addClass('shake-horizontal');
}

// MESSAGE HANDLING
function showMessage(className) {
    var t = $(className);
    t.queue('sequence', function(next) {
        t.addClass('slide-in-top');
        t.show();
        next();
    });
    t.delay(5000+500, 'sequence');
    t.queue('sequence', function(next) {
        t.removeClass('slide-in-top');
        t.addClass('fade-out');
        next();
    });
    t.delay(500, 'sequence');
    t.queue('sequence', function(next) {
        t.removeClass('fade-out');
        t.hide();
        next();
    });
    t.dequeue('sequence');
}

// MESSAGE STYLING
function messageType(name) {
    $('.msg').addClass(name).delay(6000).queue(function() {
        $(this).removeClass(name).dequeue();
    });
}
