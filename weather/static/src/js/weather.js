/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onMounted, useRef, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SystrayWeather extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            showDropdown: false,
            weatherData: {},
            weatherError: "",
        });
        this.rootRef = useRef("root");

        this.onClickOutside = (ev) => {
            const rootEl = this.rootRef.el;
            if (rootEl && !rootEl.contains(ev.target)) {
                this.state.weatherData = {};
                this.state.weatherError = "";
                this.state.showDropdown = false;
            }
        };

        onMounted(async () => {
            document.addEventListener("click", this.onClickOutside);

            const enabled = await this.orm.call(
                "ir.config_parameter",
                "get_param",
                ["weather.enable_weather"]
            );
            if (!(enabled === true || enabled === "True")) {
                registry.category("systray").remove("SystrayWeather");
            }
        });

        onWillUnmount(() => {
            document.removeEventListener("click", this.onClickOutside);
        });
    }

    async toggleDropdown(ev) {
        ev.stopPropagation();
        this.state.showDropdown = !this.state.showDropdown;

        if (this.state.showDropdown) {
            const data = await this.orm.call(
                "res.config.settings",
                "get_weather_from_settings",
                []
            );
            if (data.error) {
                this.state.weatherError = data.error;
                this.state.weatherData = {};
            } else {
                this.state.weatherError = "";
                this.state.weatherData = data;
            }
        }
    }
}

SystrayWeather.template = "systray_weather_dropdown";

export const systrayItem = {
    Component: SystrayWeather,
    isDisplayed: () => true, // Always render; we'll hide manually via onMounted
};

registry.category("systray").add("SystrayWeather", systrayItem, { sequence: 10 });
