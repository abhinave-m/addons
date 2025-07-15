/** @odoo-module **/


$(document).ready(function () {
    $(document).on("click", "#clear_cart_button", function (ev) {
        ev.preventDefault();
        $.ajax({
            url: "/shop/clear_cart",
            type: "POST",
            success: function () {
                location.reload();
            },
            error: function (xhr, status, error) {
                console.error("Error clearing cart:", error);
            }
        });
    });
});
