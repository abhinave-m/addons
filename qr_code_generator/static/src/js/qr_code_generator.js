/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";


export class SystrayQR extends Component {
    setup() {
        this.state = useState({
            text: "",
            qrDataUrl: "",
            dropdownOpen: false,
        });

        this.rootRef = useRef("root");
        this.hiddenQRRef = useRef("hiddenQR");

        this.onClickOutside = (ev) => {
            const rootEl = this.rootRef.el;
            if (!rootEl.contains(ev.target)) {
                this.state.dropdownOpen = false;
                this.state.text = "";
                this.state.qrDataUrl = "";
            }
        };

        onMounted(() => {
            document.addEventListener("click", this.onClickOutside);
        });

        onWillUnmount(() => {
            document.removeEventListener("click", this.onClickOutside);
        });
    }

    toggleDropdown(ev) {
        ev.stopPropagation();
        this.state.dropdownOpen = !this.state.dropdownOpen;
    }

    generateQR() {
    const value = this.state.text.trim();

    if (value.length === 0) {
        this.state.qrDataUrl = "";
        alert("No input text to generate QR")
        return;
    }

    if (value.length > 1000) {
        alert("Text is too long for QR code");
        return;
    }

    const container = this.hiddenQRRef.el;
    container.innerHTML = "";

    const qr = new QRCode(container, {
        text: value,
        width: 256,
        height: 256,
    });

    const canvas = container.querySelector("canvas");
    if (canvas) {
        this.state.qrDataUrl = canvas.toDataURL("image/png");
    } else {
        console.error("QR generation failed: canvas not found");
    }

}
    resetQR() {
    this.state.text = "";
    this.state.qrDataUrl = "";
    }

}

SystrayQR.template = "systray_qr_dropdown";
export const systrayItem = {
    Component: SystrayQR,
};
registry.category("systray").add("SystrayQR", systrayItem, { sequence: 1 });

