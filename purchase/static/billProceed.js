$(document).ready(function() {

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$('#getData').click(function (e) {
            e.preventDefault();   
//var csrftoken = $("[name=csrfmiddlewaretoken]").val();
                        
var cash_paid = $('#cash_paid').val();
var email = $('#email').val();
//alert(csrftoken);
var denomData = {
    500: $('#denom_500').val(),
    100: $('#denom_100').val(),
    50: $('#denom_50').val(),
    20: $('#denom_20').val(),
    10: $('#denom_10').val(),
    5: $('#denom_5').val(),
    2: $('#denom_2').val(),
    1: $('#denom_1').val()
};

console.log(denomData);


    var data = [];

    $('#product-fields-container .row').each(function () {
        var product = $(this).find('.product_id').val();
        var quantity = $(this).find('.quantity').val();

        data.push({
            product_id: product,
            quantity: quantity
        });
    });

    //console.log(data);
        $('#sample').text(JSON.stringify(data, null, 2)); 
                var payload = {
            email: email,
            cash_paid: cash_paid,
            products: data,
            denomination: denomData
        };

                $.ajax({
                            headers: {"X-CSRFToken": csrftoken},
            url: "processBill",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function(response) {
                console.log("Success:", response);
                $('#sample').text("Bill Generated Successfully!");
                if(response.status == "success") {
                            window.location.href = "/final-call";
                }
            },
                error: function(xhr, status, error) {
                        if (xhr.responseJSON && xhr.responseJSON.message) {
                            console.error("Clean Error:", xhr.responseJSON.message);
            $('#sample').html("Error: " + xhr.responseJSON.message);
        } else {
            // If the server crashed so hard it sent the HTML "Yellow Screen"
            console.error("Server crashed with HTML. Check Django console.");
            $('#sample').html("A critical server error occurred.");
        }

            }
        });

});
});

