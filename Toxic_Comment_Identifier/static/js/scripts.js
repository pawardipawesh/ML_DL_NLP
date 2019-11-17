function myFunction() {
    var text1 = $('#id_words').val();
    $('#spinner').show();
    $.ajax({
        url: "/identify_toxicity",
        type: "POST",
        data: { text1: text1 }
    }).done(function (response) {
        var html = '<div id="sub-data" class="d-flex flex-wrap align-items-start">'
        response = response.result;
        $.each(response, function (key, val) {
            console.log(val.split('<br>'));
            $.each(val.split('<br>'), function (index, word) {
                html += '<div class="p2">' + word + '</div>';
            })
        });
        html += "</div>";
        $('#spinner').hide();
        $("#sub-data").remove();
        $(".show-data").append(html);
    });
};



// Get the input field
var input = document.getElementById("id_words");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("btn-go").click();
  }
});