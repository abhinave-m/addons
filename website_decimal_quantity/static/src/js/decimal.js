import publicWidget from "@web/legacy/js/public/public_widget";
import wSaleUtils from "@website_sale/js/website_sale_utils";
import { rpc } from "@web/core/network/rpc";
import { Component } from "@odoo/owl";

publicWidget.registry.WebsiteSale.include({

    // 🔼 +/- Button Click: Adjust quantity with 0.1 step
    _onClickAddCartJSON(ev) {
        ev.preventDefault();
        const $link = $(ev.currentTarget);
        const $input = $link.closest('.input-group').find("input");

        const isProductPage = $('body').hasClass('o_wsale_product_page');
        const min = isProductPage ? 1.0 : 0.0;
        const max = parseFloat($input.data("max") || Infinity);

        const prevQty = parseFloat($input.val() || 0);

        // Determine whether it's a minus or plus button
        const isMinus = $link.has(".fa-minus").length > 0;
        const delta = isMinus ? -0.1 : 0.1;

        let newQty = prevQty + delta;

        // 🔒 Clamp quantity between min and max
        newQty = Math.max(min, Math.min(newQty, max));
        newQty = parseFloat(newQty.toFixed(1));

        if (newQty !== prevQty) {
            $input.val(newQty).trigger('change');
        }

        return false;
    },

    // 🔄 Cart Update Logic
    _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
        $($dom_optional).toArray().forEach((elem) => {
            $(elem).find('.js_quantity').text(value);
            productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
        });

        $input.data('update_change', true);

        rpc("/shop/cart/update_json", {
            line_id: line_id,
            product_id: parseInt($input.data('product-id'), 10),
            set_qty: value,
            display: true,
        }).then((data) => {
            $input.data('update_change', false);
            let check_value = parseFloat($input.val());
            if (isNaN(check_value)) check_value = 1;
            if (value !== check_value) {
                $input.trigger('change');
                return;
            }

            // 🛒 If cart becomes empty, redirect to cart
            if (!data.cart_quantity) {
                return window.location = '/shop/cart';
            }

            $input.val(data.quantity);
            $('.js_quantity[data-line-id=' + line_id + ']').val(data.quantity).text(data.quantity);

            wSaleUtils.updateCartNavBar(data);
            wSaleUtils.showWarning(data.notification_info.warning);
            Component.env.bus.trigger('cart_amount_changed', [data.amount, data.minor_amount]);
        });
    },

    // 🖊️ Manual Quantity Change
    _onChangeCartQuantity: function (ev) {
        ev.preventDefault();
        const $input = $(ev.currentTarget);
        if ($input.data('update_change')) return;

        let value = parseFloat($input.val() || 0);
        if (isNaN(value)) value = 1;

        const $dom = $input.closest('tr');
        const $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
        const line_id = parseInt($input.data('line-id'), 10);
        const productIDs = [parseInt($input.data('product-id'), 10)];

        this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
    },

});
