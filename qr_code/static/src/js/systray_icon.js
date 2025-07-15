/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";


export class SystrayQR extends Component {
    setup() {
        this.rpc= rpc
        this.state = useState({
            text: "",
            qrDataUrl: "",
            dropdownOpen: false,
        });

        this.rootRef = useRef("root");

        this.onClickOutside = (ev) => {
            const rootEl = this.rootRef.el;
            if (!this.state.dropdownOpen || !rootEl) return;

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

    async generateQR() {
    const value = this.state.text.trim();
    if (value.length == 0){
    alert("No input text to generate QR")
    this.state.qrDataUrl = "";
    return;
    }
    if (value.length > 1000) {
    window.alert("Text is too long for QR code. Please shorten it.");
    return;
    }

    const result = await this.rpc("/qr_systray/generate", { text: value });

    if (result && result.image) {
        this.state.qrDataUrl = result.image;
    }
    else {
        console.error("QR generation failed", result);
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

