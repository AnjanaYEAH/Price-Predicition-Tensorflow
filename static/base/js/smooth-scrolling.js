// Script for smooth scrolling

// Set up
var modern = requestAnimationFrame,
  duration = 600,
  initial, aim;

// If 'Find out more' button clicked, trigger smooth scrolling
document.getElementById('find-out-more').addEventListener('click', function() {

  aim = -56; // offset from navbar
  initial = Date.now();

  smoothScroll(document.getElementById('about'));
});


window.smoothScroll = function(target) {

  var scrollContainer = target;

  // While not at target, keep scrolling
  do {
    scrollContainer = scrollContainer.parentNode;
    if (!scrollContainer) return;
    scrollContainer.scrollTop += 1;
  }
  while (scrollContainer.scrollTop == 0);

  // Account for navbar offset
  do {
    if (target == scrollContainer) break;
    aim += target.offsetTop;
  }
  while (target = target.offsetParent);

  // Smooth scrolling for modern and old browsers
  scroll = function(c, a, b, i) {
    if (modern) {
      var present = Date.now(),
        elapsed = present - initial,
        progress = Math.min(elapsed / duration, 1);
      c.scrollTop = a + (b - a) * progress;
      if (progress < 1) requestAnimationFrame(function() {
        scroll(c, a, b, i);
      });
    } else {
      i++;
      if (i > 30) return;
      c.scrollTop = a + (b - a) / 30 * i;
      setTimeout(function() {
        scroll(c, a, b, i)
      }, 20);
    }
  }

  scroll(scrollContainer, scrollContainer.scrollTop, aim, 0);
}
