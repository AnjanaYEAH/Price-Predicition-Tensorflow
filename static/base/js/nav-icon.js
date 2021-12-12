$(document).ready(function() {
    var open = false;

    // Toggle nav icon animation
    $(document).ready(function() {
        $('.nav-button').on('click', function() {
            $('.menu-icon').toggleClass('open');
        });
    });

    // Toggle drop-down menu
    $('.dropdown-toggle').click(function() {
        $(this).next('.dropdown-menu').slideToggle(300);
    });
});
