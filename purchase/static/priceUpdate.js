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

$(document).on('change', '.product_id, .quantity', function () {
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
            products: data
        };

                $.ajax({
                            headers: {"X-CSRFToken": csrftoken},
            url: "totalAmount",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function(response) {
                console.log("Success:", response);
                $('#priceInfo').text(response.message);
                
            },
                error: function(xhr, status, error) {
                        if (xhr.responseJSON && xhr.responseJSON.message) {
                            console.error("Clean Error:", xhr.responseJSON.message);
            $('#priceInfo').html("Error: " + xhr.responseJSON.message);
        } else {
            // If the server crashed so hard it sent the HTML "Yellow Screen"
            console.error("Server crashed with HTML. Check Django console.");
            $('#sample').html("A critical server error occurred.");
        }

            }
        });

});
});

