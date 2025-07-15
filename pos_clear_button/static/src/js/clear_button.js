/** @odoo-module */
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";


patch(ControlButtons.prototype, {
    async onClickClear() {
        var order = this.pos.get_order();
        var lines = order.get_orderlines();
        if (lines.length) {
            this.dialog.add(ConfirmationDialog, {
                body:"Are you sure to remove all orders from the cart?",
                confirm: () => {  lines.filter(line => line.get_product()).forEach(line => order.removeOrderline(line)); },
                confirmLabel: "Clear",
                confirmClass: "btn-danger",
                cancel: () => {},
                cancelLabel: "Cancel",
            });
        }else{
            this.notification.add(("No Items in the Order to clear."), { type: "danger" });
        }
    }
})

patch(Orderline.prototype, {
    setup() {
        super.setup();
        this.numberBuffer = useService("number_buffer");
    },

    async onClickClearLine() {
        this.numberBuffer.sendKey('Backspace');
        this.numberBuffer.sendKey('Backspace');
    }
});