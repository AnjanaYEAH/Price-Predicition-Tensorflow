// Roll message display animation: slide in, pause, slide out
function showMessage(className) {
    var t = $(className);
    t.queue('sequence', function(next) {
        t.addClass('slide-in-top');
        t.show();
        next();
    });
    t.delay(5000 + 500, 'sequence');
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

// Style message based on type
function messageType(name) {
    $('.msg').addClass(name).delay(6000).queue(function() {
        $(this).removeClass(name).dequeue();
    });
}
