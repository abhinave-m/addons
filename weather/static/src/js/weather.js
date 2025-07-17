/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onMounted, useRef, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";


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
    async getWeatherFromGeolocation() {
    if (!navigator.geolocation) {
        this.state.weatherError = "Geolocation is not supported by your browser.";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const coords = [position.coords.latitude, position.coords.longitude];
            console.log(coords)
            try {
                const result = await rpc("/web/dataset/call_kw", {
                    model: "res.config.settings",
                    method: "get_weather_by_coords",
                    args: [coords],
                    kwargs: {},
                });

                if (result.error) {
                    this.state.weatherError = result.error;
                    this.state.weatherData = {};
                } else {
                    this.state.weatherData = result;
                    this.state.weatherError = "";
                }
            } catch (err) {
                this.state.weatherError = "Failed to fetch weather by coordinates.";
                this.state.weatherData = {};
            }
        },
        (error) => {
            this.state.weatherError = "Unable to retrieve your location.";
        }
    );
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
    isDisplayed: () => true,
};

registry.category("systray").add("SystrayWeather", systrayItem, { sequence: 10 });
