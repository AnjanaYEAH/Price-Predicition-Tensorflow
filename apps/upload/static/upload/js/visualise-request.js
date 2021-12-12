/*********** REQUEST TO TRIGGER TENSORFLOW BACKEND ***********/
var csrftoken = getCookie('csrftoken');

$(document).ready(function() {
  // AJAX POST request to trigger TensorFlow backend when page loads
  $.ajax({
    url: "",
    type: "post",
    dataType: 'json',
    data: JSON.stringify({
      ready: 'yes'
    }),
    success: function(data) {
      if (data.error) {
        // alert(data.error);
      } else {
        // iframe to contain TensorBoard
        const $iframe = $("<iframe scrolling='yes'/>");
        $iframe.css({
          "height": "100%",
          "width": "100%",
          "min-width": "675px"
        });
        setTimeout(() => {
          $iframe[0].src = data.visualiseLink;
        }, 10000) // Wait 10 seconds before pulling TensorBoard to ensure successful connection

        // Remove loading animations
        $(".loading-section").hide();
        // Display results table for predictions
        $("#results-table").css('display', 'table');

        // Add an exit button to quit
        $(".options").append(`<li style="margin-left:auto;" ><button id="resultsButton" class="tab-button" onclick="window.location.href='${data.killLink}'">Exit</button></li>`);

        // Insert TensorBoard into container
        $("#visualise-container").append($iframe);

        $("#buy-p").text(data.buy + '%');
        $("#sell-p").text(data.sell + '%');
        $("#hold-p").text(data.hold + '%');

        // Highlight tab buttons to notify user results are ready
        $("#resultsButton").addClass('readyButton').delay(2000).queue(function() {
          $(this).removeClass('readyButton');
        });
        $("#visualiseButton").addClass('readyButton').delay(2000).queue(function() {
          $(this).removeClass('readyButton');
        });
      }
    },
    error: function(xhr, errmsg, err) {
      alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
    }
  });
});
