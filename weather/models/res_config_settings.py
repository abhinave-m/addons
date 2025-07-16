from odoo import api, fields, models
import requests


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_weather = fields.Boolean(string="Enable Weather",config_parameter="weather.enable_weather")
    weather_api_key = fields.Char(string="API Key :",config_parameter="weather.api_key")
    weather_location = fields.Char(string="Location :",config_parameter="weather.location")

    @api.model
    def get_weather_from_settings(self):
        enable = self.env["ir.config_parameter"].sudo().get_param("weather.enable_weather")
        if not enable or enable in ["False", False]:
            return {"error": "Weather is disabled in settings."}

        api_key = self.env["ir.config_parameter"].sudo().get_param("weather.api_key")
        if not api_key:
            return {"error": "API key not configured."}

        location = self.env["ir.config_parameter"].sudo().get_param("weather.location")
        if not location:
            return {"error": "No default location configured."}

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)
            response.raise_for_status()
            print(response.json())
            return response.json()
        except Exception as e:
            return {"error": str(e)}
